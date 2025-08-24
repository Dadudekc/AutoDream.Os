import logging
from typing import List
import numpy as np
import pandas as pd
from datetime import datetime

from .models import MarketCondition

logger = logging.getLogger(__name__)


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
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
            return MarketCondition(
                volatility_regime="MEDIUM",
                trend_direction="SIDEWAYS",
                market_sentiment="NEUTRAL",
                liquidity_condition="MEDIUM",
                correlation_regime="MEDIUM",
            )

        market_data = self.market_data_service.get_real_time_data(symbols)
        if not market_data:
            return MarketCondition(
                volatility_regime="MEDIUM",
                trend_direction="SIDEWAYS",
                market_sentiment="NEUTRAL",
                liquidity_condition="MEDIUM",
                correlation_regime="MEDIUM",
            )

        price_changes = [data.change_pct for data in market_data.values()]
        volumes = [data.volume for data in market_data.values()]

        volatility = np.std(price_changes)
        if volatility < 0.01:
            volatility_regime = "LOW"
        elif volatility < 0.03:
            volatility_regime = "MEDIUM"
        elif volatility < 0.06:
            volatility_regime = "HIGH"
        else:
            volatility_regime = "EXTREME"

        avg_change = np.mean(price_changes)
        if avg_change > 0.01:
            trend_direction = "BULLISH"
        elif avg_change < -0.01:
            trend_direction = "BEARISH"
        else:
            trend_direction = "SIDEWAYS"

        positive_changes = sum(1 for change in price_changes if change > 0)
        sentiment_ratio = positive_changes / len(price_changes)
        if sentiment_ratio > 0.6:
            market_sentiment = "OPTIMISTIC"
        elif sentiment_ratio < 0.4:
            market_sentiment = "PESSIMISTIC"
        else:
            market_sentiment = "NEUTRAL"

        total_volume = np.sum(volumes)
        if total_volume > np.mean(volumes) * len(volumes) * 1.5:
            liquidity_condition = "HIGH"
        elif total_volume < np.mean(volumes) * len(volumes) * 0.5:
            liquidity_condition = "LOW"
        else:
            liquidity_condition = "MEDIUM"

        correlation_regime = "MEDIUM"

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
            volatility_regime="MEDIUM",
            trend_direction="SIDEWAYS",
            market_sentiment="NEUTRAL",
            liquidity_condition="MEDIUM",
            correlation_regime="MEDIUM",
        )
