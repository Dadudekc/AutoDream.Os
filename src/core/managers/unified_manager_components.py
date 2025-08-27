"""Supporting types for the simplified unified manager system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Type

from ..base_manager import BaseManager, ManagerPriority, ManagerStatus


class _BasicManager(BaseManager):
    """Minimal concrete manager used for registration examples."""

    def __init__(self, manager_id: str, name: str):
        super().__init__(manager_id, name)

    def start(self) -> bool:  # pragma: no cover - trivial
        self.lifecycle.running = True
        return True

    def stop(self) -> bool:  # pragma: no cover - trivial
        self.lifecycle.running = False
        return True

    def is_healthy(self) -> bool:  # pragma: no cover - trivial
        return True

    # -- BaseManager abstract hooks -------------------------------------
    def _on_initialize_resources(self) -> bool:  # pragma: no cover - simple
        return True

    def _on_cleanup_resources(self) -> bool:  # pragma: no cover - simple
        return True

    def _on_start(self) -> bool:  # pragma: no cover - simple
        return True

    def _on_stop(self) -> bool:  # pragma: no cover - simple
        return True

    def _on_heartbeat(self) -> None:  # pragma: no cover - simple
        pass

    def _on_recovery_attempt(self) -> bool:  # pragma: no cover - simple
        return True


class SystemManager(_BasicManager):
    """Placeholder for the core system manager."""


class AIManager(_BasicManager):
    """Placeholder for an extended AI manager."""


class AlertManager(_BasicManager):
    """Placeholder for a specialised alert manager."""


@dataclass
class ManagerRegistration:
    """Metadata describing a registered manager."""

    manager_id: str
    manager_class: Type[BaseManager]
    instance: Optional[BaseManager]
    status: ManagerStatus
    priority: ManagerPriority
    dependencies: List[str]
    config_path: Optional[str]
    last_health_check: datetime = field(default_factory=datetime.now)
    category: str = "core"
    version: str = "1.0.0"

