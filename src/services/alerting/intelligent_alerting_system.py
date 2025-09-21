"""
Intelligent Alerting System
==========================

Advanced alert management with smart routing, notification channels,
alert escalation, and comprehensive analytics.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from enum import Enum
import json
import logging
from pathlib import Path

# ---------- Enums ----------

class AlertSeverity(Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(Enum):
    """Alert status states."""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

class NotificationChannel(Enum):
    """Notification channel types."""
    EMAIL = "email"
    SLACK = "slack"
    DISCORD = "discord"
    WEBHOOK = "webhook"
    SMS = "sms"

# ---------- Data Models ----------

@dataclass
class Alert:
    """Alert data model."""
    id: str
    title: str
    description: str
    severity: AlertSeverity
    source: str
    category: str
    created_at: datetime
    status: AlertStatus = AlertStatus.ACTIVE
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AlertRule:
    """Alert rule configuration."""
    id: str
    name: str
    condition: str
    severity: AlertSeverity
    channels: List[NotificationChannel]
    escalation_delay: int = 300  # seconds
    suppression_duration: int = 3600  # seconds
    enabled: bool = True

@dataclass
class NotificationConfig:
    """Notification channel configuration."""
    channel: NotificationChannel
    endpoint: str
    credentials: Dict[str, str]
    enabled: bool = True
    rate_limit: int = 100  # per hour

@dataclass
class EscalationPolicy:
    """Alert escalation policy."""
    id: str
    name: str
    levels: List[Dict[str, Any]]
    max_escalations: int = 3

# ---------- Core Alerting System ----------

class IntelligentAlertingSystem:
    """Main intelligent alerting system."""
    
    def __init__(self, config_path: str = None):
        """Initialize the alerting system."""
        self.alerts: Dict[str, Alert] = {}
        self.rules: Dict[str, AlertRule] = {}
        self.notification_configs: Dict[NotificationChannel, NotificationConfig] = {}
        self.escalation_policies: Dict[str, EscalationPolicy] = {}
        self.alert_history: List[Alert] = []
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self._load_config(config_path)
        
        # Initialize notification handlers
        self._init_notification_handlers()
    
    def _load_config(self, config_path: str = None):
        """Load configuration from file."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                self._parse_config(config)
        else:
            self._load_default_config()
    
    def _load_default_config(self):
        """Load default configuration."""
        # Default notification channels
        self.notification_configs = {
            NotificationChannel.EMAIL: NotificationConfig(
                channel=NotificationChannel.EMAIL,
                endpoint="smtp://localhost:587",
                credentials={"username": "alerts", "password": "password"}
            ),
            NotificationChannel.DISCORD: NotificationConfig(
                channel=NotificationChannel.DISCORD,
                endpoint="https://discord.com/api/webhooks/...",
                credentials={"token": "your_token"}
            )
        }
        
        # Default escalation policy
        self.escalation_policies["default"] = EscalationPolicy(
            id="default",
            name="Default Escalation",
            levels=[
                {"delay": 300, "channels": [NotificationChannel.EMAIL]},
                {"delay": 900, "channels": [NotificationChannel.DISCORD]},
                {"delay": 1800, "channels": [NotificationChannel.EMAIL, NotificationChannel.DISCORD]}
            ]
        )
    
    def _parse_config(self, config: Dict[str, Any]):
        """Parse configuration data."""
        # Parse notification configs
        for channel_config in config.get("notification_channels", []):
            channel = NotificationChannel(channel_config["channel"])
            self.notification_configs[channel] = NotificationConfig(
                channel=channel,
                endpoint=channel_config["endpoint"],
                credentials=channel_config["credentials"],
                enabled=channel_config.get("enabled", True),
                rate_limit=channel_config.get("rate_limit", 100)
            )
        
        # Parse escalation policies
        for policy_config in config.get("escalation_policies", []):
            policy = EscalationPolicy(
                id=policy_config["id"],
                name=policy_config["name"],
                levels=policy_config["levels"],
                max_escalations=policy_config.get("max_escalations", 3)
            )
            self.escalation_policies[policy.id] = policy
    
    def _init_notification_handlers(self):
        """Initialize notification channel handlers."""
        self.notification_handlers = {
            NotificationChannel.EMAIL: self._send_email_notification,
            NotificationChannel.DISCORD: self._send_discord_notification,
            NotificationChannel.SLACK: self._send_slack_notification,
            NotificationChannel.WEBHOOK: self._send_webhook_notification,
            NotificationChannel.SMS: self._send_sms_notification
        }
    
    def create_alert(self, title: str, description: str, severity: AlertSeverity,
                    source: str, category: str, metadata: Dict[str, Any] = None) -> str:
        """Create a new alert."""
        alert_id = f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.alerts)}"
        
        alert = Alert(
            id=alert_id,
            title=title,
            description=description,
            severity=severity,
            source=source,
            category=category,
            created_at=datetime.now(),
            metadata=metadata or {}
        )
        
        self.alerts[alert_id] = alert
        self.alert_history.append(alert)
        
        # Process alert through rules
        self._process_alert(alert)
        
        self.logger.info(f"Created alert {alert_id}: {title}")
        return alert_id
    
    def _process_alert(self, alert: Alert):
        """Process alert through rules and send notifications."""
        # Check rules
        for rule in self.rules.values():
            if rule.enabled and self._evaluate_rule(rule, alert):
                self._send_notifications(alert, rule.channels)
        
        # Check for escalation
        self._check_escalation(alert)
    
    def _evaluate_rule(self, rule: AlertRule, alert: Alert) -> bool:
        """Evaluate if alert matches rule condition."""
        # Simple condition evaluation (can be extended)
        try:
            # Check severity
            if rule.severity != alert.severity:
                return False
            
            # Check category
            if "category" in rule.condition:
                if alert.category not in rule.condition:
                    return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error evaluating rule {rule.id}: {e}")
            return False
    
    def _send_notifications(self, alert: Alert, channels: List[NotificationChannel]):
        """Send notifications to specified channels."""
        for channel in channels:
            if channel in self.notification_handlers:
                try:
                    self.notification_handlers[channel](alert)
                except Exception as e:
                    self.logger.error(f"Failed to send {channel} notification: {e}")
    
    def _send_email_notification(self, alert: Alert):
        """Send email notification."""
        # Placeholder for email sending
        self.logger.info(f"Email notification sent for alert {alert.id}")
    
    def _send_discord_notification(self, alert: Alert):
        """Send Discord notification."""
        # Placeholder for Discord webhook
        self.logger.info(f"Discord notification sent for alert {alert.id}")
    
    def _send_slack_notification(self, alert: Alert):
        """Send Slack notification."""
        # Placeholder for Slack webhook
        self.logger.info(f"Slack notification sent for alert {alert.id}")
    
    def _send_webhook_notification(self, alert: Alert):
        """Send webhook notification."""
        # Placeholder for webhook
        self.logger.info(f"Webhook notification sent for alert {alert.id}")
    
    def _send_sms_notification(self, alert: Alert):
        """Send SMS notification."""
        # Placeholder for SMS
        self.logger.info(f"SMS notification sent for alert {alert.id}")
    
    def _check_escalation(self, alert: Alert):
        """Check if alert needs escalation."""
        # Simple escalation logic
        if alert.status == AlertStatus.ACTIVE:
            time_since_creation = datetime.now() - alert.created_at
            if time_since_creation.total_seconds() > 300:  # 5 minutes
                self._escalate_alert(alert)
    
    def _escalate_alert(self, alert: Alert):
        """Escalate alert to higher severity."""
        if alert.severity == AlertSeverity.LOW:
            alert.severity = AlertSeverity.MEDIUM
        elif alert.severity == AlertSeverity.MEDIUM:
            alert.severity = AlertSeverity.HIGH
        elif alert.severity == AlertSeverity.HIGH:
            alert.severity = AlertSeverity.CRITICAL
        
        self.logger.info(f"Escalated alert {alert.id} to {alert.severity.value}")
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert."""
        if alert_id in self.alerts:
            alert = self.alerts[alert_id]
            alert.status = AlertStatus.ACKNOWLEDGED
            alert.acknowledged_by = acknowledged_by
            alert.acknowledged_at = datetime.now()
            self.logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
            return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        if alert_id in self.alerts:
            alert = self.alerts[alert_id]
            alert.status = AlertStatus.RESOLVED
            alert.resolved_at = datetime.now()
            self.logger.info(f"Alert {alert_id} resolved")
            return True
        return False
    
    def get_alerts(self, status: AlertStatus = None, severity: AlertSeverity = None) -> List[Alert]:
        """Get alerts with optional filtering."""
        alerts = list(self.alerts.values())
        
        if status:
            alerts = [a for a in alerts if a.status == status]
        
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        
        return sorted(alerts, key=lambda x: x.created_at, reverse=True)
    
    def get_alert_analytics(self) -> Dict[str, Any]:
        """Get alert analytics."""
        total_alerts = len(self.alerts)
        active_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.ACTIVE])
        resolved_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.RESOLVED])
        
        severity_counts = {}
        for severity in AlertSeverity:
            severity_counts[severity.value] = len([
                a for a in self.alerts.values() if a.severity == severity
            ])
        
        return {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "resolved_alerts": resolved_alerts,
            "severity_distribution": severity_counts,
            "resolution_rate": resolved_alerts / total_alerts if total_alerts > 0 else 0
        }
    
    def add_rule(self, rule: AlertRule):
        """Add an alert rule."""
        self.rules[rule.id] = rule
        self.logger.info(f"Added rule {rule.id}: {rule.name}")
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove an alert rule."""
        if rule_id in self.rules:
            del self.rules[rule_id]
            self.logger.info(f"Removed rule {rule_id}")
            return True
        return False
    
    def save_config(self, config_path: str):
        """Save configuration to file."""
        config = {
            "notification_channels": [
                {
                    "channel": nc.channel.value,
                    "endpoint": nc.endpoint,
                    "credentials": nc.credentials,
                    "enabled": nc.enabled,
                    "rate_limit": nc.rate_limit
                }
                for nc in self.notification_configs.values()
            ],
            "escalation_policies": [
                {
                    "id": ep.id,
                    "name": ep.name,
                    "levels": ep.levels,
                    "max_escalations": ep.max_escalations
                }
                for ep in self.escalation_policies.values()
            ]
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2, default=str)
    
    def export_alerts(self, file_path: str):
        """Export alerts to JSON file."""
        alerts_data = []
        for alert in self.alerts.values():
            alert_data = {
                "id": alert.id,
                "title": alert.title,
                "description": alert.description,
                "severity": alert.severity.value,
                "source": alert.source,
                "category": alert.category,
                "status": alert.status.value,
                "created_at": alert.created_at.isoformat(),
                "acknowledged_by": alert.acknowledged_by,
                "acknowledged_at": alert.acknowledged_at.isoformat() if alert.acknowledged_at else None,
                "resolved_at": alert.resolved_at.isoformat() if alert.resolved_at else None,
                "metadata": alert.metadata
            }
            alerts_data.append(alert_data)
        
        with open(file_path, 'w') as f:
            json.dump(alerts_data, f, indent=2, default=str)


