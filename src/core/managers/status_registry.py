"""Centralized storage for status items and events."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import asdict
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any

from .status_entities import StatusItem, StatusEvent, StatusMetrics
from .status_types import StatusLevel, StatusEventType


class StatusRegistry:
    """Manage status items and events with thread safety."""

    def __init__(self, max_history: int = 1000) -> None:
        self.max_history = max_history
        self.status_items: Dict[str, StatusItem] = {}
        self.status_events: Dict[str, StatusEvent] = {}
        self.status_lock = threading.Lock()
        self._event_callback: Optional[Callable[[str, Dict[str, Any]], None]] = None

    def set_event_callback(
        self, callback: Callable[[str, Dict[str, Any]], None]
    ) -> None:
        """Register callback for emitted events."""
        self._event_callback = callback

    # ------------------------------------------------------------------
    # Status Item Operations
    # ------------------------------------------------------------------
    def add_status(
        self,
        component: str,
        status: str,
        level: StatusLevel,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Add a new status item and emit corresponding event."""
        with self.status_lock:
            status_id = str(uuid.uuid4())
            item = StatusItem(
                id=status_id,
                component=component,
                status=status,
                level=level,
                message=message,
                timestamp=datetime.now().isoformat(),
                duration=None,
                metadata=metadata or {},
                resolved=False,
                resolution_time=None,
            )
            self.status_items[status_id] = item

            event = StatusEvent(
                event_id=f"event_{int(time.time())}_{len(self.status_events)}",
                component_id=component,
                event_type=StatusEventType.STATUS_CHANGE,
                old_status=None,
                new_status=status,
                message=message,
                timestamp=datetime.now().isoformat(),
                metadata=metadata or {},
            )
            self.status_events[event.event_id] = event

            if self._event_callback:
                self._event_callback("status_event", asdict(event))

            self._cleanup_old_status_items()
            return status_id

    def get_status(
        self, component: Optional[str] = None
    ) -> Optional[StatusItem | List[StatusItem]]:
        """Retrieve status for a component or all statuses."""
        with self.status_lock:
            if component:
                items = [
                    i for i in self.status_items.values() if i.component == component
                ]
                return items[-1] if items else None
            return list(self.status_items.values())

    def resolve_status(self, status_id: str, resolution_message: str) -> bool:
        """Mark a status item as resolved."""
        with self.status_lock:
            if status_id in self.status_items:
                item = self.status_items[status_id]
                item.resolved = True
                item.resolution_time = datetime.now().isoformat()
                item.message = resolution_message
                return True
            return False

    def get_active_alerts(self) -> List[StatusItem]:
        """Return unresolved warning/error/critical statuses."""
        with self.status_lock:
            return [
                item
                for item in self.status_items.values()
                if item.level
                in [StatusLevel.WARNING, StatusLevel.ERROR, StatusLevel.CRITICAL]
                and not item.resolved
            ]

    def get_summary(self, uptime_seconds: float) -> StatusMetrics:
        """Generate summary metrics for current statuses."""
        with self.status_lock:
            total = len(self.status_items)
            healthy = len(
                [
                    i
                    for i in self.status_items.values()
                    if i.level == StatusLevel.SUCCESS
                ]
            )
            warning = len(
                [
                    i
                    for i in self.status_items.values()
                    if i.level == StatusLevel.WARNING
                ]
            )
            error = len(
                [i for i in self.status_items.values() if i.level == StatusLevel.ERROR]
            )
            critical = len(
                [
                    i
                    for i in self.status_items.values()
                    if i.level == StatusLevel.CRITICAL
                ]
            )
            return StatusMetrics(
                total_components=total,
                healthy_components=healthy,
                warning_components=warning,
                error_components=error,
                critical_components=critical,
                last_update=datetime.now().isoformat(),
                uptime_seconds=uptime_seconds,
            )

    # ------------------------------------------------------------------
    # Maintenance & Persistence
    # ------------------------------------------------------------------
    def _cleanup_old_status_items(self) -> None:
        if len(self.status_items) > self.max_history:
            sorted_items = sorted(
                self.status_items.items(), key=lambda x: x[1].timestamp
            )
            for key, _ in sorted_items[: len(self.status_items) - self.max_history]:
                del self.status_items[key]

    def clear(self) -> None:
        with self.status_lock:
            self.status_items.clear()
            self.status_events.clear()

    def backup(self) -> Dict[str, Dict[str, Any]]:
        with self.status_lock:
            return {
                "status_items": {k: asdict(v) for k, v in self.status_items.items()},
                "status_events": {k: asdict(v) for k, v in self.status_events.items()},
            }

    def restore(self, data: Dict[str, Dict[str, Any]]) -> None:
        with self.status_lock:
            for k, v in data.get("status_items", {}).items():
                self.status_items[k] = StatusItem(**v)
            for k, v in data.get("status_events", {}).items():
                self.status_events[k] = StatusEvent(**v)
