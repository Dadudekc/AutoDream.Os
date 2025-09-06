#!/usr/bin/env python3
"""
Trading Models - V2 Compliance Module
====================================

Data models for trading operations with V2 compliance validation.
Extracted from trading_repository.py for V2 compliance.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class Trade:
    """Trade data structure with V2 compliance validation.

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
        if self.side not in ["buy", "sell"]:
            raise ValueError("Side must be 'buy' or 'sell'")
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.price <= 0:
            raise ValueError("Price must be positive")
        if self.status not in ["pending", "executed", "cancelled"]:
            raise ValueError("Invalid status")
        if self.order_type not in ["market", "limit", "stop"]:
            raise ValueError("Invalid order type")

    def is_completed(self) -> bool:
        """Check if trade is completed."""
        return self.status in ["executed", "cancelled"]

    def calculate_value(self) -> float:
        """Calculate total trade value."""
        return self.quantity * self.price


@dataclass
class Position:
    """Position data structure with V2 compliance validation.

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
