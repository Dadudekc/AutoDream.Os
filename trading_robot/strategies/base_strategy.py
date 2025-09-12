"""
Base Trading Strategy Framework
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

# AGGRESSIVE LAZY LOADING - CRITICAL PERFORMANCE OPTIMIZATION
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.aggressive_lazy_loader import lazy_import

# Lazy load heavy modules for 30%+ performance improvement
pd = lazy_import('pandas', 'pd')

from loguru import logger
from strategies.indicators import TechnicalIndicators


class Signal(Enum):
    """Trading signals"""

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class StrategyResult:
    """Result of strategy analysis"""

    def __init__(
        self,
        symbol: str,
        signal: Signal,
        confidence: float,
        indicators: dict[str, Any] = None,
        metadata: dict[str, Any] = None,
    ):
        self.symbol = symbol
        self.signal = signal
        self.confidence = confidence
        self.indicators = indicators or {}
        self.metadata = metadata or {}
        self.timestamp = pd.Timestamp.now()


class BaseStrategy(ABC):
    """Abstract base class for trading strategies"""

    def __init__(self, name: str, parameters: dict[str, Any] = None):
        self.name = name
        self.parameters = parameters or {}
        self.indicators = TechnicalIndicators()

    @abstractmethod
    def analyze(self, data: pd.DataFrame, symbol: str) -> StrategyResult:
        """Analyze market data and generate trading signal"""
        pass

    def calculate_position_size(
        self, account_balance: float, price: float, risk_pct: float = 0.01
    ) -> int:
        """Calculate position size based on risk management"""
        risk_amount = account_balance * risk_pct
        position_size = risk_amount / price
        return max(1, int(position_size))

    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate that data has required columns and sufficient length"""
        required_columns = ["open", "high", "low", "close", "volume"]
        min_length = 50  # Minimum data points needed for analysis

        if len(data) < min_length:
            logger.warning(f"Insufficient data: {len(data)} < {min_length}")
            return False

        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            logger.warning(f"Missing required columns: {missing_columns}")
            return False

        return True

    def get_indicator_value(self, data: pd.DataFrame, indicator_name: str, **params) -> pd.Series:
        """Get indicator value with caching"""
        # This could be extended with caching mechanism
        if indicator_name == "sma":
            return self.indicators.sma(data["close"], params.get("period", 20))
        elif indicator_name == "ema":
            return self.indicators.ema(data["close"], params.get("period", 20))
        elif indicator_name == "rsi":
            return self.indicators.rsi(data["close"], params.get("period", 14))
        elif indicator_name == "macd":
            macd_line, signal_line, histogram = self.indicators.macd(
                data["close"],
                params.get("fast_period", 12),
                params.get("slow_period", 26),
                params.get("signal_period", 9),
            )
            return {"macd_line": macd_line, "signal_line": signal_line, "histogram": histogram}
        elif indicator_name == "bollinger_bands":
            upper, middle, lower = self.indicators.bollinger_bands(
                data["close"], params.get("period", 20), params.get("std_dev", 2.0)
            )
            return {"upper": upper, "middle": middle, "lower": lower}
        else:
            raise ValueError(f"Unknown indicator: {indicator_name}")


class TrendFollowingStrategy(BaseStrategy):
    """Example trend following strategy using moving averages"""

    def __init__(self, parameters: dict[str, Any] = None):
        super().__init__("Trend Following", parameters)

    def analyze(self, data: pd.DataFrame, symbol: str) -> StrategyResult:
        """Analyze using moving average crossover"""
        if not self.validate_data(data):
            return StrategyResult(symbol, Signal.HOLD, 0.0)

        # Calculate indicators
        fast_ma = self.get_indicator_value(data, "sma", period=10)
        slow_ma = self.get_indicator_value(data, "sma", period=20)
        rsi = self.get_indicator_value(data, "rsi", period=14)

        # Get latest values
        latest_fast = fast_ma.iloc[-1]
        latest_slow = slow_ma.iloc[-1]
        latest_rsi = rsi.iloc[-1]

        # Previous values for crossover detection
        prev_fast = fast_ma.iloc[-2]
        prev_slow = slow_ma.iloc[-2]

        # Generate signal
        signal = Signal.HOLD
        confidence = 0.5

        # Bullish crossover
        if prev_fast <= prev_slow and latest_fast > latest_slow:
            signal = Signal.BUY
            confidence = 0.7
        # Bearish crossover
        elif prev_fast >= prev_slow and latest_fast < latest_slow:
            signal = Signal.SELL
            confidence = 0.7

        # RSI filter
        if latest_rsi > 70 and signal == Signal.BUY:
            signal = Signal.HOLD  # Overbought
        elif latest_rsi < 30 and signal == Signal.SELL:
            signal = Signal.HOLD  # Oversold

        return StrategyResult(
            symbol=symbol,
            signal=signal,
            confidence=confidence,
            indicators={"fast_ma": latest_fast, "slow_ma": latest_slow, "rsi": latest_rsi},
        )


