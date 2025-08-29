"""Notification helpers for workspace health monitoring."""
from __future__ import annotations

from typing import List


class AlertManager:
    """Collects alert messages for later inspection."""

    def __init__(self) -> None:
        self._alerts: List[str] = []

    def notify(self, message: str) -> None:
        """Store an alert message."""
        self._alerts.append(message)

    def history(self) -> List[str]:
        """Return all previously stored alerts."""
        return list(self._alerts)
