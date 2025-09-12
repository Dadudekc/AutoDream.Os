#!/usr/bin/env python3
"""
🐝 AGENT-2 HEALTH MONITORING ALERTING SYSTEM
Notification and Alert Management for System Health

This module provides comprehensive alerting capabilities:
- Configurable alert channels (email, Slack, messaging, etc.)
- Alert escalation policies and thresholds
- Alert deduplication and rate limiting
- Integration with existing messaging systems
- Alert history and analytics
"""

from __future__ import annotations

import json
import logging
import smtplib
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

try:
    from ..automated_health_check_system import HealthCheckResult, HealthStatus
except ImportError:
    try:
        from automated_health_check_system import HealthCheckResult, HealthStatus
    except ImportError:

        class MockHealthStatus:
            HEALTHY = "healthy"
            WARNING = "warning"
            CRITICAL = "critical"
            UNKNOWN = "unknown"

        HealthStatus = MockHealthStatus
        HealthCheckResult = None

try:
    from .health_monitoring_service import AlertSeverity, HealthMetric
except ImportError:
    from health_monitoring_service import AlertSeverity, HealthMetric

logger = logging.getLogger(__name__)


class AlertChannel(Enum):
    """Alert notification channels."""

    EMAIL = "email"
    SLACK = "slack"
    MESSAGING = "messaging"
    WEBHOOK = "webhook"
    LOG = "log"
    CONSOLE = "console"


