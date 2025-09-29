"""
Unified Architecture Core - V2 Compliant (Simplified)
====================================================

Core unified architecture with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Integration Specialist)
License: MIT
"""
import logging
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class ComponentType(Enum):
    """Component type enumeration."""

    CORE = "core"
    SERVICE = "service"
    INTEGRATION = "integration"
    PATTERN = "pattern"
    UTILITY = "utility"


class ComponentStatus(Enum):
    """Component status enumeration."""

    INACTIVE = "inactive"
    ACTIVE = "active"
    ERROR = "error"
    MAINTENANCE = "maintenance"


@dataclass
class ComponentConfig:
    """Configuration for architecture components."""

    component_type: ComponentType
    name: str
    description: str
    enabled: bool = True
    dependencies: list[str] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)


@dataclass
class ComponentMetrics:
    """Metrics for component performance."""

    initialization_time: float = 0.0
    last_activity: datetime | None = None
    error_count: int = 0
    success_count: int = 0
    last_error: str | None = None


class ComponentLifecycle:
    """Manages component lifecycle operations."""

    def __init__(self):
        self._components: dict[str, ComponentConfig] = {}
        self._instances: dict[str, Any] = {}
        self._status: dict[str, ComponentStatus] = {}
        self._metrics: dict[str, ComponentMetrics] = {}
        self._lock = threading.Lock()

    def register_component(self, config: ComponentConfig) -> None:
        """Register a component."""
        with self._lock:
            self._components[config.name] = config
            self._status[config.name] = ComponentStatus.INACTIVE
            self._metrics[config.name] = ComponentMetrics()
            logger.debug(f"Component registered: {config.name}")

    def unregister_component(self, name: str) -> None:
        """Unregister a component."""
        with self._lock:
            if name in self._components:
                del self._components[name]
                if name in self._instances:
                    del self._instances[name]
                if name in self._status:
                    del self._status[name]
                if name in self._metrics:
                    del self._metrics[name]
                logger.debug(f"Component unregistered: {name}")

    def initialize_component(self, name: str, instance: Any) -> bool:
        """Initialize a component."""
        with self._lock:
            if name not in self._components:
                logger.error(f"Component not registered: {name}")
                return False

            if self._status[name] != ComponentStatus.INACTIVE:
                logger.warning(f"Component {name} not in inactive status")
                return False

            start_time = datetime.now()
            try:
                self._instances[name] = instance
                self._status[name] = ComponentStatus.ACTIVE
                self._metrics[name].initialization_time = (
                    datetime.now() - start_time
                ).total_seconds()
                self._metrics[name].last_activity = datetime.now()
                logger.info(f"Component initialized: {name}")
                return True
            except Exception as e:
                self._status[name] = ComponentStatus.ERROR
                self._metrics[name].error_count += 1
                self._metrics[name].last_error = str(e)
                logger.error(f"Failed to initialize component {name}: {e}")
                return False

    def shutdown_component(self, name: str) -> bool:
        """Shutdown a component."""
        with self._lock:
            if name not in self._components:
                logger.error(f"Component not registered: {name}")
                return False

            try:
                if name in self._instances:
                    del self._instances[name]
                self._status[name] = ComponentStatus.INACTIVE
                self._metrics[name].last_activity = datetime.now()
                logger.info(f"Component shutdown: {name}")
                return True
            except Exception as e:
                self._status[name] = ComponentStatus.ERROR
                self._metrics[name].error_count += 1
                self._metrics[name].last_error = str(e)
                logger.error(f"Failed to shutdown component {name}: {e}")
                return False

    def get_component(self, name: str) -> ComponentConfig | None:
        """Get a component configuration."""
        return self._components.get(name)

    def get_component_instance(self, name: str) -> Any | None:
        """Get a component instance."""
        return self._instances.get(name)

    def get_component_status(self, name: str) -> ComponentStatus | None:
        """Get component status."""
        return self._status.get(name)

    def get_component_metrics(self, name: str) -> ComponentMetrics | None:
        """Get component metrics."""
        return self._metrics.get(name)

    def get_active_components(self) -> list[str]:
        """Get list of active components."""
        return [name for name, status in self._status.items() if status == ComponentStatus.ACTIVE]

    def get_error_components(self) -> list[str]:
        """Get list of components with errors."""
        return [name for name, status in self._status.items() if status == ComponentStatus.ERROR]


