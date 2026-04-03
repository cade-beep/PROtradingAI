import asyncio
import json
import logging
import websockets
from typing import Set, Optional
from config.settings import settings
from auth.token_manager import TokenManager

logger = logging.getLogger(__name__)

class KiwoomWebSocketClient:
    """
    키움증권 실시간 웹소켓 클라이언트
    실시간 체결가/호가 데이터 수신 및 비동기 큐(Queue)를 통한 메시지 전달
    """
    def __init__(self, token_manager: TokenManager, message_queue: asyncio.Queue = None):
        self.ws_url = "wss://ws-api.kiwoom.com/websocket"
        self.token_manager = token_manager
        # Pub/Sub 구조를 위한 비동기 큐 설정
        self.message_queue = message_queue or asyncio.Queue()
        
        self.connection: Optional[websockets.WebSocketClientProtocol] = None
        self.is_connected = False
        self.subscribed_symbols: Set[str] = set()
        self.reconnect_interval = 3.0
        self._stop_event = asyncio.Event()

    async def _get_auth_headers(self) -> dict:
        token = await self.token_manager.issue_token()
        return {
            "Authorization": f"Bearer {token}",
            "appkey": settings.kiwoom_app_key,
            "appsecret": settings.kiwoom_app_secret
        }

    async def connect_and_listen(self):
        """웹소켓 연결 및 지속적인 메시지 수신 (자동 재접속 포함)"""
        while not self._stop_event.is_set():
            try:
                headers = await self._get_auth_headers()
                logger.info(f"웹소켓 연결 시도 중: {self.ws_url}")
                
                async with websockets.connect(
                    self.ws_url,
                    extra_headers=headers,
                    ping_interval=30,
                    ping_timeout=10
                ) as ws:
                    self.connection = ws
                    self.is_connected = True
                    logger.info("웹소켓 연결 성공")

                    if self.subscribed_symbols:
                        logger.info(f"재접속 후 기존 종목 재구독: {self.subscribed_symbols}")
                        await self._send_subscribe_request(list(self.subscribed_symbols))

                    async for message in ws:
                        if self._stop_event.is_set():
                            break
                        await self._handle_message(message)

            except websockets.exceptions.ConnectionClosed as e:
                logger.warning(f"웹소켓 연결 끊김: {e.code} - {e.reason}")
            except Exception as e:
                logger.error(f"웹소켓 연결 오류: {str(e)}")
            
            finally:
                self.is_connected = False
                self.connection = None
                
                if not self._stop_event.is_set():
                    logger.info(f"{self.reconnect_interval}초 후 재접속 시도...")
                    await asyncio.sleep(self.reconnect_interval)

    async def _handle_message(self, message: str):
        """수신된 메시지 파싱 및 큐로 전달"""
        try:
            data = json.loads(message)
            tr_id = data.get("header", {}).get("tr_id")
            
            if tr_id == "H0STCNT0":
                body = data.get("body", {})
                symbol = body.get("stnd_iscd")
                price = body.get("stck_prpr")
                logger.debug(f"[실시간 체결] 종목: {symbol}, 현재가: {price}")
                
                # 큐를 통해 데이터 전달 (다른 모듈에서 소비)
                await self.message_queue.put({
                    "type": "realtime_tick",
                    "symbol": symbol,
                    "price": price,
                    "raw": data
                })
            else:
                logger.debug(f"[수신] {message[:100]}...")

        except json.JSONDecodeError:
            logger.warning(f"JSON 파싱 실패: {message}")
        except Exception as e:
            logger.error(f"메시지 처리 중 오류: {str(e)}")

    async def _send_subscribe_request(self, symbols: list[str]):
        """구독 요청"""
        if not self.is_connected or not self.connection:
            logger.warning("연결되어 있지 않아 구독 요청 불가")
            return

        for symbol in symbols:
            payload = {
                "header": { "tr_type": "1", "tr_id": "H0STCNT0" },
                "body": { "input": { "tr_id": "H0STCNT0", "tr_key": symbol } }
            }
            try:
                await self.connection.send(json.dumps(payload))
                logger.info(f"구독 요청 전송: {symbol}")
            except Exception as e:
                logger.error(f"구독 요청 실패 ({symbol}): {str(e)}")

    async def subscribe(self, symbols: list[str]):
        new_symbols = set(symbols) - self.subscribed_symbols
        if new_symbols:
            self.subscribed_symbols.update(new_symbols)
            await self._send_subscribe_request(list(new_symbols))

    async def unsubscribe(self, symbols: list[str]):
        symbols_to_remove = set(symbols).intersection(self.subscribed_symbols)
        if not symbols_to_remove: return

        if self.is_connected and self.connection:
            for symbol in symbols_to_remove:
                payload = {
                     "header": { "tr_type": "2", "tr_id": "H0STCNT0" },
                     "body": { "input": { "tr_id": "H0STCNT0", "tr_key": symbol } }
                }
                try:
                    await self.connection.send(json.dumps(payload))
                    logger.info(f"구독 해제 요청: {symbol}")
                    self.subscribed_symbols.remove(symbol)
                except Exception as e:
                     logger.error(f"구독 해제 실패 ({symbol}): {str(e)}")
        else:
             self.subscribed_symbols.difference_update(symbols_to_remove)

    async def close(self):
        self._stop_event.set()
        if self.connection:
            await self.connection.close()
            logger.info("웹소켓 연결 정상 종료")
