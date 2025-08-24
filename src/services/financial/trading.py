"""Trading intelligence service wrapper."""
from __future__ import annotations

from typing import Optional

from .trading_intelligence_service import TradingIntelligenceService
from .market_data import MarketDataModule


class TradingService:
    """Wrapper around the trading intelligence service."""

    def __init__(self, market_data: Optional[MarketDataModule] = None) -> None:
        md_service = market_data.service if market_data else None
        self.service = TradingIntelligenceService(market_data_service=md_service)

    def available_strategies(self) -> list:
        """Return the list of configured strategy types."""
        return list(self.service.strategies.keys())
