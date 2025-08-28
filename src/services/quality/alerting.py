"""Alerting utilities for the quality monitoring system."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Dict, List

from .config import DEFAULT_ALERT_RULES
from .models import QualityAlert

logger = logging.getLogger(__name__)


class QualityAlertManager:
    """Manage quality alerts and notification history."""

    def __init__(self) -> None:
        self.alerts: Dict[str, QualityAlert] = {}
        self.alert_history: List[QualityAlert] = []
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._setup_default_rules()

    def _setup_default_rules(self) -> None:
        """Initialize default alert rules."""
        self.alert_rules = DEFAULT_ALERT_RULES.copy()

    def create_alert(
        self,
        service_id: str,
        alert_type: str,
        metric_value: Any,
        threshold: Any,
        custom_message: str | None = None,
    ) -> str:
        """Create a new quality alert and store it."""
        try:
            alert_id = f"alert_{service_id}_{alert_type}_{int(time.time())}"
            rule = self.alert_rules.get(alert_type, {})
            severity = rule.get("severity", "medium")
            message = custom_message or rule.get(
                "message", f"Quality alert: {alert_type}"
            )
            alert = QualityAlert(
                alert_id=alert_id,
                service_id=service_id,
                alert_type=alert_type,
                severity=severity,
                message=message,
                timestamp=time.time(),
                metric_value=metric_value,
                threshold=threshold,
            )
            with self._lock:
                self.alerts[alert_id] = alert
                self.alert_history.append(alert)
            logger.warning("Quality alert created: %s - %s", alert_id, message)
            return alert_id
        except Exception as exc:
            logger.error("Failed to create alert: %s", exc)
            return ""
