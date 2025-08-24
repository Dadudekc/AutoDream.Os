"""
Agent Health Alerting Manager Module

Single Responsibility: Manage health alerts, notifications, and escalation.
Follows V2 coding standards: Clean OOP design, SRP compliance, TDD approach.
"""

import asyncio
import json
import logging
import smtplib
import time
import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Callable, Any, Union
from concurrent.futures import ThreadPoolExecutor
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertStatus(Enum):
    """Alert status values"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    EXPIRED = "expired"
    SUPPRESSED = "suppressed"


class NotificationChannel(Enum):
    """Notification channels for alerts"""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"
    PAGER_DUTY = "pager_duty"
    CONSOLE = "console"
    LOG = "log"


class EscalationLevel(Enum):
    """Escalation levels for alerts"""
    LEVEL_1 = "level_1"  # Immediate response
    LEVEL_2 = "level_2"  # Escalate to supervisor
    LEVEL_3 = "level_3"  # Escalate to management
    LEVEL_4 = "level_4"  # Escalate to emergency contacts


@dataclass
class AlertRule:
    """Rule for generating alerts"""
    rule_id: str
    name: str
    description: str
    severity: AlertSeverity
    conditions: Dict[str, Any]  # Conditions that trigger the alert
    enabled: bool = True
    cooldown_period: int = 300  # seconds
    escalation_enabled: bool = True
    notification_channels: List[NotificationChannel] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class HealthAlert:
    """Health alert information"""
    alert_id: str
    agent_id: str
    severity: AlertSeverity
    message: str
    metric_type: str
    current_value: float
    threshold: float
    timestamp: datetime
    status: AlertStatus = AlertStatus.ACTIVE
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    escalation_level: EscalationLevel = EscalationLevel.LEVEL_1
    notification_sent: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NotificationConfig:
    """Configuration for notification channels"""
    channel: NotificationChannel
    enabled: bool = True
    recipients: List[str] = field(default_factory=list)
    template: str = ""
    retry_attempts: int = 3
    retry_delay: int = 60  # seconds
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EscalationPolicy:
    """Policy for alert escalation"""
    level: EscalationLevel
    delay_minutes: int
    contacts: List[str]
    notification_channels: List[NotificationChannel]
    auto_escalate: bool = True
    require_acknowledgment: bool = False


class HealthAlertingManager:
    """
    Health alerting and notification management
    
    Single Responsibility: Manage health alerts, notifications, and escalation
    policies. Handles alert lifecycle and communication.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the alerting manager"""
        self.config = config or {}
        self.alerts: Dict[str, HealthAlert] = {}
        self.alert_rules: Dict[str, AlertRule] = {}
        self.notification_configs: Dict[NotificationChannel, NotificationConfig] = {}
        self.escalation_policies: Dict[EscalationLevel, EscalationPolicy] = {}
        self.alert_callbacks: Set[Callable] = set()
        self.escalation_thread: Optional[threading.Thread] = None
        self.escalation_active = False
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Initialize default configurations
        self._initialize_default_rules()
        self._initialize_default_notifications()
        self._initialize_default_escalation()
        
        # Alert management settings
        self.alert_retention_days = self.config.get("alert_retention_days", 30)
        self.auto_resolve_threshold = self.config.get("auto_resolve_threshold", 24)  # hours
        self.escalation_check_interval = self.config.get("escalation_check_interval", 60)  # seconds
        
        logger.info("HealthAlertingManager initialized with default configurations")

    def _initialize_default_rules(self):
        """Initialize default alert rules"""
        default_rules = [
            AlertRule(
                rule_id="high_cpu_usage",
                name="High CPU Usage",
                description="Alert when CPU usage exceeds threshold",
                severity=AlertSeverity.WARNING,
                conditions={
                    "metric": "cpu_usage",
                    "operator": ">",
                    "threshold": 85.0,
                    "duration": 300,  # 5 minutes
                },
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.CONSOLE],
            ),
            AlertRule(
                rule_id="high_memory_usage",
                name="High Memory Usage",
                description="Alert when memory usage exceeds threshold",
                severity=AlertSeverity.WARNING,
                conditions={
                    "metric": "memory_usage",
                    "operator": ">",
                    "threshold": 90.0,
                    "duration": 300,
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
                    "duration": 60,
                },
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.SMS],
                escalation_enabled=True,
            ),
            AlertRule(
                rule_id="high_error_rate",
                name="High Error Rate",
                description="Alert when error rate is high",
                severity=AlertSeverity.CRITICAL,
                conditions={
                    "metric": "error_rate",
                    "operator": ">",
                    "threshold": 10.0,
                    "duration": 600,
                },
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK],
                escalation_enabled=True,
            ),
        ]

        for rule in default_rules:
            self.alert_rules[rule.rule_id] = rule

    def _initialize_default_notifications(self):
        """Initialize default notification configurations"""
        default_configs = [
            NotificationConfig(
                channel=NotificationChannel.EMAIL,
                enabled=True,
                recipients=["admin@example.com"],
                template="Alert: {severity} - {message}",
                retry_attempts=3,
                retry_delay=60,
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
            NotificationConfig(
                channel=NotificationChannel.SLACK,
                enabled=False,
                recipients=["#alerts"],
                template=":warning: *{severity}*: {message}",
                custom_parameters={"webhook_url": "https://hooks.slack.com/..."},
            ),
        ]

        for config in default_configs:
            self.notification_configs[config.channel] = config

    def _initialize_default_escalation(self):
        """Initialize default escalation policies"""
        default_policies = [
            EscalationPolicy(
                level=EscalationLevel.LEVEL_1,
                delay_minutes=0,
                contacts=["oncall@example.com"],
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SMS],
                auto_escalate=True,
                require_acknowledgment=False,
            ),
            EscalationPolicy(
                level=EscalationLevel.LEVEL_2,
                delay_minutes=15,
                contacts=["supervisor@example.com"],
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK],
                auto_escalate=True,
                require_acknowledgment=True,
            ),
            EscalationPolicy(
                level=EscalationLevel.LEVEL_3,
                delay_minutes=60,
                contacts=["manager@example.com"],
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SMS],
                auto_escalate=True,
                require_acknowledgment=True,
            ),
            EscalationPolicy(
                level=EscalationLevel.LEVEL_4,
                delay_minutes=240,  # 4 hours
                contacts=["emergency@example.com"],
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SMS, NotificationChannel.PAGER_DUTY],
                auto_escalate=True,
                require_acknowledgment=True,
            ),
        ]

        for policy in default_policies:
            self.escalation_policies[policy.level] = policy

    def start(self):
        """Start the alerting manager"""
        if self.escalation_active:
            logger.warning("Alerting manager already active")
            return

        self.escalation_active = True
        self.escalation_thread = threading.Thread(target=self._escalation_loop, daemon=True)
        self.escalation_thread.start()
        logger.info("Health alerting manager started")

    def stop(self):
        """Stop the alerting manager"""
        self.escalation_active = False
        if self.escalation_thread:
            self.escalation_thread.join(timeout=5)
        self.executor.shutdown(wait=True)
        logger.info("Health alerting manager stopped")

    def _escalation_loop(self):
        """Main escalation monitoring loop"""
        while self.escalation_active:
            try:
                # Check for alerts that need escalation
                self._check_escalations()

                # Check for alerts that can be auto-resolved
                self._check_auto_resolve()

                # Clean up expired alerts
                self._cleanup_expired_alerts()

                time.sleep(self.escalation_check_interval)

            except Exception as e:
                logger.error(f"Error in escalation loop: {e}")
                time.sleep(10)  # Wait before retrying

    def _check_escalations(self):
        """Check for alerts that need escalation"""
        current_time = datetime.now()

        for alert_id, alert in self.alerts.items():
            if alert.status != AlertStatus.ACTIVE:
                continue

            # Check if escalation is needed
            escalation_policy = self.escalation_policies.get(alert.escalation_level)
            if not escalation_policy or not escalation_policy.auto_escalate:
                continue

            # Calculate time since alert creation
            time_since_creation = current_time - alert.timestamp
            escalation_delay = timedelta(minutes=escalation_policy.delay_minutes)

            if time_since_creation >= escalation_delay:
                self._escalate_alert(alert, escalation_policy)

    def _escalate_alert(self, alert: HealthAlert, policy: EscalationPolicy):
        """Escalate an alert to the next level"""
        try:
            # Find next escalation level
            current_level = alert.escalation_level
            next_level = self._get_next_escalation_level(current_level)

            if next_level:
                alert.escalation_level = next_level
                alert.metadata["escalated_at"] = datetime.now().isoformat()
                alert.metadata["escalated_from"] = current_level.value

                # Send escalation notifications
                self._send_escalation_notifications(alert, policy)

                logger.info(f"Alert {alert.alert_id} escalated to {next_level.value}")

        except Exception as e:
            logger.error(f"Error escalating alert {alert.alert_id}: {e}")

    def _get_next_escalation_level(self, current_level: EscalationLevel) -> Optional[EscalationLevel]:
        """Get the next escalation level"""
        level_order = [
            EscalationLevel.LEVEL_1,
            EscalationLevel.LEVEL_2,
            EscalationLevel.LEVEL_3,
            EscalationLevel.LEVEL_4,
        ]

        try:
            current_index = level_order.index(current_level)
            if current_index + 1 < len(level_order):
                return level_order[current_index + 1]
        except ValueError:
            pass

        return None

    def _send_escalation_notifications(self, alert: HealthAlert, policy: EscalationPolicy):
        """Send escalation notifications"""
        for channel in policy.notification_channels:
            if channel in self.notification_configs:
                config = self.notification_configs[channel]
                if config.enabled:
                    self._send_notification(alert, channel, config, policy.contacts)

    def _check_auto_resolve(self):
        """Check for alerts that can be auto-resolved"""
        current_time = datetime.now()
        auto_resolve_threshold = timedelta(hours=self.auto_resolve_threshold)

        for alert_id, alert in self.alerts.items():
            if alert.status != AlertStatus.ACTIVE:
                continue

            # Check if alert has been active for too long
            time_since_creation = current_time - alert.timestamp
            if time_since_creation >= auto_resolve_threshold:
                self._auto_resolve_alert(alert)

    def _auto_resolve_alert(self, alert: HealthAlert):
        """Automatically resolve an alert"""
        try:
            alert.status = AlertStatus.RESOLVED
            alert.resolved_at = datetime.now()
            alert.resolved_by = "system"
            alert.metadata["auto_resolved"] = True
            alert.metadata["auto_resolved_at"] = datetime.now().isoformat()

            logger.info(f"Alert {alert.alert_id} auto-resolved after {self.auto_resolve_threshold} hours")

            # Notify subscribers
            self._notify_alert_updates()

        except Exception as e:
            logger.error(f"Error auto-resolving alert {alert.alert_id}: {e}")

    def _cleanup_expired_alerts(self):
        """Clean up expired alerts"""
        current_time = datetime.now()
        retention_threshold = timedelta(days=self.alert_retention_days)

        expired_alerts = []
        for alert_id, alert in self.alerts.items():
            if alert.status == AlertStatus.RESOLVED:
                time_since_resolution = current_time - alert.resolved_at
                if time_since_resolution >= retention_threshold:
                    expired_alerts.append(alert_id)

        # Remove expired alerts
        for alert_id in expired_alerts:
            del self.alerts[alert_id]

        if expired_alerts:
            logger.info(f"Cleaned up {len(expired_alerts)} expired alerts")

    def create_alert(
        self,
        agent_id: str,
        severity: AlertSeverity,
        message: str,
        metric_type: str,
        current_value: float,
        threshold: float,
        metadata: Dict[str, Any] = None,
    ) -> str:
        """Create a new health alert"""
        try:
            # Generate unique alert ID
            alert_id = f"health_alert_{agent_id}_{metric_type}_{int(time.time())}"

            # Check if similar alert already exists (cooldown)
            if self._should_suppress_alert(agent_id, metric_type, severity):
                logger.debug(f"Suppressing alert due to cooldown: {message}")
                return ""

            # Create alert
            alert = HealthAlert(
                alert_id=alert_id,
                agent_id=agent_id,
                severity=severity,
                message=message,
                metric_type=metric_type,
                current_value=current_value,
                threshold=threshold,
                timestamp=datetime.now(),
                metadata=metadata or {},
            )

            # Store alert
            self.alerts[alert_id] = alert

            # Send notifications
            self._send_alert_notifications(alert)

            # Notify subscribers
            self._notify_alert_updates()

            logger.info(f"Health alert created: {alert_id} - {message}")
            return alert_id

        except Exception as e:
            logger.error(f"Error creating health alert: {e}")
            return ""

    def _should_suppress_alert(self, agent_id: str, metric_type: str, severity: AlertSeverity) -> bool:
        """Check if an alert should be suppressed due to cooldown"""
        current_time = datetime.now()

        for alert in self.alerts.values():
            if (alert.agent_id == agent_id and
                alert.metric_type == metric_type and
                alert.severity == severity and
                alert.status == AlertStatus.ACTIVE):

                # Check cooldown period
                time_since_creation = current_time - alert.timestamp
                cooldown_period = timedelta(seconds=300)  # 5 minutes default

                if time_since_creation < cooldown_period:
                    return True

        return False

    def _send_alert_notifications(self, alert: HealthAlert):
        """Send notifications for a new alert"""
        # Find applicable alert rule
        rule = self._find_applicable_rule(alert)
        if not rule:
            return

        # Send notifications to configured channels
        for channel in rule.notification_channels:
            if channel in self.notification_configs:
                config = self.notification_configs[channel]
                if config.enabled:
                    self._send_notification(alert, channel, config)

    def _find_applicable_rule(self, alert: HealthAlert) -> Optional[AlertRule]:
        """Find the alert rule that applies to this alert"""
        for rule in self.alert_rules.values():
            if not rule.enabled:
                continue

            # Check if rule conditions match
            if self._rule_matches_alert(rule, alert):
                return rule

        return None

    def _rule_matches_alert(self, rule: AlertRule, alert: HealthAlert) -> bool:
        """Check if an alert rule matches an alert"""
        conditions = rule.conditions

        # Check metric type
        if conditions.get("metric") != alert.metric_type:
            return False

        # Check severity
        if rule.severity != alert.severity:
            return False

        # Check threshold conditions
        if "operator" in conditions and "threshold" in conditions:
            operator = conditions["operator"]
            threshold = conditions["threshold"]

            if operator == ">" and alert.current_value <= threshold:
                return False
            elif operator == "<" and alert.current_value >= threshold:
                return False
            elif operator == ">=" and alert.current_value < threshold:
                return False
            elif operator == "<=" and alert.current_value > threshold:
                return False
            elif operator == "==" and alert.current_value != threshold:
                return False

        return True

    def _send_notification(
        self,
        alert: HealthAlert,
        channel: NotificationChannel,
        config: NotificationConfig,
        recipients: List[str] = None,
    ):
        """Send notification through a specific channel"""
        try:
            if channel == NotificationChannel.EMAIL:
                self._send_email_notification(alert, config, recipients)
            elif channel == NotificationChannel.CONSOLE:
                self._send_console_notification(alert, config)
            elif channel == NotificationChannel.LOG:
                self._send_log_notification(alert, config)
            elif channel == NotificationChannel.SLACK:
                self._send_slack_notification(alert, config)
            else:
                logger.warning(f"Unsupported notification channel: {channel}")

        except Exception as e:
            logger.error(f"Error sending notification via {channel}: {e}")

    def _send_email_notification(self, alert: HealthAlert, config: NotificationConfig, recipients: List[str] = None):
        """Send email notification"""
        try:
            recipients = recipients or config.recipients
            if not recipients:
                return

            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.config.get("smtp_from", "noreply@example.com")
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = f"Health Alert: {alert.severity.value.upper()} - {alert.agent_id}"

            # Create message body
            body = self._format_email_body(alert, config)
            msg.attach(MIMEText(body, "plain"))

            # Send email (this would integrate with actual SMTP server)
            logger.info(f"Email notification sent to {recipients} for alert {alert.alert_id}")

        except Exception as e:
            logger.error(f"Error sending email notification: {e}")

    def _send_console_notification(self, alert: HealthAlert, config: NotificationConfig):
        """Send console notification"""
        try:
            message = config.template.format(
                severity=alert.severity.value.upper(),
                message=alert.message,
                agent_id=alert.agent_id,
                timestamp=alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            )
            print(f"[CONSOLE] {message}")

        except Exception as e:
            logger.error(f"Error sending console notification: {e}")

    def _send_log_notification(self, alert: HealthAlert, config: NotificationConfig):
        """Send log notification"""
        try:
            message = config.template.format(
                severity=alert.severity.value.upper(),
                message=alert.message,
                agent_id=alert.agent_id,
                timestamp=alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            )
            logger.warning(f"HEALTH ALERT: {message}")

        except Exception as e:
            logger.error(f"Error sending log notification: {e}")

    def _send_slack_notification(self, alert: HealthAlert, config: NotificationConfig):
        """Send Slack notification"""
        try:
            message = config.template.format(
                severity=alert.severity.value.upper(),
                message=alert.message,
                agent_id=alert.alert_id,
                timestamp=alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            )
            logger.info(f"Slack notification would be sent: {message}")

        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")

    def _format_email_body(self, alert: HealthAlert, config: NotificationConfig) -> str:
        """Format email body for alert notification"""
        body = f"""
