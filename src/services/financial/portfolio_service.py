"""Lightweight portfolio service wrapper."""
from __future__ import annotations

from .portfolio_management_service import PortfolioManager, PortfolioPosition


class PortfolioService:
    """Expose basic portfolio management operations."""

    def __init__(self) -> None:
        self.manager = PortfolioManager()

    def add_position(
        self, symbol: str, quantity: float, price: float, sector: str = ""
    ) -> bool:
        """Add or update a position via the underlying manager."""
        position = PortfolioPosition(
            symbol=symbol,
            quantity=quantity,
            avg_price=price,
            current_price=price,
            market_value=quantity * price,
            unrealized_pnl=0.0,
            unrealized_pnl_pct=0.0,
            sector=sector,
        )
        self.manager.positions[symbol] = position
        self.manager.save_portfolio()
        self.manager.calculate_metrics()
        return True

    def get_portfolio(self):
        """Return the current portfolio representation."""
        return self.manager.get_portfolio()
