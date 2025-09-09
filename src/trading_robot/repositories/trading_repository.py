"""
Trading Repository V2 - V2 Compliant Modular Architecture
========================================================

Main trading repository that coordinates all trading data access modules.
Refactored from monolithic trading_repository.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import logging
from typing import Any

from .implementations import PortfolioRepositoryImpl, PositionRepositoryImpl, TradingRepositoryImpl
from .interfaces import (
    PortfolioRepositoryInterface,
    PositionRepositoryInterface,
    TradingRepositoryInterface,
)
from .models import Portfolio, Position, Trade


class TradingRepository:
    """Main trading repository that coordinates all trading data access.

    Provides unified interface for trade, position, and portfolio operations.
    """

    def __init__(self):
        """Initialize trading repository."""
        self.logger = logging.getLogger(__name__)

        # Initialize implementations
        self.trade_repo: TradingRepositoryInterface = TradingRepositoryImpl()
        self.position_repo: PositionRepositoryInterface = PositionRepositoryImpl()
        self.portfolio_repo: PortfolioRepositoryInterface = PortfolioRepositoryImpl()

        self.logger.info("Trading Repository V2 initialized")

    # Trade operations
    async def save_trade(self, trade: Trade) -> bool:
        """Save a trade."""
        return await self.trade_repo.save_trade(trade)

    async def get_trade(self, trade_id: str) -> Trade | None:
        """Get trade by ID."""
        return await self.trade_repo.get_trade(trade_id)

    async def get_trades_by_symbol(self, symbol: str, limit: int = 100) -> list[Trade]:
        """Get trades for symbol."""
        return await self.trade_repo.get_trades_by_symbol(symbol, limit)

    async def get_all_trades(self, limit: int = 1000) -> list[Trade]:
        """Get all trades."""
        return await self.trade_repo.get_all_trades(limit)

    async def update_trade_status(self, trade_id: str, status: str) -> bool:
        """Update trade status."""
        return await self.trade_repo.update_trade_status(trade_id, status)

    async def delete_trade(self, trade_id: str) -> bool:
        """Delete trade."""
        return await self.trade_repo.delete_trade(trade_id)

    async def get_trades_by_status(self, status: str, limit: int = 100) -> list[Trade]:
        """Get trades by status."""
        return await self.trade_repo.get_trades_by_status(status, limit)

    async def get_trades_by_date_range(self, start_date, end_date, limit: int = 100) -> list[Trade]:
        """Get trades within date range."""
        return await self.trade_repo.get_trades_by_date_range(start_date, end_date, limit)

    # Position operations
    async def save_position(self, position: Position) -> bool:
        """Save position."""
        return await self.position_repo.save_position(position)

    async def get_position(self, symbol: str) -> Position | None:
        """Get position by symbol."""
        return await self.position_repo.get_position(symbol)

    async def get_all_positions(self) -> list[Position]:
        """Get all positions."""
        return await self.position_repo.get_all_positions()

    async def update_position(self, position: Position) -> bool:
        """Update position."""
        return await self.position_repo.update_position(position)

    async def delete_position(self, symbol: str) -> bool:
        """Delete position."""
        return await self.position_repo.delete_position(symbol)

    async def get_long_positions(self) -> list[Position]:
        """Get long positions."""
        return await self.position_repo.get_long_positions()

    async def get_short_positions(self) -> list[Position]:
        """Get short positions."""
        return await self.position_repo.get_short_positions()

    async def get_profitable_positions(self) -> list[Position]:
        """Get profitable positions."""
        return await self.position_repo.get_profitable_positions()

    async def get_losing_positions(self) -> list[Position]:
        """Get losing positions."""
        return await self.position_repo.get_losing_positions()

    async def update_position_prices(self, price_updates: dict) -> bool:
        """Update position prices."""
        return await self.position_repo.update_position_prices(price_updates)

    # Portfolio operations
    async def save_portfolio(self, portfolio: Portfolio) -> bool:
        """Save portfolio."""
        return await self.portfolio_repo.save_portfolio(portfolio)

    async def get_portfolio(self, portfolio_id: str) -> Portfolio | None:
        """Get portfolio by ID."""
        return await self.portfolio_repo.get_portfolio(portfolio_id)

    async def get_all_portfolios(self) -> list[Portfolio]:
        """Get all portfolios."""
        return await self.portfolio_repo.get_all_portfolios()

    async def update_portfolio(self, portfolio: Portfolio) -> bool:
        """Update portfolio."""
        return await self.portfolio_repo.update_portfolio(portfolio)

    async def delete_portfolio(self, portfolio_id: str) -> bool:
        """Delete portfolio."""
        return await self.portfolio_repo.delete_portfolio(portfolio_id)

    async def get_portfolio_by_name(self, name: str) -> Portfolio | None:
        """Get portfolio by name."""
        return await self.portfolio_repo.get_portfolio_by_name(name)

    # Statistics and reporting
    async def get_repository_stats(self) -> dict[str, Any]:
        """Get comprehensive repository statistics."""
        try:
            trade_count = await self.trade_repo.get_trade_count()
            position_count = await self.position_repo.get_position_count()
            portfolio_count = await self.portfolio_repo.get_portfolio_count()

            return {
                "trades": {
                    "total": trade_count,
                    "pending": len(await self.trade_repo.get_trades_by_status("pending")),
                    "executed": len(await self.trade_repo.get_trades_by_status("executed")),
                    "cancelled": len(await self.trade_repo.get_trades_by_status("cancelled")),
                },
                "positions": {
                    "total": position_count,
                    "long": len(await self.position_repo.get_long_positions()),
                    "short": len(await self.position_repo.get_short_positions()),
                    "profitable": len(await self.position_repo.get_profitable_positions()),
                    "losing": len(await self.position_repo.get_losing_positions()),
                },
                "portfolios": {"total": portfolio_count},
            }
        except Exception as e:
            self.logger.error(f"Failed to get repository stats: {e}")
            return {}

    async def clear_all_data(self) -> bool:
        """Clear all data from repository."""
        try:
            trade_cleared = await self.trade_repo.clear_all_trades()
            position_cleared = await self.position_repo.clear_all_positions()
            portfolio_cleared = await self.portfolio_repo.clear_all_portfolios()

            success = trade_cleared and position_cleared and portfolio_cleared
            if success:
                self.logger.info("All repository data cleared")
            else:
                self.logger.warning("Some data may not have been cleared")

            return success
        except Exception as e:
            self.logger.error(f"Failed to clear all data: {e}")
            return False


# Global instance for backward compatibility
_global_repository = None


def get_trading_repository() -> TradingRepository:
    """Get global trading repository instance."""
    global _global_repository

    if _global_repository is None:
        _global_repository = TradingRepository()

    return _global_repository
