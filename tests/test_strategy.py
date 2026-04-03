import pytest
from strategy.strategy import TradingStrategy

def test_trading_strategy_buy_signal():
    strategy = TradingStrategy(short_window=3, long_window=5)
    
    # 가격 데이터 추가
    prices = [100, 102, 104, 106, 108, 110, 112]
    for price in prices:
        strategy.update_market_data('005930', price)
    
    signal = strategy.generate_signal('005930')
    assert signal == 'buy'

def test_trading_strategy_sell_signal():
    strategy = TradingStrategy(short_window=3, long_window=5)
    
    # 상승 후 하락
    prices = [100, 102, 104, 106, 108, 110, 109, 107, 105]
    for price in prices:
        strategy.update_market_data('005930', price)
    
    signal = strategy.generate_signal('005930')
    assert signal == 'sell'

def test_trading_strategy_no_signal():
    strategy = TradingStrategy(short_window=3, long_window=5)
    
    # 적은 데이터
    prices = [100, 102]
    for price in prices:
        strategy.update_market_data('005930', price)
    
    signal = strategy.generate_signal('005930')
    assert signal is None