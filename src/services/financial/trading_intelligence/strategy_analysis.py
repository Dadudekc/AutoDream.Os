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
        params = self.strategy_params.get(StrategyType.MOMENTUM, {})
        lookback_period = params.get("lookback_period", 20)
        momentum_threshold = params.get("momentum_threshold", 0.02)
        volume_threshold = params.get("volume_threshold", 1.5)
        strong_momentum = params.get("strong_momentum", 0.05)
        strong_volume = params.get("strong_volume", 2.0)
        rsi_upper = params.get("rsi_upper", 70)
        rsi_lower = params.get("rsi_lower", 30)
        min_history = params.get("min_history", lookback_period + 10)

        if len(historical_data) < min_history:
            return None

        close_prices = historical_data["Close"]
        volume = historical_data["Volume"]

        price_momentum = (close_prices.iloc[-1] - close_prices.iloc[-lookback_period]) / close_prices.iloc[-lookback_period]
        avg_volume = volume.iloc[-lookback_period:].mean()
        current_volume = volume.iloc[-1]
        volume_ratio = current_volume / avg_volume
        rsi = self.calculate_rsi(close_prices, 14)
        current_rsi = rsi.iloc[-1]

        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        confidence = 0.0

        if price_momentum > momentum_threshold and volume_ratio > volume_threshold and current_rsi < rsi_upper:
            signal_type = SignalType.BUY
            if price_momentum > strong_momentum and volume_ratio > strong_volume:
                signal_type = SignalType.STRONG_BUY
                strength = SignalStrength.STRONG
                confidence = params.get("strong_confidence", 0.8)
            else:
                strength = SignalStrength.MODERATE
                confidence = params.get("base_confidence", 0.6)
        elif price_momentum < -momentum_threshold and volume_ratio > volume_threshold and current_rsi > rsi_lower:
            signal_type = SignalType.SELL
            if price_momentum < -strong_momentum and volume_ratio > strong_volume:
                signal_type = SignalType.STRONG_SELL
                strength = SignalStrength.STRONG
                confidence = params.get("strong_confidence", 0.8)
            else:
                strength = SignalStrength.MODERATE
                confidence = params.get("base_confidence", 0.6)

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
        params = self.strategy_params.get(StrategyType.MEAN_REVERSION, {})
        lookback_period = params.get("lookback_period", 50)
        std_threshold = params.get("std_dev_threshold", 2.0)
        strong_threshold = params.get("strong_threshold", 3.0)
        reversion_strength = params.get("reversion_strength", 0.1)
        min_history = params.get("min_history", lookback_period + 10)

        if len(historical_data) < min_history:
            return None

        close_prices = historical_data["Close"]
        sma = close_prices.rolling(window=lookback_period).mean()
        std = close_prices.rolling(window=lookback_period).std()
        upper_band = sma + (std * std_threshold)
        lower_band = sma - (std * std_threshold)

        current_price = close_prices.iloc[-1]
        current_sma = sma.iloc[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        z_score = (current_price - current_sma) / std.iloc[-1]

        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        confidence = 0.0

        if z_score > std_threshold:
            signal_type = SignalType.SELL
            if z_score > strong_threshold:
                signal_type = SignalType.STRONG_SELL
                strength = SignalStrength.STRONG
                confidence = params.get("strong_confidence", 0.8)
            else:
                strength = SignalStrength.MODERATE
                confidence = params.get("base_confidence", 0.6)
        elif z_score < -std_threshold:
            signal_type = SignalType.BUY
            if z_score < -strong_threshold:
                signal_type = SignalType.STRONG_BUY
                strength = SignalStrength.STRONG
                confidence = params.get("strong_confidence", 0.8)
            else:
                strength = SignalStrength.MODERATE
                confidence = params.get("base_confidence", 0.6)

        if signal_type != SignalType.HOLD:
            target_price = current_sma
            stop_loss = current_price * (1 + abs(z_score) * reversion_strength)
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
        params = self.strategy_params.get(StrategyType.BREAKOUT, {})
        breakout_period = params.get("breakout_period", 20)
        volume_multiplier = params.get("volume_multiplier", 1.5)
        breakout_buffer = params.get("breakout_buffer", 0.01)
        target_multiplier = params.get("target_multiplier", 0.05)
        min_history = params.get("min_history", breakout_period + 10)

        if len(historical_data) < min_history:
            return None

        close_prices = historical_data["Close"]
        volume = historical_data["Volume"]
        high_n = close_prices.rolling(window=breakout_period).max()
        low_n = close_prices.rolling(window=breakout_period).min()

        current_price = close_prices.iloc[-1]
        resistance = high_n.iloc[-2]
        support = low_n.iloc[-2]
        avg_volume = volume.iloc[-breakout_period:].mean()
        current_volume = volume.iloc[-1]
        volume_confirmation = current_volume > avg_volume * volume_multiplier
        breakout_up = current_price > resistance * (1 + breakout_buffer)
        breakout_down = current_price < support * (1 - breakout_buffer)

        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        confidence = 0.0
        if breakout_up and volume_confirmation:
            signal_type = SignalType.BUY
            strength = SignalStrength.MODERATE
            confidence = params.get("base_confidence", 0.7)
            target_price = current_price * (1 + target_multiplier)
            stop_loss = resistance
        elif breakout_down and volume_confirmation:
            signal_type = SignalType.SELL
            strength = SignalStrength.MODERATE
            confidence = params.get("base_confidence", 0.7)
            target_price = current_price * (1 - target_multiplier)
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
        params = self.strategy_params.get(StrategyType.SCALPING, {})
        sma_short = params.get("sma_short", 5)
        sma_long = params.get("sma_long", 10)
        min_spread = params.get("min_spread", 0.001)
        profit_target = params.get("profit_target", 0.002)
        volatility_threshold = params.get("volatility_threshold", 0.01)
        stop_loss_pct = params.get("stop_loss_pct", 0.001)
        min_history = params.get("min_history", max(sma_long, 10))

        if len(historical_data) < min_history:
            return None

        close_prices = historical_data["Close"]
        high_prices = historical_data["High"]
        low_prices = historical_data["Low"]
        current_price = close_prices.iloc[-1]

        sma_short_series = close_prices.rolling(window=sma_short).mean()
        sma_long_series = close_prices.rolling(window=sma_long).mean()
        price_vs_sma_short = (current_price - sma_short_series.iloc[-1]) / sma_short_series.iloc[-1]
        price_vs_sma_long = (current_price - sma_long_series.iloc[-1]) / sma_long_series.iloc[-1]
        recent_high = high_prices.iloc[-sma_short:].max()
        recent_low = low_prices.iloc[-sma_short:].min()
        volatility = (recent_high - recent_low) / current_price

        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        confidence = 0.0

        if price_vs_sma_short > min_spread and price_vs_sma_long > min_spread * 2 and volatility > volatility_threshold:
            signal_type = SignalType.BUY
            strength = SignalStrength.MODERATE
            confidence = params.get("base_confidence", 0.6)
            target_price = current_price * (1 + profit_target)
            stop_loss = current_price * (1 - stop_loss_pct)
        elif price_vs_sma_short < -min_spread and price_vs_sma_long < -min_spread * 2 and volatility > volatility_threshold:
            signal_type = SignalType.SELL
            strength = SignalStrength.MODERATE
            confidence = params.get("base_confidence", 0.6)
            target_price = current_price * (1 - profit_target)
            stop_loss = current_price * (1 + stop_loss_pct)

        if signal_type != SignalType.HOLD:
            reasoning = (
                f"Scalping: SMA{sma_short}: {price_vs_sma_short:.3%}, "
                f"SMA{sma_long}: {price_vs_sma_long:.3%}, Vol: {volatility:.3%}"
            )
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
        params = self.strategy_params.get(StrategyType.PAIRS_TRADING, {})
        min_history = params.get("min_history", 50)
        correlation_threshold = params.get("correlation_threshold", 0.7)
        z_score_threshold = params.get("z_score_threshold", 2.0)

        if len(historical_data1) < min_history or len(historical_data2) < min_history:
            return None

        returns1 = historical_data1["Close"].pct_change().dropna()
        returns2 = historical_data2["Close"].pct_change().dropna()
        min_length = min(len(returns1), len(returns2))
        returns1 = returns1.iloc[-min_length:]
        returns2 = returns2.iloc[-min_length:]
        correlation = returns1.corr(returns2)
        if abs(correlation) < correlation_threshold:
            return None

        spread = returns1 - returns2
        spread_mean = spread.mean()
        spread_std = spread.std()
        current_spread = spread.iloc[-1]
        z_score = (current_spread - spread_mean) / spread_std

        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        confidence = 0.0

        if z_score > z_score_threshold:
            signal_type = SignalType.SELL
            strength = SignalStrength.MODERATE
            confidence = params.get("base_confidence", 0.7)
            current_price = historical_data1["Close"].iloc[-1]
            target_price = current_price * (1 - abs(z_score) * 0.01)
            stop_loss = current_price * (1 + abs(z_score) * 0.01)
        elif z_score < -z_score_threshold:
            signal_type = SignalType.BUY
            strength = SignalStrength.MODERATE
            confidence = params.get("base_confidence", 0.7)
            current_price = historical_data1["Close"].iloc[-1]
            target_price = current_price * (1 + abs(z_score) * 0.01)
            stop_loss = current_price * (1 - abs(z_score) * 0.01)

        if signal_type != SignalType.HOLD:
            reasoning = f"Pairs Trading: Z-Score: {z_score:.2f}, Correlation: {correlation:.2f}"
            return TradingSignal(
                symbol=f"{symbol1}/{symbol2}",
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
        params = self.strategy_params.get(StrategyType.GRID_TRADING, {})
        grid_levels = params.get("grid_levels", grid_levels)
        price_range_pct = params.get("price_range_pct", 0.1)
        min_history = params.get("min_history", 20)

        if len(historical_data) < min_history:
            return []

        current_price = historical_data["Close"].iloc[-1]
        price_range = current_price * price_range_pct
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
