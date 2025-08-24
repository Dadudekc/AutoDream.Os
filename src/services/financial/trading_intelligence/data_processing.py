import logging
from typing import List
import numpy as np
import pandas as pd

from .models import (
    MarketCondition,
    VolatilityRegime,
    TrendDirection,
    MarketSentiment,
    LiquidityCondition,
    CorrelationRegime,
)

logger = logging.getLogger(__name__)


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    try:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / (loss + 1e-9)
        rsi = 100 - (100 / (1 + rs))
        return rsi
    except Exception as e:
        logger.error(f"Error calculating RSI: {e}")
        return pd.Series([50] * len(prices))


def analyze_market_conditions(self, symbols: List[str]) -> MarketCondition:
    """Analyze overall market conditions"""
    try:
        if not self.market_data_service:
            return MarketCondition(
                volatility_regime=VolatilityRegime.MEDIUM,
                trend_direction=TrendDirection.SIDEWAYS,
                market_sentiment=MarketSentiment.NEUTRAL,
                liquidity_condition=LiquidityCondition.MEDIUM,
                correlation_regime=CorrelationRegime.MEDIUM,
            )

        market_data = self.market_data_service.get_real_time_data(symbols)
        if not market_data:
            return MarketCondition(
                volatility_regime=VolatilityRegime.MEDIUM,
                trend_direction=TrendDirection.SIDEWAYS,
                market_sentiment=MarketSentiment.NEUTRAL,
                liquidity_condition=LiquidityCondition.MEDIUM,
                correlation_regime=CorrelationRegime.MEDIUM,
            )

        price_changes = [data.change_pct for data in market_data.values()]
        volumes = [data.volume for data in market_data.values()]

        volatility = np.std(price_changes)
        if volatility < 0.01:
            volatility_regime = VolatilityRegime.LOW
        elif volatility < 0.03:
            volatility_regime = VolatilityRegime.MEDIUM
        elif volatility < 0.06:
            volatility_regime = VolatilityRegime.HIGH
        else:
            volatility_regime = VolatilityRegime.EXTREME

        avg_change = np.mean(price_changes)
        if avg_change > 0.01:
            trend_direction = TrendDirection.BULLISH
        elif avg_change < -0.01:
            trend_direction = TrendDirection.BEARISH
        else:
            trend_direction = TrendDirection.SIDEWAYS

        positive_changes = sum(1 for change in price_changes if change > 0)
        sentiment_ratio = positive_changes / len(price_changes)
        if sentiment_ratio > 0.6:
            market_sentiment = MarketSentiment.OPTIMISTIC
        elif sentiment_ratio < 0.4:
            market_sentiment = MarketSentiment.PESSIMISTIC
        else:
            market_sentiment = MarketSentiment.NEUTRAL

        historical_volumes = []
        for symbol in symbols:
            hist = self.market_data_service.get_historical_data(symbol, period="1mo")
            if hist and hasattr(hist, "data"):
                historical_volumes.append(hist.data["Volume"].mean())
        if historical_volumes:
            historical_avg = np.mean(historical_volumes)
            current_avg = np.mean(volumes)
            volume_ratio = current_avg / historical_avg if historical_avg > 0 else 1.0
            if volume_ratio > 1.5:
                liquidity_condition = LiquidityCondition.HIGH
            elif volume_ratio < 0.5:
                liquidity_condition = LiquidityCondition.LOW
            else:
                liquidity_condition = LiquidityCondition.MEDIUM
        else:
            liquidity_condition = LiquidityCondition.MEDIUM

        correlation_regime = CorrelationRegime.MEDIUM

        return MarketCondition(
            volatility_regime=volatility_regime,
            trend_direction=trend_direction,
            market_sentiment=market_sentiment,
            liquidity_condition=liquidity_condition,
            correlation_regime=correlation_regime,
        )
    except Exception as e:
        logger.error(f"Error analyzing market conditions: {e}")
        return MarketCondition(
            volatility_regime=VolatilityRegime.MEDIUM,
            trend_direction=TrendDirection.SIDEWAYS,
            market_sentiment=MarketSentiment.NEUTRAL,
            liquidity_condition=LiquidityCondition.MEDIUM,
            correlation_regime=CorrelationRegime.MEDIUM,
        )
