"""Quality alert management module."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Dict, List

from .config import DEFAULT_ALERT_RULES
from .models import QualityAlert

logger = logging.getLogger(__name__)


class QualityAlertManager:
    """Creates and tracks quality alerts."""

    def __init__(self) -> None:
        self.alerts: Dict[str, QualityAlert] = {}
        self.alert_history: List[QualityAlert] = []
        self.alert_rules: Dict[str, Dict[str, Any]] = dict(DEFAULT_ALERT_RULES)
        self._lock = threading.Lock()
        logger.info("Quality Alert Manager initialized")

    def create_alert(
        self,
        service_id: str,
        alert_type: str,
        metric_value: Any,
        threshold: Any,
        custom_message: str | None = None,
    ) -> str:
        """Create and store a new alert."""
        try:
            alert_id = f"alert_{service_id}_{alert_type}_{int(time.time())}"
            rule = self.alert_rules.get(alert_type, {})
            severity = rule.get("severity", "medium")
            message = custom_message or rule.get("message", f"Quality alert: {alert_type}")
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
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to create alert: %s", exc)
            return ""

    def resolve_alert(self, alert_id: str) -> bool:
        """Mark the specified alert as resolved."""
        try:
            with self._lock:
                if alert_id in self.alerts:
                    self.alerts[alert_id].resolved = True
                    logger.info("Alert %s marked as resolved", alert_id)
                    return True
            return False
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to resolve alert %s: %s", alert_id, exc)
            return False

    def get_active_alerts(self, service_id: str | None = None) -> List[QualityAlert]:
        """Return unresolved alerts, optionally filtered by service."""
        with self._lock:
            if service_id:
                return [a for a in self.alerts.values() if not a.resolved and a.service_id == service_id]
            return [a for a in self.alerts.values() if not a.resolved]

    def get_alert_history(self, service_id: str | None = None, alert_type: str | None = None) -> List[QualityAlert]:
        """Return historical alerts with optional filters."""
        with self._lock:
            filtered_alerts = list(self.alert_history)
            if service_id:
                filtered_alerts = [a for a in filtered_alerts if a.service_id == service_id]
            if alert_type:
                filtered_alerts = [a for a in filtered_alerts if a.alert_type == alert_type]
            return filtered_alerts

    def add_alert_rule(self, alert_type: str, threshold: Any, severity: str, message: str) -> bool:
        """Add or update an alert rule."""
        try:
            self.alert_rules[alert_type] = {
                "threshold": threshold,
                "severity": severity,
                "message": message,
            }
            logger.info("Alert rule added: %s", alert_type)
            return True
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to add alert rule: %s", exc)
            return False


__all__ = ["QualityAlertManager"]
