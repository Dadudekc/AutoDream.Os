#!/usr/bin/env python3
"""
Base Orchestrator - V2 Compliant Foundation
============================================

Base class for all orchestrators providing common lifecycle management,
component coordination, and standardized interfaces.

Author: V2 SWARM Architecture Team
License: MIT
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from .orchestrator_components import OrchestratorComponents
from .orchestrator_events import OrchestratorEvents
from .orchestrator_lifecycle import OrchestratorLifecycle
from .orchestrator_utilities import OrchestratorUtilities


class BaseOrchestrator(ABC):
    """
    Base class for all orchestrators in the V2 system.

    Provides common infrastructure for:
    - Lifecycle management (init → register → coordinate → cleanup)
    - Component registration and management
    - Status reporting and health checks
    - Error handling and logging
    - Event coordination

    Subclasses must implement:
    - _register_components(): Setup component relationships
    - _load_default_config(): Provide default configuration

    Example:
        class MyOrchestrator(BaseOrchestrator):
            def __init__(self, config=None):
                super().__init__("my_orchestrator", config)
                self.engine = MyEngine(self.config)
                self.analyzer = MyAnalyzer(self.config)

            def _register_components(self):
                self.register_component("engine", self.engine)
                self.register_component("analyzer", self.analyzer)

            def _load_default_config(self):
                return {"setting1": "value1", "setting2": "value2"}

            def process_workflow(self, data):
                validated = self.engine.validate(data)
                analyzed = self.analyzer.analyze(validated)
                return analyzed
    """

    def __init__(self, name: str, config: dict[str, Any] | None = None):
        """
        Initialize base orchestrator.

        Args:
            name: Orchestrator identifier name
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or self._load_default_config()
        self.initialized = False
        self.creation_time = datetime.now()
        self.logger = logging.getLogger(f"orchestrator.{name}")

        # Extracted component and event management
        self._component_mgr = OrchestratorComponents(name)
        self._event_mgr = OrchestratorEvents(name)
        self.components = self._component_mgr.components  # Backward compatibility

    @abstractmethod
    def _register_components(self) -> None:
        """
        Register components with orchestrator.

        Subclasses must implement this method to:
        1. Register all managed components
        2. Setup component relationships
        3. Configure event listeners
        4. Validate component registration

        Example:
            def _register_components(self):
                self.register_component("engine", self.engine)
                self.register_component("handler", self.handler)
                self.engine.register_callback(self.handler.handle)
        """
        pass

    @abstractmethod
    def _load_default_config(self) -> dict[str, Any]:
        """
        Load default configuration for orchestrator.

        Returns:
            Dictionary of default configuration values

        Example:
            def _load_default_config(self):
                return {
                    "max_retries": 3,
                    "timeout": 30,
                    "enable_logging": True
                }
        """
        pass

    def initialize(self) -> bool:
        """
        Initialize orchestrator and all components.

        Returns:
            True if initialization successful, False otherwise

        Note:
            This method is idempotent - calling it multiple times
            will only initialize once.
        """
        if self.initialized:
            self.logger.warning(f"Orchestrator {self.name} already initialized")
            return True

        try:
            self.logger.info(f"Initializing orchestrator: {self.name}")

            # Register all components
            self._register_components()

            # Initialize using lifecycle helper
            success = OrchestratorLifecycle.initialize_components(self.components, self.logger)
            if not success:
                return False

            self.initialized = True
            self.logger.info(f"Orchestrator {self.name} initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize orchestrator {self.name}: {e}")
            return False

    def cleanup(self) -> bool:
        """
        Cleanup orchestrator and all components.

        Performs cleanup in reverse order of initialization.

        Returns:
            True if cleanup successful, False otherwise
        """
        if not self.initialized:
            self.logger.warning(f"Orchestrator {self.name} not initialized, skipping cleanup")
            return True

        try:
            self.logger.info(f"Cleaning up orchestrator: {self.name}")

            # Cleanup using lifecycle helper
            success = OrchestratorLifecycle.cleanup_components(self.components, self.logger)

            # Clear registrations
            self._component_mgr.clear_all_components()
            self._event_mgr.clear_listeners()

            self.initialized = False
            self.logger.info(f"Orchestrator {self.name} cleaned up successfully")
            return success

        except Exception as e:
            self.logger.error(f"Failed to cleanup orchestrator {self.name}: {e}")
            return False

    def register_component(self, name: str, component: Any) -> None:
        """Register a component with the orchestrator."""
        self._component_mgr.register_component(name, component)

    def get_component(self, name: str) -> Any | None:
        """Get a registered component by name."""
        return self._component_mgr.get_component(name)

    def has_component(self, name: str) -> bool:
        """Check if component is registered."""
        return self._component_mgr.has_component(name)

    def get_status(self) -> dict[str, Any]:
        """
        Get orchestrator status and health information.

        Returns:
            Dictionary containing status information
        """
        component_statuses = {}
        for name, component in self.components.items():
            if hasattr(component, "get_status"):
                component_statuses[name] = component.get_status()
            else:
                component_statuses[name] = {"available": True}

        return {
            "orchestrator": self.name,
            "initialized": self.initialized,
            "creation_time": self.creation_time.isoformat(),
            "uptime_seconds": (datetime.now() - self.creation_time).total_seconds(),
            "component_count": len(self.components),
            "components": list(self.components.keys()),
            "component_statuses": component_statuses,
            "config": self._sanitize_config(self.config),
        }

    def get_health(self) -> dict[str, Any]:
        """
        Get health check information.

        Returns:
            Dictionary with health status and issues
        """
        health_status = "healthy"
        issues = []

        # Check initialization
        if not self.initialized:
            health_status = "unhealthy"
            issues.append("Orchestrator not initialized")

        # Check components
        for name, component in self.components.items():
            if hasattr(component, "get_health"):
                component_health = component.get_health()
                if component_health.get("status") != "healthy":
                    health_status = "degraded"
                    issues.append(f"Component {name} unhealthy")

        return {
            "status": health_status,
            "issues": issues,
            "timestamp": datetime.now().isoformat(),
        }

    def on(self, event: str, callback: callable) -> None:
        """Register event listener."""
        self._event_mgr.on(event, callback)

    def off(self, event: str, callback: callable) -> None:
        """Remove event listener."""
        self._event_mgr.off(event, callback)

    def emit(self, event: str, data: Any = None) -> None:
        """Emit event to all registered listeners."""
        self._event_mgr.emit(event, data)

    def safe_execute(
        self,
        operation: callable,
        operation_name: str = "operation",
        default_return: Any = None,
        **kwargs,
    ) -> Any:
        """Safely execute an operation with error handling."""
        return OrchestratorUtilities.safe_execute(
            operation, operation_name, default_return, self.logger, self.emit, **kwargs
        )

    def _sanitize_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """Sanitize configuration for status reporting."""
        return OrchestratorUtilities.sanitize_config(config, self.logger)

    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
        return False

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<{self.__class__.__name__}(name='{self.name}', "
            f"initialized={self.initialized}, "
            f"components={len(self.components)})>"
        )
