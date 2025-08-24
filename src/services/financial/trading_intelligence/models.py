import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class StrategyType(Enum):
    """Trading strategy types"""

    MOMENTUM = "MOMENTUM"
    MEAN_REVERSION = "MEAN_REVERSION"
    ARBITRAGE = "ARBITRAGE"
    PAIRS_TRADING = "PAIRS_TRADING"
    BREAKOUT = "BREAKOUT"
    SCALPING = "SCALPING"
    GRID_TRADING = "GRID_TRADING"


class SignalType(Enum):
    """Trading signal types"""

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"


class SignalStrength(Enum):
    """Signal strength levels"""

    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"
    VERY_STRONG = "VERY_STRONG"


@dataclass
class TradingSignal:
    """Trading signal data"""

    symbol: str
    signal_type: SignalType
    strength: SignalStrength
    confidence: float  # 0.0 to 1.0
    price: float
    target_price: float
    stop_loss: float
    strategy: StrategyType
    reasoning: str
    timestamp: datetime
    expiration: Optional[datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.expiration is None:
            self.expiration = self.timestamp + timedelta(hours=24)


@dataclass
class StrategyPerformance:
    """Strategy performance metrics"""

    strategy_type: StrategyType
    total_signals: int
    successful_signals: int
    win_rate: float
    avg_return: float
    max_drawdown: float
    sharpe_ratio: float
    total_pnl: float
    last_updated: Optional[datetime] = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


@dataclass
class MarketCondition:
    """Market condition analysis"""

    volatility_regime: str  # LOW, MEDIUM, HIGH, EXTREME
    trend_direction: str  # BULLISH, BEARISH, SIDEWAYS
    market_sentiment: str  # OPTIMISTIC, NEUTRAL, PESSIMISTIC
    liquidity_condition: str  # HIGH, MEDIUM, LOW
    correlation_regime: str  # LOW, MEDIUM, HIGH
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
