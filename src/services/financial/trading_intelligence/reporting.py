"""Reporting helpers for the trading intelligence service."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List

from .models import StrategyType, StrategyPerformance, TradingSignal

logger = logging.getLogger(__name__)


def log_signal(signal: TradingSignal) -> None:
    """Log a trading signal for audit purposes."""

    logger.info("Signal generated: %s", signal)


def get_strategy_recommendations(
    metrics: Dict[StrategyType, StrategyPerformance]
) -> List[str]:
    """Generate simple strategy recommendations.

    Strategies with a win rate above 60% are recommended for increased
    allocation while those below 40% are flagged for review.
    """

    recommendations: List[str] = []
    for strategy, performance in metrics.items():
        if performance.win_rate > 0.6:
            recommendations.append(f"{strategy.value}: consider increasing allocation")
        elif performance.win_rate < 0.4:
            recommendations.append(f"{strategy.value}: review or disable")
    return recommendations


def save_data(path: Path, data: Dict) -> None:
    """Persist *data* as JSON at *path*."""

    logger.info("Saving trading data to %s", path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, default=str, indent=2)


def load_data(path: Path) -> Dict:
    """Load JSON data from *path* if it exists, otherwise return an empty dict."""

    if not path.exists():
        logger.warning("Data file %s not found", path)
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
