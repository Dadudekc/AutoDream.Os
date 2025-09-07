import logging
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List

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


class VolatilityRegime(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    EXTREME = "EXTREME"


class TrendDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    SIDEWAYS = "SIDEWAYS"


class MarketSentiment(Enum):
    OPTIMISTIC = "OPTIMISTIC"
    NEUTRAL = "NEUTRAL"
    PESSIMISTIC = "PESSIMISTIC"


class LiquidityCondition(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CorrelationRegime(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


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
    timestamp: datetime = field(default_factory=datetime.now)
    expiration: Optional[datetime] = None

    def __post_init__(self):
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
    returns: List[float] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class MarketCondition:
    """Market condition analysis"""

    volatility_regime: VolatilityRegime
    trend_direction: TrendDirection
    market_sentiment: MarketSentiment
    liquidity_condition: LiquidityCondition
    correlation_regime: CorrelationRegime
    timestamp: datetime = field(default_factory=datetime.now)
