"""
Interface Models - Refactored Entry Point
=========================================

Unified entry point for interface models with backward compatibility.
V2 Compliance: < 50 lines, single responsibility, unified interface.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

# Core models and enums
from .models_core import (
    InterfaceMetadata, InterfaceDefinition, InterfaceImplementation,
    InterfaceValidation, InterfaceInstance, InterfaceValidationResult,
    InterfaceRegistryConfig, BaseInterface
)

# Enums
from .enums import (
    InterfaceType, InterfaceStatus, InterfacePriority,
    ValidationLevel, InterfaceCategory
)

# Extended models
from .models_extended import (
    InterfaceRegistry, InterfaceMetrics, InterfaceConfiguration,
    InterfaceDependency, InterfaceError, InterfacePerformance, InterfaceSecurity
)

# Factory methods and configuration
from .models_factory import InterfaceModelsFactory, InterfaceModels

# Re-export everything for backward compatibility
__all__ = [
    # Enums
    'InterfaceType', 'InterfaceStatus', 'InterfacePriority',
    'ValidationLevel', 'InterfaceCategory',
    
    # Core Models
    'InterfaceMetadata', 'InterfaceDefinition', 'InterfaceImplementation',
    'InterfaceValidation', 'InterfaceInstance', 'InterfaceValidationResult',
    'InterfaceRegistryConfig', 'BaseInterface',
    
    # Extended Models
    'InterfaceRegistry', 'InterfaceMetrics', 'InterfaceConfiguration',
    'InterfaceDependency', 'InterfaceError', 'InterfacePerformance', 'InterfaceSecurity',
    
    # Factory
    'InterfaceModelsFactory', 'InterfaceModels'
]
