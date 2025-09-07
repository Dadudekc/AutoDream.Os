"""Status broadcast and update utilities."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Dict, Optional

from ..status_entities import ComponentHealth
from ..status_types import HealthStatus
from ..health_monitor import HealthMonitor


class StatusBroadcaster:
    """Manage health checks and broadcast updates."""

    def __init__(
        self,
        interval: int,
        event_callback: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ) -> None:
        self.health_monitor = HealthMonitor(interval)
        self.component_health: Dict[str, ComponentHealth] = {}
        self.health_monitor.setup_default_checks()
        self._event_callback = event_callback

    def set_event_callback(
        self, callback: Callable[[str, Dict[str, Any]], None]
    ) -> None:
        """Register callback for health update broadcasts."""
        self._event_callback = callback

    def register_health_check(
        self, name: str, check: Callable[[], HealthStatus]
    ) -> None:
        self.health_monitor.register_health_check(name, check)

    def run_health_checks(self) -> Dict[str, HealthStatus]:
        results = self.health_monitor.run_checks()
        for name, status in results.items():
            self.component_health[name] = ComponentHealth(
                component_id=name,
                name=name,
                status=status,
                last_check=datetime.now().isoformat(),
                uptime=0.0,
                response_time=0.0,
                error_count=0,
                success_rate=1.0,
                metrics=[],
                dependencies=[],
            )
            if self._event_callback:
                self._event_callback(
                    "health_check",
                    {"component_id": name, "status": status.value},
                )
        return results

    def get_health_status(self, component_id: str) -> Optional[ComponentHealth]:
        return self.component_health.get(component_id)

    def start(self, interval: int) -> None:
        self.health_monitor.interval = interval
        self.health_monitor.start()

    def stop(self) -> None:
        self.health_monitor.stop()

    def clear(self) -> None:
        self.component_health.clear()
