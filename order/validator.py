import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class PreTradeValidator:
    """
    주문 전송 전 사전 유효성 검사 (Pre-trade Validation)
    안전한 자동매매를 위한 최우선 방어선입니다.
    """
    def __init__(self):
        self.live_trading = settings.live_trading_enabled

    def validate_order(self, symbol: str, qty: int, price: int, order_type: str) -> bool:
        """
        주문 파라미터가 유효한지 검사합니다.
        하나라도 실패하면 False를 반환하여 주문을 차단합니다.
        """
        try:
            # 1. 라이브 트레이딩 플래그 확인
            if not self.live_trading:
                logger.info(f"[유효성 검사] 모의/테스트 모드입니다. (LIVE_TRADING_ENABLED=False)")
            
            # 2. 필수 파라미터 타입 및 논리 검증
            if not symbol or len(symbol) != 6 or not symbol.isdigit():
                logger.error(f"[유효성 검사 실패] 잘못된 종목 코드입니다: {symbol}")
                return False
                
            if qty <= 0:
                logger.error(f"[유효성 검사 실패] 주문 수량은 0보다 커야 합니다: {qty}")
                return False
                
            # 시장가 주문(market)이 아닌 지정가 주문의 경우 가격 검증
            if order_type.lower() != "market" and price <= 0:
                logger.error(f"[유효성 검사 실패] 지정가 주문 가격은 0보다 커야 합니다: {price}")
                return False

            valid_order_types = ["buy", "sell", "market"]
            if order_type.lower() not in valid_order_types:
                logger.error(f"[유효성 검사 실패] 지원하지 않는 주문 타입입니다: {order_type}")
                return False

            # TODO: 시장 운영 시간(KST) 검증 (market_calendar.py 연동) 추가 예정
            # TODO: 포트폴리오 리스크(1일 최대 손실, 종목별 최대 비중) 검증 추가 예정

            return True

        except Exception as e:
            logger.error(f"[유효성 검사 예외 발생] {str(e)}")
            return False