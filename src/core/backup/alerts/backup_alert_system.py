#!/usr/bin/env python3
"""
Backup Alert System - V2 Compliant Module
=======================================

Alert management and notification system for backup monitoring.
V2 COMPLIANT: Focused alert management under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..database.backup_database import BackupMonitoringDatabase
from ..models.backup_models import Alert, AlertHistory, MonitoringConfig
from ..models.backup_enums import AlertSeverity, AlertStatus, AlertType

logger = logging.getLogger(__name__)


class BackupAlertSystem:
    """Alert management and notification system."""

    def __init__(self, database: BackupMonitoringDatabase, config: MonitoringConfig):
        self.database = database
        self.config = config
        self.active_alerts: Dict[str, Alert] = {}
        self.notification_cooldowns: Dict[str, datetime] = {}
        self._load_active_alerts()

    def _load_active_alerts(self) -> None:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.backup.alerts.backup_alert_system import Backup_Alert_System

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Backup_Alert_System(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

        """Load active alerts from database."""
        alerts = self.database.get_active_alerts()
        self.active_alerts = {alert.alert_id: alert for alert in alerts}

    def create_alert(self, alert_type: AlertType, severity: AlertSeverity,
                    title: str, message: str, **kwargs) -> Optional[Alert]:
        """Create a new alert."""
        try:
            alert_id = f"{alert_type.value}_{int(time.time())}_{hash(title) % 1000}"

            # Check if similar alert already exists
            for existing_alert in self.active_alerts.values():
                if (existing_alert.alert_type == alert_type and
                    existing_alert.title == title and
                    existing_alert.status in [AlertStatus.ACTIVE, AlertStatus.ACKNOWLEDGED]):
                    logger.info(f"Similar alert already exists: {alert_id}")
                    return None

            alert = Alert(
                alert_id=alert_id,
                alert_type=alert_type,
                severity=severity,
                title=title,
                message=message,
                tags=kwargs.get('tags', {}),
                metadata=kwargs.get('metadata', {})
            )

            # Store alert
            if self.database.store_alert(alert):
                self.active_alerts[alert_id] = alert

                # Send notification
                self._send_notification(alert)

                # Store alert history
                self._store_alert_history(alert, "created", "Alert created")

                logger.info(f"Alert created: {alert_id} - {title}")
                return alert
            else:
                logger.error(f"Failed to store alert: {alert_id}")
                return None

        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return None

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert."""
        try:
            if alert_id not in self.active_alerts:
                logger.warning(f"Alert not found: {alert_id}")
                return False

            alert = self.active_alerts[alert_id]
            alert.acknowledge(acknowledged_by)

            if self.database.store_alert(alert):
                self._store_alert_history(alert, "acknowledged", f"Acknowledged by {acknowledged_by}")
                logger.info(f"Alert acknowledged: {alert_id}")
                return True
            else:
                logger.error(f"Failed to update alert: {alert_id}")
                return False

        except Exception as e:
            logger.error(f"Error acknowledging alert: {e}")
            return False

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        try:
            if alert_id not in self.active_alerts:
                logger.warning(f"Alert not found: {alert_id}")
                return False

            alert = self.active_alerts[alert_id]
            alert.resolve()

            if self.database.store_alert(alert):
                self._store_alert_history(alert, "resolved", "Alert resolved")
                # Remove from active alerts
                del self.active_alerts[alert_id]
                logger.info(f"Alert resolved: {alert_id}")
                return True
            else:
                logger.error(f"Failed to resolve alert: {alert_id}")
                return False

        except Exception as e:
            logger.error(f"Error resolving alert: {e}")
            return False

    def escalate_alert(self, alert_id: str) -> bool:
        """Escalate an alert."""
        try:
            if alert_id not in self.active_alerts:
                logger.warning(f"Alert not found: {alert_id}")
                return False

            alert = self.active_alerts[alert_id]

            # Check escalation thresholds
            severity_config = self._get_severity_config(alert.severity)
            if alert.escalation_count >= severity_config.get("threshold", 1):
                logger.info(f"Alert already at max escalation: {alert_id}")
                return True

            alert.escalate()

            if self.database.store_alert(alert):
                self._store_alert_history(alert, "escalated", f"Escalated to level {alert.escalation_count}")

                # Send escalated notification
                self._send_notification(alert, escalated=True)

                logger.info(f"Alert escalated: {alert_id}")
                return True
            else:
                logger.error(f"Failed to escalate alert: {alert_id}")
                return False

        except Exception as e:
            logger.error(f"Error escalating alert: {e}")
            return False

    def get_active_alerts(self, severity_filter: Optional[AlertSeverity] = None) -> List[Alert]:
        """Get active alerts, optionally filtered by severity."""
        alerts = list(self.active_alerts.values())

        if severity_filter:
            alerts = [alert for alert in alerts if alert.severity == severity_filter]

        return sorted(alerts, key=lambda x: x.created_at, reverse=True)

    def check_alert_escalation(self) -> None:
        """Check for alerts that need escalation."""
        try:
            current_time = datetime.now()

            for alert in list(self.active_alerts.values()):
                if alert.status == AlertStatus.ACTIVE:
                    severity_config = self._get_severity_config(alert.severity)
                    escalation_minutes = severity_config.get("escalation_minutes", 60)

                    time_since_creation = (current_time - alert.created_at).total_seconds() / 60

                    if time_since_creation >= escalation_minutes:
                        self.escalate_alert(alert.alert_id)

        except Exception as e:
            logger.error(f"Error checking alert escalation: {e}")

    def _send_notification(self, alert: Alert, escalated: bool = False) -> None:
        """Send alert notification."""
        try:
            # Check cooldown
            if self._is_on_cooldown(alert.alert_id):
                logger.debug(f"Alert notification on cooldown: {alert.alert_id}")
                return

            # Send to configured channels
            for channel in self.config.alert_channels:
                if channel == "console":
                    self._send_console_notification(alert, escalated)
                elif channel == "file":
                    self._send_file_notification(alert, escalated)
                # Add other channels as needed (discord, email, etc.)

            # Set cooldown
            self.notification_cooldowns[alert.alert_id] = datetime.now()

        except Exception as e:
            logger.error(f"Error sending notification: {e}")

    def _send_console_notification(self, alert: Alert, escalated: bool = False) -> None:
        """Send notification to console."""
        prefix = "[ESCALATED] " if escalated else "[ALERT] "
        severity_emoji = {
            AlertSeverity.CRITICAL: "🚨",
            AlertSeverity.HIGH: "⚠️",
            AlertSeverity.MEDIUM: "ℹ️",
            AlertSeverity.LOW: "📝",
            AlertSeverity.INFO: "💡"
        }.get(alert.severity, "❓")

        print(f"{severity_emoji} {prefix}{alert.title}")
        print(f"   {alert.message}")
        print(f"   Severity: {alert.severity.value.upper()}")
        print(f"   Time: {alert.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    def _send_file_notification(self, alert: Alert, escalated: bool = False) -> None:
        """Send notification to log file."""
        try:
            status = "ESCALATED" if escalated else "NEW"
            logger.warning(f"ALERT {status}: {alert.title} - {alert.message} (Severity: {alert.severity.value})")
        except Exception as e:
            logger.error(f"Error writing file notification: {e}")

    def _store_alert_history(self, alert: Alert, action: str,
                           details: Optional[str] = None) -> None:
        """Store alert history."""
        try:
            alert_history = AlertHistory(
                alert_id=alert.alert_id,
                action=action,
                details=details,
                metadata={"severity": alert.severity.value, "status": alert.status.value}
            )
            self.database.store_alert_history(alert_history)
        except Exception as e:
            logger.error(f"Error storing alert history: {e}")

    def _get_severity_config(self, severity: AlertSeverity) -> Dict[str, Any]:
        """Get severity configuration."""
        # Default configurations
        configs = {
            AlertSeverity.CRITICAL: {"threshold": 1, "escalation_minutes": 5},
            AlertSeverity.HIGH: {"threshold": 3, "escalation_minutes": 15},
            AlertSeverity.MEDIUM: {"threshold": 5, "escalation_minutes": 60},
            AlertSeverity.LOW: {"threshold": 10, "escalation_minutes": 240},
            AlertSeverity.INFO: {"threshold": 20, "escalation_minutes": 480}
        }
        return configs.get(severity, configs[AlertSeverity.MEDIUM])

    def _is_on_cooldown(self, alert_id: str) -> bool:
        """Check if alert is on notification cooldown."""
        if alert_id not in self.notification_cooldowns:
            return False

        cooldown_end = self.notification_cooldowns[alert_id] + timedelta(
            minutes=self.config.notification_cooldown_minutes
        )

        return datetime.now() < cooldown_end

    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics."""
        try:
            stats = {
                "total_active": len(self.active_alerts),
                "by_severity": {},
                "by_type": {},
                "recent_escalations": 0
            }

            for alert in self.active_alerts.values():
                # Count by severity
                severity = alert.severity.value
                stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1

                # Count by type
                alert_type = alert.alert_type.value
                stats["by_type"][alert_type] = stats["by_type"].get(alert_type, 0) + 1

                # Count recent escalations
                if alert.escalation_count > 0:
                    stats["recent_escalations"] += 1

            return stats

        except Exception as e:
            logger.error(f"Error getting alert statistics: {e}")
            return {}

