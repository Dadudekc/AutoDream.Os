"""Strategy logic for portfolio performance calculations."""

from __future__ import annotations

import logging
from typing import Dict, List

from .models import PerformanceSnapshot

logger = logging.getLogger(__name__)


class PerformanceCalculator:
    """Calculate portfolio performance metrics."""

    def calculate_daily_return(
        self, history: List[PerformanceSnapshot], current_value: float
    ) -> float:
        """Compute the daily return based on the last snapshot."""

        try:
            if not history:
                return 0.0
            prev = history[-1].total_value
            return (current_value - prev) / prev if prev else 0.0
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Error calculating daily return: %s", exc)
            return 0.0

    def calculate_total_return(
        self, history: List[PerformanceSnapshot], current_value: float
    ) -> float:
        """Compute total return from the first snapshot."""

        try:
            if not history:
                return 0.0
            initial = history[0].total_value
            return (current_value - initial) / initial if initial else 0.0
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Error calculating total return: %s", exc)
            return 0.0

    def calculate_metrics(
        self, weights: Dict[str, float], prices: Dict[str, float]
    ) -> Dict[str, float]:
        """Return simple aggregate metrics for a portfolio."""

        try:
            return {
                "total_weight": sum(weights.values()),
                "num_positions": len(weights),
                "largest_price": max(prices.values()) if prices else 0.0,
            }
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Error calculating metrics: %s", exc)
            return {}
