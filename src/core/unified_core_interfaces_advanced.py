#!/usr/bin/env python3
"""
Unified Core Interfaces - Advanced
==================================

This module contains advanced core system interfaces including lifecycle,
monitoring, data processing, async operations, unified interfaces, factories,
and registries.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Modularize unified_core_interfaces.py for V2 compliance
License: MIT
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, Union
from concurrent.futures import Future

# Import basic interfaces for composition
from .unified_core_interfaces_basic import (
    ICoreSystem, IConfigurable, IObservable, IMonitor, IHealthCheck
)


# ============================================================================
# LIFECYCLE INTERFACES
# ============================================================================

class ILifecycleAware(Protocol):
    """Interface for components with lifecycle management."""

    def on_start(self) -> None:
        """Called when component starts."""
        ...

    def on_stop(self) -> None:
        """Called when component stops."""
        ...

    def on_restart(self) -> None:
        """Called when component restarts."""
        ...

    def is_running(self) -> bool:
        """Check if component is running."""
        ...


class IInitializable(Protocol):
    """Interface for initializable components."""

    def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Initialize component."""
        ...

    def is_initialized(self) -> bool:
        """Check if component is initialized."""
        ...


class IDisposable(Protocol):
    """Interface for disposable components."""

    def dispose(self) -> None:
        """Dispose component resources."""
        ...

    def is_disposed(self) -> bool:
        """Check if component is disposed."""
        ...


# ============================================================================
# MONITORING AND METRICS INTERFACES
# ============================================================================

class IMonitor(Protocol):
    """Interface for monitoring components."""

    def start_monitoring(self) -> None:
        """Start monitoring."""
        ...

    def stop_monitoring(self) -> None:
        """Stop monitoring."""
        ...

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        ...

    def reset_metrics(self) -> None:
        """Reset metrics."""
        ...


class IHealthCheck(Protocol):
    """Interface for health check components."""

    def check_health(self) -> Dict[str, Any]:
        """Perform health check."""
        ...

    def is_healthy(self) -> bool:
        """Check if component is healthy."""
        ...

    def get_health_status(self) -> str:
        """Get health status string."""
        ...


# ============================================================================
# DATA PROCESSING INTERFACES
# ============================================================================

class IDataProcessor(Protocol):
    """Interface for data processing components."""

    def process(self, data: Any) -> Any:
        """Process data."""
        ...

    def can_process(self, data: Any) -> bool:
        """Check if data can be processed."""
        ...

    def get_supported_formats(self) -> List[str]:
        """Get supported data formats."""
        ...


