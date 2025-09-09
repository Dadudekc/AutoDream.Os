#!/usr/bin/env python3
"""
In-Memory Trading Repository - V2 Compliance Module
==================================================

In-memory implementation of trading repository with V2 compliance.
Extracted from trading_repository.py for V2 compliance.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import asyncio

from ...core.unified_logging_system import get_logger
from ...core.unified_validation_system import get_unified_validator
from ..interfaces.trading_repository_interface import TradingRepositoryInterface
from ..models.trading_models import Position, Trade


class InMemoryTradingRepository(TradingRepositoryInterface):
    """In-memory implementation of trading repository with V2 compliance.

    V2 COMPLIANCE: Thread-safe async operations, comprehensive error handling, proper logging.
    """

    def __init__(self):
        """Initialize in-memory repository with V2 compliance."""
        self.logger = get_logger(__name__)
        self.validator = get_unified_validator()
        self.trades: dict[str, Trade] = {}
        self.positions: dict[str, Position] = {}
        self._lock = asyncio.Lock()

    async def save_trade(self, trade: Trade) -> bool:
        """Save trade to memory with V2 compliance.

        Args:
            trade: Trade object to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate trade before saving
            if not self.validator.validate_required(trade):
                self.logger.error("Cannot save invalid trade")
                return False

            async with self._lock:
                self.trades[trade.id] = trade
                self.logger.info(f"Trade saved: {trade.id} ({trade.symbol})")
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
            self.logger.debug(f"Trade lookup: {trade_id} - {'found' if trade else 'not found'}")
            return trade

        except Exception as e:
            self.logger.error(f"Failed to get trade {trade_id}: {e}")
            return None

    async def get_trades_by_symbol(self, symbol: str, limit: int = 100) -> list[Trade]:
        """Get trades by symbol with V2 compliance.

        Args:
            symbol: Trading symbol
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects
        """
        try:
            if not symbol or not symbol.strip():
                self.logger.error("Symbol cannot be empty")
                return []

            symbol_trades = [trade for trade in self.trades.values() if trade.symbol == symbol]
            symbol_trades.sort(key=lambda t: t.timestamp, reverse=True)

            result = symbol_trades[:limit]
            self.logger.debug(f"Found {len(result)} trades for symbol {symbol}")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get trades for symbol {symbol}: {e}")
            return []

    async def get_trades_by_status(self, status: str, limit: int = 100) -> list[Trade]:
        """Get trades by status with V2 compliance.

        Args:
            status: Trade status
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects
        """
        try:
            if not status or not status.strip():
                self.logger.error("Status cannot be empty")
                return []

            status_trades = [trade for trade in self.trades.values() if trade.status == status]
            status_trades.sort(key=lambda t: t.timestamp, reverse=True)

            result = status_trades[:limit]
            self.logger.debug(f"Found {len(result)} trades with status {status}")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get trades for status {status}: {e}")
            return []

    async def get_all_trades(self, limit: int = 1000) -> list[Trade]:
        """Get all trades with V2 compliance.

        Args:
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects
        """
        try:
            all_trades = list(self.trades.values())
            all_trades.sort(key=lambda t: t.timestamp, reverse=True)

            result = all_trades[:limit]
            self.logger.debug(f"Retrieved {len(result)} trades")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get all trades: {e}")
            return []

    async def update_trade_status(self, trade_id: str, status: str) -> bool:
        """Update trade status with V2 compliance.

        Args:
            trade_id: Unique identifier for the trade
            status: New status

        Returns:
            True if successful, False otherwise
        """
        try:
            if not trade_id or not trade_id.strip():
                self.logger.error("Trade ID cannot be empty")
                return False

            if status not in ["pending", "executed", "cancelled"]:
                self.logger.error("Invalid status")
                return False

            async with self._lock:
                if trade_id in self.trades:
                    self.trades[trade_id].status = status
                    self.logger.info(f"Updated trade {trade_id} status to {status}")
                    return True
                else:
                    self.logger.warning(f"Trade {trade_id} not found")
                    return False

        except Exception as e:
            self.logger.error(f"Failed to update trade {trade_id} status: {e}")
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
                    self.logger.info(f"Deleted trade {trade_id}")
                    return True
                else:
                    self.logger.warning(f"Trade {trade_id} not found")
                    return False

        except Exception as e:
            self.logger.error(f"Failed to delete trade {trade_id}: {e}")
            return False

    async def save_position(self, position: Position) -> bool:
        """Save position with V2 compliance.

        Args:
            position: Position object to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate position before saving
            if not self.validator.validate_required(position):
                self.logger.error("Cannot save invalid position")
                return False

            async with self._lock:
                self.positions[position.symbol] = position
                self.logger.info(f"Position saved: {position.symbol}")
                return True

        except Exception as e:
            self.logger.error(f"Failed to save position {position.symbol}: {e}")
            return False

    async def get_position(self, symbol: str) -> Position | None:
        """Get position by symbol with V2 compliance.

        Args:
            symbol: Trading symbol

        Returns:
            Position object if found, None otherwise
        """
        try:
            if not symbol or not symbol.strip():
                self.logger.error("Symbol cannot be empty")
                return None

            position = self.positions.get(symbol)
            self.logger.debug(f"Position lookup: {symbol} - {'found' if position else 'not found'}")
            return position

        except Exception as e:
            self.logger.error(f"Failed to get position {symbol}: {e}")
            return None

    async def get_all_positions(self) -> list[Position]:
        """Get all positions with V2 compliance.

        Returns:
            List of Position objects
        """
        try:
            positions = list(self.positions.values())
            self.logger.debug(f"Retrieved {len(positions)} positions")
            return positions

        except Exception as e:
            self.logger.error(f"Failed to get all positions: {e}")
            return []

    async def delete_position(self, symbol: str) -> bool:
        """Delete position with V2 compliance.

        Args:
            symbol: Trading symbol

        Returns:
            True if successful, False otherwise
        """
        try:
            if not symbol or not symbol.strip():
                self.logger.error("Symbol cannot be empty")
                return False

            async with self._lock:
                if symbol in self.positions:
                    del self.positions[symbol]
                    self.logger.info(f"Deleted position {symbol}")
                    return True
                else:
                    self.logger.warning(f"Position {symbol} not found")
                    return False

        except Exception as e:
            self.logger.error(f"Failed to delete position {symbol}: {e}")
            return False
