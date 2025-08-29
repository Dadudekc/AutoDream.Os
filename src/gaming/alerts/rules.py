"""Alert rule definitions for the gaming alert system."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple

from src.core.health_models import AlertSeverity

Comparator = Callable[[float, float], bool]


@dataclass
class AlertRule:
    """Rule used to evaluate a metric against severity thresholds."""

    metric: str
    thresholds: Dict[AlertSeverity, float]
    comparator: Comparator

    def evaluate(self, value: float) -> Optional[Tuple[AlertSeverity, float]]:
        """Return the severity and threshold if the rule triggers."""
        for severity in (
            AlertSeverity.CRITICAL,
            AlertSeverity.ERROR,
            AlertSeverity.WARNING,
        ):
            threshold = self.thresholds.get(severity)
            if threshold is not None and self.comparator(value, threshold):
                return severity, threshold
        return None


def lt(a: float, b: float) -> bool:
    return a < b


def gt(a: float, b: float) -> bool:
    return a > b


DEFAULT_RULES: Dict[str, AlertRule] = {
    "frame_rate": AlertRule(
        "frame_rate",
        {
            AlertSeverity.WARNING: 30.0,
            AlertSeverity.ERROR: 15.0,
            AlertSeverity.CRITICAL: 5.0,
        },
        lt,
    ),
    "response_time": AlertRule(
        "response_time",
        {
            AlertSeverity.WARNING: 100.0,
            AlertSeverity.ERROR: 200.0,
            AlertSeverity.CRITICAL: 500.0,
        },
        gt,
    ),
    "memory_usage": AlertRule(
        "memory_usage",
        {
            AlertSeverity.WARNING: 2048.0,
            AlertSeverity.ERROR: 4096.0,
            AlertSeverity.CRITICAL: 8192.0,
        },
        gt,
    ),
    "system_health": AlertRule(
        "system_health",
        {
            AlertSeverity.WARNING: 80.0,
            AlertSeverity.ERROR: 60.0,
            AlertSeverity.CRITICAL: 40.0,
        },
        lt,
    ),
}
