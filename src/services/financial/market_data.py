"""Market data service wrapper."""
from __future__ import annotations

from .market_data_service import MarketDataService, MarketData


class MarketDataModule:
    """Expose simplified market data access methods."""

    def __init__(self) -> None:
        self.service = MarketDataService()

    def get_mock_price(self, symbol: str) -> MarketData | None:
        """Return mock real-time data for the given symbol."""
        data = self.service.get_real_time_data([symbol], source="mock")
        return data.get(symbol.upper())
