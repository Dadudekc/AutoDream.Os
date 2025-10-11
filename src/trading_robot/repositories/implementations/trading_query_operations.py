"""
Trading Repository Query Operations - V2 Compliant
===================================================

Query operations for trading repository.
Extracted from trading_repository_impl.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted from Agent-7's work)
"""

import logging

from ..models import Trade


class TradingQueryOperations:
    """Query operations for trading repository."""

    def __init__(self, storage_ref):
        """Initialize with reference to storage."""
        self.logger = logging.getLogger(__name__)
        self.storage = storage_ref

    async def get_trade(self, trade_id: str) -> Trade | None:
        """Get trade by ID."""
        try:
            if not trade_id or not trade_id.strip():
                self.logger.error("Trade ID cannot be empty")
                return None

            trade = self.storage.get(trade_id)
            if trade:
                self.logger.debug(f"Trade retrieved: {trade_id}")
            else:
                self.logger.warning(f"Trade not found: {trade_id}")

            return trade

        except Exception as e:
            self.logger.error(f"Failed to get trade {trade_id}: {e}")
            return None

    async def get_trades_by_symbol(self, symbol: str, limit: int = 100) -> list[Trade]:
        """Get trades for symbol."""
        try:
            if not symbol or not symbol.strip():
                self.logger.error("Symbol cannot be empty")
                return []

            if limit <= 0:
                self.logger.error("Limit must be positive")
                return []

            trades = [t for t in self.storage.values() if t.symbol == symbol]
            trades.sort(key=lambda x: x.timestamp, reverse=True)
            result = trades[:limit]

            self.logger.debug(f"Found {len(result)} trades for symbol {symbol}")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get trades for symbol {symbol}: {e}")
            return []

    async def get_all_trades(self, limit: int = 1000) -> list[Trade]:
        """Get all trades."""
        try:
            if limit <= 0:
                self.logger.error("Limit must be positive")
                return []

            trades = list(self.storage.values())
            trades.sort(key=lambda x: x.timestamp, reverse=True)
            result = trades[:limit]

            self.logger.debug(f"Retrieved {len(result)} trades")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get all trades: {e}")
            return []

    async def get_trades_by_status(self, status: str, limit: int = 100) -> list[Trade]:
        """Get trades by status."""
        try:
            if status not in ["pending", "executed", "cancelled"]:
                self.logger.error(f"Invalid status: {status}")
                return []

            if limit <= 0:
                self.logger.error("Limit must be positive")
                return []

            trades = [t for t in self.storage.values() if t.status == status]
            trades.sort(key=lambda x: x.timestamp, reverse=True)
            result = trades[:limit]

            self.logger.debug(f"Found {len(result)} trades with status {status}")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get trades by status {status}: {e}")
            return []

    async def get_trades_by_date_range(self, start_date, end_date, limit: int = 100) -> list[Trade]:
        """Get trades within date range."""
        try:
            if limit <= 0:
                self.logger.error("Limit must be positive")
                return []

            trades = [t for t in self.storage.values() if start_date <= t.timestamp <= end_date]
            trades.sort(key=lambda x: x.timestamp, reverse=True)
            result = trades[:limit]

            self.logger.debug(f"Found {len(result)} trades in date range")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get trades by date range: {e}")
            return []

    async def get_trade_count(self) -> int:
        """Get total number of trades."""
        try:
            count = len(self.storage)
            self.logger.debug(f"Total trades: {count}")
            return count

        except Exception as e:
            self.logger.error(f"Failed to get trade count: {e}")
            return 0
