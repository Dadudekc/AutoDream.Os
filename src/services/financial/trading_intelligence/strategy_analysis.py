import logging
from typing import Optional, List
import pandas as pd
import numpy as np

from .models import (
    TradingSignal,
    StrategyType,
    SignalType,
    SignalStrength,
)

logger = logging.getLogger(__name__)


def momentum_strategy(self, symbol: str, historical_data: pd.DataFrame) -> Optional[TradingSignal]:
    """Momentum-based trading strategy"""
    try:
        if len(historical_data) < 30:
            return None

        close_prices = historical_data["Close"]
        volume = historical_data["Volume"]

        price_momentum = (close_prices.iloc[-1] - close_prices.iloc[-20]) / close_prices.iloc[-20]
        avg_volume = volume.iloc[-20:].mean()
        current_volume = volume.iloc[-1]
        volume_ratio = current_volume / avg_volume
        rsi = self.calculate_rsi(close_prices, 14)
        current_rsi = rsi.iloc[-1]

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


def mean_reversion_strategy(self, symbol: str, historical_data: pd.DataFrame) -> Optional[TradingSignal]:
    """Mean reversion trading strategy"""
    try:
        if len(historical_data) < 60:
            return None

        close_prices = historical_data["Close"]
        sma = close_prices.rolling(window=20).mean()
        std = close_prices.rolling(window=20).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)

        current_price = close_prices.iloc[-1]
        current_sma = sma.iloc[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        z_score = (current_price - current_sma) / std.iloc[-1]

        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        confidence = 0.0

        if z_score > 2.0:
            signal_type = SignalType.SELL
            if z_score > 3.0:
                signal_type = SignalType.STRONG_SELL
                strength = SignalStrength.STRONG
                confidence = 0.8
            else:
                strength = SignalStrength.MODERATE
                confidence = 0.6
        elif z_score < -2.0:
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


def breakout_strategy(self, symbol: str, historical_data: pd.DataFrame) -> Optional[TradingSignal]:
    """Breakout trading strategy"""
    try:
        if len(historical_data) < 30:
            return None

        close_prices = historical_data["Close"]
        volume = historical_data["Volume"]
        high_20 = close_prices.rolling(window=20).max()
        low_20 = close_prices.rolling(window=20).min()

        current_price = close_prices.iloc[-1]
        resistance = high_20.iloc[-2]
        support = low_20.iloc[-2]
        avg_volume = volume.iloc[-20:].mean()
        current_volume = volume.iloc[-1]
        volume_confirmation = current_volume > avg_volume * 1.5
        breakout_up = current_price > resistance * 1.01
        breakout_down = current_price < support * 0.99

        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        confidence = 0.0
        if breakout_up and volume_confirmation:
            signal_type = SignalType.BUY
            strength = SignalStrength.MODERATE
            confidence = 0.7
            target_price = current_price * 1.05
            stop_loss = resistance
        elif breakout_down and volume_confirmation:
            signal_type = SignalType.SELL
            strength = SignalStrength.MODERATE
            confidence = 0.7
            target_price = current_price * 0.95
            stop_loss = support

        if signal_type != SignalType.HOLD:
            reasoning = (
                f"Breakout: {'UP' if breakout_up else 'DOWN'}, Volume: {volume_confirmation}, "
                f"Resistance: ${resistance:.2f}, Support: ${support:.2f}"
            )
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


def scalping_strategy(self, symbol: str, historical_data: pd.DataFrame) -> Optional[TradingSignal]:
    """Scalping trading strategy"""
    try:
        if len(historical_data) < 10:
            return None

        close_prices = historical_data["Close"]
        high_prices = historical_data["High"]
        low_prices = historical_data["Low"]
        current_price = close_prices.iloc[-1]

        sma_5 = close_prices.rolling(window=5).mean()
        sma_10 = close_prices.rolling(window=10).mean()
        price_vs_sma5 = (current_price - sma_5.iloc[-1]) / sma_5.iloc[-1]
        price_vs_sma10 = (current_price - sma_10.iloc[-1]) / sma_10.iloc[-1]
        recent_high = high_prices.iloc[-5:].max()
        recent_low = low_prices.iloc[-5:].min()
        volatility = (recent_high - recent_low) / current_price

        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        confidence = 0.0

        if price_vs_sma5 > 0.001 and price_vs_sma10 > 0.002 and volatility > 0.01:
            signal_type = SignalType.BUY
            strength = SignalStrength.MODERATE
            confidence = 0.6
            target_price = current_price * 1.002
            stop_loss = current_price * 0.999
        elif price_vs_sma5 < -0.001 and price_vs_sma10 < -0.002 and volatility > 0.01:
            signal_type = SignalType.SELL
            strength = SignalStrength.MODERATE
            confidence = 0.6
            target_price = current_price * 0.998
            stop_loss = current_price * 1.001

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

        returns1 = historical_data1["Close"].pct_change().dropna()
        returns2 = historical_data2["Close"].pct_change().dropna()
        min_length = min(len(returns1), len(returns2))
        returns1 = returns1.iloc[-min_length:]
        returns2 = returns2.iloc[-min_length:]
        correlation = returns1.corr(returns2)
        if abs(correlation) < 0.7:
            return None

        spread = returns1 - returns2
        spread_mean = spread.mean()
        spread_std = spread.std()
        current_spread = spread.iloc[-1]
        z_score = (current_spread - spread_mean) / spread_std

        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        confidence = 0.0

        if z_score > 2.0:
            signal_type = SignalType.SELL
            strength = SignalStrength.MODERATE
            confidence = 0.7
            current_price = historical_data1["Close"].iloc[-1]
            target_price = current_price * (1 - abs(z_score) * 0.01)
            stop_loss = current_price * (1 + abs(z_score) * 0.01)
        elif z_score < -2.0:
            signal_type = SignalType.BUY
            strength = SignalStrength.MODERATE
            confidence = 0.7
            current_price = historical_data1["Close"].iloc[-1]
            target_price = current_price * (1 + abs(z_score) * 0.01)
            stop_loss = current_price * (1 - abs(z_score) * 0.01)

        if signal_type != SignalType.HOLD:
            reasoning = f"Pairs Trading: Z-Score: {z_score:.2f}, Correlation: {correlation:.2f}"
            return TradingSignal(
                symbol=symbol1,
                signal_type=signal_type,
                strength=strength,
                confidence=confidence,
                price=historical_data1["Close"].iloc[-1],
                target_price=target_price,
                stop_loss=stop_loss,
                strategy=StrategyType.PAIRS_TRADING,
                reasoning=reasoning,
            )
        return None
    except Exception as e:
        logger.error(f"Error in pairs trading strategy for {symbol1}/{symbol2}: {e}")
        return None


def grid_trading_strategy(self, symbol: str, historical_data: pd.DataFrame, grid_levels: int = 5) -> List[TradingSignal]:
    """Grid trading strategy"""
    try:
        if len(historical_data) < 20:
            return []

        current_price = historical_data["Close"].iloc[-1]
        price_range = current_price * 0.1
        grid_step = price_range / grid_levels
        signals = []

        for i in range(grid_levels):
            grid_price = current_price - (price_range / 2) + (i * grid_step)
            if grid_price < current_price:
                signal_type = SignalType.BUY
                target_price = grid_price + grid_step
                stop_loss = grid_price - grid_step
            else:
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
