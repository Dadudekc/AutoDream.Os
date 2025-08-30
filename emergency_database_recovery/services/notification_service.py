#!/usr/bin/env python3
"""
Notification Service - Emergency Database Recovery System
Provides notification and alerting functionality for critical events
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .logging_service import LoggingService


class NotificationService:
    """Notification and alerting service for emergency database recovery"""

    def __init__(self):
        self.logger = LoggingService().get_logger("NotificationService")
        self.notification_channels = {
            "emergency": "emergency_alerts.json",
            "critical": "critical_alerts.json",
            "warning": "warning_alerts.json",
            "info": "info_alerts.json",
        }
        self.alert_priorities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

    def send_emergency_alert(
        self,
        alert_type: str,
        message: str,
        context: Dict[str, Any],
        recipients: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Send emergency alert with highest priority"""
        return self._send_alert(
            "emergency", alert_type, message, context, recipients, "CRITICAL"
        )

    def send_critical_alert(
        self,
        alert_type: str,
        message: str,
        context: Dict[str, Any],
        recipients: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Send critical alert with high priority"""
        return self._send_alert(
            "critical", alert_type, message, context, recipients, "HIGH"
        )

    def send_warning_alert(
        self,
        alert_type: str,
        message: str,
        context: Dict[str, Any],
        recipients: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Send warning alert with medium priority"""
        return self._send_alert(
            "warning", alert_type, message, context, recipients, "MEDIUM"
        )

    def send_info_notification(
        self,
        notification_type: str,
        message: str,
        context: Dict[str, Any],
        recipients: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Send informational notification with low priority"""
        return self._send_alert(
            "info", notification_type, message, context, recipients, "LOW"
        )

    def broadcast_system_status(
        self, system_status: Dict[str, Any], include_health_metrics: bool = True
    ) -> Dict[str, Any]:
        """Broadcast system status to all notification channels"""
        timestamp = datetime.now().isoformat()

        broadcast_result = {
            "timestamp": timestamp,
            "broadcast_type": "system_status",
            "channels_used": [],
            "recipients_notified": 0,
            "status_summary": self._generate_status_summary(system_status),
        }

        # Determine appropriate channels based on system health
        health_score = system_status.get("health_score", 100)
        critical_issues = system_status.get("critical_issues", 0)

        if critical_issues > 0 or health_score < 50:
            # Use emergency and critical channels
            channels = ["emergency", "critical"]
        elif health_score < 75:
            # Use warning channel
            channels = ["warning"]
        else:
            # Use info channel
            channels = ["info"]

        # Send to each channel
        for channel in channels:
            try:
                notification = self._send_alert(
                    channel,
                    "system_status",
                    f"System health: {health_score}%, Critical issues: {critical_issues}",
                    system_status,
                    None,
                    self._get_priority_for_channel(channel),
                )

                if notification.get("sent", False):
                    broadcast_result["channels_used"].append(channel)
                    broadcast_result["recipients_notified"] += notification.get(
                        "recipients_notified", 0
                    )

            except Exception as e:
                self.logger.error(f"Failed to broadcast to {channel} channel: {e}")

        self.logger.info(
            f"System status broadcast completed: {len(broadcast_result['channels_used'])} channels used"
        )
        return broadcast_result

    def notify_recovery_completion(
        self, recovery_summary: Dict[str, Any], success_rate: float, time_taken: float
    ) -> Dict[str, Any]:
        """Notify stakeholders of recovery completion"""
        timestamp = datetime.now().isoformat()

        if success_rate == 100.0:
            message = f"Recovery completed successfully in {time_taken:.2f} seconds"
            channel = "info"
            priority = "LOW"
        elif success_rate >= 80.0:
            message = f"Recovery completed with {success_rate:.1f}% success rate in {time_taken:.2f} seconds"
            channel = "warning"
            priority = "MEDIUM"
        else:
            message = f"Recovery completed with {success_rate:.1f}% success rate - ATTENTION REQUIRED"
            channel = "critical"
            priority = "HIGH"

        notification = self._send_alert(
            channel,
            "recovery_completion",
            message,
            {
                "recovery_summary": recovery_summary,
                "success_rate": success_rate,
                "time_taken": time_taken,
                "timestamp": timestamp,
            },
            None,
            priority,
        )

        self.logger.info(f"Recovery completion notification sent: {message}")
        return notification

    def notify_integrity_violation(
        self,
        violation_type: str,
        affected_files: List[str],
        severity: str,
        recommendations: List[str],
    ) -> Dict[str, Any]:
        """Notify stakeholders of database integrity violations"""
        message = f"Database integrity violation detected: {violation_type} affecting {len(affected_files)} files"

        # Determine channel based on severity
        if severity == "CRITICAL":
            channel = "emergency"
        elif severity == "HIGH":
            channel = "critical"
        elif severity == "MEDIUM":
            channel = "warning"
        else:
            channel = "info"

        notification = self._send_alert(
            channel,
            "integrity_violation",
            message,
            {
                "violation_type": violation_type,
                "affected_files": affected_files,
                "severity": severity,
                "recommendations": recommendations,
                "timestamp": datetime.now().isoformat(),
            },
            None,
            severity,
        )

        self.logger.warning(
            f"Integrity violation notification sent: {violation_type} - {severity}"
        )
        return notification

    def _send_alert(
        self,
        channel: str,
        alert_type: str,
        message: str,
        context: Dict[str, Any],
        recipients: Optional[List[str]] = None,
        priority: str = "MEDIUM",
    ) -> Dict[str, Any]:
        """Internal method to send alerts to specific channels"""
        timestamp = datetime.now().isoformat()

        notification = {
            "timestamp": timestamp,
            "channel": channel,
            "alert_type": alert_type,
            "message": message,
            "context": context,
            "priority": priority,
            "recipients": recipients or self._get_default_recipients(channel),
            "sent": False,
            "recipients_notified": 0,
        }

        try:
            # Save notification to appropriate channel file
            self._save_notification(channel, notification)

            # Log the notification
            self.logger.info(
                f"Notification sent to {channel} channel: {alert_type} - {priority}"
            )

            notification["sent"] = True
            notification["recipients_notified"] = len(notification["recipients"])

        except Exception as e:
            self.logger.error(f"Failed to send notification to {channel} channel: {e}")
            notification["error"] = str(e)

        return notification

    def _save_notification(self, channel: str, notification: Dict[str, Any]):
        """Save notification to channel-specific file"""
        try:
            # Create notifications directory if it doesn't exist
            notifications_dir = Path("emergency_database_recovery/notifications")
            notifications_dir.mkdir(exist_ok=True)

            # Get channel file path
            channel_file = notifications_dir / self.notification_channels[channel]

            # Load existing notifications or create new list
            if channel_file.exists():
                with open(channel_file, "r", encoding="utf-8") as f:
                    notifications = json.load(f)
            else:
                notifications = []

            # Add new notification
            notifications.append(notification)

            # Keep only last 100 notifications per channel
            if len(notifications) > 100:
                notifications = notifications[-100:]

            # Save updated notifications
            with open(channel_file, "w", encoding="utf-8") as f:
                json.dump(notifications, f, indent=2, ensure_ascii=False)

        except Exception as e:
            raise Exception(f"Failed to save notification to {channel} channel: {e}")

    def _get_default_recipients(self, channel: str) -> List[str]:
        """Get default recipients for each channel"""
        if channel == "emergency":
            return ["emergency_response_team", "system_administrators", "captain_agent"]
        elif channel == "critical":
            return ["system_administrators", "captain_agent", "monitoring_team"]
        elif channel == "warning":
            return ["monitoring_team", "maintenance_team"]
        else:
            return ["monitoring_team"]

    def _get_priority_for_channel(self, channel: str) -> str:
        """Get priority level for each channel"""
        if channel == "emergency":
            return "CRITICAL"
        elif channel == "critical":
            return "HIGH"
        elif channel == "warning":
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_status_summary(self, system_status: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of system status for notifications"""
        return {
            "overall_health": system_status.get("health_score", "unknown"),
            "critical_issues": system_status.get("critical_issues", 0),
            "warnings": system_status.get("warnings", 0),
            "systems_operational": system_status.get("systems_operational", 0),
            "systems_degraded": system_status.get("systems_degraded", 0),
            "systems_failed": system_status.get("systems_failed", 0),
            "last_updated": system_status.get("last_updated", "unknown"),
        }

    def get_notification_history(
        self, channel: str = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get notification history for specified channel or all channels"""
        notifications = []

        try:
            notifications_dir = Path("emergency_database_recovery/notifications")

            if channel:
                # Get notifications for specific channel
                if channel in self.notification_channels:
                    channel_file = (
                        notifications_dir / self.notification_channels[channel]
                    )
                    if channel_file.exists():
                        with open(channel_file, "r", encoding="utf-8") as f:
                            channel_notifications = json.load(f)
                            notifications.extend(channel_notifications[-limit:])
            else:
                # Get notifications from all channels
                for channel_name, filename in self.notification_channels.items():
                    channel_file = notifications_dir / filename
                    if channel_file.exists():
                        with open(channel_file, "r", encoding="utf-8") as f:
                            channel_notifications = json.load(f)
                            notifications.extend(channel_notifications)

                # Sort by timestamp and limit results
                notifications.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
                notifications = notifications[:limit]

        except Exception as e:
            self.logger.error(f"Failed to get notification history: {e}")

        return notifications
