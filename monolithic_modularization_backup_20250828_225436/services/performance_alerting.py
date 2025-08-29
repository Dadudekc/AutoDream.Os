"""Orchestrator for the performance alerting system.

This module wires together the alert configuration, generation, monitoring and
notification components.  The original monolithic implementation mixed all of
these responsibilities in a single file.  It has been refactored into focused
modules with this orchestrator providing a small public surface that mirrors the
previous API used by the tests.
"""

from typing import Dict, List, Optional

from .performance_alerting_config import AlertRule
from .performance_alerting_generator import AlertGenerator, AlertManager
from .performance_alerting_monitor import PerformanceAlertMonitor
from .performance_alerting_notifier import (
    AlertChannel,
    EmailAlertChannel,
    SlackAlertChannel,
    WebhookAlertChannel,
)
from .performance_monitor import PerformanceAlert

__all__ = [
    "AlertingSystem",
    "AlertRule",
    "EmailAlertChannel",
    "SlackAlertChannel",
    "WebhookAlertChannel",
]


class AlertingSystem:
    """Small façade coordinating alert rules and channels."""

    def __init__(self) -> None:
        self.alert_rules: List[AlertRule] = []
        self.alert_channels: List[AlertChannel] = []
        self.generator = AlertGenerator()
        self.alert_manager = AlertManager()
        self.monitor = PerformanceAlertMonitor(self.generator, self.alert_manager)

    # ------------------------------------------------------------------
    # Configuration helpers
    def add_alert_rule(self, rule: AlertRule) -> None:
        self.alert_rules.append(rule)

    def add_alert_channel(self, channel: AlertChannel) -> None:
        self.alert_channels.append(channel)
        self.alert_manager.register_channel(channel)

    # ------------------------------------------------------------------
    # Processing
    async def process_alert(self, alert: PerformanceAlert) -> List[bool]:
        """Send an alert through all configured channels."""

        self.alert_manager.record_alert(alert)
        results: List[bool] = []
        for channel in self.alert_channels:
            if channel.should_send_alert(alert):
                results.append(await channel.send_alert(alert))
            else:
                results.append(False)
        return results

    async def check_alerts(
        self, metrics: Dict[str, float], tags: Optional[Dict[str, str]] = None
    ) -> List[PerformanceAlert]:
        """Evaluate all alert rules against a metrics dictionary."""

        alerts = self.generator.generate_alerts(self.alert_rules, metrics, tags)
        for alert in alerts:
            await self.process_alert(alert)
        return alerts
