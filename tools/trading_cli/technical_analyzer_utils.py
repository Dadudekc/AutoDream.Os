#!/usr/bin/env python3
"""
Technical Analyzer Utils
========================

Utility functions and technical calculations for trading analysis.

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

from typing import Any


def calculate_technical_indicators(historical_data: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate all technical indicators"""
    if len(historical_data) < 20:
        return {"error": "Insufficient data for technical analysis"}

    # Extract closing prices
    closes = [float(data["close"]) for data in historical_data]

    # Calculate indicators
    indicators = {
        "sma_20": calculate_sma(closes, 20),
        "ema_12": calculate_ema(closes, 12),
        "rsi_14": calculate_rsi(closes, 14),
        "macd": calculate_macd(closes),
        "bollinger_bands": calculate_bollinger_bands(closes, 20),
        "stochastic": calculate_stochastic(closes),
    }

    return indicators


def calculate_sma(prices: list[float], period: int) -> float:
    """Calculate Simple Moving Average"""
    if len(prices) < period:
        return prices[-1] if prices else 0.0

    return sum(prices[-period:]) / period


def calculate_ema(prices: list[float], period: int) -> float:
    """Calculate Exponential Moving Average"""
    if len(prices) < period:
        return prices[-1] if prices else 0.0

    # Calculate smoothing factor
    multiplier = 2 / (period + 1)

    # Start with SMA
    ema = calculate_sma(prices[:period], period)

    # Calculate EMA for remaining prices
    for price in prices[period:]:
        ema = (price * multiplier) + (ema * (1 - multiplier))

    return ema


def calculate_rsi(prices: list[float], period: int = 14) -> float:
    """Calculate Relative Strength Index"""
    if len(prices) < period + 1:
        return 50.0  # Neutral RSI

    # Calculate price changes
    changes = []
    for i in range(1, len(prices)):
        changes.append(prices[i] - prices[i - 1])

    # Separate gains and losses
    gains = [change if change > 0 else 0 for change in changes]
    losses = [-change if change < 0 else 0 for change in changes]

    # Calculate average gains and losses
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100.0

    # Calculate RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_macd(prices: list[float]) -> dict[str, float]:
    """Calculate MACD (Moving Average Convergence Divergence)"""
    if len(prices) < 26:
        return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}

    # Calculate EMAs
    ema_12 = calculate_ema(prices, 12)
    ema_26 = calculate_ema(prices, 26)

    # Calculate MACD line
    macd_line = ema_12 - ema_26

    # Calculate signal line (9-period EMA of MACD)
    # For simplicity, we'll use a basic approximation
    signal_line = macd_line * 0.9  # Simplified signal calculation

    # Calculate histogram
    histogram = macd_line - signal_line

    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram,
    }


def calculate_bollinger_bands(prices: list[float], period: int = 20) -> dict[str, float]:
    """Calculate Bollinger Bands"""
    if len(prices) < period:
        current_price = prices[-1] if prices else 0.0
        return {"upper": current_price, "middle": current_price, "lower": current_price}

    # Calculate SMA (middle band)
    sma = calculate_sma(prices, period)

    # Calculate standard deviation
    recent_prices = prices[-period:]
    variance = sum((price - sma) ** 2 for price in recent_prices) / period
    std_dev = variance**0.5

    # Calculate bands
    upper_band = sma + (2 * std_dev)
    lower_band = sma - (2 * std_dev)

    return {
        "upper": upper_band,
        "middle": sma,
        "lower": lower_band,
    }


def calculate_stochastic(
    prices: list[float], k_period: int = 14, d_period: int = 3
) -> dict[str, float]:
    """Calculate Stochastic Oscillator"""
    if len(prices) < k_period:
        return {"k_percent": 50.0, "d_percent": 50.0}

    # Get recent prices for calculation
    recent_prices = prices[-k_period:]

    # Calculate %K
    current_price = recent_prices[-1]
    lowest_low = min(recent_prices)
    highest_high = max(recent_prices)

    if highest_high == lowest_low:
        k_percent = 50.0
    else:
        k_percent = ((current_price - lowest_low) / (highest_high - lowest_low)) * 100

    # Calculate %D (simplified as moving average of %K)
    d_percent = k_percent * 0.9  # Simplified %D calculation

    return {
        "k_percent": k_percent,
        "d_percent": d_percent,
    }


def generate_technical_signals(
    historical_data: list[dict[str, Any]], indicators: dict[str, Any]
) -> dict[str, Any]:
    """Generate trading signals based on technical indicators"""
    if "error" in indicators:
        return {"error": indicators["error"]}

    current_price = historical_data[-1]["close"]
    signals = []
    signal_strength = 0

    # RSI signals
    rsi = indicators["rsi_14"]
    if rsi < 30:
        signals.append("BUY (RSI Oversold)")
        signal_strength += 2
    elif rsi > 70:
        signals.append("SELL (RSI Overbought)")
        signal_strength -= 2

    # MACD signals
    macd = indicators["macd"]
    macd_signal = indicators["macd"]["signal"]
    if macd > macd_signal:
        signals.append("BUY (MACD Bullish)")
        signal_strength += 1
    else:
        signals.append("SELL (MACD Bearish)")
        signal_strength -= 1

    # Bollinger Bands signals
    bb = indicators["bollinger_bands"]
    if current_price < bb["lower"]:
        signals.append("BUY (Price Below Lower Band)")
        signal_strength += 2
    elif current_price > bb["upper"]:
        signals.append("SELL (Price Above Upper Band)")
        signal_strength -= 2

    # Stochastic signals
    stoch = indicators["stochastic"]
    if stoch["k_percent"] < 20:
        signals.append("BUY (Stochastic Oversold)")
        signal_strength += 1
    elif stoch["k_percent"] > 80:
        signals.append("SELL (Stochastic Overbought)")
        signal_strength -= 1

    # Moving Average signals
    sma_20 = indicators["sma_20"]
    if current_price > sma_20:
        signals.append("BUY (Price Above SMA)")
        signal_strength += 1
    else:
        signals.append("SELL (Price Below SMA)")
        signal_strength -= 1

    # Determine overall signal
    if signal_strength > 2:
        overall_signal = "BUY"
        strength = "STRONG"
    elif signal_strength > 0:
        overall_signal = "BUY"
        strength = "MODERATE"
    elif signal_strength < -2:
        overall_signal = "SELL"
        strength = "STRONG"
    elif signal_strength < 0:
        overall_signal = "SELL"
        strength = "MODERATE"
    else:
        overall_signal = "HOLD"
        strength = "WEAK"

    # Determine trend direction
    if current_price > sma_20:
        trend_direction = "UPTREND"
    elif current_price < sma_20:
        trend_direction = "DOWNTREND"
    else:
        trend_direction = "SIDEWAYS"

    return {
        "overall_signal": overall_signal,
        "signal_strength": strength,
        "trend_direction": trend_direction,
        "individual_signals": signals,
        "signal_score": signal_strength,
    }
