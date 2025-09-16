#!/usr/bin/env python3
"""
Configuration and Coordination Interfaces - Configuration and Coordination Protocol Definitions
==========================================================================================

Configuration and coordination interface definitions for system components.
Part of the modularization of unified_core_interfaces.py for V2 compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol


class IConfigurationProvider(Protocol):
    """Interface for configuration providers."""

    def get_config(self, key: str) -> Optional[Any]:
        """Get configuration value by key."""
        ...

    def set_config(self, key: str, value: Any) -> bool:
        """Set configuration value."""
        ...

    def has_config(self, key: str) -> bool:
        """Check if configuration key exists."""
        ...

    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration values."""
        ...

    def reload_config(self) -> bool:
        """Reload configuration from source."""
        ...


class IConfigurationValidator(Protocol):
    """Interface for configuration validation."""

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration settings."""
        ...

    def get_validation_errors(self) -> List[str]:
        """Get configuration validation errors."""
        ...

    def is_valid(self, config: Dict[str, Any]) -> bool:
        """Check if configuration is valid."""
        ...


class ICoordinator(ABC):
    """Abstract base class for coordination components."""

    @abstractmethod
    def coordinate(self, task: Any) -> bool:
        """Coordinate a task."""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get coordination status."""
        pass

    @abstractmethod
    def is_active(self) -> bool:
        """Check if coordinator is active."""
        pass


class ICoordinatorRegistry(Protocol):
    """Interface for coordinator registry."""

    def register_coordinator(self, coordinator_id: str, coordinator: ICoordinator) -> bool:
        """Register a coordinator."""
        ...

    def unregister_coordinator(self, coordinator_id: str) -> bool:
        """Unregister a coordinator."""
        ...

    def get_coordinator(self, coordinator_id: str) -> Optional[ICoordinator]:
        """Get coordinator by ID."""
        ...

    def list_coordinators(self) -> List[str]:
        """List all coordinator IDs."""
        ...


class ICoordinatorFactory(Protocol):
    """Interface for coordinator factory."""

    def create_coordinator(self, coordinator_type: str, **kwargs) -> Optional[ICoordinator]:
        """Create a coordinator instance."""
        ...

    def get_supported_types(self) -> List[str]:
        """Get supported coordinator types."""
        ...

    def register_coordinator_type(self, type_name: str, coordinator_class: type) -> bool:
        """Register a new coordinator type."""
        ...


class ICoreSystemFactory(Protocol):
    """Interface for core system factory."""

    def create_system(self, system_type: str, **kwargs) -> Optional[Any]:
        """Create a core system instance."""
        ...

    def get_supported_types(self) -> List[str]:
        """Get supported system types."""
        ...

    def register_system_type(self, type_name: str, system_class: type) -> bool:
        """Register a new system type."""
        ...


class ICoreSystemRegistry(Protocol):
    """Interface for core system registry."""

    def register_system(self, system_id: str, system: Any) -> bool:
        """Register a core system."""
        ...

    def unregister_system(self, system_id: str) -> bool:
        """Unregister a core system."""
        ...

    def get_system(self, system_id: str) -> Optional[Any]:
        """Get system by ID."""
        ...

    def list_systems(self) -> List[str]:
        """List all system IDs."""
        ...





