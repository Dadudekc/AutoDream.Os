"""
Trading Repository Implementation - V2 Compliant
================================================

In-memory trading repository orchestrator.
Refactored for V2 compliance by Agent-3.

Original Author: Agent-7 - Web Development Specialist
V2 Refactor: Agent-3 - Infrastructure & DevOps Specialist
"""

import asyncio
import logging

from ..interfaces.trading_repository_interface import TradingRepositoryInterface
from ..models import Trade
from .trading_query_operations import TradingQueryOperations
from .trading_write_operations import TradingWriteOperations


class TradingRepositoryImpl(TradingRepositoryInterface):
    """In-memory trading repository with V2 compliance.

    Orchestrates query and write operations through modular components.
    """

    def __init__(self):
        """Initialize trading repository."""
        self.logger = logging.getLogger(__name__)
        self.trades: dict[str, Trade] = {}
        self._lock = asyncio.Lock()

        # Initialize operation modules
        self.queries = TradingQueryOperations(self.trades)
        self.writes = TradingWriteOperations(self.trades, self._lock)

    # Delegate to query operations
    async def get_trade(self, trade_id: str) -> Trade | None:
        """Get trade by ID."""
        return await self.queries.get_trade(trade_id)

    async def get_trades_by_symbol(self, symbol: str, limit: int = 100) -> list[Trade]:
        """Get trades for symbol."""
        return await self.queries.get_trades_by_symbol(symbol, limit)

    async def get_all_trades(self, limit: int = 1000) -> list[Trade]:
        """Get all trades."""
        return await self.queries.get_all_trades(limit)

    async def get_trades_by_status(self, status: str, limit: int = 100) -> list[Trade]:
        """Get trades by status."""
        return await self.queries.get_trades_by_status(status, limit)

    async def get_trades_by_date_range(self, start_date, end_date, limit: int = 100) -> list[Trade]:
        """Get trades within date range."""
        return await self.queries.get_trades_by_date_range(start_date, end_date, limit)

    async def get_trade_count(self) -> int:
        """Get total number of trades."""
        return await self.queries.get_trade_count()

    # Delegate to write operations
    async def save_trade(self, trade: Trade) -> bool:
        """Save trade."""
        return await self.writes.save_trade(trade)

    async def update_trade_status(self, trade_id: str, status: str) -> bool:
        """Update trade status."""
        return await self.writes.update_trade_status(trade_id, status)

    async def delete_trade(self, trade_id: str) -> bool:
        """Delete trade."""
        return await self.writes.delete_trade(trade_id)

    async def clear_all_trades(self) -> bool:
        """Clear all trades."""
        return await self.writes.clear_all_trades()
