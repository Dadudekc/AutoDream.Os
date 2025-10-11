"""
Trading Repository Write Operations - V2 Compliant
===================================================

Write operations for trading repository.
Extracted from trading_repository_impl.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted from Agent-7's work)
"""

import logging

from ..models import Trade


class TradingWriteOperations:
    """Write operations for trading repository."""

    def __init__(self, storage_ref, lock_ref):
        """Initialize with references to storage and lock."""
        self.logger = logging.getLogger(__name__)
        self.storage = storage_ref
        self.lock = lock_ref

    async def save_trade(self, trade: Trade) -> bool:
        """Save trade."""
        try:
            if not isinstance(trade, Trade):
                self.logger.error("Trade must be a Trade object")
                return False

            async with self.lock:
                self.storage[trade.id] = trade
                self.logger.debug(f"Trade saved: {trade.id}")

            return True

        except Exception as e:
            self.logger.error(f"Failed to save trade {trade.id}: {e}")
            return False

    async def update_trade_status(self, trade_id: str, status: str) -> bool:
        """Update trade status."""
        try:
            if not trade_id or not trade_id.strip():
                self.logger.error("Trade ID cannot be empty")
                return False

            if status not in ["pending", "executed", "cancelled"]:
                self.logger.error(f"Invalid status: {status}")
                return False

            async with self.lock:
                if trade_id in self.storage:
                    self.storage[trade_id].status = status
                    self.logger.info(f"Trade status updated: {trade_id} -> {status}")
                    return True
                else:
                    self.logger.warning(f"Trade not found: {trade_id}")
                    return False

        except Exception as e:
            self.logger.error(f"Failed to update trade status {trade_id}: {e}")
            return False

    async def delete_trade(self, trade_id: str) -> bool:
        """Delete trade."""
        try:
            if not trade_id or not trade_id.strip():
                self.logger.error("Trade ID cannot be empty")
                return False

            async with self.lock:
                if trade_id in self.storage:
                    del self.storage[trade_id]
                    self.logger.info(f"Trade deleted: {trade_id}")
                    return True
                else:
                    self.logger.warning(f"Trade not found: {trade_id}")
                    return False

        except Exception as e:
            self.logger.error(f"Failed to delete trade {trade_id}: {e}")
            return False

    async def clear_all_trades(self) -> bool:
        """Clear all trades."""
        try:
            async with self.lock:
                count = len(self.storage)
                self.storage.clear()
                self.logger.info(f"Cleared {count} trades")
                return True

        except Exception as e:
            self.logger.error(f"Failed to clear all trades: {e}")
            return False