class AlertPriority(Enum):
    """Alert priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AlertRule:
    """Alert rule configuration."""

    id: str
    name: str
    condition: str  # Python expression to evaluate
    severity: AlertSeverity
    priority: AlertPriority
    channels: List[AlertChannel]
    cooldown_minutes: int = 15
    enabled: bool = True
    description: str = ""
    last_triggered: Optional[datetime] = None


@dataclass
class AlertNotification:
    """Alert notification details."""

    alert_id: str
    title: str
    message: str
    severity: AlertSeverity
    priority: AlertPriority
    channels: List[AlertChannel]
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False
    resolved_at: Optional[datetime] = None


@dataclass
class AlertChannelConfig:
    """Configuration for alert channels."""

    channel: AlertChannel
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


class HealthAlertingSystem:
    """
    Comprehensive alerting system for health monitoring.

    Provides:
    - Multi-channel alert notifications
    - Alert escalation and deduplication
    - Integration with messaging systems
    - Alert history and analytics
    - Configurable alert rules and policies
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/health_alerting.json"
        self.data_directory = Path("data/health_alerting")
        self.data_directory.mkdir(parents=True, exist_ok=True)

        # Alert configuration
        self.alert_rules: Dict[str, AlertRule] = {}
        self.channel_configs: Dict[AlertChannel, AlertChannelConfig] = {}

        # Alert management
        self.active_alerts: Dict[str, AlertNotification] = {}
        self.alert_history: List[AlertNotification] = []
        self.alert_handlers: Dict[AlertChannel, Callable[[AlertNotification], None]] = {}

        # Alert control
        self.alerting_active = False
        self.alert_thread: Optional[threading.Thread] = None
        self.check_interval_seconds = 10

        # Load configuration and setup
        self._load_configuration()
        self._setup_default_channels()
        self._setup_channel_handlers()

    def _load_configuration(self) -> None:
        """Load alerting configuration."""
        config_file = Path(self.config_path)
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)

                # Load alert rules
                for rule_config in config.get("rules", []):
                    rule = AlertRule(
                        id=rule_config["id"],
                        name=rule_config["name"],
                        condition=rule_config["condition"],
                        severity=AlertSeverity(rule_config["severity"]),
                        priority=AlertPriority(rule_config["priority"]),
                        channels=[AlertChannel(c) for c in rule_config["channels"]],
                        cooldown_minutes=rule_config.get("cooldown_minutes", 15),
                        enabled=rule_config.get("enabled", True),
                        description=rule_config.get("description", ""),
                    )
                    self.alert_rules[rule.id] = rule

                # Load channel configurations
                for channel_config in config.get("channels", []):
                    channel = AlertChannel(channel_config["channel"])
                    config_obj = AlertChannelConfig(
                        channel=channel,
                        enabled=channel_config.get("enabled", True),
                        config=channel_config.get("config", {}),
                    )
                    self.channel_configs[channel] = config_obj

                logger.info(f"✅ Alerting configuration loaded from {config_file}")

            except Exception as e:
                logger.warning(f"⚠️ Failed to load alerting configuration: {e}")
                self._create_default_configuration()

    def _create_default_configuration(self) -> None:
        """Create default alerting configuration."""
        default_config = {
            "rules": [
                {
                    "id": "service_down",
                    "name": "Service Down Alert",
                    "condition": "service_status == 'CRITICAL'",
                    "severity": "critical",
                    "priority": "high",
                    "channels": ["console", "log"],
                    "cooldown_minutes": 5,
                    "description": "Alert when critical services go down",
                },
                {
                    "id": "high_cpu",
                    "name": "High CPU Usage Alert",
                    "condition": "cpu_usage > 85",
                    "severity": "warning",
                    "priority": "medium",
                    "channels": ["console", "log"],
                    "cooldown_minutes": 10,
                    "description": "Alert when CPU usage exceeds 85%",
                },
                {
                    "id": "high_memory",
                    "name": "High Memory Usage Alert",
                    "condition": "memory_usage > 90",
                    "severity": "critical",
                    "priority": "high",
                    "channels": ["console", "log"],
                    "cooldown_minutes": 10,
                    "description": "Alert when memory usage exceeds 90%",
                },
            ],
            "channels": [
                {"channel": "console", "enabled": True, "config": {}},
                {"channel": "log", "enabled": True, "config": {}},
            ],
        }

        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, "w") as f:
            json.dump(default_config, f, indent=2)

        logger.info(f"✅ Default alerting configuration created at {config_file}")

    def _setup_default_channels(self) -> None:
        """Setup default alert channels."""
        default_channels = [
            AlertChannelConfig(channel=AlertChannel.CONSOLE, enabled=True),
            AlertChannelConfig(channel=AlertChannel.LOG, enabled=True),
            AlertChannelConfig(
                channel=AlertChannel.MESSAGING, enabled=False  # Requires additional setup
            ),
        ]

        for channel_config in default_channels:
            if channel_config.channel not in self.channel_configs:
                self.channel_configs[channel_config.channel] = channel_config

    def _setup_channel_handlers(self) -> None:
        """Setup handlers for different alert channels."""
        self.alert_handlers = {
            AlertChannel.CONSOLE: self._handle_console_alert,
            AlertChannel.LOG: self._handle_log_alert,
            AlertChannel.EMAIL: self._handle_email_alert,
            AlertChannel.SLACK: self._handle_slack_alert,
            AlertChannel.MESSAGING: self._handle_messaging_alert,
            AlertChannel.WEBHOOK: self._handle_webhook_alert,
        }

    def start_alerting(self) -> None:
        """Start the alerting system."""
        if self.alerting_active:
            return

        self.alerting_active = True
        self.alert_thread = threading.Thread(
            target=self._alerting_loop, daemon=True, name="HealthAlertingSystem"
        )
        self.alert_thread.start()

        logger.info("✅ Health alerting system started")

    def stop_alerting(self) -> None:
        """Stop the alerting system."""
        self.alerting_active = False

        if self.alert_thread and self.alert_thread.is_alive():
            self.alert_thread.join(timeout=5)

        logger.info("🛑 Health alerting system stopped")

    def _alerting_loop(self) -> None:
        """Main alerting loop."""
        while self.alerting_active:
            try:
                # Process active alerts for escalation
                self._process_alert_escalation()

                # Clean up old alerts
                self._cleanup_old_alerts()

                time.sleep(self.check_interval_seconds)

            except Exception as e:
                logger.error(f"❌ Alerting loop error: {e}")
                time.sleep(5)

    def process_health_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Process a health monitoring event and generate alerts if needed."""
        try:
            # Evaluate alert rules
            for rule in self.alert_rules.values():
                if not rule.enabled:
                    continue

                # Check cooldown
                if rule.last_triggered:
                    cooldown_end = rule.last_triggered + timedelta(minutes=rule.cooldown_minutes)
                    if datetime.now() < cooldown_end:
                        continue

                # Evaluate condition
                if self._evaluate_condition(rule.condition, event_type, data):
                    self._trigger_alert(rule, event_type, data)
                    rule.last_triggered = datetime.now()

        except Exception as e:
            logger.warning(f"⚠️ Error processing health event: {e}")

    def _evaluate_condition(self, condition: str, event_type: str, data: Dict[str, Any]) -> bool:
        """Evaluate an alert condition."""
        try:
            # Create safe evaluation context
            context = {
                "event_type": event_type,
                "data": data,
                **data,  # Flatten data for easier access
            }

            # Evaluate condition safely
            result = eval(condition, {"__builtins__": {}}, context)
            return bool(result)

        except Exception as e:
            logger.warning(f"⚠️ Error evaluating condition '{condition}': {e}")
            return False

    def _trigger_alert(self, rule: AlertRule, event_type: str, data: Dict[str, Any]) -> None:
        """Trigger an alert based on a rule."""
        alert_id = f"alert_{int(time.time())}_{rule.id}"

        alert = AlertNotification(
            alert_id=alert_id,
            title=f"🚨 {rule.name}",
            message=self._generate_alert_message(rule, event_type, data),
            severity=rule.severity,
            priority=rule.priority,
            channels=rule.channels,
            timestamp=datetime.now(),
            context={
                "rule_id": rule.id,
                "event_type": event_type,
                "trigger_data": data,
                "rule_description": rule.description,
            },
        )

        # Store alert
        self.active_alerts[alert_id] = alert
        self.alert_history.append(alert)

        # Send notifications
        self._send_alert_notifications(alert)

        logger.warning(f"🚨 ALERT TRIGGERED: {rule.name} - {alert.message}")

    def _generate_alert_message(
        self, rule: AlertRule, event_type: str, data: Dict[str, Any]
    ) -> str:
        """Generate alert message from rule and data."""
        message = f"{rule.name}: "

        # Add relevant data to message
        relevant_data = []
        for key, value in data.items():
            if isinstance(value, (int, float)) and key in [
                "cpu_usage",
                "memory_usage",
                "disk_usage",
            ]:
                relevant_data.append(f"{key.replace('_', ' ')}: {value:.1f}%")
            elif isinstance(value, str) and key in ["service_name", "component"]:
                relevant_data.append(f"{key}: {value}")

        if relevant_data:
            message += " | ".join(relevant_data)
        else:
            message += f"Event: {event_type}"

        return message

    def _send_alert_notifications(self, alert: AlertNotification) -> None:
        """Send alert notifications through configured channels."""
        for channel in alert.channels:
            if channel in self.alert_handlers:
                try:
                    channel_config = self.channel_configs.get(channel)
                    if channel_config and channel_config.enabled:
                        self.alert_handlers[channel](alert)
                except Exception as e:
                    logger.warning(f"⚠️ Failed to send alert via {channel.value}: {e}")

    def _handle_console_alert(self, alert: AlertNotification) -> None:
        """Handle console alert notifications."""
        severity_icon = {
            AlertSeverity.CRITICAL: "🚨",
            AlertSeverity.ERROR: "❌",
            AlertSeverity.WARNING: "⚠️",
            AlertSeverity.INFO: "ℹ️",
        }.get(alert.severity, "❓")

        print(f"\n{severity_icon} HEALTH ALERT {severity_icon}")
        print(f"Title: {alert.title}")
        print(f"Message: {alert.message}")
        print(f"Severity: {alert.severity.value.upper()}")
        print(f"Priority: {alert.priority.value.upper()}")
        print(f"Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)

    def _handle_log_alert(self, alert: AlertNotification) -> None:
        """Handle log alert notifications."""
        log_message = (
            f"HEALTH_ALERT | {alert.alert_id} | {alert.severity.value.upper()} | "
            f"{alert.priority.value.upper()} | {alert.title} | {alert.message}"
        )

        # Log to file
        log_file = self.data_directory / "health_alerts.log"
        with open(log_file, "a") as f:
            f.write(f"{alert.timestamp.isoformat()} | {log_message}\n")

        logger.warning(log_message)

    def _handle_email_alert(self, alert: AlertNotification) -> None:
        """Handle email alert notifications."""
        channel_config = self.channel_configs.get(AlertChannel.EMAIL)
        if not channel_config:
            return

        config = channel_config.config
        smtp_server = config.get("smtp_server", "localhost")
        smtp_port = config.get("smtp_port", 587)
        smtp_user = config.get("smtp_user")
        smtp_password = config.get("smtp_password")
        from_email = config.get("from_email", "health-monitor@localhost")
        to_emails = config.get("to_emails", [])

        if not to_emails:
            return

        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = from_email
            msg["To"] = ", ".join(to_emails)
            msg["Subject"] = f"[{alert.severity.value.upper()}] {alert.title}"

            body = f"""
