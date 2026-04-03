import httpx
import logging
from typing import Dict, Any
from config.settings import settings
from auth.token_manager import TokenManager

logger = logging.getLogger(__name__)

class OrderEndpointClient:
    """
    키움증권 REST API 주문 전송 래퍼 (kt10000, kt10001 등)
    """
    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager
        self.host = settings.kiwoom_api_host
        self.app_key = settings.kiwoom_app_key
        self.app_secret = settings.kiwoom_app_secret

    async def place_order(self, account_no: str, symbol: str, qty: int, price: int, order_type: str) -> Dict[str, Any]:
        """
        실제 매수/매도 주문을 API로 전송합니다.
        """
        # 1. 안전 장치: LIVE_TRADING_ENABLED가 False이면 실제 HTTP 요청을 보내지 않고 Mock 반환
        if not settings.live_trading_enabled:
            logger.warning(f"[모의 주문] 실제 API로 전송되지 않았습니다: {order_type} {symbol} {qty}주 @ {price}원")
            return {
                "rt_cd": "0",
                "msg1": "모의 주문 성공 (API 미전송)",
                "mock": True
            }

        token = await self.token_manager.issue_token()
        
        # 주문 엔드포인트 및 TR 코드 결정 (공식 문서 기준 확인 필요)
        # 예: 매수 kt10000 / 매도 kt10001
        tr_id = "TTTC0802U" if order_type.lower() == "buy" else "TTTC0801U"
        url = f"{self.host}/uapi/domestic-stock/v1/trading/order-cash"
        
        headers = {
            "authorization": f"Bearer {token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id,
            "content-type": "application/json"
        }
        
        # 키움증권 표준 주문 payload 구성 (실제 파라미터명은 최신 문서와 대조 필수)
        payload = {
            "CANO": account_no[:8],          # 종합계좌번호 앞 8자리
            "ACNT_PRDT_CD": account_no[8:],  # 계좌상품코드 (보통 "01" 등)
            "PDNO": symbol,                  # 종목코드
            "ORD_DVSN": "00",                # 주문구분 (00: 지정가, 01: 시장가 등)
            "ORD_QTY": str(qty),             # 주문수량
            "ORD_UNPR": str(price)           # 주문단가
        }

        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"주문 API 호출 시작: {symbol} {order_type} {qty}주")
                response = await client.post(url, headers=headers, json=payload, timeout=5.0)
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"주문 API 통신 중 오류 발생: {str(e)}")
            # TODO: 타임아웃 발생 시 '주문 상태 재조회(Re-query)' 방어 로직 연동
            return {"rt_cd": "-1", "msg1": str(e), "error": True}