class MeanReversionStrategy(BaseStrategy):
    """Example mean reversion strategy using RSI and Bollinger Bands"""

    def __init__(self, parameters: dict[str, Any] = None):
        super().__init__("Mean Reversion", parameters)

    def analyze(self, data: pd.DataFrame, symbol: str) -> StrategyResult:
        """Analyze using RSI and Bollinger Bands"""
        if not self.validate_data(data):
            return StrategyResult(symbol, Signal.HOLD, 0.0)

        # Calculate indicators
        rsi = self.get_indicator_value(data, "rsi", period=14)
        bb = self.get_indicator_value(data, "bollinger_bands", period=20)

        # Get latest values
        latest_price = data["close"].iloc[-1]
        latest_rsi = rsi.iloc[-1]
        upper_bb = bb["upper"].iloc[-1]
        lower_bb = bb["lower"].iloc[-1]

        # Generate signal
        signal = Signal.HOLD
        confidence = 0.5

        # Oversold condition
        if latest_rsi < 30 and latest_price <= lower_bb:
            signal = Signal.BUY
            confidence = 0.8
        # Overbought condition
        elif latest_rsi > 70 and latest_price >= upper_bb:
            signal = Signal.SELL
            confidence = 0.8

        return StrategyResult(
            symbol=symbol,
            signal=signal,
            confidence=confidence,
            indicators={
                "rsi": latest_rsi,
                "price": latest_price,
                "upper_bb": upper_bb,
                "lower_bb": lower_bb,
            },
        )


class StrategyManager:
    """Manages multiple trading strategies"""

    def __init__(self):
        self.strategies: dict[str, BaseStrategy] = {}

    def add_strategy(self, strategy: BaseStrategy):
        """Add a strategy to the manager"""
        self.strategies[strategy.name] = strategy
        logger.info(f"✅ Strategy added: {strategy.name}")

    def remove_strategy(self, strategy_name: str):
        """Remove a strategy from the manager"""
        if strategy_name in self.strategies:
            del self.strategies[strategy_name]
            logger.info(f"❌ Strategy removed: {strategy_name}")

    def get_strategies(self) -> list[str]:
        """Get list of available strategies"""
        return list(self.strategies.keys())

    def analyze_symbol(self, symbol: str, data: pd.DataFrame) -> list[StrategyResult]:
        """Analyze symbol with all strategies"""
        results = []
        for strategy_name, strategy in self.strategies.items():
            try:
                result = strategy.analyze(data, symbol)
                results.append(result)
                logger.debug(
                    f"📊 {strategy_name} signal for {symbol}: {result.signal.value} ({result.confidence:.2f})"
                )
            except Exception as e:
                logger.error(f"❌ Error in {strategy_name} for {symbol}: {e}")

        return results

    def get_consensus_signal(self, results: list[StrategyResult]) -> tuple[Signal, float]:
        """Get consensus signal from multiple strategy results"""
        if not results:
            return Signal.HOLD, 0.0

        # Weight signals by confidence
        buy_weight = 0
        sell_weight = 0
        total_weight = 0

        for result in results:
            weight = result.confidence
            total_weight += weight

            if result.signal == Signal.BUY:
                buy_weight += weight
            elif result.signal == Signal.SELL:
                sell_weight += weight

        if total_weight == 0:
            return Signal.HOLD, 0.0

        buy_pct = buy_weight / total_weight
        sell_pct = sell_weight / total_weight

        if buy_pct > 0.6:  # 60%+ consensus for buy
            return Signal.BUY, buy_pct
        elif sell_pct > 0.6:  # 60%+ consensus for sell
            return Signal.SELL, sell_pct
        else:
            return Signal.HOLD, 0.5
