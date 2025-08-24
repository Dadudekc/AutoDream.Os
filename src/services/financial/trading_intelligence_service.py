"""
Trading Intelligence Service - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides algorithmic trading strategies, market analysis, and automated decision-making.
"""

import asyncio
import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
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
    expiration: datetime = None

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
    last_updated: datetime = None

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
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class TradingIntelligenceService:
    """Advanced trading intelligence and strategy execution service"""

    def __init__(
        self, market_data_service=None, data_dir: str = "trading_intelligence"
    ):
        self.market_data_service = market_data_service
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.strategies: Dict[StrategyType, Callable] = {}
        self.performance_metrics: Dict[StrategyType, StrategyPerformance] = {}
        self.active_signals: List[TradingSignal] = []
        self.market_conditions: MarketCondition = None

        self.signals_file = self.data_dir / "trading_signals.json"
        self.performance_file = self.data_dir / "strategy_performance.json"

        # Strategy parameters
        self.strategy_params = {
            StrategyType.MOMENTUM: {
                "lookback_period": 20,
                "momentum_threshold": 0.02,
                "volume_threshold": 1.5,
            },
            StrategyType.MEAN_REVERSION: {
                "lookback_period": 50,
                "std_dev_threshold": 2.0,
                "reversion_strength": 0.1,
            },
            StrategyType.BREAKOUT: {
                "breakout_period": 20,
                "volume_confirmation": True,
                "breakout_threshold": 0.05,
            },
            StrategyType.SCALPING: {
                "min_spread": 0.001,
                "max_hold_time": 300,  # 5 minutes
                "profit_target": 0.002,
            },
        }

        self.initialize_strategies()
        self.load_data()

    def initialize_strategies(self):
        """Initialize trading strategies"""
        self.strategies = {
            StrategyType.MOMENTUM: self.momentum_strategy,
            StrategyType.MEAN_REVERSION: self.mean_reversion_strategy,
            StrategyType.BREAKOUT: self.breakout_strategy,
            StrategyType.SCALPING: self.scalping_strategy,
            StrategyType.PAIRS_TRADING: self.pairs_trading_strategy,
            StrategyType.GRID_TRADING: self.grid_trading_strategy,
        }

        # Initialize performance metrics
        for strategy_type in StrategyType:
            self.performance_metrics[strategy_type] = StrategyPerformance(
                strategy_type=strategy_type,
                total_signals=0,
                successful_signals=0,
                win_rate=0.0,
                avg_return=0.0,
                max_drawdown=0.0,
                sharpe_ratio=0.0,
                total_pnl=0.0,
            )

    def momentum_strategy(
        self, symbol: str, historical_data: pd.DataFrame
    ) -> Optional[TradingSignal]:
        """Momentum-based trading strategy"""
        try:
            if len(historical_data) < 30:
                return None

            # Calculate momentum indicators
            close_prices = historical_data["Close"]
            volume = historical_data["Volume"]

            # Price momentum
            price_momentum = (
                close_prices.iloc[-1] - close_prices.iloc[-20]
            ) / close_prices.iloc[-20]

            # Volume momentum
            avg_volume = volume.iloc[-20:].mean()
            current_volume = volume.iloc[-1]
            volume_ratio = current_volume / avg_volume

            # RSI for confirmation
            rsi = self.calculate_rsi(close_prices, 14)
            current_rsi = rsi.iloc[-1]

            # Generate signal
            signal_type = SignalType.HOLD
            strength = SignalStrength.WEAK
            confidence = 0.0

            if price_momentum > 0.02 and volume_ratio > 1.5 and current_rsi < 70:
                signal_type = SignalType.BUY
                if price_momentum > 0.05 and volume_ratio > 2.0:
                    signal_type = SignalType.STRONG_BUY
                    strength = SignalStrength.STRONG
                    confidence = 0.8
                else:
                    strength = SignalStrength.MODERATE
                    confidence = 0.6
            elif price_momentum < -0.02 and volume_ratio > 1.5 and current_rsi > 30:
                signal_type = SignalType.SELL
                if price_momentum < -0.05 and volume_ratio > 2.0:
                    signal_type = SignalType.STRONG_SELL
                    strength = SignalStrength.STRONG
                    confidence = 0.8
                else:
                    strength = SignalStrength.MODERATE
                    confidence = 0.6

            if signal_type != SignalType.HOLD:
                current_price = close_prices.iloc[-1]
                target_price = current_price * (1 + price_momentum * 0.5)
                stop_loss = current_price * (1 - abs(price_momentum) * 0.3)

                reasoning = f"Momentum: {price_momentum:.2%}, Volume: {volume_ratio:.2f}x, RSI: {current_rsi:.1f}"

                return TradingSignal(
                    symbol=symbol,
                    signal_type=signal_type,
                    strength=strength,
                    confidence=confidence,
                    price=current_price,
                    target_price=target_price,
                    stop_loss=stop_loss,
                    strategy=StrategyType.MOMENTUM,
                    reasoning=reasoning,
                )

            return None

        except Exception as e:
            logger.error(f"Error in momentum strategy for {symbol}: {e}")
            return None

    def mean_reversion_strategy(
        self, symbol: str, historical_data: pd.DataFrame
    ) -> Optional[TradingSignal]:
        """Mean reversion trading strategy"""
        try:
            if len(historical_data) < 60:
                return None

            close_prices = historical_data["Close"]

            # Calculate Bollinger Bands
            sma = close_prices.rolling(window=20).mean()
            std = close_prices.rolling(window=20).std()
            upper_band = sma + (std * 2)
            lower_band = sma - (std * 2)

            current_price = close_prices.iloc[-1]
            current_sma = sma.iloc[-1]
            current_upper = upper_band.iloc[-1]
            current_lower = lower_band.iloc[-1]

            # Calculate z-score
            z_score = (current_price - current_sma) / std.iloc[-1]

            # Generate signal
            signal_type = SignalType.HOLD
            strength = SignalStrength.WEAK
            confidence = 0.0

            if z_score > 2.0:  # Price above upper band
                signal_type = SignalType.SELL
                if z_score > 3.0:
                    signal_type = SignalType.STRONG_SELL
                    strength = SignalStrength.STRONG
                    confidence = 0.8
                else:
                    strength = SignalStrength.MODERATE
                    confidence = 0.6
            elif z_score < -2.0:  # Price below lower band
                signal_type = SignalType.BUY
                if z_score < -3.0:
                    signal_type = SignalType.STRONG_BUY
                    strength = SignalStrength.STRONG
                    confidence = 0.8
                else:
                    strength = SignalStrength.MODERATE
                    confidence = 0.6

            if signal_type != SignalType.HOLD:
                target_price = current_sma
                stop_loss = current_price * (1 + abs(z_score) * 0.1)

                reasoning = f"Z-Score: {z_score:.2f}, SMA: ${current_sma:.2f}, Bands: ${current_lower:.2f}-${current_upper:.2f}"

                return TradingSignal(
                    symbol=symbol,
                    signal_type=signal_type,
                    strength=strength,
                    confidence=confidence,
                    price=current_price,
                    target_price=target_price,
                    stop_loss=stop_loss,
                    strategy=StrategyType.MEAN_REVERSION,
                    reasoning=reasoning,
                )

            return None

        except Exception as e:
            logger.error(f"Error in mean reversion strategy for {symbol}: {e}")
            return None

    def breakout_strategy(
        self, symbol: str, historical_data: pd.DataFrame
    ) -> Optional[TradingSignal]:
        """Breakout trading strategy"""
        try:
            if len(historical_data) < 30:
                return None

            close_prices = historical_data["Close"]
            volume = historical_data["Volume"]

            # Calculate resistance and support levels
            high_20 = close_prices.rolling(window=20).max()
            low_20 = close_prices.rolling(window=20).min()

            current_price = close_prices.iloc[-1]
            resistance = high_20.iloc[-2]  # Previous high
            support = low_20.iloc[-2]  # Previous low

            # Volume confirmation
            avg_volume = volume.iloc[-20:].mean()
            current_volume = volume.iloc[-1]
            volume_confirmation = current_volume > avg_volume * 1.5

            # Breakout detection
            breakout_up = current_price > resistance * 1.01  # 1% above resistance
            breakout_down = current_price < support * 0.99  # 1% below support

            # Generate signal
            signal_type = SignalType.HOLD
            strength = SignalStrength.WEAK
            confidence = 0.0

            if breakout_up and volume_confirmation:
                signal_type = SignalType.BUY
                strength = SignalStrength.MODERATE
                confidence = 0.7

                target_price = current_price * 1.05  # 5% target
                stop_loss = resistance  # Support at previous resistance

            elif breakout_down and volume_confirmation:
                signal_type = SignalType.SELL
                strength = SignalStrength.MODERATE
                confidence = 0.7

                target_price = current_price * 0.95  # 5% target
                stop_loss = support  # Resistance at previous support

            if signal_type != SignalType.HOLD:
                reasoning = f"Breakout: {'UP' if breakout_up else 'DOWN'}, Volume: {volume_confirmation}, Resistance: ${resistance:.2f}, Support: ${support:.2f}"

                return TradingSignal(
                    symbol=symbol,
                    signal_type=signal_type,
                    strength=strength,
                    confidence=confidence,
                    price=current_price,
                    target_price=target_price,
                    stop_loss=stop_loss,
                    strategy=StrategyType.BREAKOUT,
                    reasoning=reasoning,
                )

            return None

        except Exception as e:
            logger.error(f"Error in breakout strategy for {symbol}: {e}")
            return None

    def scalping_strategy(
        self, symbol: str, historical_data: pd.DataFrame
    ) -> Optional[TradingSignal]:
        """Scalping trading strategy"""
        try:
            if len(historical_data) < 10:
                return None

            close_prices = historical_data["Close"]
            high_prices = historical_data["High"]
            low_prices = historical_data["Low"]

            current_price = close_prices.iloc[-1]

            # Calculate short-term indicators
            sma_5 = close_prices.rolling(window=5).mean()
            sma_10 = close_prices.rolling(window=10).mean()

            # Price relative to moving averages
            price_vs_sma5 = (current_price - sma_5.iloc[-1]) / sma_5.iloc[-1]
            price_vs_sma10 = (current_price - sma_10.iloc[-1]) / sma_10.iloc[-1]

            # Volatility calculation
            recent_high = high_prices.iloc[-5:].max()
            recent_low = low_prices.iloc[-5:].min()
            volatility = (recent_high - recent_low) / current_price

            # Generate signal
            signal_type = SignalType.HOLD
            strength = SignalStrength.WEAK
            confidence = 0.0

            # Scalping conditions
            if price_vs_sma5 > 0.001 and price_vs_sma10 > 0.002 and volatility > 0.01:
                signal_type = SignalType.BUY
                strength = SignalStrength.MODERATE
                confidence = 0.6

                target_price = current_price * 1.002  # 0.2% target
                stop_loss = current_price * 0.999  # 0.1% stop loss

            elif (
                price_vs_sma5 < -0.001 and price_vs_sma10 < -0.002 and volatility > 0.01
            ):
                signal_type = SignalType.SELL
                strength = SignalStrength.MODERATE
                confidence = 0.6

                target_price = current_price * 0.998  # 0.2% target
                stop_loss = current_price * 1.001  # 0.1% stop loss

            if signal_type != SignalType.HOLD:
                reasoning = f"Scalping: SMA5: {price_vs_sma5:.3%}, SMA10: {price_vs_sma10:.3%}, Vol: {volatility:.3%}"

                return TradingSignal(
                    symbol=symbol,
                    signal_type=signal_type,
                    strength=strength,
                    confidence=confidence,
                    price=current_price,
                    target_price=target_price,
                    stop_loss=stop_loss,
                    strategy=StrategyType.SCALPING,
                    reasoning=reasoning,
                )

            return None

        except Exception as e:
            logger.error(f"Error in scalping strategy for {symbol}: {e}")
            return None

    def pairs_trading_strategy(
        self,
        symbol1: str,
        symbol2: str,
        historical_data1: pd.DataFrame,
        historical_data2: pd.DataFrame,
    ) -> Optional[TradingSignal]:
        """Pairs trading strategy"""
        try:
            if len(historical_data1) < 50 or len(historical_data2) < 50:
                return None

            # Calculate correlation and spread
            returns1 = historical_data1["Close"].pct_change().dropna()
            returns2 = historical_data2["Close"].pct_change().dropna()

            # Align data
            min_length = min(len(returns1), len(returns2))
            returns1 = returns1.iloc[-min_length:]
            returns2 = returns2.iloc[-min_length:]

            correlation = returns1.corr(returns2)

            if abs(correlation) < 0.7:  # Need high correlation
                return None

            # Calculate spread
            spread = returns1 - returns2
            spread_mean = spread.mean()
            spread_std = spread.std()
            current_spread = spread.iloc[-1]

            # Z-score of spread
            z_score = (current_spread - spread_mean) / spread_std

            # Generate signal
            signal_type = SignalType.HOLD
            strength = SignalStrength.WEAK
            confidence = 0.0

            if z_score > 2.0:  # Spread is wide, short symbol1, long symbol2
                signal_type = SignalType.SELL
                strength = SignalStrength.MODERATE
                confidence = 0.7

                current_price = historical_data1["Close"].iloc[-1]
                target_price = current_price * (1 - abs(z_score) * 0.01)
                stop_loss = current_price * (1 + abs(z_score) * 0.005)

            elif z_score < -2.0:  # Spread is narrow, long symbol1, short symbol2
                signal_type = SignalType.BUY
                strength = SignalStrength.MODERATE
                confidence = 0.7

                current_price = historical_data1["Close"].iloc[-1]
                target_price = current_price * (1 + abs(z_score) * 0.01)
                stop_loss = current_price * (1 - abs(z_score) * 0.005)

            if signal_type != SignalType.HOLD:
                reasoning = f"Pairs: Corr: {correlation:.3f}, Z-Score: {z_score:.2f}, Spread: {current_spread:.4f}"

                return TradingSignal(
                    symbol=f"{symbol1}-{symbol2}",
                    signal_type=signal_type,
                    strength=strength,
                    confidence=confidence,
                    price=current_price,
                    target_price=target_price,
                    stop_loss=stop_loss,
                    strategy=StrategyType.PAIRS_TRADING,
                    reasoning=reasoning,
                )

            return None

        except Exception as e:
            logger.error(f"Error in pairs trading strategy: {e}")
            return None

    def grid_trading_strategy(
        self, symbol: str, historical_data: pd.DataFrame, grid_levels: int = 5
    ) -> List[TradingSignal]:
        """Grid trading strategy"""
        try:
            if len(historical_data) < 20:
                return []

            current_price = historical_data["Close"].iloc[-1]

            # Calculate grid levels
            price_range = current_price * 0.1  # 10% range
            grid_step = price_range / grid_levels

            signals = []

            for i in range(grid_levels):
                grid_price = current_price - (price_range / 2) + (i * grid_step)

                if grid_price < current_price:
                    # Buy signal below current price
                    signal_type = SignalType.BUY
                    target_price = grid_price + grid_step
                    stop_loss = grid_price - grid_step
                else:
                    # Sell signal above current price
                    signal_type = SignalType.SELL
                    target_price = grid_price - grid_step
                    stop_loss = grid_price + grid_step

                confidence = 0.5 - (abs(grid_price - current_price) / current_price) * 2
                confidence = max(0.3, min(0.7, confidence))

                signal = TradingSignal(
                    symbol=symbol,
                    signal_type=signal_type,
                    strength=SignalStrength.WEAK,
                    confidence=confidence,
                    price=grid_price,
                    target_price=target_price,
                    stop_loss=stop_loss,
                    strategy=StrategyType.GRID_TRADING,
                    reasoning=f"Grid Level {i+1}: ${grid_price:.2f}",
                )

                signals.append(signal)

            return signals

        except Exception as e:
            logger.error(f"Error in grid trading strategy for {symbol}: {e}")
            return []

    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return pd.Series([50] * len(prices))

    def analyze_market_conditions(self, symbols: List[str]) -> MarketCondition:
        """Analyze overall market conditions"""
        try:
            if not self.market_data_service:
                return MarketCondition()

            # Get market data for analysis
            market_data = self.market_data_service.get_real_time_data(symbols)

            if not market_data:
                return MarketCondition()

            # Calculate market metrics
            price_changes = [data.change_pct for data in market_data.values()]
            volumes = [data.volume for data in market_data.values()]

            # Volatility regime
            volatility = np.std(price_changes)
            if volatility < 0.01:
                volatility_regime = "LOW"
            elif volatility < 0.03:
                volatility_regime = "MEDIUM"
            elif volatility < 0.06:
                volatility_regime = "HIGH"
            else:
                volatility_regime = "EXTREME"

            # Trend direction
            avg_change = np.mean(price_changes)
            if avg_change > 0.01:
                trend_direction = "BULLISH"
            elif avg_change < -0.01:
                trend_direction = "BEARISH"
            else:
                trend_direction = "SIDEWAYS"

            # Market sentiment
            positive_changes = sum(1 for change in price_changes if change > 0)
            sentiment_ratio = positive_changes / len(price_changes)

            if sentiment_ratio > 0.6:
                market_sentiment = "OPTIMISTIC"
            elif sentiment_ratio < 0.4:
                market_sentiment = "PESSIMISTIC"
            else:
                market_sentiment = "NEUTRAL"

            # Liquidity condition
            avg_volume = np.mean(volumes)
            if avg_volume > 1000000:
                liquidity_condition = "HIGH"
            elif avg_volume > 500000:
                liquidity_condition = "MEDIUM"
            else:
                liquidity_condition = "LOW"

            # Correlation regime (simplified)
            correlation_regime = "MEDIUM"  # Would need more sophisticated calculation

            self.market_conditions = MarketCondition(
                volatility_regime=volatility_regime,
                trend_direction=trend_direction,
                market_sentiment=market_sentiment,
                liquidity_condition=liquidity_condition,
                correlation_regime=correlation_regime,
            )

            return self.market_conditions

        except Exception as e:
            logger.error(f"Error analyzing market conditions: {e}")
            return MarketCondition()

    def generate_trading_signals(self, symbols: List[str]) -> List[TradingSignal]:
        """Generate trading signals for multiple symbols"""
        try:
            signals = []

            for symbol in symbols:
                # Get historical data
                if self.market_data_service:
                    historical_data = self.market_data_service.get_historical_data(
                        symbol, period="3mo"
                    )
                    if not historical_data:
                        continue

                    # Run strategies
                    for strategy_type, strategy_func in self.strategies.items():
                        if strategy_type == StrategyType.PAIRS_TRADING:
                            continue  # Skip pairs trading for single symbols

                        signal = strategy_func(symbol, historical_data.data)
                        if signal:
                            signals.append(signal)

            # Add pairs trading signals for correlated symbols
            if len(symbols) >= 2:
                for i in range(len(symbols)):
                    for j in range(i + 1, len(symbols)):
                        hist1 = self.market_data_service.get_historical_data(
                            symbols[i], period="3mo"
                        )
                        hist2 = self.market_data_service.get_historical_data(
                            symbols[j], period="3mo"
                        )

                        if hist1 and hist2:
                            pairs_signal = self.pairs_trading_strategy(
                                symbols[i], symbols[j], hist1.data, hist2.data
                            )
                            if pairs_signal:
                                signals.append(pairs_signal)

            # Update active signals
            self.active_signals.extend(signals)

            # Save signals
            self.save_data()

            return signals

        except Exception as e:
            logger.error(f"Error generating trading signals: {e}")
            return []

    def update_signal_performance(
        self, signal: TradingSignal, exit_price: float, exit_time: datetime
    ):
        """Update strategy performance metrics"""
        try:
            strategy_type = signal.strategy

            if strategy_type not in self.performance_metrics:
                return

            # Calculate return
            if signal.signal_type in [SignalType.BUY, SignalType.STRONG_BUY]:
                return_pct = (exit_price - signal.price) / signal.price
            else:
                return_pct = (signal.price - exit_price) / signal.price

            # Update metrics
            metrics = self.performance_metrics[strategy_type]
            metrics.total_signals += 1

            if return_pct > 0:
                metrics.successful_signals += 1

            metrics.win_rate = metrics.successful_signals / metrics.total_signals

            # Update average return
            total_return = metrics.avg_return * (metrics.total_signals - 1) + return_pct
            metrics.avg_return = total_return / metrics.total_signals

            # Update total P&L
            metrics.total_pnl += return_pct

            # Update max drawdown
            if return_pct < metrics.max_drawdown:
                metrics.max_drawdown = return_pct

            # Update Sharpe ratio (simplified)
            if metrics.total_signals > 1:
                returns = [return_pct]  # Would need to store all returns
                metrics.sharpe_ratio = (
                    np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
                )

            metrics.last_updated = datetime.now()

            # Save performance data
            self.save_data()

        except Exception as e:
            logger.error(f"Error updating signal performance: {e}")

    def get_strategy_recommendations(self, symbol: str) -> Dict[str, Any]:
        """Get trading strategy recommendations for a symbol"""
        try:
            recommendations = {
                "symbol": symbol,
                "market_conditions": asdict(self.market_conditions)
                if self.market_conditions
                else None,
                "active_signals": [],
                "strategy_performance": {},
                "recommendations": [],
            }

            # Get active signals for symbol
            symbol_signals = [s for s in self.active_signals if s.symbol == symbol]
            recommendations["active_signals"] = [asdict(s) for s in symbol_signals]

            # Get strategy performance
            for strategy_type, performance in self.performance_metrics.items():
                recommendations["strategy_performance"][strategy_type.value] = asdict(
                    performance
                )

            # Generate recommendations based on market conditions and performance
            if self.market_conditions:
                if self.market_conditions.volatility_regime == "HIGH":
                    recommendations["recommendations"].append(
                        "Consider mean reversion strategies in high volatility"
                    )
                elif self.market_conditions.volatility_regime == "LOW":
                    recommendations["recommendations"].append(
                        "Consider momentum strategies in low volatility"
                    )

                if self.market_conditions.trend_direction == "BULLISH":
                    recommendations["recommendations"].append(
                        "Favorable conditions for trend-following strategies"
                    )
                elif self.market_conditions.trend_direction == "BEARISH":
                    recommendations["recommendations"].append(
                        "Consider defensive strategies and risk management"
                    )

            return recommendations

        except Exception as e:
            logger.error(f"Error getting strategy recommendations: {e}")
            return {}

    def save_data(self):
        """Save trading intelligence data"""
        try:
            # Save signals
            signals_data = [asdict(signal) for signal in self.active_signals]
            with open(self.signals_file, "w") as f:
                json.dump(signals_data, f, indent=2, default=str)

            # Save performance metrics
            performance_data = {
                strategy.value: asdict(metrics)
                for strategy, metrics in self.performance_metrics.items()
            }
            with open(self.performance_file, "w") as f:
                json.dump(performance_data, f, indent=2, default=str)

            logger.info("Trading intelligence data saved successfully")

        except Exception as e:
            logger.error(f"Error saving trading intelligence data: {e}")

    def load_data(self):
        """Load trading intelligence data"""
        try:
            # Load signals
            if self.signals_file.exists():
                with open(self.signals_file, "r") as f:
                    signals_data = json.load(f)

                for signal_data in signals_data:
                    if "timestamp" in signal_data:
                        signal_data["timestamp"] = datetime.fromisoformat(
                            signal_data["timestamp"]
                        )
                    if "expiration" in signal_data and signal_data["expiration"]:
                        signal_data["expiration"] = datetime.fromisoformat(
                            signal_data["expiration"]
                        )

                    signal = TradingSignal(**signal_data)
                    self.active_signals.append(signal)

                logger.info(f"Loaded {len(self.active_signals)} trading signals")

            # Load performance metrics
            if self.performance_file.exists():
                with open(self.performance_file, "r") as f:
                    performance_data = json.load(f)

                for strategy_name, metrics_data in performance_data.items():
                    if "last_updated" in metrics_data and metrics_data["last_updated"]:
                        metrics_data["last_updated"] = datetime.fromisoformat(
                            metrics_data["last_updated"]
                        )

                    strategy_type = StrategyType(strategy_name)
                    if strategy_type in self.performance_metrics:
                        for key, value in metrics_data.items():
                            if hasattr(self.performance_metrics[strategy_type], key):
                                setattr(
                                    self.performance_metrics[strategy_type], key, value
                                )

                logger.info("Loaded strategy performance metrics")

        except Exception as e:
            logger.error(f"Error loading trading intelligence data: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Create trading intelligence service
    tis = TradingIntelligenceService()

    # Test strategy generation
    test_data = pd.DataFrame(
        {
            "Close": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            "Volume": [1000000] * 11,
            "High": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            "Low": [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        }
    )

    # Test momentum strategy
    momentum_signal = tis.momentum_strategy("TEST", test_data)
    if momentum_signal:
        print("Momentum Signal:", asdict(momentum_signal))

    # Test mean reversion strategy
    mean_rev_signal = tis.mean_reversion_strategy("TEST", test_data)
    if mean_rev_signal:
        print("Mean Reversion Signal:", asdict(mean_rev_signal))

    print("Trading Intelligence Service initialized successfully")
