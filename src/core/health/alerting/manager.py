"""
Agent Health Alerting Manager Module

This module orchestrates health alert creation, notification dispatch,
escalation handling, and logging. Implementation details for each concern
are delegated to dedicated modules to maintain separation of concerns.
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Set, Callable
from concurrent.futures import ThreadPoolExecutor

from .alert_generation import (
    generate_alert,
    should_suppress_alert,
    find_applicable_rule,
)
from .channel_dispatch import send_alert_notifications
from .escalation import check_escalations
from .logging_utils import logger
from .models import (
    AlertSeverity,
    AlertStatus,
    NotificationChannel,
    EscalationLevel,
    AlertRule,
    HealthAlert,
    NotificationConfig,
    EscalationPolicy,
)


class HealthAlertingManager:
    """High level manager coordinating alerting subsystems."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.alerts: Dict[str, HealthAlert] = {}
        self.alert_rules: Dict[str, AlertRule] = {}
        self.notification_configs: Dict[NotificationChannel, NotificationConfig] = {}
        self.escalation_policies: Dict[EscalationLevel, EscalationPolicy] = {}
        self.alert_callbacks: Set[Callable] = set()
        self.escalation_thread: Optional[threading.Thread] = None
        self.escalation_active = False
        self.executor = ThreadPoolExecutor(max_workers=4)

        self._initialize_default_rules()
        self._initialize_default_notifications()
        self._initialize_default_escalation()

        self.alert_retention_days = self.config.get("alert_retention_days", 30)
        self.escalation_check_interval = self.config.get("escalation_check_interval", 60)

        logger.info("HealthAlertingManager initialized with default configurations")

    def _initialize_default_rules(self) -> None:
        rules = [
            AlertRule(
                rule_id="high_cpu_usage",
                name="High CPU Usage",
                description="Alert when CPU usage exceeds threshold",
                severity=AlertSeverity.WARNING,
                conditions={
                    "metric": "cpu_usage",
                    "operator": ">",
                    "threshold": 85.0,
                },
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.CONSOLE],
            ),
            AlertRule(
                rule_id="critical_response_time",
                name="Critical Response Time",
                description="Alert when response time is critically high",
                severity=AlertSeverity.CRITICAL,
                conditions={
                    "metric": "response_time",
                    "operator": ">",
                    "threshold": 5000.0,
                },
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK],
                escalation_enabled=True,
            ),
        ]
        for rule in rules:
            self.alert_rules[rule.rule_id] = rule

    def _initialize_default_notifications(self) -> None:
        configs = [
            NotificationConfig(
                channel=NotificationChannel.EMAIL,
                enabled=True,
                recipients=["admin@example.com"],
                template="Alert: {severity} - {message}",
            ),
            NotificationConfig(
                channel=NotificationChannel.CONSOLE,
                enabled=True,
                template="[{severity}] {message}",
            ),
            NotificationConfig(
                channel=NotificationChannel.LOG,
                enabled=True,
                template="Health Alert: {severity} - {message}",
            ),
        ]
        for config in configs:
            self.notification_configs[config.channel] = config

    def _initialize_default_escalation(self) -> None:
        policies = [
            EscalationPolicy(
                level=EscalationLevel.LEVEL_1,
                delay_minutes=0,
                contacts=["oncall@example.com"],
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SMS],
                auto_escalate=True,
            ),
            EscalationPolicy(
                level=EscalationLevel.LEVEL_2,
                delay_minutes=15,
                contacts=["supervisor@example.com"],
                notification_channels=[NotificationChannel.EMAIL],
                auto_escalate=True,
                require_acknowledgment=True,
            ),
        ]
        for policy in policies:
            self.escalation_policies[policy.level] = policy

    def start(self) -> None:
        if self.escalation_active:
            logger.warning("Alerting manager already active")
            return
        self.escalation_active = True
        self.escalation_thread = threading.Thread(target=self._escalation_loop, daemon=True)
        self.escalation_thread.start()
        logger.info("Health alerting manager started")

    def stop(self) -> None:
        self.escalation_active = False
        if self.escalation_thread:
            self.escalation_thread.join(timeout=5)
        self.executor.shutdown(wait=True)
        logger.info("Health alerting manager stopped")

    def _escalation_loop(self) -> None:
        while self.escalation_active:
            try:
                self._check_escalations()
                time.sleep(self.escalation_check_interval)
            except Exception as e:
                logger.error(f"Error in escalation loop: {e}")
                time.sleep(10)

    def _check_escalations(self) -> None:
        check_escalations(self.alerts, self.escalation_policies, self.notification_configs)

    def create_alert(
        self,
        agent_id: str,
        severity: AlertSeverity,
        message: str,
        metric_type: str,
        current_value: float,
        threshold: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        try:
            if should_suppress_alert(self.alerts, agent_id, metric_type, severity):
                logger.debug("Suppressing alert due to cooldown")
                return ""
            alert = generate_alert(
                agent_id,
                severity,
                message,
                metric_type,
                current_value,
                threshold,
                metadata,
            )
            self.alerts[alert.alert_id] = alert
            rule = find_applicable_rule(self.alert_rules, alert)
            if rule:
                send_alert_notifications(alert, rule, self.notification_configs)
            self._notify_alert_updates()
            logger.info(f"Health alert created: {alert.alert_id} - {message}")
            return alert.alert_id
        except Exception as e:
            logger.error(f"Error creating health alert: {e}")
            return ""

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        if alert_id not in self.alerts:
            return False
        try:
            alert = self.alerts[alert_id]
            alert.status = AlertStatus.ACKNOWLEDGED
            alert.acknowledged_by = acknowledged_by
            alert.acknowledged_at = datetime.now()
            logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
            self._notify_alert_updates()
            return True
        except Exception as e:
            logger.error(f"Error acknowledging alert {alert_id}: {e}")
            return False

    def resolve_alert(self, alert_id: str, resolved_by: str) -> bool:
        if alert_id not in self.alerts:
            return False
        try:
            alert = self.alerts[alert_id]
            alert.status = AlertStatus.RESOLVED
            alert.resolved_by = resolved_by
            alert.resolved_at = datetime.now()
            logger.info(f"Alert {alert_id} resolved by {resolved_by}")
            self._notify_alert_updates()
            return True
        except Exception as e:
            logger.error(f"Error resolving alert {alert_id}: {e}")
            return False

    def get_alert(self, alert_id: str) -> Optional[HealthAlert]:
        return self.alerts.get(alert_id)

    def get_alerts(
        self,
        status: Optional[AlertStatus] = None,
        severity: Optional[AlertSeverity] = None,
        agent_id: Optional[str] = None,
        limit: int = 100,
    ) -> Dict[str, HealthAlert]:
        alerts = list(self.alerts.values())
        if status:
            alerts = [a for a in alerts if a.status == status]
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        if agent_id:
            alerts = [a for a in alerts if a.agent_id == agent_id]
        alerts.sort(key=lambda x: x.timestamp, reverse=True)
        return alerts[:limit]

    def get_alerts_summary(self) -> Dict[str, Any]:
        total_alerts = len(self.alerts)
        active_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.ACTIVE])
        acknowledged_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.ACKNOWLEDGED])
        resolved_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.RESOLVED])
        severity_counts: Dict[str, int] = {}
        for alert in self.alerts.values():
            severity_counts[alert.severity.value] = severity_counts.get(alert.severity.value, 0) + 1
        agent_counts: Dict[str, int] = {}
        for alert in self.alerts.values():
            agent_counts[alert.agent_id] = agent_counts.get(alert.agent_id, 0) + 1
        return {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "acknowledged_alerts": acknowledged_alerts,
            "resolved_alerts": resolved_alerts,
            "alerts_by_severity": severity_counts,
            "alerts_by_agent": agent_counts,
            "last_update": datetime.now().isoformat(),
        }

    def add_alert_rule(self, rule: AlertRule) -> None:
        self.alert_rules[rule.rule_id] = rule
        logger.info(f"Alert rule added: {rule.rule_id}")

    def update_alert_rule(self, rule_id: str, updates: Dict[str, Any]) -> None:
        if rule_id in self.alert_rules:
            rule = self.alert_rules[rule_id]
            for key, value in updates.items():
                if hasattr(rule, key):
                    setattr(rule, key, value)
            rule.updated_at = datetime.now()
            logger.info(f"Alert rule updated: {rule_id}")

    def remove_alert_rule(self, rule_id: str) -> None:
        if rule_id in self.alert_rules:
            del self.alert_rules[rule_id]
            logger.info(f"Alert rule removed: {rule_id}")

    def subscribe_to_alert_updates(self, callback: Callable) -> None:
        self.alert_callbacks.add(callback)

    def unsubscribe_from_alert_updates(self, callback: Callable) -> None:
        self.alert_callbacks.discard(callback)

    def _notify_alert_updates(self) -> None:
        for callback in self.alert_callbacks:
            try:
                callback(self.alerts)
            except Exception as e:
                logger.error(f"Error in alert update callback: {e}")

    def shutdown(self) -> None:
        self.stop()
        logger.info("HealthAlertingManager shutdown complete")
