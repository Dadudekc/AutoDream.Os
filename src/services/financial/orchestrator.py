"""Simple orchestrator composing core financial services."""
from __future__ import annotations

from .portfolio_service import PortfolioService
from .risk import RiskService
from .market_data import MarketDataModule
from .trading import TradingService
from .options_service import OptionsService


class FinancialServicesOrchestrator:
    """Compose individual financial service modules for external use."""

    def __init__(self) -> None:
        self.market_data = MarketDataModule()
        self.portfolio = PortfolioService()
        self.risk = RiskService(self.portfolio)
        self.trading = TradingService(self.market_data)
        self.options = OptionsService(self.market_data)
