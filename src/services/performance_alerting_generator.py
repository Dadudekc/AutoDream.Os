"""Alert generation utilities for the performance alerting system."""

import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .performance_monitor import AlertCondition, PerformanceAlert
from .performance_monitor import AlertSeverity
from .performance_alerting_config import AlertRule


@dataclass
class AlertManager:
    """Simple in-memory tracker for alerts and channels."""

    history: List[PerformanceAlert] = field(default_factory=list)
    channels: List[object] = field(default_factory=list)

    def record_alert(self, alert: PerformanceAlert) -> None:
        self.history.append(alert)

    def register_channel(self, channel: object) -> None:
        if channel not in self.channels:
            self.channels.append(channel)

    def get_alert_history(self, limit: int = 100) -> List[PerformanceAlert]:
        return self.history[-limit:]

    def get_active_channels(self) -> List[object]:
        return [c for c in self.channels if getattr(c, "enabled", False)]


class AlertGenerator:
    """Evaluate metrics against rules and create alerts."""

    def _compare(self, condition: AlertCondition, value: float, threshold: float) -> bool:
        if condition == AlertCondition.GREATER_THAN:
            return value > threshold
        if condition == AlertCondition.GREATER_THAN_OR_EQUAL:
            return value >= threshold
        if condition == AlertCondition.LESS_THAN:
            return value < threshold
        if condition == AlertCondition.LESS_THAN_OR_EQUAL:
            return value <= threshold
        if condition == AlertCondition.EQUALS:
            return value == threshold
        if condition == AlertCondition.NOT_EQUALS:
            return value != threshold
        return False

    def evaluate_rule(
        self, rule: AlertRule, value: float, tags: Optional[Dict[str, str]] = None
    ) -> Optional[PerformanceAlert]:
        if not rule.enabled:
            return None
        if not self._compare(rule.condition, value, rule.threshold):
            return None
        alert_id = uuid.uuid4().hex
        message = (
            f"{rule.metric_name} is {value} which violates {rule.condition.value} {rule.threshold}"
        )
        return PerformanceAlert(
            alert_id=alert_id,
            rule_name=rule.name,
            metric_name=rule.metric_name,
            current_value=value,
            threshold=rule.threshold,
            severity=rule.severity,
            message=message,
            timestamp=time.time(),
            tags=tags or {},
        )

    def generate_alerts(
        self, rules: List[AlertRule], metrics: Dict[str, float], tags: Optional[Dict[str, str]] = None
    ) -> List[PerformanceAlert]:
        alerts: List[PerformanceAlert] = []
        for rule in rules:
            if rule.metric_name not in metrics:
                continue
            alert = self.evaluate_rule(rule, metrics[rule.metric_name], tags)
            if alert:
                alerts.append(alert)
        return alerts
