"""
Trading Repository - V2 Compliant Repository Pattern Implementation
===================================================================

Single source of truth for trading data access operations with V2 compliance standards.

V2 COMPLIANCE: Repository pattern, dependency injection, async operations, comprehensive error handling
DESIGN PATTERN: Repository pattern with CQRS principles
ARCHITECTURE: Clean architecture with proper separation of concerns

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Enhancement
Status: V2 COMPLIANT - Advanced Repository Pattern Implementation
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import asyncio
from ..core.unified_logging_system import get_logger
from ..core.unified_validation_system import get_unified_validator



@dataclass
class Trade:
    """
    Trade data structure with V2 compliance validation.

    V2 COMPLIANCE: Type-safe data structure with validation and metadata.
    """
    id: str
    symbol: str
    side: str  # 'buy' or 'sell'
    quantity: float
    price: float
    timestamp: datetime
    status: str = "pending"  # 'pending', 'executed', 'cancelled'
    order_type: str = "market"  # 'market', 'limit', 'stop'
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate trade data on initialization."""
        if not self.id or not self.id.strip():
            raise ValueError("Trade ID cannot be empty")
        if not self.symbol or not self.symbol.strip():
            raise ValueError("Symbol cannot be empty")
        if self.side not in ['buy', 'sell']:
            raise ValueError("Side must be 'buy' or 'sell'")
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.price <= 0:
            raise ValueError("Price must be positive")
        if self.status not in ['pending', 'executed', 'cancelled']:
            raise ValueError("Invalid status")
        if self.order_type not in ['market', 'limit', 'stop']:
            raise ValueError("Invalid order type")

    def is_completed(self) -> bool:
        """Check if trade is completed."""
        return self.status in ['executed', 'cancelled']

    def calculate_value(self) -> float:
        """Calculate total trade value."""
        return self.quantity * self.price


@dataclass
class Position:
    """
    Position data structure with V2 compliance validation.

    V2 COMPLIANCE: Type-safe data structure with validation and performance metrics.
    """
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    pnl: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate position data on initialization."""
        if not self.symbol or not self.symbol.strip():
            raise ValueError("Symbol cannot be empty")

    def update_pnl(self, new_price: float) -> None:
        """Update P&L based on new price."""
        self.current_price = new_price
        self.pnl = (new_price - self.average_price) * self.quantity
        self.timestamp = datetime.now()

    def get_pnl_percentage(self) -> float:
        """Calculate P&L as percentage."""
        if self.average_price == 0:
            return 0.0
        return (self.pnl / (self.average_price * abs(self.quantity))) * 100

    def is_long(self) -> bool:
        """Check if this is a long position."""
        return self.quantity > 0

    def is_short(self) -> bool:
        """Check if this is a short position."""
        return self.quantity < 0


class TradingRepositoryInterface(ABC):
    """
    Abstract interface for trading data access with V2 compliance.

    V2 COMPLIANCE: Repository pattern with async operations and comprehensive error handling.
    DESIGN PATTERN: Repository pattern providing clean data access abstraction.
    """

    @abstractmethod
    async def save_trade(self, trade: Trade) -> bool:
        """
        Save a trade to storage.

        Args:
            trade: Trade object to save

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_trade(self, trade_id: str) -> Optional[Trade]:
        """
        Retrieve a trade by ID.

        Args:
            trade_id: Unique identifier for the trade

        Returns:
            Trade object if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_trades_by_symbol(self, symbol: str, limit: int = 100) -> List[Trade]:
        """
        Get trades for a specific symbol.

        Args:
            symbol: Trading symbol (e.g., 'AAPL', 'GOOGL')
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects, ordered by timestamp (newest first)
        """
        pass

    @abstractmethod
    async def get_all_trades(self, limit: int = 1000) -> List[Trade]:
        """
        Get all trades.

        Args:
            limit: Maximum number of trades to return

        Returns:
            List of Trade objects, ordered by timestamp (newest first)
        """
        pass

    @abstractmethod
    async def update_trade_status(self, trade_id: str, status: str) -> bool:
        """
        Update trade status.

        Args:
            trade_id: Unique identifier for the trade
            status: New status ('pending', 'executed', 'cancelled')

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def save_position(self, position: Position) -> bool:
        """
        Save position to storage.

        Args:
            position: Position object to save

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_position(self, symbol: str) -> Optional[Position]:
        """
        Get position for symbol.

        Args:
            symbol: Trading symbol

        Returns:
            Position object if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all_positions(self) -> List[Position]:
        """
        Get all positions.

        Returns:
            List of Position objects
        """
        pass

    @abstractmethod
    async def delete_position(self, symbol: str) -> bool:
        """
        Delete position.

        Args:
            symbol: Trading symbol

        Returns:
            True if successful, False otherwise
        """
        pass


class InMemoryTradingRepository(TradingRepositoryInterface):
    """
    In-memory implementation of trading repository with V2 compliance.

    V2 COMPLIANCE: Thread-safe async operations, comprehensive error handling, proper logging.
    """

    def __init__(self):
        """Initialize in-memory repository with V2 compliance."""
        self.logger = get_logger(__name__)
        self.validator = get_unified_validator()
        self.trades: Dict[str, Trade] = {}
        self.positions: Dict[str, Position] = {}
        self._lock = asyncio.Lock()

    async def save_trade(self, trade: Trade) -> bool:
        """
        Save trade to memory with V2 compliance.

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

    async def get_trade(self, trade_id: str) -> Optional[Trade]:
        """
        Get trade by ID with V2 compliance.

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

    async def get_trades_by_symbol(self, symbol: str, limit: int = 100) -> List[Trade]:
        """
        Get trades for symbol with V2 compliance.

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

    async def get_all_trades(self, limit: int = 1000) -> List[Trade]:
        """
        Get all trades with V2 compliance.

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
        """
        Update trade status with V2 compliance.

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

            if status not in ['pending', 'executed', 'cancelled']:
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

    async def save_position(self, position: Position) -> bool:
        """
        Save position with V2 compliance.

        Args:
            position: Position object to save

        Returns:
            True if successful, False otherwise
        """
        try:
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

    async def get_position(self, symbol: str) -> Optional[Position]:
        """
        Get position by symbol with V2 compliance.

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

    async def get_all_positions(self) -> List[Position]:
        """
        Get all positions with V2 compliance.

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
        """
        Delete position with V2 compliance.

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
                    self.logger.info(f"Position deleted: {symbol}")
                    return True
                else:
                    self.logger.warning(f"Position not found: {symbol}")
                    return False

        except Exception as e:
            self.logger.error(f"Failed to delete position {symbol}: {e}")
            return False


# Factory function for dependency injection
def create_trading_repository() -> TradingRepositoryInterface:
    """Factory function to create trading repository instance"""
    return InMemoryTradingRepository()


# Export the factory function for DI
__all__ = ['TradingRepositoryInterface', 'Trade', 'Position', 'create_trading_repository']

