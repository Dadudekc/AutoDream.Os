"""Monitoring helpers for the performance alerting system."""

from typing import Dict, Optional

from .performance_alerting_generator import AlertGenerator, AlertManager
from .performance_alerting_config import AlertRule
from .performance_monitor import PerformanceAlert


class PerformanceAlertMonitor:
    """Evaluate metrics and route generated alerts to the manager."""

    def __init__(
        self,
        generator: Optional[AlertGenerator] = None,
        manager: Optional[AlertManager] = None,
    ) -> None:
        self.generator = generator or AlertGenerator()
        self.manager = manager or AlertManager()

    def evaluate(
        self, rule: AlertRule, value: float, tags: Optional[Dict[str, str]] = None
    ) -> Optional[PerformanceAlert]:
        """Evaluate a single rule against a metric value.

        If the rule condition is met an alert is created, recorded in the
        manager and returned to the caller.
        """

        alert = self.generator.evaluate_rule(rule, value, tags)
        if alert:
            self.manager.record_alert(alert)
        return alert
