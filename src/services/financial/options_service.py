"""Options trading service wrapper."""
from __future__ import annotations

from typing import Optional

from .options_trading_service import OptionsTradingService
from .options.pricing import OptionType
from .market_data import MarketDataModule


class OptionsService:
    """Thin wrapper around the options trading service."""

    def __init__(self, market_data: Optional[MarketDataModule] = None) -> None:
        md_service = market_data.service if market_data else None
        self.service = OptionsTradingService(market_data_service=md_service)

    def price_option(self, S: float, K: float, T: float, r: float, sigma: float, option_type: OptionType):
        """Price an option using Black-Scholes via the underlying service."""
        return self.service.calculate_black_scholes(S, K, T, r, sigma, option_type)
