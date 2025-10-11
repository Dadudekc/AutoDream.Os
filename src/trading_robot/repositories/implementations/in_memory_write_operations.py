"""
In-Memory Write Operations - V2 Compliant
==========================================

Write operations for in-memory trading repository.
Extracted for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted from Agent-7's work)
"""

from ...core.unified_logging_system import get_logger
from ...core.unified_validation_system import get_unified_validator
from ..models.trading_models import Position, Trade


class InMemoryWriteOperations:
    """Write operations for in-memory repository."""

    def __init__(self, trades_ref, positions_ref, lock_ref):
        """Initialize with storage and lock references."""
        self.logger = get_logger(__name__)
        self.validator = get_unified_validator()
        self.trades = trades_ref
        self.positions = positions_ref
        self.lock = lock_ref

    async def save_trade(self, trade: Trade) -> bool:
        """Save trade to memory."""
        try:
            if not self.validator.validate_required(trade):
                self.logger.error("Cannot save invalid trade")
                return False

            async with self.lock:
                self.trades[trade.id] = trade
                self.logger.info(f"Trade saved: {trade.id} ({trade.symbol})")
                return True

        except Exception as e:
            self.logger.error(f"Failed to save trade {trade.id}: {e}")
            return False

    async def update_trade(self, trade: Trade) -> bool:
        """Update existing trade."""
        try:
            if not trade.id or trade.id not in self.trades:
                self.logger.error(f"Trade not found: {trade.id}")
                return False

            async with self.lock:
                self.trades[trade.id] = trade
                self.logger.info(f"Trade updated: {trade.id}")
                return True

        except Exception as e:
            self.logger.error(f"Failed to update trade {trade.id}: {e}")
            return False

    async def delete_trade(self, trade_id: str) -> bool:
        """Delete trade from memory."""
        try:
            if not trade_id or not trade_id.strip():
                self.logger.error("Trade ID cannot be empty")
                return False

            async with self.lock:
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

    async def save_position(self, position: Position) -> bool:
        """Save position to memory."""
        try:
            if not self.validator.validate_required(position):
                self.logger.error("Cannot save invalid position")
                return False

            async with self.lock:
                self.positions[position.symbol] = position
                self.logger.info(f"Position saved: {position.symbol}")
                return True

        except Exception as e:
            self.logger.error(f"Failed to save position {position.symbol}: {e}")
            return False

    async def update_position(self, position: Position) -> bool:
        """Update existing position."""
        try:
            if not position.symbol or position.symbol not in self.positions:
                self.logger.error(f"Position not found: {position.symbol}")
                return False

            async with self.lock:
                self.positions[position.symbol] = position
                self.logger.info(f"Position updated: {position.symbol}")
                return True

        except Exception as e:
            self.logger.error(f"Failed to update position {position.symbol}: {e}")
            return False

    async def delete_position(self, symbol: str) -> bool:
        """Delete position from memory."""
        try:
            if not symbol or not symbol.strip():
                self.logger.error("Symbol cannot be empty")
                return False

            async with self.lock:
                if symbol in self.positions:
                    del self.positions[symbol]
                    self.logger.info(f"Position deleted: {symbol}")
                    return True
                else:
                    self.logger.warning(f"Position not found: {symbol}")
                    return False

        except Exception as e:
            self.logger.error(f"Failed to delete position {symbol}: {e}")
            return False

    async def clear_all_data(self) -> bool:
        """Clear all data from memory."""
        try:
            async with self.lock:
                trade_count = len(self.trades)
                position_count = len(self.positions)
                self.trades.clear()
                self.positions.clear()
                self.logger.info(f"Cleared {trade_count} trades, {position_count} positions")
                return True

        except Exception as e:
            self.logger.error(f"Failed to clear all data: {e}")
            return False
