"""Helpers for reading status and health information."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from .status_entities import ComponentHealth, StatusItem, StatusMetrics
from .status_registry import StatusRegistry


class StatusTracker:
    """Provide read-only access to status information."""

    def __init__(
        self, registry: StatusRegistry, component_health: Dict[str, ComponentHealth]
    ):
        self._registry = registry
        self._component_health = component_health

    def get_status(self, component: Optional[str] = None):
        """Return status for a component or all statuses."""
        return self._registry.get_status(component)

    def get_health_status(self, component_id: str) -> Optional[ComponentHealth]:
        """Return health status for a component."""
        return self._component_health.get(component_id)

    def get_status_summary(self, startup_time: Optional[datetime]) -> StatusMetrics:
        """Return summary metrics including uptime."""
        uptime = (
            (datetime.now() - startup_time).total_seconds() if startup_time else 0.0
        )
        return self._registry.get_summary(uptime)

    def get_active_alerts(self) -> List[StatusItem]:
        """Return unresolved warning/error/critical statuses."""
        return self._registry.get_active_alerts()


__all__ = ["StatusTracker"]
