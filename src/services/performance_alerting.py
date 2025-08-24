"""
Performance Alerting System for Agent_Cellphone_V2_Repository
Comprehensive alerting system with multiple notification channels.
"""

import asyncio
import json
import logging
import smtplib
import time

from src.utils.stability_improvements import stability_manager, safe_import
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any, Dict, List, Optional, Union
import aiohttp
from urllib.parse import urljoin

# Import from our performance monitor
from .performance_monitor import PerformanceAlert, AlertSeverity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AlertRule:
    """Alert rule definition (imported from performance_monitor)."""

    name: str
    metric_name: str
    condition: str  # AlertCondition enum value
    threshold: Union[float, int]
    severity: AlertSeverity
    description: str = ""
    enabled: bool = True
    tags_filter: Dict[str, str] = field(default_factory=dict)
    cooldown_period: int = 300  # 5 minutes default
    consecutive_violations: int = 1
    channels: List[str] = field(default_factory=list)  # Channel names to notify


class AlertChannel(ABC):
    """Abstract base class for alert notification channels."""

    def __init__(self, name: str, enabled: bool = True):
        self.name = name
        self.enabled = enabled
        self.min_severity = AlertSeverity.INFO
        self.max_severity = AlertSeverity.EMERGENCY
        self.rate_limit_seconds = 60  # Minimum time between alerts
        self.last_alert_time: Dict[str, float] = {}

    @abstractmethod
    async def send_alert(self, alert: PerformanceAlert) -> bool:
        """Send alert through this channel. Returns True if successful."""
        pass

    def should_send_alert(self, alert: PerformanceAlert) -> bool:
        """Check if alert should be sent through this channel."""
        if not self.enabled:
            return False

        # Check severity range
        severity_levels = {
            AlertSeverity.INFO: 1,
            AlertSeverity.WARNING: 2,
            AlertSeverity.CRITICAL: 3,
            AlertSeverity.EMERGENCY: 4,
        }

        alert_level = severity_levels.get(alert.severity, 1)
        min_level = severity_levels.get(self.min_severity, 1)
        max_level = severity_levels.get(self.max_severity, 4)

        if alert_level < min_level or alert_level > max_level:
            return False

        # Check rate limiting
        alert_key = f"{alert.rule_name}_{alert.metric_name}"
        last_time = self.last_alert_time.get(alert_key, 0)

        if time.time() - last_time < self.rate_limit_seconds:
            return False

        return True

    def format_alert_message(self, alert: PerformanceAlert) -> str:
        """Format alert message for this channel."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(alert.timestamp))

        message = f"""
🚨 PERFORMANCE ALERT

Rule: {alert.rule_name}
Severity: {alert.severity.value.upper()}
Metric: {alert.metric_name}
Current Value: {alert.current_value}
Threshold: {alert.threshold}
Time: {timestamp}

Message: {alert.message}

