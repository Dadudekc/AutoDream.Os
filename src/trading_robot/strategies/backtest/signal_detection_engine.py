#!/usr/bin/env python3
"""
Trading Backtest Signal Detection Engine
=======================================

Signal detection engine for trading strategy backtesting.
Handles entry/exit signal logic and signal validation.
V2 COMPLIANT: Focused signal detection under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR SIGNAL DETECTION
@license MIT
"""

import pandas as pd
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TradeSide(Enum):
    """Trade side enumeration."""

    LONG = "long"
    SHORT = "short"


@dataclass
class SignalConfig:
    """Configuration for signal detection."""

    rsi_ob: int = 70
    rsi_os: int = 30
    atr_mult: float = 2.0
    rr_ratio: float = 2.0
    cooldown_bars: int = 5
    use_rth: bool = True
    vol_gate: bool = True
    min_vol: float = 0.004


class SignalDetectionEngine:
    """Signal detection engine for trading backtesting."""

    def __init__(self, config: SignalConfig):
        """Initialize signal detection engine with configuration."""
        self.config = config
        self.last_exit_bar = -999
        self.current_bar = 0

    def check_entry_signals(self, row: pd.Series) -> Tuple[bool, bool]:
        """Check for entry signals (long, short)"""
        # Check cooldown period
        cooldown_ok = (self.last_exit_bar == -999) or (
            self.current_bar - self.last_exit_bar >= self.config.cooldown_bars
        )

        if not cooldown_ok:
            return False, False

        # Check long signal
        long_signal = self._check_long_signal(row)

        # Check short signal
        short_signal = self._check_short_signal(row)

        return long_signal, short_signal

    def _check_long_signal(self, row: pd.Series) -> bool:
        """Check for long entry signal."""
        try:
            # Event-based long signal conditions
            long_sig = (
                row["trend_up"]
                and (row["close"] > row["ma_short"])
                and (row["rsi"] < self.config.rsi_ob)
                and (row["rsi"] > row["rsi"])  # RSI crossover up (simplified)
                and row["in_session"]
                and row["vol_ok"]
            )

            return bool(long_sig)
        except (KeyError, TypeError):
            return False

    def _check_short_signal(self, row: pd.Series) -> bool:
        """Check for short entry signal."""
        try:
            # Event-based short signal conditions
            short_sig = (
                row["trend_dn"]
                and (row["close"] < row["ma_short"])
                and (row["rsi"] > self.config.rsi_os)
                and (row["rsi"] < row["rsi"])  # RSI crossover down (simplified)
                and row["in_session"]
                and row["vol_ok"]
            )

            return bool(short_sig)
        except (KeyError, TypeError):
            return False

    def check_exit_signals(
        self,
        row: pd.Series,
        position_side: TradeSide,
        entry_price: float,
        stop_price: float,
        target_price: float,
    ) -> Optional[str]:
        """Check for exit signals."""
        try:
            current_price = row["close"]

            if position_side == TradeSide.LONG:
                # Long position exit conditions
                if current_price <= stop_price:
                    return "stop_loss"
                elif current_price >= target_price:
                    return "take_profit"
                elif row["rsi"] > self.config.rsi_ob:
                    return "rsi_overbought"
                elif not row["trend_up"]:
                    return "trend_reversal"

            elif position_side == TradeSide.SHORT:
                # Short position exit conditions
                if current_price >= stop_price:
                    return "stop_loss"
                elif current_price <= target_price:
                    return "take_profit"
                elif row["rsi"] < self.config.rsi_os:
                    return "rsi_oversold"
                elif not row["trend_dn"]:
                    return "trend_reversal"

            return None

        except (KeyError, TypeError):
            return None

    def calculate_stop_distance(self, row: pd.Series) -> float:
        """Calculate stop distance based on ATR."""
        try:
            atr_value = row["atr"]
            stop_distance = atr_value * self.config.atr_mult
            return float(stop_distance)
        except (KeyError, TypeError):
            return 0.0

    def calculate_target_price(
        self, entry_price: float, stop_distance: float, side: TradeSide
    ) -> float:
        """Calculate target price based on risk-reward ratio."""
        if side == TradeSide.LONG:
            return entry_price + (stop_distance * self.config.rr_ratio)
        else:
            return entry_price - (stop_distance * self.config.rr_ratio)

    def calculate_stop_price(
        self, entry_price: float, stop_distance: float, side: TradeSide
    ) -> float:
        """Calculate stop price based on entry and stop distance."""
        if side == TradeSide.LONG:
            return entry_price - stop_distance
        else:
            return entry_price + stop_distance

    def validate_signal_conditions(self, row: pd.Series) -> Dict[str, Any]:
        """Validate all signal conditions and return detailed status."""
        try:
            conditions = {
                "trend_up": bool(row.get("trend_up", False)),
                "trend_dn": bool(row.get("trend_dn", False)),
                "price_above_ma_short": bool(
                    row.get("close", 0) > row.get("ma_short", 0)
                ),
                "price_below_ma_short": bool(
                    row.get("close", 0) < row.get("ma_short", 0)
                ),
                "rsi_ok_long": bool(row.get("rsi", 50) < self.config.rsi_ob),
                "rsi_ok_short": bool(row.get("rsi", 50) > self.config.rsi_os),
                "in_session": bool(row.get("in_session", True)),
                "vol_ok": bool(row.get("vol_ok", True)),
                "cooldown_ok": (
                    (self.last_exit_bar == -999)
                    or (
                        self.current_bar - self.last_exit_bar
                        >= self.config.cooldown_bars
                    )
                ),
            }

            # Calculate signal scores
            long_score = sum(
                [
                    conditions["trend_up"],
                    conditions["price_above_ma_short"],
                    conditions["rsi_ok_long"],
                    conditions["in_session"],
                    conditions["vol_ok"],
                    conditions["cooldown_ok"],
                ]
            )

            short_score = sum(
                [
                    conditions["trend_dn"],
                    conditions["price_below_ma_short"],
                    conditions["rsi_ok_short"],
                    conditions["in_session"],
                    conditions["vol_ok"],
                    conditions["cooldown_ok"],
                ]
            )

            conditions["long_signal_score"] = long_score
            conditions["short_signal_score"] = short_score
            conditions["max_possible_score"] = 6

            return conditions

        except Exception as e:
            return {"error": str(e)}

    def get_signal_strength(self, row: pd.Series, side: TradeSide) -> float:
        """Calculate signal strength (0-1) for a given side."""
        try:
            if side == TradeSide.LONG:
                # Long signal strength factors
                trend_strength = 1.0 if row.get("trend_up", False) else 0.0
                price_strength = (
                    1.0 if row.get("close", 0) > row.get("ma_short", 0) else 0.0
                )
                rsi_strength = max(
                    0, (self.config.rsi_ob - row.get("rsi", 50)) / self.config.rsi_ob
                )
                session_strength = 1.0 if row.get("in_session", True) else 0.0
                vol_strength = 1.0 if row.get("vol_ok", True) else 0.0

                # Weighted average
                strength = (
                    trend_strength * 0.3
                    + price_strength * 0.2
                    + rsi_strength * 0.2
                    + session_strength * 0.15
                    + vol_strength * 0.15
                )

            else:  # SHORT
                # Short signal strength factors
                trend_strength = 1.0 if row.get("trend_dn", False) else 0.0
                price_strength = (
                    1.0 if row.get("close", 0) < row.get("ma_short", 0) else 0.0
                )
                rsi_strength = max(
                    0,
                    (row.get("rsi", 50) - self.config.rsi_os)
                    / (100 - self.config.rsi_os),
                )
                session_strength = 1.0 if row.get("in_session", True) else 0.0
                vol_strength = 1.0 if row.get("vol_ok", True) else 0.0

                # Weighted average
                strength = (
                    trend_strength * 0.3
                    + price_strength * 0.2
                    + rsi_strength * 0.2
                    + session_strength * 0.15
                    + vol_strength * 0.15
                )

            return min(max(strength, 0.0), 1.0)

        except Exception:
            return 0.0

    def update_bar_index(self, bar_index: int):
        """Update current bar index for cooldown tracking."""
        self.current_bar = bar_index

    def record_exit(self, bar_index: int):
        """Record exit for cooldown tracking."""
        self.last_exit_bar = bar_index

    def reset_cooldown(self):
        """Reset cooldown tracking."""
        self.last_exit_bar = -999

    def get_cooldown_status(self) -> Dict[str, Any]:
        """Get current cooldown status."""
        bars_since_exit = (
            self.current_bar - self.last_exit_bar if self.last_exit_bar != -999 else 0
        )
        cooldown_remaining = max(0, self.config.cooldown_bars - bars_since_exit)

        return {
            "last_exit_bar": self.last_exit_bar,
            "current_bar": self.current_bar,
            "bars_since_exit": bars_since_exit,
            "cooldown_remaining": cooldown_remaining,
            "cooldown_ok": cooldown_remaining == 0,
        }


# Factory function for dependency injection
def create_signal_detection_engine(config: SignalConfig) -> SignalDetectionEngine:
    """Factory function to create signal detection engine with configuration."""
    return SignalDetectionEngine(config)


# Export for DI
__all__ = [
    "SignalDetectionEngine",
    "SignalConfig",
    "TradeSide",
    "create_signal_detection_engine",
]
