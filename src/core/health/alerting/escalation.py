from datetime import datetime, timedelta
from typing import Dict, Optional

from .channel_dispatch import dispatch_to_channels
from .logging_utils import logger
from .models import (
    HealthAlert,
    AlertStatus,
    EscalationLevel,
    EscalationPolicy,
    NotificationChannel,
    NotificationConfig,
)


def get_next_escalation_level(current_level: EscalationLevel) -> Optional[EscalationLevel]:
    levels = [
        EscalationLevel.LEVEL_1,
        EscalationLevel.LEVEL_2,
        EscalationLevel.LEVEL_3,
        EscalationLevel.LEVEL_4,
    ]
    try:
        idx = levels.index(current_level)
        if idx + 1 < len(levels):
            return levels[idx + 1]
    except ValueError:
        logger.error(f"Unknown escalation level: {current_level}")
    return None


def send_escalation_notifications(
    alert: HealthAlert,
    policy: EscalationPolicy,
    configs: Dict[NotificationChannel, NotificationConfig],
) -> None:
    dispatch_to_channels(
        alert, policy.notification_channels, configs, policy.contacts
    )


def escalate_alert(
    alert: HealthAlert,
    policy: EscalationPolicy,
    configs: Dict[NotificationChannel, NotificationConfig],
) -> None:
    try:
        next_level = get_next_escalation_level(alert.escalation_level)
        if next_level:
            alert.escalation_level = next_level
            alert.metadata["escalated_at"] = datetime.now().isoformat()
            send_escalation_notifications(alert, policy, configs)
            logger.info(
                f"Alert {alert.alert_id} escalated to {next_level.value}"
            )
    except Exception as e:
        logger.error(f"Error escalating alert {alert.alert_id}: {e}")


def check_escalations(
    alerts: Dict[str, HealthAlert],
    policies: Dict[EscalationLevel, EscalationPolicy],
    configs: Dict[NotificationChannel, NotificationConfig],
) -> None:
    current_time = datetime.now()
    for alert in alerts.values():
        if alert.status != AlertStatus.ACTIVE:
            continue
        policy = policies.get(alert.escalation_level)
        if not policy or not policy.auto_escalate:
            continue
        delay = timedelta(minutes=policy.delay_minutes)
        if current_time - alert.timestamp >= delay:
            escalate_alert(alert, policy, configs)
