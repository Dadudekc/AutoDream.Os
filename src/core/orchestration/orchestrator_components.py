"""
Orchestrator Component Management
==================================

Component registration and management extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class OrchestratorComponents:
    """Manages orchestrator component registration and retrieval."""

    def __init__(self, orchestrator_name: str):
        """Initialize component manager."""
        self.orchestrator_name = orchestrator_name
        self.components: dict[str, Any] = {}
        self.logger = logging.getLogger(f"orchestrator.{orchestrator_name}.components")

    def register_component(self, name: str, component: Any) -> None:
        """Register a component with the orchestrator."""
        if not name or name.strip() == "":
            raise ValueError("Component name cannot be empty")

        if name in self.components:
            self.logger.warning(f"Component '{name}' already registered, replacing")

        self.components[name] = component
        self.logger.info(f"Component registered: {name}")

    def get_component(self, name: str) -> Any | None:
        """Get a registered component by name."""
        component = self.components.get(name)

        if component is None:
            self.logger.warning(f"Component '{name}' not found")

        return component

    def has_component(self, name: str) -> bool:
        """Check if a component is registered."""
        return name in self.components

    def get_all_components(self) -> dict[str, Any]:
        """Get all registered components."""
        return self.components.copy()

    def unregister_component(self, name: str) -> bool:
        """Unregister a component."""
        if name in self.components:
            del self.components[name]
            self.logger.info(f"Component unregistered: {name}")
            return True
        return False

    def clear_all_components(self) -> None:
        """Clear all registered components."""
        count = len(self.components)
        self.components.clear()
        self.logger.info(f"Cleared {count} components")
