"""
Position Model - V2 Compliant Module
===================================

Position data structure with V2 compliance validation.
Extracted from trading_repository.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Position:
    """Position data structure with V2 compliance validation.

    V2 COMPLIANCE: Type-safe data structure with validation and metadata.
    """

    symbol: str
    quantity: float
    average_price: float
    current_price: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate position data on initialization."""
        if not self.symbol or not self.symbol.strip():
            raise ValueError("Symbol cannot be empty")
        if self.quantity == 0:
            raise ValueError("Quantity cannot be zero")
        if self.average_price <= 0:
            raise ValueError("Average price must be positive")
        if self.current_price < 0:
            raise ValueError("Current price cannot be negative")

    def get_market_value(self) -> float:
        """Calculate current market value of position."""
        return abs(self.quantity) * self.current_price

    def get_cost_basis(self) -> float:
        """Calculate cost basis of position."""
        return abs(self.quantity) * self.average_price

    def get_unrealized_pnl(self) -> float:
        """Calculate unrealized profit/loss."""
        if self.quantity == 0:
            return 0.0

        if self.quantity > 0:  # Long position
            return (self.current_price - self.average_price) * self.quantity
        else:  # Short position
            return (self.average_price - self.current_price) * abs(self.quantity)

    def get_unrealized_pnl_percentage(self) -> float:
        """Calculate unrealized P&L as percentage."""
        cost_basis = self.get_cost_basis()
        if cost_basis == 0:
            return 0.0

        return (self.get_unrealized_pnl() / cost_basis) * 100

    def is_long(self) -> bool:
        """Check if this is a long position."""
        return self.quantity > 0

    def is_short(self) -> bool:
        """Check if this is a short position."""
        return self.quantity < 0

    def is_flat(self) -> bool:
        """Check if position is flat (no quantity)."""
        return self.quantity == 0

    def is_profitable(self) -> bool:
        """Check if position is currently profitable."""
        return self.get_unrealized_pnl() > 0

    def update_price(self, new_price: float):
        """Update current price."""
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.current_price = new_price

    def add_quantity(self, quantity: float, price: float):
        """Add quantity to position and update average price."""
        if quantity == 0:
            return

        if price <= 0:
            raise ValueError("Price must be positive")

        # Calculate new average price
        total_quantity = self.quantity + quantity
        if total_quantity == 0:
            self.quantity = 0
            self.average_price = 0
        else:
            total_cost = (self.quantity * self.average_price) + (quantity * price)
            self.average_price = total_cost / total_quantity
            self.quantity = total_quantity

    def to_dict(self) -> dict[str, Any]:
        """Convert position to dictionary."""
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "average_price": self.average_price,
            "current_price": self.current_price,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Position":
        """Create position from dictionary."""
        return cls(
            symbol=data["symbol"],
            quantity=data["quantity"],
            average_price=data["average_price"],
            current_price=data.get("current_price", 0.0),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
        )

    def __str__(self) -> str:
        """String representation of position."""
        return f"Position({self.symbol} {self.quantity}@{self.average_price})"

    def __repr__(self) -> str:
        """Detailed string representation of position."""
        return (
            f"Position(symbol='{self.symbol}', quantity={self.quantity}, "
            f"average_price={self.average_price}, current_price={self.current_price})"
        )