class IDataValidator(Protocol):
    """Interface for data validation components."""

    def validate(self, data: Any) -> List[str]:
        """Validate data, return list of errors."""
        ...

    def get_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules."""
        ...


# ============================================================================
# ASYNC INTERFACES
# ============================================================================

class IAsyncTask(Protocol):
    """Interface for async tasks."""

    async def execute(self) -> Any:
        """Execute async task."""
        ...

    def cancel(self) -> None:
        """Cancel task."""
        ...

    def is_cancelled(self) -> bool:
        """Check if task is cancelled."""
        ...

    def get_status(self) -> str:
        """Get task status."""
        ...


class IAsyncTaskManager(Protocol):
    """Interface for async task managers."""

    def submit_task(self, task: IAsyncTask) -> str:
        """Submit async task, return task ID."""
        ...

    def get_task_status(self, task_id: str) -> str:
        """Get task status."""
        ...

    def cancel_task(self, task_id: str) -> bool:
        """Cancel task."""
        ...

    def get_task_result(self, task_id: str) -> Any:
        """Get task result."""
        ...


# ============================================================================
# UNIFIED CORE SYSTEM INTERFACE
# ============================================================================

@dataclass
class CoreSystemMetadata:
    """Metadata for core systems."""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)


class IUnifiedCoreSystem(ICoreSystem, IConfigurable, IObservable, ILifecycleAware, IHealthCheck, IMonitor):
    """Unified interface for all core systems combining multiple interface contracts."""

    @property
    def metadata(self) -> CoreSystemMetadata:
        """Get system metadata."""
        ...

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Get system capabilities."""
        ...

    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """Get system dependencies."""
        ...

    @abstractmethod
    def integrate_with_system(self, system: IUnifiedCoreSystem) -> bool:
        """Integrate with another core system."""
        ...

    @abstractmethod
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status with other systems."""
        ...


# ============================================================================
# FACTORY INTERFACES
# ============================================================================

class ICoreSystemFactory(Protocol):
    """Factory interface for creating core systems."""

    def create_system(self, system_type: str, config: Dict[str, Any]) -> IUnifiedCoreSystem:
        """Create a core system instance."""
        ...

    def get_supported_systems(self) -> List[str]:
        """Get list of supported system types."""
        ...

    def validate_system_config(self, system_type: str, config: Dict[str, Any]) -> List[str]:
        """Validate system configuration."""
        ...


# ============================================================================
# REGISTRY INTERFACES
# ============================================================================

class ICoreSystemRegistry(Protocol):
    """Registry interface for core systems."""

    def register_system(self, system: IUnifiedCoreSystem) -> None:
        """Register a core system."""
        ...

    def get_system(self, system_name: str) -> Optional[IUnifiedCoreSystem]:
        """Get system by name."""
        ...

    def list_systems(self) -> List[IUnifiedCoreSystem]:
        """List all registered systems."""
        ...

    def unregister_system(self, system_name: str) -> bool:
        """Unregister system."""
        ...

    def get_systems_by_capability(self, capability: str) -> List[IUnifiedCoreSystem]:
        """Get systems by capability."""
        ...


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_interface_contract(*interfaces: type) -> type:
    """Create a combined interface contract from multiple interfaces."""
    class CombinedInterface(*interfaces):
        """Combined interface from multiple interface types."""
        pass
    return CombinedInterface


def validate_interface_implementation(instance: Any, interface: type) -> List[str]:
    """Validate that an instance properly implements an interface."""
    errors = []

    # Check if instance has all required methods
    for attr_name in dir(interface):
        if not attr_name.startswith('_'):
            attr = getattr(interface, attr_name, None)
            if callable(attr) or isinstance(attr, property):
                if not hasattr(instance, attr_name):
                    errors.append(f"Missing interface method: {attr_name}")

    return errors


# ============================================================================
# TYPE HINTS AND ALIASES
# ============================================================================

AdvancedSystemType = Union[
    ILifecycleAware,
    IInitializable,
    IDisposable,
    IMonitor,
    IHealthCheck,
    IDataProcessor,
    IDataValidator,
    IAsyncTask,
    IAsyncTaskManager,
    IUnifiedCoreSystem,
    ICoreSystemFactory,
    ICoreSystemRegistry
]

# Export all interfaces
__all__ = [
    # Lifecycle interfaces
    'ILifecycleAware',
    'IInitializable',
    'IDisposable',

    # Monitoring interfaces
    'IMonitor',
    'IHealthCheck',

    # Data processing interfaces
    'IDataProcessor',
    'IDataValidator',

    # Async interfaces
    'IAsyncTask',
    'IAsyncTaskManager',

    # Unified interfaces
    'IUnifiedCoreSystem',
    'ICoreSystemFactory',
    'ICoreSystemRegistry',

    # Types and utilities
    'AdvancedSystemType',
    'create_interface_contract',
    'validate_interface_implementation',
    'CoreSystemMetadata'
]


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""
    print("🐝 Unified Core Interfaces - Advanced Module")
    print("=" * 50)
    print("✅ Lifecycle interfaces loaded successfully")
    print("✅ Monitoring interfaces loaded successfully")
    print("✅ Data processing interfaces loaded successfully")
    print("✅ Async interfaces loaded successfully")
    print("✅ Unified system interfaces loaded successfully")
    print("✅ Factory and registry interfaces loaded successfully")
    print("🐝 WE ARE SWARM - Advanced interfaces ready!")
