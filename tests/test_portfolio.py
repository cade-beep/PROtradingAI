import pytest
from portfolio.portfolio import Portfolio

def test_portfolio_initialization():
    portfolio = Portfolio(initial_cash=1000000)
    assert portfolio.cash == 1000000
    assert portfolio.positions == {}

def test_portfolio_buy():
    portfolio = Portfolio(initial_cash=1000000)
    success = portfolio.update_position('005930', 10, 100, 'buy')
    assert success
    assert portfolio.cash == 999000
    assert portfolio.positions['005930']['qty'] == 10
    assert portfolio.positions['005930']['avg_price'] == 100

def test_portfolio_sell():
    portfolio = Portfolio(initial_cash=1000000)
    portfolio.update_position('005930', 10, 100, 'buy')
    success = portfolio.update_position('005930', 5, 110, 'sell')
    assert success
    assert portfolio.cash == 999000 + 550
    assert portfolio.positions['005930']['qty'] == 5

def test_portfolio_insufficient_cash():
    portfolio = Portfolio(initial_cash=500)
    success = portfolio.update_position('005930', 10, 100, 'buy')
    assert not success
    assert portfolio.cash == 500

def test_portfolio_get_total_value():
    portfolio = Portfolio(initial_cash=1000000)
    portfolio.update_position('005930', 10, 100, 'buy')
    current_prices = {'005930': 110}
    value = portfolio.get_total_value(current_prices)
    assert value == 1000000 - 1000 + 1100  # 1001000