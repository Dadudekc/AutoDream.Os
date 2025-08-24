"""Agent Health Alerting Manager Module

Single Responsibility: Manage health alerts, notifications, and escalation.

This manager delegates alert generation, notification dispatch, and
configuration handling to dedicated modules, providing a clear separation of
concerns and simplifying the alerting workflow.
"""

from __future__ import annotations

import logging
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Optional, Set, Callable, Any, List

from .logging_utils import logger
from .models import (
    AlertRule,
    HealthAlert,
    AlertSeverity,
    AlertStatus,
    NotificationChannel,
    NotificationConfig,
    EscalationPolicy,
    EscalationLevel,
)
from .alert_generation import (
    generate_alert,
    should_suppress_alert,
    find_applicable_rule,
)
from .channel_dispatch import send_alert_notifications
from .escalation import check_escalations
from .configuration import (
    load_default_rules,
    load_default_notifications,
    load_default_escalation,
)


class HealthAlertingManager:
    """Health alerting and notification management."""

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        """Initialize the alerting manager with default configurations."""

        self.config = config or {}

        # Core alerting state
        self.alerts: Dict[str, HealthAlert] = {}
        self.alert_rules: Dict[str, AlertRule] = load_default_rules()
        self.notification_configs: Dict[NotificationChannel, NotificationConfig] = (
            load_default_notifications()
        )
        self.escalation_policies: Dict[EscalationLevel, EscalationPolicy] = (
            load_default_escalation()
        )

        # Callback subscriptions
        self.alert_callbacks: Set[Callable[[Dict[str, HealthAlert]], None]] = set()

        # Escalation loop management
        self.escalation_thread: Optional[threading.Thread] = None
        self.escalation_active = False

        # Configuration values
        self.alert_retention_days = self.config.get("alert_retention_days", 30)
        self.auto_resolve_threshold = self.config.get("auto_resolve_threshold", 24)
        self.escalation_check_interval = self.config.get(
            "escalation_check_interval", 60
        )

        logger.info("HealthAlertingManager initialized with default configurations")

    # ------------------------------------------------------------------
    # Lifecycle management
    # ------------------------------------------------------------------
    def start(self) -> None:
        """Start background escalation checks."""

        if self.escalation_active:
            logger.warning("Alerting manager already active")
            return

        self.escalation_active = True
        self.escalation_thread = threading.Thread(
            target=self._escalation_loop, daemon=True
        )
        self.escalation_thread.start()
        logger.info("Health alerting manager started")

    def stop(self) -> None:
        """Stop background escalation checks."""

        self.escalation_active = False
        if self.escalation_thread:
            self.escalation_thread.join(timeout=5)
        logger.info("Health alerting manager stopped")

    def _escalation_loop(self) -> None:
        """Main escalation monitoring loop."""

        while self.escalation_active:
            try:
                check_escalations(
                    self.alerts, self.escalation_policies, self.notification_configs
                )
                self._check_auto_resolve()
                self._cleanup_expired_alerts()
                time.sleep(self.escalation_check_interval)
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.error(f"Error in escalation loop: {exc}")
                time.sleep(10)

    # ------------------------------------------------------------------
    # Core alert operations
    # ------------------------------------------------------------------
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
        """Create and dispatch a new health alert."""

        try:
            if should_suppress_alert(
                self.alerts, agent_id, metric_type, severity
            ):
                logger.debug(f"Suppressing alert due to cooldown: {message}")
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
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error(f"Error creating health alert: {exc}")
            return ""

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert."""

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
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error(f"Error acknowledging alert {alert_id}: {exc}")
            return False

    def resolve_alert(self, alert_id: str, resolved_by: str) -> bool:
        """Resolve an alert."""

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
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error(f"Error resolving alert {alert_id}: {exc}")
            return False

    # ------------------------------------------------------------------
    # Retrieval helpers
    # ------------------------------------------------------------------
    def get_alert(self, alert_id: str) -> Optional[HealthAlert]:
        """Get a specific alert by ID."""

        return self.alerts.get(alert_id)

    def get_alerts(
        self,
        status: Optional[AlertStatus] = None,
        severity: Optional[AlertSeverity] = None,
        agent_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[HealthAlert]:
        """Get alerts with optional filtering."""

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
        """Get a summary of all alerts."""

        total_alerts = len(self.alerts)
        active_alerts = len(
            [a for a in self.alerts.values() if a.status == AlertStatus.ACTIVE]
        )
        acknowledged_alerts = len(
            [a for a in self.alerts.values() if a.status == AlertStatus.ACKNOWLEDGED]
        )
        resolved_alerts = len(
            [a for a in self.alerts.values() if a.status == AlertStatus.RESOLVED]
        )

        severity_counts: Dict[str, int] = {}
        for alert in self.alerts.values():
            sev = alert.severity.value
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        agent_counts: Dict[str, int] = {}
        for alert in self.alerts.values():
            agent = alert.agent_id
            agent_counts[agent] = agent_counts.get(agent, 0) + 1

        return {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "acknowledged_alerts": acknowledged_alerts,
            "resolved_alerts": resolved_alerts,
            "alerts_by_severity": severity_counts,
            "alerts_by_agent": agent_counts,
            "last_update": datetime.now().isoformat(),
        }

    # ------------------------------------------------------------------
    # Configuration management helpers
    # ------------------------------------------------------------------
    def add_alert_rule(self, rule: AlertRule) -> None:
        """Add a new alert rule."""

        self.alert_rules[rule.rule_id] = rule
        logger.info(f"Alert rule added: {rule.rule_id}")

    def update_alert_rule(self, rule_id: str, updates: Dict[str, Any]) -> None:
        """Update an existing alert rule."""

        if rule_id in self.alert_rules:
            rule = self.alert_rules[rule_id]
            for key, value in updates.items():
                if hasattr(rule, key):
                    setattr(rule, key, value)
            rule.updated_at = datetime.now()
            logger.info(f"Alert rule updated: {rule_id}")

    def remove_alert_rule(self, rule_id: str) -> None:
        """Remove an alert rule."""

        if rule_id in self.alert_rules:
            del self.alert_rules[rule_id]
            logger.info(f"Alert rule removed: {rule_id}")

    # ------------------------------------------------------------------
    # Subscription helpers
    # ------------------------------------------------------------------
    def subscribe_to_alert_updates(self, callback: Callable[[Dict[str, HealthAlert]], None]) -> None:
        """Subscribe to alert update notifications."""

        self.alert_callbacks.add(callback)

    def unsubscribe_from_alert_updates(self, callback: Callable[[Dict[str, HealthAlert]], None]) -> None:
        """Unsubscribe from alert update notifications."""

        self.alert_callbacks.discard(callback)

    def _notify_alert_updates(self) -> None:
        """Notify subscribers of alert updates."""

        for callback in self.alert_callbacks:
            try:
                callback(self.alerts)
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.error(f"Error in alert update callback: {exc}")

    # ------------------------------------------------------------------
    # Internal maintenance helpers
    # ------------------------------------------------------------------
    def _check_auto_resolve(self) -> None:
        """Check for alerts that can be auto-resolved."""

        current_time = datetime.now()
        threshold = timedelta(hours=self.auto_resolve_threshold)
        for alert in list(self.alerts.values()):
            if alert.status != AlertStatus.ACTIVE:
                continue
            if current_time - alert.timestamp >= threshold:
                self._auto_resolve_alert(alert)

    def _auto_resolve_alert(self, alert: HealthAlert) -> None:
        """Automatically resolve an alert."""

        try:
            alert.status = AlertStatus.RESOLVED
            alert.resolved_at = datetime.now()
            alert.resolved_by = "system"
            alert.metadata["auto_resolved"] = True
            alert.metadata["auto_resolved_at"] = datetime.now().isoformat()
            logger.info(
                f"Alert {alert.alert_id} auto-resolved after {self.auto_resolve_threshold} hours"
            )
            self._notify_alert_updates()
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error(f"Error auto-resolving alert {alert.alert_id}: {exc}")

    def _cleanup_expired_alerts(self) -> None:
        """Clean up expired alerts."""

        current_time = datetime.now()
        retention = timedelta(days=self.alert_retention_days)
        expired = []
        for alert_id, alert in self.alerts.items():
            if alert.status == AlertStatus.RESOLVED and alert.resolved_at:
                if current_time - alert.resolved_at >= retention:
                    expired.append(alert_id)
        for alert_id in expired:
            del self.alerts[alert_id]
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired alerts")

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------
    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality."""

        try:
            logger.info("Running HealthAlertingManager smoke test...")

            assert len(self.alert_rules) > 0
            assert len(self.notification_configs) > 0
            assert len(self.escalation_policies) > 0

            alert_id = self.create_alert(
                "test_agent",
                AlertSeverity.WARNING,
                "Test alert message",
                "cpu_usage",
                90.0,
                85.0,
            )
            assert alert_id != "" and alert_id in self.alerts

            alert = self.get_alert(alert_id)
            assert alert is not None and alert.agent_id == "test_agent"

            success = self.acknowledge_alert(alert_id, "test_user")
            assert success and self.alerts[alert_id].status == AlertStatus.ACKNOWLEDGED

            success = self.resolve_alert(alert_id, "test_user")
            assert success and self.alerts[alert_id].status == AlertStatus.RESOLVED

            summary = self.get_alerts_summary()
            assert "total_alerts" in summary and "active_alerts" in summary

            if alert_id in self.alerts:
                del self.alerts[alert_id]

            logger.info("✅ HealthAlertingManager smoke test PASSED")
            return True
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error(f"❌ HealthAlertingManager smoke test FAILED: {exc}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return False

    # ------------------------------------------------------------------
    # Shutdown helper
    # ------------------------------------------------------------------
    def shutdown(self) -> None:
        """Shutdown the alerting manager."""

        self.stop()
        logger.info("HealthAlertingManager shutdown complete")


def main() -> None:  # pragma: no cover - CLI helper
    """CLI testing function."""

    import argparse

    parser = argparse.ArgumentParser(description="Health Alerting Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")

    args = parser.parse_args()

    if args.test:
        manager = HealthAlertingManager()
        success = manager.run_smoke_test()
        manager.shutdown()
        raise SystemExit(0 if success else 1)
    parser.print_help()


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()

