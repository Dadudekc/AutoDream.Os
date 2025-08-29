"""Orchestrates gaming alert evaluation and delivery."""
from __future__ import annotations

import time
from typing import Dict

from .rules import DEFAULT_RULES, AlertRule
from .state import AlertState, GamingAlert
from .channels import AlertChannel, LoggerChannel


class GamingAlertManager:
    """Coordinates rule evaluation, state tracking and delivery."""

    def __init__(
        self,
        rules: Dict[str, AlertRule] | None = None,
        state: AlertState | None = None,
        channel: AlertChannel | None = None,
    ) -> None:
        self.rules = rules or DEFAULT_RULES
        self.state = state or AlertState()
        self.channel = channel or LoggerChannel()

    def check_metrics(self, system_id: str, metrics: Dict[str, float]):
        """Evaluate metrics against rules and dispatch alerts."""
        for metric, value in metrics.items():
            rule = self.rules.get(metric)
            if not rule:
                continue
            result = rule.evaluate(value)
            if not result:
                continue
            severity, threshold = result
            alert_id = f"{metric}_{int(time.time())}"
            alert = GamingAlert(
                alert_id=alert_id,
                metric=metric,
                severity=severity,
                value=value,
                threshold=threshold,
                system_id=system_id,
            )
            self.state.add(alert)
            self.channel.send(alert)
        return list(self.state.active.values())
