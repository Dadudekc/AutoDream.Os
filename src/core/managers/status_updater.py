"""Status update logic and health monitoring."""

from __future__ import annotations

from datetime import datetime
from typing import Callable, Dict, Optional

from .status_entities import ComponentHealth
from .status_types import HealthStatus
from .health_monitor import HealthMonitor


class StatusUpdater:
    """Manage health checks and component health state."""

    def __init__(self, interval: int) -> None:
        self.health_monitor = HealthMonitor(interval)
        self.component_health: Dict[str, ComponentHealth] = {}
        self.health_monitor.setup_default_checks()

    def register_health_check(
        self, name: str, check: Callable[[], HealthStatus]
    ) -> None:
        self.health_monitor.register_health_check(name, check)

    def run_health_checks(self) -> Dict[str, HealthStatus]:
        results = self.health_monitor.run_checks()
        for name, status in results.items():
            self.component_health[name] = ComponentHealth(
                component_id=name,
                status=status,
                last_check=datetime.now().isoformat(),
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
