"""
Manager Registry - Phase-2 Manager Consolidation
===============================================

Centralized registry for core managers following DIP principles.
Manages instantiation and lifecycle of 5 core managers.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations

from typing import Any

from .contracts import MANAGER_TYPES, Manager, ManagerContext


class ManagerRegistry:
    """DIP registry: high-level depends on abstraction, not concretion."""

    def __init__(self):
        """Initialize manager registry."""
        self._managers: dict[str, Manager] = {}
        self._manager_types: dict[str, type[Manager]] = {}
        self._initialized = False

    def register_manager_type(self, name: str, manager_class: type[Manager]) -> None:
        """Register a manager type."""
        if name in self._manager_types:
            raise ValueError(f"Manager type already registered: {name}")
        self._manager_types[name] = manager_class

    def create_manager(self, name: str, context: ManagerContext) -> Manager | None:
        """Create and initialize a manager instance."""
        try:
            if name not in self._manager_types:
                raise ValueError(f"Unknown manager type: {name}")

            manager_class = self._manager_types[name]
            manager = manager_class()

            # Initialize the manager
            if manager.initialize(context):
                self._managers[name] = manager
                return manager
            else:
                return None
        except Exception as e:
            context.logger(f"Failed to create manager {name}: {e}")
            return None

    def get_manager(self, name: str) -> Manager | None:
        """Get an existing manager instance."""
        return self._managers.get(name)

    def get_all_managers(self) -> dict[str, Manager]:
        """Get all manager instances."""
        return dict(self._managers)

    def execute_operation(
        self,
        manager_name: str,
        context: ManagerContext,
        operation: str,
        payload: dict[str, Any],
    ) -> Any:
        """Execute an operation on a specific manager."""
        manager = self.get_manager(manager_name)
        if not manager:
            raise ValueError(f"Manager not found: {manager_name}")

        return manager.execute(context, operation, payload)

    def cleanup_all(self, context: ManagerContext) -> None:
        """Cleanup all managers."""
        for name, manager in self._managers.items():
            try:
                manager.cleanup(context)
            except Exception as e:
                context.logger(f"Failed to cleanup manager {name}: {e}")

        self._managers.clear()

    def get_status(self) -> dict[str, Any]:
        """Get registry status."""
        return {
            "total_managers": len(self._managers),
            "manager_names": list(self._managers.keys()),
            "registered_types": list(self._manager_types.keys()),
            "initialized": self._initialized,
        }

    def initialize_default_managers(self, context: ManagerContext) -> bool:
        """Initialize all default manager types."""
        try:
            # Register default manager types
            for name, manager_type in MANAGER_TYPES.items():
                self.register_manager_type(name, manager_type)

            # Create core managers
            core_managers = [
                "resource",
                "configuration",
                "execution",
                "monitoring",
                "service",
            ]
            for manager_name in core_managers:
                if not self.create_manager(manager_name, context):
                    context.logger(f"Failed to initialize core manager: {manager_name}")
                    return False

            self._initialized = True
            return True
        except Exception as e:
            context.logger(f"Failed to initialize default managers: {e}")
            return False


# Global registry instance
_global_registry: ManagerRegistry | None = None


def get_manager_registry() -> ManagerRegistry:
    """Get global manager registry instance."""
    global _global_registry
    if _global_registry is None:
        _global_registry = ManagerRegistry()
    return _global_registry


def create_manager_registry() -> ManagerRegistry:
    """Create a new manager registry instance."""
    return ManagerRegistry()
