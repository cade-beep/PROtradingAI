import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Portfolio:
    """
    포트폴리오 관리 모듈
    현금, 포지션, 총 자산을 추적합니다.
    """
    def __init__(self, initial_cash: float = 1000000.0):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Dict[str, Any]] = {}  # symbol: {'qty': int, 'avg_price': float}

    def update_position(self, symbol: str, qty: int, price: float, action: str) -> bool:
        """
        포지션을 업데이트합니다.
        action: 'buy' or 'sell'
        성공 시 True 반환
        """
        if action == 'buy':
            cost = qty * price
            if self.cash >= cost:
                self.cash -= cost
                if symbol in self.positions:
                    old_qty = self.positions[symbol]['qty']
                    old_avg = self.positions[symbol]['avg_price']
                    new_qty = old_qty + qty
                    self.positions[symbol]['qty'] = new_qty
                    self.positions[symbol]['avg_price'] = (old_avg * old_qty + cost) / new_qty
                else:
                    self.positions[symbol] = {'qty': qty, 'avg_price': price}
                logger.info(f"포지션 업데이트: {action} {qty}주 {symbol} @ {price}원")
                return True
            else:
                logger.error(f"현금 부족: 필요 {cost}원, 보유 {self.cash}원")
                return False
        elif action == 'sell':
            if symbol in self.positions and self.positions[symbol]['qty'] >= qty:
                revenue = qty * price
                self.cash += revenue
                self.positions[symbol]['qty'] -= qty
                if self.positions[symbol]['qty'] == 0:
                    del self.positions[symbol]
                logger.info(f"포지션 업데이트: {action} {qty}주 {symbol} @ {price}원")
                return True
            else:
                logger.error(f"포지션 부족: {symbol} 보유 {self.positions.get(symbol, {'qty': 0})['qty']}주")
                return False
        return False

    def get_position(self, symbol: str) -> Dict[str, Any]:
        """
        특정 종목의 포지션을 반환합니다.
        """
        return self.positions.get(symbol, {'qty': 0, 'avg_price': 0.0})

    def get_total_value(self, current_prices: Dict[str, float]) -> float:
        """
        현재 가격으로 총 자산 가치를 계산합니다.
        """
        value = self.cash
        for symbol, pos in self.positions.items():
            value += pos['qty'] * current_prices.get(symbol, pos['avg_price'])
        return value

    def get_pnl(self, current_prices: Dict[str, float]) -> float:
        """
        현재 가격으로 손익을 계산합니다.
        """
        return self.get_total_value(current_prices) - self.initial_cash