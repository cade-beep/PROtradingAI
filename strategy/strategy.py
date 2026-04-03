import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class TradingStrategy:
    """
    자동매매 전략 모듈
    시장 데이터를 분석하여 매수/매도 신호를 생성합니다.
    현재: 간단한 이동평균 크로스오버 전략 구현
    """
    def __init__(self, short_window: int = 5, long_window: int = 10):
        self.short_window = short_window
        self.long_window = long_window
        self.prices: Dict[str, list] = {}  # symbol: [prices]
        self.signals: Dict[str, str] = {}  # symbol: last_signal

    def update_market_data(self, symbol: str, price: float):
        """
        실시간 시장 데이터를 업데이트합니다.
        """
        if symbol not in self.prices:
            self.prices[symbol] = []
        self.prices[symbol].append(price)
        # 윈도우 크기 유지
        if len(self.prices[symbol]) > self.long_window:
            self.prices[symbol].pop(0)
        logger.debug(f"시장 데이터 업데이트: {symbol} @ {price}")

    def generate_signal(self, symbol: str) -> Optional[str]:
        """
        현재 데이터로 매매 신호를 생성합니다.
        'buy', 'sell', None 반환
        """
        if symbol not in self.prices or len(self.prices[symbol]) < self.long_window:
            return None

        prices = self.prices[symbol]
        short_avg = sum(prices[-self.short_window:]) / self.short_window
        long_avg = sum(prices) / len(prices)

        last_signal = self.signals.get(symbol)

        if short_avg > long_avg and last_signal != 'buy':
            self.signals[symbol] = 'buy'
            logger.info(f"매수 신호 생성: {symbol} (단기 MA: {short_avg:.2f}, 장기 MA: {long_avg:.2f})")
            return 'buy'
        elif short_avg < long_avg and last_signal != 'sell':
            self.signals[symbol] = 'sell'
            logger.info(f"매도 신호 생성: {symbol} (단기 MA: {short_avg:.2f}, 장기 MA: {long_avg:.2f})")
            return 'sell'

        return None

    def reset_signal(self, symbol: str):
        """
        신호를 리셋합니다 (주문 실행 후).
        """
        self.signals[symbol] = None