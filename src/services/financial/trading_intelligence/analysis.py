"""Market analysis utilities for the trading intelligence service."""

from __future__ import annotations

import logging
from typing import Optional

import pandas as pd

from .constants import RSI_PERIOD
from .models import (
    MarketCondition,
    VolatilityRegime,
    TrendDirection,
    MarketSentiment,
    LiquidityCondition,
    CorrelationRegime,
)

logger = logging.getLogger(__name__)


def calculate_rsi(prices: pd.Series, period: int = RSI_PERIOD) -> pd.Series:
    """Calculate the Relative Strength Index (RSI).

    Parameters
    ----------
    prices:
        Series of closing prices.
    period:
        Number of periods to use for the RSI calculation.

    Returns
    -------
    pandas.Series
        RSI values corresponding to *prices*.
    """

    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0.0).rolling(window=period).mean()
    rs = gain / loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))


def analyze_market_conditions(df: pd.DataFrame) -> Optional[MarketCondition]:
    """Analyze basic market conditions from historical data.

    The heuristics implemented here are intentionally simple but provide
    reasonable defaults for trend, volatility, sentiment, liquidity, and
    correlation regimes.

    Parameters
    ----------
    df:
        DataFrame containing ``Close`` and ``Volume`` columns.

    Returns
    -------
    MarketCondition or None
        A snapshot of market conditions or ``None`` if *df* is empty.
    """

    if df.empty:
        logger.warning("No data supplied for market condition analysis")
        return None

    returns = df["Close"].pct_change().dropna()
    volatility = returns.rolling(window=10).std().iloc[-1]
    volume = df["Volume"].rolling(window=10).mean().iloc[-1]
    price_change = df["Close"].iloc[-1] - df["Close"].iloc[0]

    volatility_regime = (
        VolatilityRegime.HIGH
        if volatility > 0.05
        else VolatilityRegime.MEDIUM
        if volatility > 0.02
        else VolatilityRegime.LOW
    )

    trend_direction = (
        TrendDirection.BULLISH
        if price_change > 0
        else TrendDirection.BEARISH
        if price_change < 0
        else TrendDirection.SIDEWAYS
    )

    sentiment = (
        MarketSentiment.OPTIMISTIC
        if price_change > 0
        else MarketSentiment.PESSIMISTIC
        if price_change < 0
        else MarketSentiment.NEUTRAL
    )

    liquidity = (
        LiquidityCondition.HIGH
        if volume > df["Volume"].median()
        else LiquidityCondition.LOW
    )

    correlation_regime = CorrelationRegime.MEDIUM

    return MarketCondition(
        volatility_regime=volatility_regime,
        trend_direction=trend_direction,
        market_sentiment=sentiment,
        liquidity_condition=liquidity,
        correlation_regime=correlation_regime,
    )
