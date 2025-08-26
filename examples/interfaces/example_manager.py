"""Example implementation of BaseManager."""

from src.core.base_manager import BaseManager


class ExampleManager(BaseManager):
    """Minimal manager implementation for demonstration purposes."""

    def _on_start(self) -> bool:
        return True

    def _on_stop(self) -> None:  # pragma: no cover - example method
        return None

    def _on_heartbeat(self) -> None:  # pragma: no cover - example method
        return None

    def _on_initialize_resources(self) -> bool:
        return True

    def _on_cleanup_resources(self) -> None:  # pragma: no cover - example method
        return None

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        return False
