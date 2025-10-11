"""
In-Memory Query Operations - V2 Compliant
==========================================

Query operations for in-memory trading repository.
Extracted for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted from Agent-7's work)
"""

from ...core.unified_logging_system import get_logger
from ..models.trading_models import Position, Trade


class InMemoryQueryOperations:
    """Query operations for in-memory repository."""

    def __init__(self, trades_ref, positions_ref):
        """Initialize with storage references."""
        self.logger = get_logger(__name__)
        self.trades = trades_ref
        self.positions = positions_ref

    async def get_trade(self, trade_id: str) -> Trade | None:
        """Get trade by ID."""
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
        """Get trades by symbol."""
        try:
            if not symbol or not symbol.strip():
                self.logger.error("Symbol cannot be empty")
                return []

            symbol_trades = [t for t in self.trades.values() if t.symbol == symbol]
            symbol_trades.sort(key=lambda t: t.timestamp, reverse=True)

            result = symbol_trades[:limit]
            self.logger.debug(f"Found {len(result)} trades for symbol {symbol}")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get trades for symbol {symbol}: {e}")
            return []

    async def get_all_trades(self, limit: int = 1000) -> list[Trade]:
        """Get all trades."""
        try:
            all_trades = list(self.trades.values())
            all_trades.sort(key=lambda t: t.timestamp, reverse=True)
            result = all_trades[:limit]
            self.logger.debug(f"Retrieved {len(result)} trades")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get all trades: {e}")
            return []

    async def get_position(self, symbol: str) -> Position | None:
        """Get position by symbol."""
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
        """Get all positions."""
        try:
            positions = list(self.positions.values())
            self.logger.debug(f"Retrieved {len(positions)} positions")
            return positions

        except Exception as e:
            self.logger.error(f"Failed to get all positions: {e}")
            return []

    async def get_trade_count(self) -> int:
        """Get total trade count."""
        try:
            count = len(self.trades)
            self.logger.debug(f"Total trades: {count}")
            return count

        except Exception as e:
            self.logger.error(f"Failed to get trade count: {e}")
            return 0

    async def get_position_count(self) -> int:
        """Get total position count."""
        try:
            count = len(self.positions)
            self.logger.debug(f"Total positions: {count}")
            return count

        except Exception as e:
            self.logger.error(f"Failed to get position count: {e}")
            return 0
