import logging
from typing import Dict, Any
from portfolio.portfolio import Portfolio

logger = logging.getLogger(__name__)

class RiskManager:
    """
    리스크 관리 모듈
    주문 전 리스크 검증을 수행합니다.
    """
    def __init__(self, max_position_percent: float = 0.1, max_daily_loss_percent: float = 0.05, initial_cash: float = 1000000.0):
        self.max_position_percent = max_position_percent  # 최대 포지션 비중
        self.max_daily_loss_percent = max_daily_loss_percent
        self.initial_cash = initial_cash
        self.daily_pnl = 0.0

    def check_order_risk(self, symbol: str, qty: int, price: float, action: str, portfolio: Portfolio, current_prices: Dict[str, float]) -> bool:
        """
        주문의 리스크를 검증합니다.
        """
        # 1. 포지션 사이즈 체크
        order_value = qty * price
        total_value = portfolio.get_total_value(current_prices)
        if action == 'buy':
            new_position_value = portfolio.get_position(symbol)['qty'] * price + order_value
            if new_position_value / total_value > self.max_position_percent:
                logger.error(f"포지션 사이즈 초과: {new_position_value / total_value:.2%} > {self.max_position_percent:.2%}")
                return False

        # 2. 현금 체크 (이미 portfolio에서 하지만 추가)
        if action == 'buy' and portfolio.cash < order_value:
            return False

        # 3. 일일 손실 제한 (단순화: 현재 pnl 체크)
        current_pnl = portfolio.get_pnl(current_prices)
        if current_pnl < -self.initial_cash * self.max_daily_loss_percent:
            logger.error(f"일일 손실 제한 초과: {current_pnl}원")
            return False

        # 4. 기타 리스크 (추후 추가: 변동성, 상관관계 등)
        return True

    def update_daily_pnl(self, pnl: float):
        """
        일일 손익 업데이트 (단순화).
        """
        self.daily_pnl = pnl