Health Alert Notification

Title: {alert.title}
Severity: {alert.severity.value.upper()}
Priority: {alert.priority.value.upper()}
Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

Message:
{alert.message}

Context:
{json.dumps(alert.context, indent=2, default=str)}

--
System Health Monitor
            """.strip()

            msg.attach(MIMEText(body, "plain"))

            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            if smtp_user and smtp_password:
                server.login(smtp_user, smtp_password)
            server.send_message(msg)
            server.quit()

        except Exception as e:
            logger.warning(f"⚠️ Failed to send email alert: {e}")

    def _handle_slack_alert(self, alert: AlertNotification) -> None:
        """Handle Slack alert notifications."""
        channel_config = self.channel_configs.get(AlertChannel.SLACK)
        if not channel_config:
            return

        webhook_url = channel_config.config.get("webhook_url")
        if not webhook_url:
            return

        try:
            import requests

            color_map = {
                AlertSeverity.CRITICAL: "danger",
                AlertSeverity.ERROR: "danger",
                AlertSeverity.WARNING: "warning",
                AlertSeverity.INFO: "good",
            }

            payload = {
                "attachments": [
                    {
                        "color": color_map.get(alert.severity, "good"),
                        "title": alert.title,
                        "text": alert.message,
                        "fields": [
                            {
                                "title": "Severity",
                                "value": alert.severity.value.upper(),
                                "short": True,
                            },
                            {
                                "title": "Priority",
                                "value": alert.priority.value.upper(),
                                "short": True,
                            },
                            {
                                "title": "Time",
                                "value": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                "short": True,
                            },
                        ],
                    }
                ]
            }

            requests.post(webhook_url, json=payload, timeout=10)

        except Exception as e:
            logger.warning(f"⚠️ Failed to send Slack alert: {e}")

    def _handle_messaging_alert(self, alert: AlertNotification) -> None:
        """Handle messaging system alert notifications."""
        try:
            # Import messaging system (lazy import to avoid circular dependencies)
            from src.services.messaging.service import MessagingService

            service = MessagingService()
            priority_map = {
                AlertPriority.CRITICAL: "URGENT",
                AlertPriority.HIGH: "HIGH",
                AlertPriority.MEDIUM: "NORMAL",
                AlertPriority.LOW: "LOW",
            }

            message = f"""