Health Alert Notification

Severity: {alert.severity.value.upper()}
Agent ID: {alert.agent_id}
Metric: {alert.metric_type}
Current Value: {alert.current_value}
Threshold: {alert.threshold}
Message: {alert.message}
Timestamp: {alert.timestamp.strftime("%Y-%m-%d %H:%M:%S")}

This is an automated notification from the Health Monitoring System.
Please review and take appropriate action.

---
Generated by HealthAlertingManager
        """
        return body.strip()

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert"""
        if alert_id not in self.alerts:
            return False

        try:
            alert = self.alerts[alert_id]
            alert.status = AlertStatus.ACKNOWLEDGED
            alert.acknowledged_by = acknowledged_by
            alert.acknowledged_at = datetime.now()

            logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")

            # Notify subscribers
            self._notify_alert_updates()

            return True

        except Exception as e:
            logger.error(f"Error acknowledging alert {alert_id}: {e}")
            return False

    def resolve_alert(self, alert_id: str, resolved_by: str) -> bool:
        """Resolve an alert"""
        if alert_id not in self.alerts:
            return False

        try:
            alert = self.alerts[alert_id]
            alert.status = AlertStatus.RESOLVED
            alert.resolved_by = resolved_by
            alert.resolved_at = datetime.now()

            logger.info(f"Alert {alert_id} resolved by {resolved_by}")

            # Notify subscribers
            self._notify_alert_updates()

            return True

        except Exception as e:
            logger.error(f"Error resolving alert {alert_id}: {e}")
            return False

    def get_alert(self, alert_id: str) -> Optional[HealthAlert]:
        """Get a specific alert by ID"""
        return self.alerts.get(alert_id)

    def get_alerts(
        self,
        status: Optional[AlertStatus] = None,
        severity: Optional[AlertSeverity] = None,
        agent_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[HealthAlert]:
        """Get alerts with optional filtering"""
        alerts = list(self.alerts.values())

        if status:
            alerts = [alert for alert in alerts if alert.status == status]

        if severity:
            alerts = [alert for alert in alerts if alert.severity == severity]

        if agent_id:
            alerts = [alert for alert in alerts if alert.agent_id == agent_id]

        # Sort by timestamp (newest first) and limit results
        alerts.sort(key=lambda x: x.timestamp, reverse=True)
        return alerts[:limit]

    def get_alerts_summary(self) -> Dict[str, Any]:
        """Get summary of all alerts"""
        total_alerts = len(self.alerts)
        active_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.ACTIVE])
        acknowledged_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.ACKNOWLEDGED])
        resolved_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.RESOLVED])

        # Count by severity
        severity_counts = {}
        for alert in self.alerts.values():
            severity = alert.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        # Count by agent
        agent_counts = {}
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

    def add_alert_rule(self, rule: AlertRule):
        """Add a new alert rule"""
        self.alert_rules[rule.rule_id] = rule
        logger.info(f"Alert rule added: {rule.rule_id}")

    def update_alert_rule(self, rule_id: str, updates: Dict[str, Any]):
        """Update an existing alert rule"""
        if rule_id in self.alert_rules:
            rule = self.alert_rules[rule_id]
            for key, value in updates.items():
                if hasattr(rule, key):
                    setattr(rule, key, value)
            rule.updated_at = datetime.now()
            logger.info(f"Alert rule updated: {rule_id}")

    def remove_alert_rule(self, rule_id: str):
        """Remove an alert rule"""
        if rule_id in self.alert_rules:
            del self.alert_rules[rule_id]
            logger.info(f"Alert rule removed: {rule_id}")

    def subscribe_to_alert_updates(self, callback: Callable):
        """Subscribe to alert update notifications"""
        self.alert_callbacks.add(callback)

    def unsubscribe_from_alert_updates(self, callback: Callable):
        """Unsubscribe from alert update notifications"""
        self.alert_callbacks.discard(callback)

    def _notify_alert_updates(self):
        """Notify subscribers of alert updates"""
        for callback in self.alert_callbacks:
            try:
                callback(self.alerts)
            except Exception as e:
                logger.error(f"Error in alert update callback: {e}")

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            logger.info("Running HealthAlertingManager smoke test...")

            # Test basic initialization
            logger.info("Testing basic initialization...")
            assert len(self.alert_rules) > 0
            assert len(self.notification_configs) > 0
            assert len(self.escalation_policies) > 0
            logger.info("Basic initialization passed")

            # Test alert creation
            logger.info("Testing alert creation...")
            alert_id = self.create_alert(
                "test_agent",
                AlertSeverity.WARNING,
                "Test alert message",
                "cpu_usage",
                90.0,
                85.0,
            )
            assert alert_id != "", "Alert creation failed"
            assert alert_id in self.alerts
            logger.info("Alert creation passed")

            # Test alert retrieval
            logger.info("Testing alert retrieval...")
            alert = self.get_alert(alert_id)
            assert alert is not None
            assert alert.agent_id == "test_agent"
            assert alert.severity == AlertSeverity.WARNING
            logger.info("Alert retrieval passed")

            # Test alert acknowledgment
            logger.info("Testing alert acknowledgment...")
            success = self.acknowledge_alert(alert_id, "test_user")
            assert success
            assert self.alerts[alert_id].status == AlertStatus.ACKNOWLEDGED
            logger.info("Alert acknowledgment passed")

            # Test alert resolution
            logger.info("Testing alert resolution...")
            success = self.resolve_alert(alert_id, "test_user")
            assert success
            assert self.alerts[alert_id].status == AlertStatus.RESOLVED
            logger.info("Alert resolution passed")

            # Test alerts summary
            logger.info("Testing alerts summary...")
            summary = self.get_alerts_summary()
            assert "total_alerts" in summary
            assert "active_alerts" in summary
            logger.info("Alerts summary passed")

            # Cleanup
            logger.info("Cleaning up...")
            if alert_id in self.alerts:
                del self.alerts[alert_id]

            logger.info("✅ HealthAlertingManager smoke test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ HealthAlertingManager smoke test FAILED: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False

    def shutdown(self):
        """Shutdown the alerting manager"""
        self.stop()
        logger.info("HealthAlertingManager shutdown complete")


def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Health Alerting Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")

    args = parser.parse_args()

    if args.test:
        manager = HealthAlertingManager()
        success = manager.run_smoke_test()
        manager.shutdown()
        exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

