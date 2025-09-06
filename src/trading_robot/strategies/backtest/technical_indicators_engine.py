#!/usr/bin/env python3
"""
Trading Backtest Technical Indicators Engine
===========================================

Technical indicators engine for trading strategy backtesting.
Handles MA, RSI, ATR calculations and other technical indicators.
V2 COMPLIANT: Focused technical indicators under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR TECHNICAL INDICATORS
@license MIT
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class IndicatorConfig:
    """Configuration for technical indicators."""

    ma_short_len: int = 20
    ma_long_len: int = 50
    rsi_period: int = 14
    rsi_ob: int = 70
    rsi_os: int = 30
    atr_period: int = 14
    atr_mult: float = 2.0
    min_vol: float = 0.004


class TechnicalIndicatorsEngine:
    """Technical indicators engine for trading backtesting."""

    def __init__(self, config: IndicatorConfig):
        """Initialize technical indicators engine with configuration."""
        self.config = config

    def calculate_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators for the dataframe."""
        df = df.copy()

        # Calculate moving averages
        df = self._calculate_moving_averages(df)

        # Calculate RSI
        df = self._calculate_rsi(df)

        # Calculate ATR
        df = self._calculate_atr(df)

        # Calculate trend filters
        df = self._calculate_trend_filters(df)

        # Calculate volatility filter
        df = self._calculate_volatility_filter(df)

        # Calculate session filter
        df = self._calculate_session_filter(df)

        # Drop rows with NaN values
        df = df.dropna()

        return df

    def _calculate_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate moving averages."""
        df["ma_short"] = df["close"].rolling(window=self.config.ma_short_len).mean()
        df["ma_long"] = df["close"].rolling(window=self.config.ma_long_len).mean()
        return df

    def _calculate_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate RSI (Relative Strength Index)"""

        def calculate_rsi(prices, period=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))

        df["rsi"] = calculate_rsi(df["close"], self.config.rsi_period)
        return df

    def _calculate_atr(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate ATR (Average True Range)"""

        def calculate_atr(high, low, close, period=14):
            tr1 = high - low
            tr2 = abs(high - close.shift(1))
            tr3 = abs(low - close.shift(1))
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            return tr.rolling(period).mean()

        df["atr"] = calculate_atr(
            df["high"], df["low"], df["close"], self.config.atr_period
        )
        return df

    def _calculate_trend_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate trend direction filters."""
        df["trend_up"] = (
            (df["ma_short"] > df["ma_long"])
            & (df["ma_short"].notna())
            & (df["ma_long"].notna())
        )
        df["trend_dn"] = (
            (df["ma_short"] < df["ma_long"])
            & (df["ma_short"].notna())
            & (df["ma_long"].notna())
        )
        return df

    def _calculate_volatility_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate volatility filter."""
        df["vol_ok"] = (df["atr"] / df["close"]) >= self.config.min_vol
        return df

    def _calculate_session_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate session filter (RTH: 9:30-16:00 EST)"""
        df["hour"] = df.index.hour
        df["in_session"] = (df["hour"] >= 9) & (df["hour"] <= 16)
        return df

    def calculate_custom_indicator(
        self, df: pd.DataFrame, indicator_name: str, **kwargs
    ) -> pd.DataFrame:
        """Calculate a custom technical indicator."""
        if indicator_name == "bollinger_bands":
            return self._calculate_bollinger_bands(df, **kwargs)
        elif indicator_name == "macd":
            return self._calculate_macd(df, **kwargs)
        elif indicator_name == "stochastic":
            return self._calculate_stochastic(df, **kwargs)
        else:
            raise ValueError(f"Unknown indicator: {indicator_name}")

    def _calculate_bollinger_bands(
        self, df: pd.DataFrame, period: int = 20, std_dev: float = 2.0
    ) -> pd.DataFrame:
        """Calculate Bollinger Bands."""
        df["bb_middle"] = df["close"].rolling(window=period).mean()
        bb_std = df["close"].rolling(window=period).std()
        df["bb_upper"] = df["bb_middle"] + (bb_std * std_dev)
        df["bb_lower"] = df["bb_middle"] - (bb_std * std_dev)
        df["bb_width"] = (df["bb_upper"] - df["bb_lower"]) / df["bb_middle"]
        return df

    def _calculate_macd(
        self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9
    ) -> pd.DataFrame:
        """Calculate MACD."""
        df["macd_fast"] = df["close"].ewm(span=fast).mean()
        df["macd_slow"] = df["close"].ewm(span=slow).mean()
        df["macd"] = df["macd_fast"] - df["macd_slow"]
        df["macd_signal"] = df["macd"].ewm(span=signal).mean()
        df["macd_histogram"] = df["macd"] - df["macd_signal"]
        return df

    def _calculate_stochastic(
        self, df: pd.DataFrame, k_period: int = 14, d_period: int = 3
    ) -> pd.DataFrame:
        """Calculate Stochastic Oscillator."""
        lowest_low = df["low"].rolling(window=k_period).min()
        highest_high = df["high"].rolling(window=k_period).max()
        df["stoch_k"] = 100 * (df["close"] - lowest_low) / (highest_high - lowest_low)
        df["stoch_d"] = df["stoch_k"].rolling(window=d_period).mean()
        return df

    def get_indicator_values(
        self, df: pd.DataFrame, indicator: str, row_idx: int
    ) -> Optional[float]:
        """Get indicator value for a specific row."""
        if indicator not in df.columns:
            return None

        if row_idx >= len(df):
            return None

        return float(df.iloc[row_idx][indicator])

    def get_indicator_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary of all calculated indicators."""
        indicator_columns = [
            "ma_short",
            "ma_long",
            "rsi",
            "atr",
            "trend_up",
            "trend_dn",
            "vol_ok",
            "in_session",
        ]

        summary = {}
        for col in indicator_columns:
            if col in df.columns:
                if col in ["trend_up", "trend_dn", "vol_ok", "in_session"]:
                    # Boolean columns
                    summary[col] = {
                        "true_count": int(df[col].sum()),
                        "false_count": int((~df[col]).sum()),
                        "true_percentage": float(df[col].mean() * 100),
                    }
                else:
                    # Numeric columns
                    summary[col] = {
                        "min": float(df[col].min()),
                        "max": float(df[col].max()),
                        "mean": float(df[col].mean()),
                        "std": float(df[col].std()),
                        "valid_count": int(df[col].count()),
                    }

        return summary

    def validate_indicators(self, df: pd.DataFrame) -> bool:
        """Validate that all required indicators are present and valid."""
        required_indicators = [
            "ma_short",
            "ma_long",
            "rsi",
            "atr",
            "trend_up",
            "trend_dn",
            "vol_ok",
            "in_session",
        ]

        for indicator in required_indicators:
            if indicator not in df.columns:
                print(f"Error: Missing required indicator: {indicator}")
                return False

            if df[indicator].isna().all():
                print(f"Error: All values are NaN for indicator: {indicator}")
                return False

        # Validate RSI range
        if "rsi" in df.columns:
            rsi_values = df["rsi"].dropna()
            if len(rsi_values) > 0:
                if rsi_values.min() < 0 or rsi_values.max() > 100:
                    print(
                        f"Error: RSI values out of range: min={rsi_values.min()}, max={rsi_values.max()}"
                    )
                    return False

        # Validate ATR values
        if "atr" in df.columns:
            atr_values = df["atr"].dropna()
            if len(atr_values) > 0:
                if atr_values.min() < 0:
                    print(f"Error: ATR values negative: min={atr_values.min()}")
                    return False

        print("All indicators validated successfully")
        return True

    def get_trend_strength(self, df: pd.DataFrame, row_idx: int) -> Dict[str, Any]:
        """Calculate trend strength for a specific row."""
        if row_idx >= len(df):
            return {"error": "Invalid row index"}

        row = df.iloc[row_idx]

        # Calculate trend strength based on MA separation
        ma_separation = abs(row["ma_short"] - row["ma_long"]) / row["close"] * 100

        # Determine trend direction and strength
        if row["trend_up"]:
            trend_direction = "up"
            trend_strength = min(ma_separation / 5.0, 1.0)  # Normalize to 0-1
        elif row["trend_dn"]:
            trend_direction = "down"
            trend_strength = min(ma_separation / 5.0, 1.0)  # Normalize to 0-1
        else:
            trend_direction = "sideways"
            trend_strength = 0.0

        return {
            "trend_direction": trend_direction,
            "trend_strength": trend_strength,
            "ma_separation_pct": ma_separation,
            "rsi": float(row["rsi"]),
            "atr": float(row["atr"]),
            "volatility_ok": bool(row["vol_ok"]),
        }


# Factory function for dependency injection
def create_technical_indicators_engine(
    config: IndicatorConfig,
) -> TechnicalIndicatorsEngine:
    """Factory function to create technical indicators engine with configuration."""
    return TechnicalIndicatorsEngine(config)


# Export for DI
__all__ = [
    "TechnicalIndicatorsEngine",
    "IndicatorConfig",
    "create_technical_indicators_engine",
]
