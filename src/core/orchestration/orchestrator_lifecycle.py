"""
Orchestrator Lifecycle Management
==================================

Lifecycle operations (init, cleanup) extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class OrchestratorLifecycle:
    """Manages orchestrator lifecycle operations."""

    @staticmethod
    def initialize_components(components: dict[str, Any], logger_instance) -> bool:
        """Initialize all registered components."""
        try:
            for component_name, component in components.items():
                if hasattr(component, "initialize"):
                    logger_instance.debug(f"Initializing component: {component_name}")
                    component.initialize()
            return True
        except Exception as e:
            logger_instance.error(f"Failed to initialize components: {e}")
            return False

    @staticmethod
    def cleanup_components(components: dict[str, Any], logger_instance) -> bool:
        """Cleanup all registered components in reverse order."""
        try:
            for component_name in reversed(list(components.keys())):
                component = components[component_name]
                if hasattr(component, "cleanup"):
                    logger_instance.debug(f"Cleaning up component: {component_name}")
                    component.cleanup()
            return True
        except Exception as e:
            logger_instance.error(f"Failed to cleanup components: {e}")
            return False
