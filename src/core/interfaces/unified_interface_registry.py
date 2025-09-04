#!/usr/bin/env python3
"""
Unified Interface Registry - V2 Compliance Interface Management
============================================================

This module provides a unified interface registry for V2 compliance system integration.

V2 COMPLIANCE: Centralized interface management with type safety and validation
DESIGN PATTERN: Registry pattern for interface discovery and management
DEPENDENCY INJECTION: Supports clean architecture principles

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Interface Registry Optimized
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Callable
from ..unified_logging_system import get_logger
from ..unified_validation_system import get_unified_validator

# ================================
# INTERFACE TYPES
# ================================

class InterfaceType(Enum):
    """Interface types for V2 compliance system."""

    SERVICE = "service"
    REPOSITORY = "repository"
    VALIDATOR = "validator"
    COORDINATOR = "coordinator"
    UTILITY = "utility"
    CONFIGURATION = "configuration"
    LOGGING = "logging"

# ================================
# INTERFACE DEFINITION
# ================================

@dataclass
class InterfaceDefinition:
    """Interface definition with V2 compliance features."""

    interface_id: str
    interface_type: InterfaceType
    interface_class: Type[Any]
    metadata: Dict[str, Any]
    version: str = "1.0.0"
    dependencies: List[str] = None
    singleton: bool = False

    def __post_init__(self):
        """Initialize default values."""
        if self.dependencies is None:
            self.dependencies = []

# ================================
# INTERFACE VALIDATOR
# ================================

class InterfaceValidator(ABC):
    """Abstract base class for interface validators."""

    @abstractmethod
    def validate_interface(self, interface_def: InterfaceDefinition) -> bool:
        """Validate an interface definition."""
        pass

class DefaultInterfaceValidator(InterfaceValidator):
    """Default interface validator."""

    def __init__(self):
        self.validator = get_unified_validator()
        self.logger = get_logger(__name__)

    def validate_interface(self, interface_def: InterfaceDefinition) -> bool:
        """Validate interface definition."""
        try:
            # Validate required fields
            required_fields = ['interface_id', 'interface_type', 'interface_class']
            missing = self.validator.validate_required_fields(
                interface_def.__dict__, required_fields
            )

            if missing.errors:
                self.logger.error(f"Invalid interface definition: {missing.errors}")
                return False

            # Validate interface class is a type
            if not isinstance(interface_def.interface_class, type):
                self.logger.error(f"Interface class must be a type: {interface_def.interface_id}")
                return False

            # Validate dependencies exist
            for dep_id in interface_def.dependencies:
                # Note: Dependency validation would be implemented in registry
                pass

            return True

        except Exception as e:
            self.logger.error(f"Interface validation error: {e}")
            return False

# ================================
# UNIFIED INTERFACE REGISTRY
# ================================

class UnifiedInterfaceRegistry:
    """Unified interface registry with V2 compliance features."""

    def __init__(self):
        self.interfaces: Dict[str, InterfaceDefinition] = {}
        self.validator = DefaultInterfaceValidator()
        self.logger = get_logger(__name__)
        self._instances: Dict[str, Any] = {}

    def register_interface(
        self,
        interface_id: str,
        interface_type: InterfaceType,
        interface_class: Type[Any],
        metadata: Optional[Dict[str, Any]] = None,
        version: str = "1.0.0",
        dependencies: Optional[List[str]] = None,
        singleton: bool = False,
    ) -> bool:
        """Register an interface with V2 compliance validation."""
        try:
            # Create interface definition
            interface_def = InterfaceDefinition(
                interface_id=interface_id,
                interface_type=interface_type,
                interface_class=interface_class,
                metadata=metadata or {},
                version=version,
                dependencies=dependencies or [],
                singleton=singleton
            )

            # Validate interface
            if not self.validator.validate_interface(interface_def):
                self.logger.error(f"Interface validation failed: {interface_id}")
                return False

            # Check for duplicate registration
            if interface_id in self.interfaces:
                self.logger.warning(f"Interface already registered, updating: {interface_id}")

            # Register interface
            self.interfaces[interface_id] = interface_def
            self.logger.info(f"Interface registered successfully: {interface_id} ({interface_type.value})")

            return True

        except Exception as e:
            self.logger.error(f"Interface registration error: {e}")
            return False

    def get_interface(self, interface_id: str) -> Optional[InterfaceDefinition]:
        """Get an interface definition by ID."""
        return self.interfaces.get(interface_id)

    def get_interface_instance(self, interface_id: str) -> Optional[Any]:
        """Get or create interface instance (singleton pattern)."""
        interface_def = self.get_interface(interface_id)
        if not interface_def:
            return None

        if interface_def.singleton:
            if interface_id not in self._instances:
                try:
                    self._instances[interface_id] = interface_def.interface_class()
                except Exception as e:
                    self.logger.error(f"Failed to create singleton instance: {interface_id} - {e}")
                    return None
            return self._instances[interface_id]
        else:
            try:
                return interface_def.interface_class()
            except Exception as e:
                self.logger.error(f"Failed to create interface instance: {interface_id} - {e}")
                return None

    def list_interfaces(self, interface_type: Optional[InterfaceType] = None) -> List[str]:
        """List interface IDs, optionally filtered by type."""
        if interface_type:
            return [iid for iid, idef in self.interfaces.items()
                   if idef.interface_type == interface_type]
        return list(self.interfaces.keys())

    def unregister_interface(self, interface_id: str) -> bool:
        """Unregister an interface."""
        if interface_id in self.interfaces:
            del self.interfaces[interface_id]
            if interface_id in self._instances:
                del self._instances[interface_id]
            self.logger.info(f"Interface unregistered: {interface_id}")
            return True
        return False

    def get_dependencies(self, interface_id: str) -> List[str]:
        """Get dependencies for an interface."""
        interface_def = self.get_interface(interface_id)
        return interface_def.dependencies if interface_def else []

    def validate_dependencies(self, interface_id: str) -> bool:
        """Validate that all dependencies for an interface exist."""
        dependencies = self.get_dependencies(interface_id)
        missing_deps = []

        for dep_id in dependencies:
            if dep_id not in self.interfaces:
                missing_deps.append(dep_id)

        if missing_deps:
            self.logger.error(f"Missing dependencies for {interface_id}: {missing_deps}")
            return False

        return True

# ================================
# GLOBAL INTERFACE REGISTRY
# ================================

# Single global instance to eliminate duplicate registry objects
_unified_interface_registry = None

def get_unified_interface_registry() -> UnifiedInterfaceRegistry:
    """Get global unified interface registry instance."""
    global _unified_interface_registry
    if _unified_interface_registry is None:
        _unified_interface_registry = UnifiedInterfaceRegistry()
    return _unified_interface_registry

# ================================
# CONVENIENCE FUNCTIONS
# ================================

def register_interface(
    interface_id: str,
    interface_type: InterfaceType,
    interface_class: Type[Any],
    metadata: Optional[Dict[str, Any]] = None,
    version: str = "1.0.0",
    dependencies: Optional[List[str]] = None,
    singleton: bool = False,
) -> bool:
    """Register an interface with the global registry."""
    return get_unified_interface_registry().register_interface(
        interface_id=interface_id,
        interface_type=interface_type,
        interface_class=interface_class,
        metadata=metadata,
        version=version,
        dependencies=dependencies,
        singleton=singleton
    )

def get_interface(interface_id: str) -> Optional[InterfaceDefinition]:
    """Get an interface definition from the global registry."""
    return get_unified_interface_registry().get_interface(interface_id)

def get_interface_instance(interface_id: str) -> Optional[Any]:
    """Get an interface instance from the global registry."""
    return get_unified_interface_registry().get_interface_instance(interface_id)

def list_interfaces(interface_type: Optional[InterfaceType] = None) -> List[str]:
    """List interface IDs from the global registry."""
    return get_unified_interface_registry().list_interfaces(interface_type)

def unregister_interface(interface_id: str) -> bool:
    """Unregister an interface from the global registry."""
    return get_unified_interface_registry().unregister_interface(interface_id)

def validate_dependencies(interface_id: str) -> bool:
    """Validate dependencies for an interface in the global registry."""
    return get_unified_interface_registry().validate_dependencies(interface_id)

# ================================
# INTERFACE DECORATORS
# ================================

def interface(interface_type: InterfaceType, singleton: bool = False, dependencies: Optional[List[str]] = None):
    """Decorator to register a class as an interface."""
    def decorator(cls: Type[Any]):
        interface_id = f"{cls.__module__}.{cls.__name__}"
        register_interface(
            interface_id=interface_id,
            interface_type=interface_type,
            interface_class=cls,
            singleton=singleton,
            dependencies=dependencies or []
        )
        return cls
    return decorator
