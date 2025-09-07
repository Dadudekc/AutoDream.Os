"""Utilities for detecting and generating health alerts."""

import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from .logging_utils import logger
from .models import AlertRule, AlertSeverity, HealthAlert, AlertStatus


def should_suppress_alert(alerts: Dict[str, HealthAlert], agent_id: str, metric_type: str, severity: AlertSeverity) -> bool:
    """Check if an alert should be suppressed due to cooldown."""
    try:
        current_time = datetime.now()
        for alert in alerts.values():
            if (
                alert.agent_id == agent_id
                and alert.metric_type == metric_type
                and alert.severity == severity
                and alert.status == AlertStatus.ACTIVE
            ):
                time_since_creation = current_time - alert.timestamp
                cooldown_period = timedelta(seconds=300)
                if time_since_creation < cooldown_period:
                    return True
    except Exception as e:
        logger.error(f"Error checking alert suppression: {e}")
    return False


def rule_matches_alert(rule: AlertRule, alert: HealthAlert) -> bool:
    """Check if an alert rule matches an alert."""
    try:
        conditions = rule.conditions
        if conditions.get("metric") != alert.metric_type:
            return False
        if rule.severity != alert.severity:
            return False
        if "operator" in conditions and "threshold" in conditions:
            operator = conditions["operator"]
            threshold = conditions["threshold"]
            if operator == ">" and alert.current_value <= threshold:
                return False
            if operator == "<" and alert.current_value >= threshold:
                return False
            if operator == ">=" and alert.current_value < threshold:
                return False
            if operator == "<=" and alert.current_value > threshold:
                return False
            if operator == "==" and alert.current_value != threshold:
                return False
        return True
    except Exception as e:
        logger.error(f"Error matching rule to alert: {e}")
        return False


def find_applicable_rule(alert_rules: Dict[str, AlertRule], alert: HealthAlert) -> Optional[AlertRule]:
    """Find the alert rule that applies to this alert."""
    try:
        for rule in alert_rules.values():
            if rule.enabled and rule_matches_alert(rule, alert):
                return rule
    except Exception as e:
        logger.error(f"Error finding applicable rule: {e}")
    return None


def generate_alert(
    agent_id: str,
    severity: AlertSeverity,
    message: str,
    metric_type: str,
    current_value: float,
    threshold: float,
    metadata: Optional[Dict[str, Any]] = None,
) -> HealthAlert:
    """Generate a new HealthAlert instance."""
    alert_id = f"health_alert_{agent_id}_{metric_type}_{int(time.time())}"
    return HealthAlert(
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