class DependencyInjection:
    """Simple dependency injection container."""

    def __init__(self):
        self._services: dict[str, Any] = {}
        self._factories: dict[str, Callable] = {}
        self._lock = threading.Lock()

    def register_service(self, name: str, service: Any) -> None:
        """Register a service instance."""
        with self._lock:
            self._services[name] = service
            logger.debug(f"Service registered: {name}")

    def register_factory(self, name: str, factory: Callable) -> None:
        """Register a service factory."""
        with self._lock:
            self._factories[name] = factory
            logger.debug(f"Factory registered: {name}")

    def get_service(self, name: str) -> Any | None:
        """Get a service instance."""
        with self._lock:
            if name in self._services:
                return self._services[name]

            if name in self._factories:
                try:
                    service = self._factories[name]()
                    self._services[name] = service
                    return service
                except Exception as e:
                    logger.error(f"Failed to create service {name}: {e}")
                    return None

            return None

    def has_service(self, name: str) -> bool:
        """Check if a service is registered."""
        return name in self._services or name in self._factories

    def remove_service(self, name: str) -> None:
        """Remove a service."""
        with self._lock:
            if name in self._services:
                del self._services[name]
            if name in self._factories:
                del self._factories[name]
            logger.debug(f"Service removed: {name}")


class UnifiedArchitecture:
    """Unified architecture framework."""

    def __init__(self):
        self._lifecycle = ComponentLifecycle()
        self._di_container = DependencyInjection()
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize the unified architecture."""
        if self._initialized:
            logger.warning("Architecture already initialized")
            return True

        try:
            # Initialize core components
            self._lifecycle.register_component(
                ComponentConfig(
                    component_type=ComponentType.CORE,
                    name="lifecycle_manager",
                    description="Component lifecycle manager",
                )
            )

            self._lifecycle.register_component(
                ComponentConfig(
                    component_type=ComponentType.CORE,
                    name="dependency_injection",
                    description="Dependency injection container",
                )
            )

            self._initialized = True
            logger.info("Unified architecture initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize architecture: {e}")
            return False

    def shutdown(self) -> bool:
        """Shutdown the unified architecture."""
        if not self._initialized:
            logger.warning("Architecture not initialized")
            return True

        try:
            # Shutdown all components
            active_components = self._lifecycle.get_active_components()
            for component_name in active_components:
                self._lifecycle.shutdown_component(component_name)

            self._initialized = False
            logger.info("Unified architecture shutdown")
            return True
        except Exception as e:
            logger.error(f"Failed to shutdown architecture: {e}")
            return False

    def get_lifecycle_manager(self) -> ComponentLifecycle:
        """Get the component lifecycle manager."""
        return self._lifecycle

    def get_di_container(self) -> DependencyInjection:
        """Get the dependency injection container."""
        return self._di_container

    def is_initialized(self) -> bool:
        """Check if the architecture is initialized."""
        return self._initialized

    def cleanup(self) -> bool:
        """Cleanup the unified architecture."""
        if not self._initialized:
            logger.warning("Architecture not initialized")
            return True

        try:
            self._initialized = False
            logger.info("Unified architecture cleaned up")
            return True
        except Exception as e:
            logger.error(f"Failed to cleanup architecture: {e}")
            return False


# Global unified architecture instance
unified_architecture = UnifiedArchitecture()
unified_architecture_core = unified_architecture


def initialize_architecture() -> bool:
    """Initialize the unified architecture."""
    return unified_architecture.initialize()


def shutdown_architecture() -> bool:
    """Shutdown the unified architecture."""
    return unified_architecture.shutdown()


def get_architecture() -> UnifiedArchitecture:
    """Get the unified architecture instance."""
    return unified_architecture
