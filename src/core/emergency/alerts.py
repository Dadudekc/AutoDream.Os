"""Alerting and notification utilities for emergency protocols."""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def send_alert(alert_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
    """Send an alert or notification.

    This function centralizes alerting logic so that protocol execution and
    escalation procedures can trigger notifications without embedding the
    implementation details.
    """
    logger.info(f"Alert triggered: {alert_type}", extra={"details": details})
    return {"status": "sent", "alert_type": alert_type, **details}


__all__ = ["send_alert"]
