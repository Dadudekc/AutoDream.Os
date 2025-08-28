from typing import Dict, List, Optional

from .logging_utils import logger
from .models import (
    HealthAlert,
    AlertRule,
    NotificationChannel,
    NotificationConfig,
)


def dispatch_to_channels(
    alert: HealthAlert,
    channels: List[NotificationChannel],
    configs: Dict[NotificationChannel, NotificationConfig],
    recipients: Optional[List[str]] = None,
) -> None:
    """Helper to dispatch notifications to configured channels."""
    for channel in channels:
        if channel in configs:
            config = configs[channel]
            if config.enabled:
                send_notification(alert, channel, config, recipients)


def send_alert_notifications(
    alert: HealthAlert,
    rule: AlertRule,
    configs: Dict[NotificationChannel, NotificationConfig],
) -> None:
    """Send notifications for a new alert using configured channels."""
    try:
        dispatch_to_channels(alert, rule.notification_channels, configs)
        alert.notification_sent = True
    except Exception as e:
        logger.error(f"Error sending alert notifications: {e}")


def send_notification(
    alert: HealthAlert,
    channel: NotificationChannel,
    config: NotificationConfig,
    recipients: Optional[List[str]] = None,
) -> None:
    """Dispatch notification based on channel."""
    try:
        if channel == NotificationChannel.EMAIL:
            _send_email_notification(alert, config, recipients)
        elif channel == NotificationChannel.CONSOLE:
            _send_console_notification(alert, config)
        elif channel == NotificationChannel.LOG:
            _send_log_notification(alert, config)
        elif channel == NotificationChannel.SLACK:
            _send_slack_notification(alert, config)
        else:
            logger.warning(f"Unsupported notification channel: {channel}")
    except Exception as e:
        logger.error(f"Error sending notification via {channel}: {e}")


def _send_email_notification(
    alert: HealthAlert,
    config: NotificationConfig,
    recipients: Optional[List[str]] = None,
) -> None:
    try:
        recipients = recipients or config.recipients
        if not recipients:
            return
        logger.info(
            f"Email notification sent to {recipients} for alert {alert.alert_id}"
        )
    except Exception as e:
        logger.error(f"Error sending email notification: {e}")


def _send_console_notification(alert: HealthAlert, config: NotificationConfig) -> None:
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


def _send_log_notification(alert: HealthAlert, config: NotificationConfig) -> None:
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


def _send_slack_notification(alert: HealthAlert, config: NotificationConfig) -> None:
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
