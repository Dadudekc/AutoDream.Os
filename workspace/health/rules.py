"""Rule evaluation for workspace health monitoring."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List


Comparator = Callable[[float, float], bool]


@dataclass
class Rule:
    """Defines a threshold rule for a metric."""
    metric: str
    threshold: float
    comparator: Comparator
    message: str


class RuleEvaluator:
    """Evaluate rules against collected metrics."""

    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def evaluate(self, metrics: Dict[str, float]) -> List[str]:
        """Return alert messages for rules that trigger."""
        alerts: List[str] = []
        for rule in self.rules:
            value = metrics.get(rule.metric)
            if value is not None and rule.comparator(value, rule.threshold):
                alerts.append(rule.message.format(value=value, threshold=rule.threshold))
        return alerts
