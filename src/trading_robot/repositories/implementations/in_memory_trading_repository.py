"""
In-Memory Trading Repository - V2 Compliant
============================================

In-memory trading repository orchestrator.
Refactored for V2 compliance by Agent-3.

Original: Agent-7 - Web Development Specialist
V2 Refactor: Agent-3 - Infrastructure & DevOps Specialist
"""

import asyncio

from ...core.unified_logging_system import get_logger
from ...core.unified_validation_system import get_unified_validator
from ..interfaces.trading_repository_interface import TradingRepositoryInterface
from ..models.trading_models import Position, Trade
from .in_memory_query_operations import InMemoryQueryOperations
from .in_memory_write_operations import InMemoryWriteOperations


class InMemoryTradingRepository(TradingRepositoryInterface):
    """In-memory trading repository with V2 compliance.

    Orchestrates query and write operations through modular components.
    """

    def __init__(self):
        """Initialize in-memory repository."""
        self.logger = get_logger(__name__)
        self.validator = get_unified_validator()
        self.trades: dict[str, Trade] = {}
        self.positions: dict[str, Position] = {}
        self._lock = asyncio.Lock()

        # Initialize operation modules
        self.queries = InMemoryQueryOperations(self.trades, self.positions)
        self.writes = InMemoryWriteOperations(self.trades, self.positions, self._lock)

    # Delegate to query operations
    async def get_trade(self, trade_id: str) -> Trade | None:
        """Get trade by ID."""
        return await self.queries.get_trade(trade_id)

    async def get_trades_by_symbol(self, symbol: str, limit: int = 100) -> list[Trade]:
        """Get trades by symbol."""
        return await self.queries.get_trades_by_symbol(symbol, limit)

    async def get_all_trades(self, limit: int = 1000) -> list[Trade]:
        """Get all trades."""
        return await self.queries.get_all_trades(limit)

    async def get_position(self, symbol: str) -> Position | None:
        """Get position by symbol."""
        return await self.queries.get_position(symbol)

    async def get_all_positions(self) -> list[Position]:
        """Get all positions."""
        return await self.queries.get_all_positions()

    async def get_trade_count(self) -> int:
        """Get trade count."""
        return await self.queries.get_trade_count()

    async def get_position_count(self) -> int:
        """Get position count."""
        return await self.queries.get_position_count()

    # Delegate to write operations
    async def save_trade(self, trade: Trade) -> bool:
        """Save trade."""
        return await self.writes.save_trade(trade)

    async def update_trade(self, trade: Trade) -> bool:
        """Update trade."""
        return await self.writes.update_trade(trade)

    async def delete_trade(self, trade_id: str) -> bool:
        """Delete trade."""
        return await self.writes.delete_trade(trade_id)

    async def save_position(self, position: Position) -> bool:
        """Save position."""
        return await self.writes.save_position(position)

    async def update_position(self, position: Position) -> bool:
        """Update position."""
        return await self.writes.update_position(position)

    async def delete_position(self, symbol: str) -> bool:
        """Delete position."""
        return await self.writes.delete_position(symbol)

    async def clear_all_data(self) -> bool:
        """Clear all data."""
        return await self.writes.clear_all_data()
