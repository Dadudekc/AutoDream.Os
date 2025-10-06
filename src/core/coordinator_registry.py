#!/usr/bin/env python3
"""
Coordinator Registry Implementation - V2 Compliant Module
========================================================

Concrete implementation of ICoordinatorRegistry for managing coordinators.
V2 Compliance: < 200 lines, single responsibility.

Author: V2 Implementation Team
License: MIT
"""

from typing import Any, Dict, Optional

from .unified_logging_system import get_logger
from .coordinator_interfaces import ICoordinatorRegistry


class CoordinatorRegistry(ICoordinatorRegistry):
    """Concrete implementation of coordinator registry."""

    def __init__(self):
        """Initialize coordinator registry."""
        self.logger = get_logger(__name__)
        self._coordinators: Dict[str, Any] = {}
        self.logger.info("CoordinatorRegistry initialized")

    def register_coordinator(self, coordinator: Any) -> bool:
        """Register a coordinator instance."""
        try:
            if not hasattr(coordinator, 'name'):
                self.logger.error("Coordinator must have a 'name' attribute")
                return False

            coordinator_name = coordinator.name
            if coordinator_name in self._coordinators:
                self.logger.warning(f"Coordinator '{coordinator_name}' already registered")
                return False

            self._coordinators[coordinator_name] = coordinator
            self.logger.info(f"Registered coordinator: {coordinator_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error registering coordinator: {e}")
            return False

    def get_coordinator(self, name: str) -> Optional[Any]:
        """Get coordinator by name."""
        return self._coordinators.get(name)

    def get_all_coordinators(self) -> Dict[str, Any]:
        """Get all registered coordinators."""
        return self._coordinators.copy()

    def unregister_coordinator(self, name: str) -> bool:
        """Unregister a coordinator."""
        try:
            if name not in self._coordinators:
                self.logger.warning(f"Coordinator '{name}' not found")
                return False

            coordinator = self._coordinators[name]
            if hasattr(coordinator, 'shutdown'):
                coordinator.shutdown()

            del self._coordinators[name]
            self.logger.info(f"Unregistered coordinator: {name}")
            return True

        except Exception as e:
            self.logger.error(f"Error unregistering coordinator '{name}': {e}")
            return False

    def get_coordinator_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all coordinators."""
        try:
            statuses = {}
            for name, coordinator in self._coordinators.items():
                try:
                    if hasattr(coordinator, 'get_status'):
                        statuses[name] = coordinator.get_status()
                    else:
                        statuses[name] = {"status": "unknown", "error": "No get_status method"}
                except Exception as e:
                    statuses[name] = {"status": "error", "error": str(e)}

            return statuses

        except Exception as e:
            self.logger.error(f"Error getting coordinator statuses: {e}")
            return {}

    def shutdown_all_coordinators(self) -> None:
        """Shutdown all registered coordinators."""
        try:
            self.logger.info("Shutting down all coordinators")
            for name, coordinator in list(self._coordinators.items()):
                try:
                    if hasattr(coordinator, 'shutdown'):
                        coordinator.shutdown()
                    self.logger.info(f"Shutdown coordinator: {name}")
                except Exception as e:
                    self.logger.error(f"Error shutting down coordinator '{name}': {e}")

            self._coordinators.clear()
            self.logger.info("All coordinators shutdown complete")

        except Exception as e:
            self.logger.error(f"Error during coordinator shutdown: {e}")

    def get_coordinator_count(self) -> int:
        """Get total number of registered coordinators."""
        return len(self._coordinators)


# Global registry instance
_registry_instance: Optional[CoordinatorRegistry] = None


def get_coordinator_registry() -> CoordinatorRegistry:
    """Get the global coordinator registry instance."""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = CoordinatorRegistry()
    return _registry_instance


__all__ = [
    "CoordinatorRegistry",
    "get_coordinator_registry",
]