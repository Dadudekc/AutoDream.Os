"""High level workspace health monitor tying metrics, rules and alerts."""
from __future__ import annotations

from typing import List

from src.core.metrics import MetricsCollector
from .rules import RuleEvaluator, Rule
from .alerts import AlertManager


class WorkspaceHealthMonitor:
    """Orchestrates metric recording, rule evaluation and alerting."""

    def __init__(self, rules: List[Rule]):
        self.metrics = MetricsCollector()
        self.alerts = AlertManager()
        self.rules = RuleEvaluator(rules)

    def record_metric(self, name: str, value: float) -> None:
        """Proxy to :class:`MetricsCollector.record`."""
        self.metrics.record(name, value)

    def run_checks(self) -> List[str]:
        """Evaluate rules and dispatch any resulting alerts."""
        triggered = self.rules.evaluate(self.metrics.all())
        for message in triggered:
            self.alerts.notify(message)
        return triggered
