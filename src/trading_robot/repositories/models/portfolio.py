"""
Portfolio Model - V2 Compliant Module
====================================

Portfolio data structure with V2 compliance validation.
Extracted from trading_repository.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .position import Position


@dataclass
class Portfolio:
    """Portfolio data structure with V2 compliance validation.

    V2 COMPLIANCE: Type-safe data structure with validation and metadata.
    """

    id: str
    name: str
    positions: dict[str, Position] = field(default_factory=dict)
    cash_balance: float = 0.0
    total_value: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate portfolio data on initialization."""
        if not self.id or not self.id.strip():
            raise ValueError("Portfolio ID cannot be empty")
        if not self.name or not self.name.strip():
            raise ValueError("Portfolio name cannot be empty")
        if self.cash_balance < 0:
            raise ValueError("Cash balance cannot be negative")

    def add_position(self, position: Position):
        """Add or update position in portfolio."""
        if not isinstance(position, Position):
            raise ValueError("Position must be a Position object")

        self.positions[position.symbol] = position
        self._update_total_value()

    def remove_position(self, symbol: str):
        """Remove position from portfolio."""
        if symbol in self.positions:
            del self.positions[symbol]
            self._update_total_value()

    def get_position(self, symbol: str) -> Position:
        """Get position for symbol."""
        return self.positions.get(symbol)

    def has_position(self, symbol: str) -> bool:
        """Check if portfolio has position for symbol."""
        return symbol in self.positions

    def get_total_market_value(self) -> float:
        """Calculate total market value of all positions."""
        return sum(pos.get_market_value() for pos in self.positions.values())

    def get_total_cost_basis(self) -> float:
        """Calculate total cost basis of all positions."""
        return sum(pos.get_cost_basis() for pos in self.positions.values())

    def get_total_unrealized_pnl(self) -> float:
        """Calculate total unrealized P&L."""
        return sum(pos.get_unrealized_pnl() for pos in self.positions.values())

    def get_total_unrealized_pnl_percentage(self) -> float:
        """Calculate total unrealized P&L as percentage."""
        cost_basis = self.get_total_cost_basis()
        if cost_basis == 0:
            return 0.0

        return (self.get_total_unrealized_pnl() / cost_basis) * 100

    def get_portfolio_value(self) -> float:
        """Calculate total portfolio value (positions + cash)."""
        return self.get_total_market_value() + self.cash_balance

    def get_position_count(self) -> int:
        """Get number of positions in portfolio."""
        return len(self.positions)

    def get_long_positions(self) -> list[Position]:
        """Get all long positions."""
        return [pos for pos in self.positions.values() if pos.is_long()]

    def get_short_positions(self) -> list[Position]:
        """Get all short positions."""
        return [pos for pos in self.positions.values() if pos.is_short()]

    def get_flat_positions(self) -> list[Position]:
        """Get all flat positions."""
        return [pos for pos in self.positions.values() if pos.is_flat()]

    def get_profitable_positions(self) -> list[Position]:
        """Get all profitable positions."""
        return [pos for pos in self.positions.values() if pos.is_profitable()]

    def get_losing_positions(self) -> list[Position]:
        """Get all losing positions."""
        return [pos for pos in self.positions.values() if not pos.is_profitable()]

    def update_position_prices(self, price_updates: dict[str, float]):
        """Update current prices for positions."""
        for symbol, price in price_updates.items():
            if symbol in self.positions:
                self.positions[symbol].update_price(price)

        self._update_total_value()

    def _update_total_value(self):
        """Update total portfolio value."""
        self.total_value = self.get_portfolio_value()

    def get_portfolio_summary(self) -> dict[str, Any]:
        """Get comprehensive portfolio summary."""
        return {
            "id": self.id,
            "name": self.name,
            "total_value": self.get_portfolio_value(),
            "cash_balance": self.cash_balance,
            "market_value": self.get_total_market_value(),
            "cost_basis": self.get_total_cost_basis(),
            "unrealized_pnl": self.get_total_unrealized_pnl(),
            "unrealized_pnl_percentage": self.get_total_unrealized_pnl_percentage(),
            "position_count": self.get_position_count(),
            "long_positions": len(self.get_long_positions()),
            "short_positions": len(self.get_short_positions()),
            "profitable_positions": len(self.get_profitable_positions()),
            "losing_positions": len(self.get_losing_positions()),
            "timestamp": self.timestamp.isoformat(),
        }

    def to_dict(self) -> dict[str, Any]:
        """Convert portfolio to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "positions": {symbol: pos.to_dict() for symbol, pos in self.positions.items()},
            "cash_balance": self.cash_balance,
            "total_value": self.total_value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Portfolio":
        """Create portfolio from dictionary."""
        positions = {}
        for symbol, pos_data in data.get("positions", {}).items():
            positions[symbol] = Position.from_dict(pos_data)

        return cls(
            id=data["id"],
            name=data["name"],
            positions=positions,
            cash_balance=data.get("cash_balance", 0.0),
            total_value=data.get("total_value", 0.0),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
        )

    def __str__(self) -> str:
        """String representation of portfolio."""
        return f"Portfolio({self.name} - {self.get_position_count()} positions)"

    def __repr__(self) -> str:
        """Detailed string representation of portfolio."""
        return (
            f"Portfolio(id='{self.id}', name='{self.name}', "
            f"positions={len(self.positions)}, value={self.get_portfolio_value()})"
        )
