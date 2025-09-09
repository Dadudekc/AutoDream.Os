"""
Trading Repository Implementation - V2 Compliant Module
=====================================================

In-memory implementation of trading repository with V2 compliance.
Extracted from trading_repository.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import asyncio
import logging

from ..interfaces.trading_repository_interface import TradingRepositoryInterface
from ..models import Trade


class TradingRepositoryImpl(TradingRepositoryInterface):
    """In-memory implementation of trading repository with V2 compliance.

    V2 COMPLIANCE: Repository pattern with async operations and comprehensive error handling.
    DESIGN PATTERN: Repository pattern providing clean data access abstraction.
    """

    def __init__(self):
        """Initialize trading repository implementation."""
        self.logger = logging.getLogger(__name__)
        self.trades: dict[str, Trade] = {}
        self._lock = asyncio.Lock()

    async def save_trade(self, trade: Trade) -> bool:
        """Save trade with V2 compliance.

        Args:
            trade: Trade object to save

        Returns:
            True if successful, False otherwise
        """
        try:
            if not isinstance(trade, Trade):
                self.logger.error("Trade must be a Trade object")
                return False

            async with self._lock:
                self.trades[trade.id] = trade
                self.logger.debug(f"Trade saved: {trade.id}")

            return True

        except Exception as e:
            self.logger.error(f"Failed to save trade {trade.id}: {e}")
            return False

    async def get_trade(self, trade_id: str) -> Trade | None:
        """Get trade by ID with V2 compliance.

        Args:
            trade_id: Unique identifier for the trade

        Returns:
            Trade object if found, None otherwise
        """
        try:
            if not trade_id or not trade_id.strip():
                self.logger.error("Trade ID cannot be empty")
                return None

            trade = self.trades.get(trade_id)
            if trade:
                self.logger.debug(f"Trade retrieved: {trade_id}")
            else:
                self.logger.warning(f"Trade not found: {trade_id}")

            return trade

        except Exception as e:
            self.logger.error(f"Failed to get trade {trade_id}: {e}")
            return None

    async def get_trades_by_symbol(self, symbol: str, limit: int = 100) -> list[Trade]:
        """Get trades for symbol with V2 compliance.

        Args:
            symbol: Trading symbol
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects, ordered by timestamp (newest first)
        """
        try:
            if not symbol or not symbol.strip():
                self.logger.error("Symbol cannot be empty")
                return []

            if limit <= 0:
                self.logger.error("Limit must be positive")
                return []

            trades = [t for t in self.trades.values() if t.symbol == symbol]
            trades.sort(key=lambda x: x.timestamp, reverse=True)
            result = trades[:limit]

            self.logger.debug(f"Found {len(result)} trades for symbol {symbol}")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get trades for symbol {symbol}: {e}")
            return []

    async def get_all_trades(self, limit: int = 1000) -> list[Trade]:
        """Get all trades with V2 compliance.

        Args:
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects, ordered by timestamp (newest first)
        """
        try:
            if limit <= 0:
                self.logger.error("Limit must be positive")
                return []

            trades = list(self.trades.values())
            trades.sort(key=lambda x: x.timestamp, reverse=True)
            result = trades[:limit]

            self.logger.debug(f"Retrieved {len(result)} trades (total: {len(trades)})")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get all trades: {e}")
            return []

    async def update_trade_status(self, trade_id: str, status: str) -> bool:
        """Update trade status with V2 compliance.

        Args:
            trade_id: Unique identifier for the trade
            status: New status ('pending', 'executed', 'cancelled')

        Returns:
            True if successful, False otherwise
        """
        try:
            if not trade_id or not trade_id.strip():
                self.logger.error("Trade ID cannot be empty")
                return False

            if status not in ["pending", "executed", "cancelled"]:
                self.logger.error(f"Invalid status: {status}")
                return False

            async with self._lock:
                if trade_id in self.trades:
                    self.trades[trade_id].status = status
                    self.logger.info(f"Trade status updated: {trade_id} -> {status}")
                    return True
                else:
                    self.logger.warning(f"Trade not found: {trade_id}")
                    return False

        except Exception as e:
            self.logger.error(f"Failed to update trade status {trade_id}: {e}")
            return False

    async def delete_trade(self, trade_id: str) -> bool:
        """Delete trade with V2 compliance.

        Args:
            trade_id: Unique identifier for the trade

        Returns:
            True if successful, False otherwise
        """
        try:
            if not trade_id or not trade_id.strip():
                self.logger.error("Trade ID cannot be empty")
                return False

            async with self._lock:
                if trade_id in self.trades:
                    del self.trades[trade_id]
                    self.logger.info(f"Trade deleted: {trade_id}")
                    return True
                else:
                    self.logger.warning(f"Trade not found: {trade_id}")
                    return False

        except Exception as e:
            self.logger.error(f"Failed to delete trade {trade_id}: {e}")
            return False

    async def get_trades_by_status(self, status: str, limit: int = 100) -> list[Trade]:
        """Get trades by status with V2 compliance.

        Args:
            status: Trade status ('pending', 'executed', 'cancelled')
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects with specified status
        """
        try:
            if status not in ["pending", "executed", "cancelled"]:
                self.logger.error(f"Invalid status: {status}")
                return []

            if limit <= 0:
                self.logger.error("Limit must be positive")
                return []

            trades = [t for t in self.trades.values() if t.status == status]
            trades.sort(key=lambda x: x.timestamp, reverse=True)
            result = trades[:limit]

            self.logger.debug(f"Found {len(result)} trades with status {status}")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get trades by status {status}: {e}")
            return []

    async def get_trades_by_date_range(self, start_date, end_date, limit: int = 100) -> list[Trade]:
        """Get trades within date range with V2 compliance.

        Args:
            start_date: Start date for filtering
            end_date: End date for filtering
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects within date range
        """
        try:
            if limit <= 0:
                self.logger.error("Limit must be positive")
                return []

            trades = [t for t in self.trades.values() if start_date <= t.timestamp <= end_date]
            trades.sort(key=lambda x: x.timestamp, reverse=True)
            result = trades[:limit]

            self.logger.debug(f"Found {len(result)} trades in date range")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get trades by date range: {e}")
            return []

    async def get_trade_count(self) -> int:
        """Get total number of trades with V2 compliance.

        Returns:
            Total number of trades in storage
        """
        try:
            count = len(self.trades)
            self.logger.debug(f"Total trades: {count}")
            return count

        except Exception as e:
            self.logger.error(f"Failed to get trade count: {e}")
            return 0

    async def clear_all_trades(self) -> bool:
        """Clear all trades with V2 compliance.

        Returns:
            True if successful, False otherwise
        """
        try:
            async with self._lock:
                count = len(self.trades)
                self.trades.clear()
                self.logger.info(f"Cleared {count} trades")
                return True

        except Exception as e:
            self.logger.error(f"Failed to clear all trades: {e}")
            return False
