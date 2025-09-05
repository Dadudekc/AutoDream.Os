"""
Interface Models - Backward Compatibility Wrapper
=================================================

Backward compatibility wrapper for interface models.
V2 Compliance: < 30 lines, single responsibility, compatibility layer.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

# Import everything from the refactored modules
from .models_refactored import *

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