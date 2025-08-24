"""Unit tests for standalone financial service modules."""

import pytest

pytest.importorskip("pandas")

from src.services.financial.portfolio_service import PortfolioService
from src.services.financial.risk import RiskService
from src.services.financial.market_data import MarketDataModule
from src.services.financial.trading import TradingService
from src.services.financial.options_service import OptionsService
from src.services.financial.options.pricing import OptionType


def test_portfolio_service_add_and_get():
    service = PortfolioService()
    assert service.add_position("AAPL", 1, 150.0)
    portfolio = service.get_portfolio()
    assert "AAPL" in portfolio["positions"]


def test_risk_service_profile():
    portfolio = PortfolioService()
    risk = RiskService(portfolio)
    profile = risk.get_risk_profile()
    assert profile is not None


def test_market_data_mock_price():
    md = MarketDataModule()
    data = md.get_mock_price("AAPL")
    assert data is not None
    assert data.symbol == "AAPL"


def test_trading_service_strategies():
    md = MarketDataModule()
    trading = TradingService(md)
    assert trading.available_strategies()


def test_options_service_pricing():
    md = MarketDataModule()
    options = OptionsService(md)
    result = options.price_option(100, 100, 0.5, 0.01, 0.2, OptionType.CALL)
    assert "price" in result and result["price"] > 0
