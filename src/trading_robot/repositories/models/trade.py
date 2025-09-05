"""
Trade Model - V2 Compliant Module
================================

Trade data structure with V2 compliance validation.
Extracted from trading_repository.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


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
            raise ValueError("Status must be 'pending', 'executed', or 'cancelled'")
        if self.order_type not in ['market', 'limit', 'stop']:
            raise ValueError("Order type must be 'market', 'limit', or 'stop'")

    def get_value(self) -> float:
        """Calculate total trade value."""
        return self.quantity * self.price

    def is_buy(self) -> bool:
        """Check if this is a buy trade."""
        return self.side == 'buy'

    def is_sell(self) -> bool:
        """Check if this is a sell trade."""
        return self.side == 'sell'

    def is_executed(self) -> bool:
        """Check if trade is executed."""
        return self.status == 'executed'

    def is_pending(self) -> bool:
        """Check if trade is pending."""
        return self.status == 'pending'

    def is_cancelled(self) -> bool:
        """Check if trade is cancelled."""
        return self.status == 'cancelled'

    def to_dict(self) -> Dict[str, Any]:
        """Convert trade to dictionary."""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'side': self.side,
            'quantity': self.quantity,
            'price': self.price,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status,
            'order_type': self.order_type,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Trade':
        """Create trade from dictionary."""
        return cls(
            id=data['id'],
            symbol=data['symbol'],
            side=data['side'],
            quantity=data['quantity'],
            price=data['price'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            status=data.get('status', 'pending'),
            order_type=data.get('order_type', 'market'),
            metadata=data.get('metadata', {})
        )

    def __str__(self) -> str:
        """String representation of trade."""
        return f"Trade({self.symbol} {self.side} {self.quantity}@{self.price})"

    def __repr__(self) -> str:
        """Detailed string representation of trade."""
        return (f"Trade(id='{self.id}', symbol='{self.symbol}', side='{self.side}', "
                f"quantity={self.quantity}, price={self.price}, status='{self.status}')")
