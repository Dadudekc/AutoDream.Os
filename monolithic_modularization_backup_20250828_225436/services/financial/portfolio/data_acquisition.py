"""Data acquisition utilities for portfolio tracking."""

from __future__ import annotations

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class MarketDataService:
    """Fetch market and benchmark data.

    This implementation returns static data suitable for unit testing. In a
    production system this class would connect to external data providers.
    """

    def fetch_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Return mock price data for the given ``symbols``."""

        prices = {symbol: float(index + 1) * 10.0 for index, symbol in enumerate(symbols)}
        logger.debug("Fetched prices: %s", prices)
        return prices

    def fetch_benchmark(self, symbol: str) -> Dict[str, float]:
        """Return mock benchmark data for ``symbol``."""

        data = {"symbol": symbol, "return": 0.05}
        logger.debug("Fetched benchmark data: %s", data)
        return data
