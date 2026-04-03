import pytest
from backtest.backtest import Backtester

def test_backtester_initialization():
    bt = Backtester()
    assert bt.initial_cash == 1000000
    assert bt.portfolio.cash == 1000000

def test_backtester_mock_data():
    data = Backtester.generate_mock_data('005930', 5)
    assert len(data) == 5 * 24
    assert data[0]['symbol'] == '005930'
    assert 'price' in data[0]
    assert 'timestamp' in data[0]

def test_backtester_run():
    bt = Backtester(initial_cash=100000)
    data = Backtester.generate_mock_data('005930', 10)
    bt.load_historical_data(data)
    result = bt.run_backtest()
    
    assert 'total_trades' in result
    assert 'final_pnl' in result
    assert 'total_return_percent' in result
    assert 'trades' in result
    assert 'pnl_history' in result
    assert len(result['pnl_history']) == len(data)