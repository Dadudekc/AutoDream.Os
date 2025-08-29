"""Delivery channels for gaming alerts."""
from __future__ import annotations

import logging
from typing import Protocol

from src.core.health_models import AlertSeverity
from .state import GamingAlert


class AlertChannel(Protocol):
    """Protocol for alert delivery channels."""

    def send(self, alert: GamingAlert) -> None:
        ...


class LoggerChannel:
    """Simple logging-based alert delivery."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def send(self, alert: GamingAlert) -> None:
        level = {
            AlertSeverity.INFO: logging.INFO,
            AlertSeverity.WARNING: logging.WARNING,
            AlertSeverity.ERROR: logging.ERROR,
            AlertSeverity.CRITICAL: logging.CRITICAL,
            AlertSeverity.EMERGENCY: logging.CRITICAL,
        }.get(alert.severity, logging.INFO)
        self.logger.log(
            level,
            f"[{alert.system_id}] {alert.metric} {alert.severity.value}: "
            f"{alert.value} (threshold {alert.threshold})",
        )
