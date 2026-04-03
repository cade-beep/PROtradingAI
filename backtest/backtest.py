import logging
from typing import List, Dict, Any
from strategy.strategy import TradingStrategy
from portfolio.portfolio import Portfolio
from risk.risk import RiskManager

logger = logging.getLogger(__name__)

class Backtester:
    """
    백테스트 모듈: 과거 데이터를 사용하여 전략 성능 평가
    """
    def __init__(self, initial_cash: float = 1000000.0):
        self.initial_cash = initial_cash
        self.portfolio = Portfolio(initial_cash)
        self.strategy = TradingStrategy()
        self.risk = RiskManager(initial_cash=initial_cash)

    def load_historical_data(self, data: List[Dict[str, Any]]) -> None:
        """
        과거 데이터 로드 (mock 데이터 사용)
        data: [{'symbol': str, 'price': float, 'timestamp': str}, ...]
        """
        self.historical_data = data
        logger.info(f"과거 데이터 {len(data)}개 로드 완료")

    def run_backtest(self) -> Dict[str, Any]:
        """
        백테스트 실행
        """
        logger.info("백테스트 시작")
        
        trades = []
        pnl_history = []
        
        for i, data_point in enumerate(self.historical_data):
            symbol = data_point['symbol']
            price = data_point['price']
            
            # 전략 업데이트
            self.strategy.update_market_data(symbol, price)
            
            # 신호 생성
            signal = self.strategy.generate_signal(symbol)
            
            if signal:
                qty = 1  # 단순화
                current_prices = {symbol: price}
                
                # 리스크 체크
                if self.risk.check_order_risk(symbol, qty, price, signal, self.portfolio, current_prices):
                    # 포트폴리오 업데이트
                    if self.portfolio.update_position(symbol, qty, price, signal):
                        trades.append({
                            'timestamp': data_point.get('timestamp', i),
                            'symbol': symbol,
                            'signal': signal,
                            'price': price,
                            'qty': qty
                        })
                        self.strategy.reset_signal(symbol)
                        logger.debug(f"백테스트 거래: {signal} {qty}주 {symbol} @ {price}")
            
            # PnL 기록
            pnl = self.portfolio.get_pnl({symbol: price})
            pnl_history.append({'timestamp': data_point.get('timestamp', i), 'pnl': pnl})
        
        # 결과 계산
        final_pnl = self.portfolio.get_pnl({data_point['symbol']: data_point['price']})
        total_return = final_pnl / self.initial_cash * 100
        
        result = {
            'total_trades': len(trades),
            'final_pnl': final_pnl,
            'total_return_percent': total_return,
            'trades': trades,
            'pnl_history': pnl_history
        }
        
        logger.info(f"백테스트 완료: 총 거래 {len(trades)}건, 수익률 {total_return:.2f}%")
        return result

    @staticmethod
    def generate_mock_data(symbol: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        모의 과거 데이터 생성
        """
        import random
        data = []
        price = 100.0
        for i in range(days * 24):  # 시간별 데이터 가정
            change = random.uniform(-2, 2)
            price += change
            price = max(price, 1.0)  # 최소 가격
            data.append({
                'symbol': symbol,
                'price': round(price, 2),
                'timestamp': f"2024-01-01 {i//24:02d}:{i%24:02d}:00"
            })
        return data