Tags: {', '.join(f'{k}={v}' for k, v in alert.tags.items()) if alert.tags else 'None'}
Alert ID: {alert.alert_id}
        """.strip()

        return message


class EmailAlertChannel(AlertChannel):
    """Email notification channel for alerts."""

    def __init__(
        self,
        name: str,
        recipients: List[str],
        smtp_server: str,
        smtp_port: int = 587,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True,
        sender_email: Optional[str] = None,
    ):
        super().__init__(name)
        self.recipients = recipients
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.sender_email = sender_email or username or "noreply@agent-cellphone.local"

        logger.info(f"Email alert channel initialized: {name}")

    async def send_alert(self, alert: PerformanceAlert) -> bool:
        """Send alert via email."""
        if not self.should_send_alert(alert):
            return False

        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = ", ".join(self.recipients)
            msg[
                "Subject"
            ] = f"[{alert.severity.value.upper()}] Performance Alert: {alert.rule_name}"

            # Format message body
            body = self.format_alert_message(alert)
            msg.attach(MIMEText(body, "plain"))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()

                if self.username and self.password:
                    server.login(self.username, self.password)

                server.send_message(msg)

            # Update rate limiting
            alert_key = f"{alert.rule_name}_{alert.metric_name}"
            self.last_alert_time[alert_key] = time.time()

            logger.info(f"Email alert sent via {self.name}: {alert.rule_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email alert via {self.name}: {e}")
            return False


class SlackAlertChannel(AlertChannel):
    """Slack notification channel for alerts."""

    def __init__(
        self,
        name: str,
        webhook_url: str,
        channel: Optional[str] = None,
        username: str = "AlertBot",
        icon_emoji: str = ":warning:",
    ):
        super().__init__(name)
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji

        logger.info(f"Slack alert channel initialized: {name}")

    async def send_alert(self, alert: PerformanceAlert) -> bool:
        """Send alert via Slack webhook."""
        if not self.should_send_alert(alert):
            return False

        try:
            # Format Slack message
            color = self._get_alert_color(alert.severity)
            timestamp = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(alert.timestamp)
            )

            payload = {
                "username": self.username,
                "icon_emoji": self.icon_emoji,
                "attachments": [
                    {
                        "color": color,
                        "title": f"Performance Alert: {alert.rule_name}",
                        "text": alert.message,
                        "fields": [
                            {
                                "title": "Severity",
                                "value": alert.severity.value.upper(),
                                "short": True,
                            },
                            {
                                "title": "Metric",
                                "value": alert.metric_name,
                                "short": True,
                            },
                            {
                                "title": "Current Value",
                                "value": str(alert.current_value),
                                "short": True,
                            },
                            {
                                "title": "Threshold",
                                "value": str(alert.threshold),
                                "short": True,
                            },
                            {"title": "Time", "value": timestamp, "short": False},
                        ],
                        "footer": f"Alert ID: {alert.alert_id}",
                        "ts": int(alert.timestamp),
                    }
                ],
            }

            if self.channel:
                payload["channel"] = self.channel

            # Send to Slack
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 200:
                        # Update rate limiting
                        alert_key = f"{alert.rule_name}_{alert.metric_name}"
                        self.last_alert_time[alert_key] = time.time()

                        logger.info(
                            f"Slack alert sent via {self.name}: {alert.rule_name}"
                        )
                        return True
                    else:
                        logger.error(f"Slack webhook returned status {response.status}")
                        return False

        except Exception as e:
            logger.error(f"Failed to send Slack alert via {self.name}: {e}")
            return False

    def _get_alert_color(self, severity: AlertSeverity) -> str:
        """Get color for alert based on severity."""
        color_map = {
            AlertSeverity.INFO: "good",
            AlertSeverity.WARNING: "warning",
            AlertSeverity.CRITICAL: "danger",
            AlertSeverity.EMERGENCY: "#8B0000",  # Dark red
        }
        return color_map.get(severity, "warning")


class WebhookAlertChannel(AlertChannel):
    """Generic webhook notification channel for alerts."""

    def __init__(
        self,
        name: str,
        webhook_url: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        template: Optional[str] = None,
    ):
        super().__init__(name)
        self.webhook_url = webhook_url
        self.method = method.upper()
        self.headers = headers or {"Content-Type": "application/json"}
        self.template = template

        logger.info(f"Webhook alert channel initialized: {name}")

    async def send_alert(self, alert: PerformanceAlert) -> bool:
        """Send alert via generic webhook."""
        if not self.should_send_alert(alert):
            return False

        try:
            # Prepare payload
            if self.template:
                # Use custom template
                payload = self._format_with_template(alert)
            else:
                # Use default JSON format
                payload = {
                    "alert": {
                        "id": alert.alert_id,
                        "rule_name": alert.rule_name,
                        "metric_name": alert.metric_name,
                        "severity": alert.severity.value,
                        "current_value": alert.current_value,
                        "threshold": alert.threshold,
                        "message": alert.message,
                        "timestamp": alert.timestamp,
                        "tags": alert.tags,
                        "resolved": alert.resolved,
                    }
                }

            # Send webhook
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=self.method,
                    url=self.webhook_url,
                    json=payload,
                    headers=self.headers,
                ) as response:
                    if 200 <= response.status < 300:
                        # Update rate limiting
                        alert_key = f"{alert.rule_name}_{alert.metric_name}"
                        self.last_alert_time[alert_key] = time.time()

                        logger.info(
                            f"Webhook alert sent via {self.name}: {alert.rule_name}"
                        )
                        return True
                    else:
                        logger.error(f"Webhook returned status {response.status}")
                        return False

        except Exception as e:
            logger.error(f"Failed to send webhook alert via {self.name}: {e}")
            return False

    def _format_with_template(self, alert: PerformanceAlert) -> Dict[str, Any]:
        """Format alert using custom template."""
        # Simple template substitution
        template_str = self.template

        substitutions = {
            "alert_id": alert.alert_id,
            "rule_name": alert.rule_name,
            "metric_name": alert.metric_name,
            "severity": alert.severity.value,
            "current_value": str(alert.current_value),
            "threshold": str(alert.threshold),
            "message": alert.message,
            "timestamp": str(alert.timestamp),
            "tags": json.dumps(alert.tags),
        }

        for key, value in substitutions.items():
            template_str = template_str.replace(f"{{{key}}}", value)

        try:
            return json.loads(template_str)
        except json.JSONDecodeError:
            # Fallback to plain text
            return {"message": template_str}


class DiscordAlertChannel(AlertChannel):
    """Discord notification channel for alerts."""

    def __init__(self, name: str, webhook_url: str, username: str = "AlertBot"):
        super().__init__(name)
        self.webhook_url = webhook_url
        self.username = username

        logger.info(f"Discord alert channel initialized: {name}")

    async def send_alert(self, alert: PerformanceAlert) -> bool:
        """Send alert via Discord webhook."""
        if not self.should_send_alert(alert):
            return False

        try:
            # Format Discord message
            color = self._get_alert_color(alert.severity)
            timestamp = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(alert.timestamp)
            )

            payload = {
                "username": self.username,
                "embeds": [
                    {
                        "title": f"🚨 Performance Alert: {alert.rule_name}",
                        "description": alert.message,
                        "color": color,
                        "fields": [
                            {
                                "name": "Severity",
                                "value": alert.severity.value.upper(),
                                "inline": True,
                            },
                            {
                                "name": "Metric",
                                "value": alert.metric_name,
                                "inline": True,
                            },
                            {
                                "name": "Current Value",
                                "value": str(alert.current_value),
                                "inline": True,
                            },
                            {
                                "name": "Threshold",
                                "value": str(alert.threshold),
                                "inline": True,
                            },
                            {"name": "Time", "value": timestamp, "inline": False},
                        ],
                        "footer": {"text": f"Alert ID: {alert.alert_id}"},
                        "timestamp": time.strftime(
                            "%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(alert.timestamp)
                        ),
                    }
                ],
            }

            # Send to Discord
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 204:  # Discord returns 204 for success
                        # Update rate limiting
                        alert_key = f"{alert.rule_name}_{alert.metric_name}"
                        self.last_alert_time[alert_key] = time.time()

                        logger.info(
                            f"Discord alert sent via {self.name}: {alert.rule_name}"
                        )
                        return True
                    else:
                        logger.error(
                            f"Discord webhook returned status {response.status}"
                        )
                        return False

        except Exception as e:
            logger.error(f"Failed to send Discord alert via {self.name}: {e}")
            return False

    def _get_alert_color(self, severity: AlertSeverity) -> int:
        """Get color for Discord embed based on severity."""
        color_map = {
            AlertSeverity.INFO: 0x00FF00,  # Green
            AlertSeverity.WARNING: 0xFFFF00,  # Yellow
            AlertSeverity.CRITICAL: 0xFF0000,  # Red
            AlertSeverity.EMERGENCY: 0x8B0000,  # Dark red
        }
        return color_map.get(severity, 0xFFFF00)


class PagerDutyAlertChannel(AlertChannel):
    """PagerDuty notification channel for alerts."""

    def __init__(
        self,
        name: str,
        integration_key: str,
        api_url: str = "https://events.pagerduty.com/v2/enqueue",
    ):
        super().__init__(name)
        self.integration_key = integration_key
        self.api_url = api_url

        logger.info(f"PagerDuty alert channel initialized: {name}")

    async def send_alert(self, alert: PerformanceAlert) -> bool:
        """Send alert via PagerDuty Events API."""
        if not self.should_send_alert(alert):
            return False

        try:
            # Map severity to PagerDuty severity
            pd_severity = self._map_severity(alert.severity)

            payload = {
                "routing_key": self.integration_key,
                "event_action": "trigger",
                "dedup_key": f"{alert.rule_name}_{alert.metric_name}",
                "payload": {
                    "summary": f"Performance Alert: {alert.rule_name}",
                    "source": "agent-cellphone-v2",
                    "severity": pd_severity,
                    "custom_details": {
                        "metric_name": alert.metric_name,
                        "current_value": alert.current_value,
                        "threshold": alert.threshold,
                        "message": alert.message,
                        "tags": alert.tags,
                        "alert_id": alert.alert_id,
                    },
                },
            }

            # Send to PagerDuty
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload) as response:
                    if response.status == 202:  # PagerDuty returns 202 for accepted
                        # Update rate limiting
                        alert_key = f"{alert.rule_name}_{alert.metric_name}"
                        self.last_alert_time[alert_key] = time.time()

                        logger.info(
                            f"PagerDuty alert sent via {self.name}: {alert.rule_name}"
                        )
                        return True
                    else:
                        logger.error(f"PagerDuty API returned status {response.status}")
                        return False

        except Exception as e:
            logger.error(f"Failed to send PagerDuty alert via {self.name}: {e}")
            return False

    def _map_severity(self, severity: AlertSeverity) -> str:
        """Map AlertSeverity to PagerDuty severity."""
        severity_map = {
            AlertSeverity.INFO: "info",
            AlertSeverity.WARNING: "warning",
            AlertSeverity.CRITICAL: "error",
            AlertSeverity.EMERGENCY: "critical",
        }
        return severity_map.get(severity, "warning")


class PerformanceAlertManager:
    """Central manager for alert processing and routing."""

    def __init__(self):
        self.channels: Dict[str, AlertChannel] = {}
        self.alert_history: List[PerformanceAlert] = []
        self.max_history = 1000

        logger.info("Alert manager initialized")

    def add_channel(self, channel: AlertChannel):
        """Add an alert channel."""
        self.channels[channel.name] = channel
        logger.info(f"Added alert channel: {channel.name}")

    def remove_channel(self, channel_name: str):
        """Remove an alert channel."""
        if channel_name in self.channels:
            del self.channels[channel_name]
            logger.info(f"Removed alert channel: {channel_name}")

    def get_channel(self, channel_name: str) -> Optional[AlertChannel]:
        """Get an alert channel by name."""
        return self.channels.get(channel_name)

    async def send_alert(
        self, alert: PerformanceAlert, channel_names: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """Send alert through specified channels or all channels."""
        if channel_names is None:
            channels_to_use = list(self.channels.values())
        else:
            channels_to_use = [
                self.channels[name] for name in channel_names if name in self.channels
            ]

        results = {}

        # Send alert through each channel
        for channel in channels_to_use:
            try:
                success = await channel.send_alert(alert)
                results[channel.name] = success
            except Exception as e:
                logger.error(f"Error sending alert through channel {channel.name}: {e}")
                results[channel.name] = False

        # Add to history
        self.alert_history.append(alert)
        if len(self.alert_history) > self.max_history:
            self.alert_history = self.alert_history[-self.max_history :]

        return results

    def get_alert_history(self, limit: int = 100) -> List[PerformanceAlert]:
        """Get recent alert history."""
        return self.alert_history[-limit:]

    def get_active_channels(self) -> List[str]:
        """Get list of active channel names."""
        return [name for name, channel in self.channels.items() if channel.enabled]


class AlertingSystem:
    """Main alerting system that integrates with performance monitoring."""

    def __init__(self):
        self.alert_rules: List[AlertRule] = []
        self.alert_channels: List[AlertChannel] = []
        self.alert_manager = PerformanceAlertManager()
        self.active_alerts: Dict[str, PerformanceAlert] = {}

        logger.info("Alerting system initialized")

    def add_alert_rule(self, rule: AlertRule):
        """Add an alert rule."""
        self.alert_rules.append(rule)
        logger.info(f"Added alert rule: {rule.name}")

    def add_alert_channel(self, channel: AlertChannel):
        """Add an alert channel."""
        self.alert_channels.append(channel)
        self.alert_manager.add_channel(channel)
        logger.info(f"Added alert channel: {channel.name}")

    async def process_alert(self, alert: PerformanceAlert):
        """Process a triggered alert."""
        # Add to active alerts (for deduplication)
        self.active_alerts[alert.alert_id] = alert

        # Find the rule for this alert
        rule = None
        for r in self.alert_rules:
            if r.name == alert.rule_name:
                rule = r
                break

        # Determine which channels to use
        if rule and rule.channels:
            channel_names = rule.channels
        else:
            # Use all channels
            channel_names = None

        # Send alert
        results = await self.alert_manager.send_alert(alert, channel_names)

        logger.info(f"Alert processed: {alert.rule_name}, Results: {results}")

        return results

    async def send_alert(self, alert: PerformanceAlert):
        """Send alert through all channels."""
        return await self.alert_manager.send_alert(alert)

    def get_channels_for_alert(self, alert: PerformanceAlert) -> List[AlertChannel]:
        """Get channels that should receive this alert."""
        channels = []
        for channel in self.alert_channels:
            if channel.should_send_alert(alert):
                channels.append(channel)
        return channels


# Export all classes
__all__ = [
    "AlertRule",
    "AlertChannel",
    "EmailAlertChannel",
    "SlackAlertChannel",
    "WebhookAlertChannel",
    "DiscordAlertChannel",
    "PagerDutyAlertChannel",
    "PerformanceAlertManager",
    "AlertingSystem",
]
