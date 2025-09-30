"""
Trading Robot Models
V2 Compliant data models for trading robot
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
import numpy as np


class TradingSignal(Enum):
    """Trading signal types"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class OrderType(Enum):
    """Order types"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"


class OrderStatus(Enum):
    """Order status"""
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class MarketData:
    """Market data structure"""
    symbol: str
    price: float
    volume: int
    timestamp: datetime
    high: float
    low: float
    open: float
    close: float


@dataclass
class Order:
    """Order structure"""
    order_id: str
    symbol: str
    order_type: OrderType
    side: TradingSignal
    quantity: int
    price: Optional[float]
    status: OrderStatus
    timestamp: datetime


@dataclass
class Position:
    """Position structure"""
    symbol: str
    quantity: int
    avg_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float


@dataclass
class TradingMetrics:
    """Trading performance metrics"""
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_pnl: float
    max_drawdown: float
    sharpe_ratio: float
