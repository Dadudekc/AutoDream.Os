"""Status tracking utilities for manager system."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Union

from ..status_entities import StatusItem, StatusMetrics
from ..status_registry import StatusRegistry
from ..status_types import StatusLevel


class StatusTracker:
    """Track status items and component health."""

    def __init__(self, max_history: int) -> None:
        self.registry = StatusRegistry(max_history)

    def set_event_callback(
        self, callback: Callable[[str, Dict[str, Any]], None]
    ) -> None:
        self.registry.set_event_callback(callback)

    def add_status(
        self,
        component: str,
        status: str,
        level: StatusLevel,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        return self.registry.add_status(component, status, level, message, metadata)

    def get_status(
        self, component: Optional[str] = None
    ) -> Union[StatusItem, List[StatusItem], None]:
        return self.registry.get_status(component)

    def resolve_status(
        self, status_id: str, resolution_message: str = "Resolved"
    ) -> bool:
        return self.registry.resolve_status(status_id, resolution_message)

    def get_active_alerts(self) -> List[StatusItem]:
        return self.registry.get_active_alerts()

    def get_status_summary(self, uptime_seconds: float) -> StatusMetrics:
        return self.registry.get_summary(uptime_seconds)

    def clear(self) -> None:
        self.registry.clear()