🚨 HEALTH ALERT 🚨

{alert.title}

{alert.message}

Severity: {alert.severity.value.upper()}
Priority: {alert.priority.value.upper()}
Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

This is an automated alert from the system health monitor.
            """.strip()

            # Send to all agents
            service.broadcast(message, priority_map[alert.priority], "ALERT")

        except Exception as e:
            logger.warning(f"⚠️ Failed to send messaging alert: {e}")

    def _handle_webhook_alert(self, alert: AlertNotification) -> None:
        """Handle webhook alert notifications."""
        channel_config = self.channel_configs.get(AlertChannel.WEBHOOK)
        if not channel_config:
            return

        webhook_url = channel_config.config.get("webhook_url")
        if not webhook_url:
            return

        try:
            import requests

            payload = {
                "alert_id": alert.alert_id,
                "title": alert.title,
                "message": alert.message,
                "severity": alert.severity.value,
                "priority": alert.priority.value,
                "timestamp": alert.timestamp.isoformat(),
                "context": alert.context,
            }

            requests.post(webhook_url, json=payload, timeout=10)

        except Exception as e:
            logger.warning(f"⚠️ Failed to send webhook alert: {e}")

    def _process_alert_escalation(self) -> None:
        """Process alert escalation for unresolved alerts."""
        now = datetime.now()

        for alert in self.active_alerts.values():
            if alert.resolved:
                continue

            # Check for escalation based on alert age
            alert_age_hours = (now - alert.timestamp).total_seconds() / 3600

            # Escalate critical alerts after 1 hour
            if (
                alert.severity == AlertSeverity.CRITICAL
                and alert_age_hours >= 1
                and AlertChannel.MESSAGING not in alert.channels
            ):
                alert.channels.append(AlertChannel.MESSAGING)
                self._send_alert_notifications(alert)
                logger.warning(f"🚨 ESCALATED: {alert.title}")

    def _cleanup_old_alerts(self) -> None:
        """Clean up old alerts."""
        # Keep only last 1000 alerts in history
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]

        # Clean resolved alerts older than 24 hours
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.active_alerts = {
            alert_id: alert
            for alert_id, alert in self.active_alerts.items()
            if not alert.resolved or alert.resolved_at > cutoff_time
        }

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an active alert."""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.resolved = True
            alert.resolved_at = datetime.now()
            logger.info(f"✅ Alert resolved: {alert.title}")
            return True
        return False

    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics."""
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)

        recent_alerts = [a for a in self.alert_history if a.timestamp > last_24h]
        weekly_alerts = [a for a in self.alert_history if a.timestamp > last_7d]

        return {
            "active_alerts": len(self.active_alerts),
            "alerts_last_24h": len(recent_alerts),
            "alerts_last_7d": len(weekly_alerts),
            "critical_alerts_active": len(
                [a for a in self.active_alerts.values() if a.severity == AlertSeverity.CRITICAL]
            ),
            "resolved_rate_24h": len([a for a in recent_alerts if a.resolved])
            / max(len(recent_alerts), 1),
            "avg_resolution_time_hours": self._calculate_avg_resolution_time(recent_alerts),
        }

    def _calculate_avg_resolution_time(self, alerts: List[AlertNotification]) -> float:
        """Calculate average resolution time for alerts."""
        resolved_alerts = [a for a in alerts if a.resolved and a.resolved_at]
        if not resolved_alerts:
            return 0.0

        total_time = sum((a.resolved_at - a.timestamp).total_seconds() for a in resolved_alerts)

        return (total_time / len(resolved_alerts)) / 3600  # Convert to hours

    def export_alert_data(self, filepath: Optional[str] = None) -> str:
        """Export alert data to JSON file."""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = str(self.data_directory / f"alert_data_{timestamp}.json")

        data = {
            "export_timestamp": datetime.now().isoformat(),
            "active_alerts": [
                {
                    "alert_id": a.alert_id,
                    "title": a.title,
                    "severity": a.severity.value,
                    "priority": a.priority.value,
                    "timestamp": a.timestamp.isoformat(),
                    "resolved": a.resolved,
                }
                for a in self.active_alerts.values()
            ],
            "alert_history": [
                {
                    "alert_id": a.alert_id,
                    "title": a.title,
                    "message": a.message,
                    "severity": a.severity.value,
                    "priority": a.priority.value,
                    "channels": [c.value for c in a.channels],
                    "timestamp": a.timestamp.isoformat(),
                    "resolved": a.resolved,
                    "resolved_at": a.resolved_at.isoformat() if a.resolved_at else None,
                }
                for a in self.alert_history[-500:]
            ],  # Last 500 alerts
            "statistics": self.get_alert_statistics(),
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"✅ Alert data exported to {filepath}")
        return filepath
