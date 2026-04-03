import logging
from typing import Dict, Any, Optional
from config.settings import settings
from market_calendar import MarketCalendar
from risk.risk import RiskManager
from portfolio.portfolio import Portfolio

logger = logging.getLogger(__name__)

class PreTradeValidator:
    """
    주문 전송 전 사전 유효성 검사 (Pre-trade Validation)
    안전한 자동매매를 위한 최우선 방어선입니다.
    """
    def __init__(self, risk_manager: Optional[RiskManager] = None):
        self.live_trading = settings.live_trading_enabled
        self.risk_manager = risk_manager or RiskManager()

    def validate_order(self, symbol: str, qty: int, price: int, order_type: str, portfolio: Optional[Portfolio] = None, current_prices: Optional[Dict[str, float]] = None) -> bool:
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

            # 3. 시장 운영 시간(KST) 검증
            if not MarketCalendar.is_market_open():
                logger.error(f"[유효성 검사 실패] 시장이 폐장되었습니다. 현재 상태: {MarketCalendar.get_market_status()}")
                return False

            # 4. 마감 경매 시간 주문 금지 (15:20-15:30)
            if MarketCalendar.is_closing_auction():
                logger.error(f"[유효성 검사 실패] 마감 경매 시간에는 신규 주문을 할 수 없습니다.")
                return False

            # 5. 포트폴리오 리스크 검증 (선택적)
            if portfolio and current_prices and order_type.lower() in ["buy", "sell"]:
                action = order_type.lower()
                if not self.risk_manager.check_order_risk(symbol, qty, price, action, portfolio, current_prices):
                    logger.error(f"[유효성 검사 실패] 리스크 검증 실패: {symbol} {action} {qty}주 @ {price}원")
                    return False

            return True

        except Exception as e:
            logger.error(f"[유효성 검사 예외 발생] {str(e)}")
            return False