import asyncio
import logging
import sys
from config.settings import settings
from auth.token_manager import TokenManager
from broker_api.kiwoom_client import KiwoomClient
from broker_api.endpoints import OrderableAmountClient
from market_data.quotes import MarketDataClient
from market_data.realtime import KiwoomWebSocketClient
from broker_api.order_endpoints import OrderEndpointClient
from order.validator import PreTradeValidator
from order.reconciler import OrderReconciler
from strategy.strategy import TradingStrategy
from portfolio.portfolio import Portfolio
from risk.risk import RiskManager
from notifications.discord import DiscordNotifier

# 로깅 기본 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("runner.main")

async def consume_market_data(queue: asyncio.Queue, strategy: TradingStrategy, portfolio: Portfolio, risk: RiskManager, order_client: OrderEndpointClient, validator: PreTradeValidator, reconciler: OrderReconciler, notifier: DiscordNotifier, account_no: str):
    """
    웹소켓으로부터 수신된 데이터(Pub/Sub의 Consumer 역할)를 처리하는 태스크
    전략 분석 및 자동 주문 실행
    """
    logger.info("시장 데이터 컨슈머 태스크 시작")
    while True:
        try:
            message = await queue.get()
            logger.info(f"큐에서 실시간 데이터 처리 (Consumer): {message}")
            
            # 전략 업데이트 및 신호 생성
            if 'symbol' in message and 'price' in message:
                strategy.update_market_data(message['symbol'], message['price'])
                signal = strategy.generate_signal(message['symbol'])
                
                if signal:
                    qty = 1  # 단순화
                    price = message['price']
                    current_prices = {message['symbol']: price}
                    
                    if risk.check_order_risk(message['symbol'], qty, price, signal, portfolio, current_prices):
                        if validator.validate_order(message['symbol'], qty, price, signal):
                            if portfolio.update_position(message['symbol'], qty, price, signal):
                                order_res = await order_client.place_order(account_no, message['symbol'], qty, price, signal)
                                if order_res.get('rt_cd') == '0':
                                    order_no = order_res.get('output', {}).get('ODNO', f"mock_{signal}_{message['symbol']}")
                                    await reconciler.store_order(order_no, message['symbol'], qty, price, signal)
                                    await notifier.notify_order(signal, message['symbol'], qty, price)
                                    strategy.reset_signal(message['symbol'])
                                else:
                                    await notifier.notify_error(f"주문 실패: {order_res}")
                    
                    # 동기화
                    await reconciler.reconcile_orders(account_no)
            
            queue.task_done()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"컨슈머 오류: {str(e)}")
            await notifier.notify_error(str(e))

async def main():
    logger.info("=== 시스템 시작: 통합 테스트 (REST API + WebSocket + Order Pipeline) ===")
    
    if settings.live_trading_enabled:
        logger.warning("경고: LIVE_TRADING_ENABLED가 True입니다. 실제 주문이 나갈 수 있습니다!")
    else:
        logger.info("안내: 현재 모의/테스트 모드입니다. (LIVE_TRADING_ENABLED=False)")

    try:
        token_manager = TokenManager()
        account_no = settings.kiwoom_account_no
        
        orderable_client = OrderableAmountClient(token_manager)
        market_data_client = MarketDataClient(token_manager)
        
        order_client = OrderEndpointClient(token_manager)
        validator = PreTradeValidator()
        reconciler = OrderReconciler(token_manager)
        await reconciler.init_db()
        
        strategy = TradingStrategy()
        portfolio = Portfolio()
        risk = RiskManager()
        notifier = DiscordNotifier()
        
        message_queue = asyncio.Queue()
        ws_client = KiwoomWebSocketClient(token_manager, message_queue)
        
        # 2. 백그라운드 태스크 실행 (웹소켓 연결 및 큐 컨슈머)
        logger.info("--- 실시간 웹소켓 & Pub/Sub 백그라운드 구동 ---")
        ws_task = asyncio.create_task(ws_client.connect_and_listen())
        consumer_task = asyncio.create_task(consume_market_data(message_queue, strategy, portfolio, risk, order_client, validator, reconciler, notifier, account_no))
        
        # 웹소켓이 연결될 수 있는 여유 시간 대기
        await asyncio.sleep(2)
        
        # 3. 데이터 조회 및 웹소켓 구독 (Step 2 & 3 통합)
        logger.info("--- 데이터 연동 테스트 ---")
        try:
            # 안전을 위해 호출은 하되 결과 처리만 확인하도록 로깅
            logger.info("주문가능금액, 현재가 조회 호출 대기 (실제 코드는 문서에 맞게 파라미터 교체 필요)")
            await orderable_client.get_orderable_cash(account_no)
            await market_data_client.get_current_price("005930")
            
            logger.info("삼성전자(005930) 실시간 웹소켓 구독 요청")
            await ws_client.subscribe(["005930"])
        except Exception as e:
            logger.error(f"조회 연동 중 오류 발생: {e}")

        # 4. 주문 파이프라인 (Step 4)
        logger.info("--- 주문 유효성 검사 및 전송 파이프라인 테스트 ---")
        symbol_to_trade = "005930"
        trade_qty = 10
        trade_price = 70000
        order_type = "buy"
        
        # 4-1. Pre-trade validation (절대 건너뛰지 않음)
        if validator.validate_order(symbol_to_trade, trade_qty, trade_price, order_type):
            logger.info("유효성 검사 통과: 브로커 API로 주문을 전송합니다.")
            
            # 실제 주문 호출 (테스트 모드이므로 실제로 API 통신 시도 시 예외 또는 Mock 반환)
            order_res = await order_client.place_order(account_no, symbol_to_trade, trade_qty, trade_price, order_type)
            logger.info(f"주문 결과: {order_res}")
        else:
            logger.warning("유효성 검사 실패: 주문 전송이 차단되었습니다.")

        # 4-2. 상태 동기화 (Reconciler - Step 5)
        # 주문 직후 또는 타임아웃 발생 시 무조건 미체결 상태를 확인하여 중복 주문 방지
        logger.info("--- 주문/체결 동기화 (Reconciler) 테스트 ---")
        await asyncio.sleep(1) # 네트워크 지연/서버 반영 시간 시뮬레이션
        open_orders = await reconciler.fetch_open_orders(account_no)
        logger.info(f"동기화 완료: 현재 미체결 내역 {len(open_orders)}건")

        # 5. 시스템 유지 및 정상 종료 (3초 대기 후 종료 처리)
        await asyncio.sleep(3)
        logger.info("테스트가 완료되었습니다. 리소스를 정리하고 종료합니다...")
        
        # 최종 손익 알림
        await notifier.notify_pnl(portfolio.get_pnl({}))
        
        await ws_client.close()
        ws_task.cancel()
        consumer_task.cancel()
        
    except Exception as e:
        logger.critical(f"시스템 실행 중 치명적 오류 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
