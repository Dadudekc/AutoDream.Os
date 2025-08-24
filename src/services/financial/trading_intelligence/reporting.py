import json
import logging
from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, List

from .models import TradingSignal, StrategyType

logger = logging.getLogger(__name__)


def get_strategy_recommendations(self, symbol: str) -> Dict[str, Any]:
    """Get trading strategy recommendations for a symbol"""
    try:
        recommendations = {
            "symbol": symbol,
            "market_conditions": asdict(self.market_conditions) if self.market_conditions else None,
            "active_signals": [],
            "strategy_performance": {},
            "recommendations": [],
        }
        symbol_signals = [s for s in self.active_signals if s.symbol == symbol]
        recommendations["active_signals"] = [asdict(s) for s in symbol_signals]
        for strategy_type, performance in self.performance_metrics.items():
            recommendations["strategy_performance"][strategy_type.value] = asdict(performance)
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
        signals_data = [asdict(signal) for signal in self.active_signals]
        with open(self.signals_file, "w") as f:
            json.dump(signals_data, f, indent=2, default=str)
        performance_data = {
            strategy.value: asdict(metrics) for strategy, metrics in self.performance_metrics.items()
        }
        with open(self.performance_file, "w") as f:
            json.dump(performance_data, f, indent=2, default=str)
        logger.info("Trading intelligence data saved successfully")
    except Exception as e:
        logger.error(f"Error saving trading intelligence data: {e}")


def load_data(self):
    """Load trading intelligence data"""
    try:
        if self.signals_file.exists():
            with open(self.signals_file, "r") as f:
                signals_data = json.load(f)
            for signal_data in signals_data:
                if "timestamp" in signal_data:
                    signal_data["timestamp"] = datetime.fromisoformat(signal_data["timestamp"])
                if "expiration" in signal_data and signal_data["expiration"]:
                    signal_data["expiration"] = datetime.fromisoformat(signal_data["expiration"])
                signal = TradingSignal(**signal_data)
                self.active_signals.append(signal)
            logger.info(f"Loaded {len(self.active_signals)} trading signals")
        if self.performance_file.exists():
            with open(self.performance_file, "r") as f:
                performance_data = json.load(f)
            for strategy_name, metrics_data in performance_data.items():
                if "last_updated" in metrics_data and metrics_data["last_updated"]:
                    metrics_data["last_updated"] = datetime.fromisoformat(metrics_data["last_updated"])
                strategy_type = StrategyType(strategy_name)
                if strategy_type in self.performance_metrics:
                    for key, value in metrics_data.items():
                        if hasattr(self.performance_metrics[strategy_type], key):
                            setattr(self.performance_metrics[strategy_type], key, value)
            logger.info("Loaded strategy performance metrics")
    except Exception as e:
        logger.error(f"Error loading trading intelligence data: {e}")
