"""
Trading Repository Interface - V2 Compliant Module
=================================================

Abstract interface for trading data access with V2 compliance.
Extracted from trading_repository.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from abc import ABC, abstractmethod

from ..models import Trade


class TradingRepositoryInterface(ABC):
    """Abstract interface for trading data access with V2 compliance.

    V2 COMPLIANCE: Repository pattern with async operations and comprehensive error handling.
    DESIGN PATTERN: Repository pattern providing clean data access abstraction.
    """

    @abstractmethod
    async def save_trade(self, trade: Trade) -> bool:
        """Save a trade to storage.

        Args:
            trade: Trade object to save

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_trade(self, trade_id: str) -> Trade | None:
        """Retrieve a trade by ID.

        Args:
            trade_id: Unique identifier for the trade

        Returns:
            Trade object if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_trades_by_symbol(self, symbol: str, limit: int = 100) -> list[Trade]:
        """Get trades for a specific symbol.

        Args:
            symbol: Trading symbol (e.g., 'AAPL', 'GOOGL')
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects, ordered by timestamp (newest first)
        """
        pass

    @abstractmethod
    async def get_all_trades(self, limit: int = 1000) -> list[Trade]:
        """Get all trades.

        Args:
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects, ordered by timestamp (newest first)
        """
        pass

    @abstractmethod
    async def update_trade_status(self, trade_id: str, status: str) -> bool:
        """Update trade status.

        Args:
            trade_id: Unique identifier for the trade
            status: New status ('pending', 'executed', 'cancelled')

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def delete_trade(self, trade_id: str) -> bool:
        """Delete a trade.

        Args:
            trade_id: Unique identifier for the trade

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_trades_by_status(self, status: str, limit: int = 100) -> list[Trade]:
        """Get trades by status.

        Args:
            status: Trade status ('pending', 'executed', 'cancelled')
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects with specified status
        """
        pass

    @abstractmethod
    async def get_trades_by_date_range(self, start_date, end_date, limit: int = 100) -> list[Trade]:
        """Get trades within date range.

        Args:
            start_date: Start date for filtering
            end_date: End date for filtering
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects within date range
        """
        pass

    @abstractmethod
    async def get_trade_count(self) -> int:
        """Get total number of trades.

        Returns:
            Total number of trades in storage
        """
        pass

    @abstractmethod
    async def clear_all_trades(self) -> bool:
        """Clear all trades from storage.

        Returns:
            True if successful, False otherwise
        """
        pass
