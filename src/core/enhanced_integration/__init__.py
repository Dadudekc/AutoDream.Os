#!/usr/bin/env python3
"""
Enhanced Integration Package - V2 Compliance
===========================================

Modular enhanced integration coordination system with V2 compliance.
Replaces the monolithic enhanced_integration_coordinator.py.

Package Structure:
- integration_models.py: Data models and configuration
- enhanced_integration_orchestrator.py: Main orchestrator and unified interface

V2 Compliance: Modular design, single responsibility, dependency injection.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
Original: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

# Import main classes for easy access
from .integration_models import (
    EnhancedOptimizationConfig,
    IntegrationPerformanceMetrics,
    IntegrationPerformanceReport,
    IntegrationTask,
    CoordinationStrategy,
    ResourceAllocationStrategy,
    IntegrationType,
    OptimizationLevel,
    IntegrationStatus,
    create_default_optimization_config,
    create_performance_metrics,
    create_performance_report,
    create_integration_task,
    validate_optimization_config,
    validate_integration_task,
    DEFAULT_COORDINATION_STRATEGIES,
    RESOURCE_ALLOCATION_WEIGHTS,
    OPTIMIZATION_MULTIPLIERS
)

from .enhanced_integration_orchestrator import (
    EnhancedIntegrationCoordinator,
    create_enhanced_integration_coordinator,
    get_enhanced_integration_coordinator
)

# Package metadata
__version__ = "2.0.0"
__author__ = "Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager"
__description__ = "Modular enhanced integration coordination system with V2 compliance"

# Export main interface functions
__all__ = [
    # Core classes
    "EnhancedIntegrationCoordinator",
    
    # Data models
    "EnhancedOptimizationConfig",
    "IntegrationPerformanceMetrics",
    "IntegrationPerformanceReport",
    "IntegrationTask",
    
    # Enums
    "CoordinationStrategy",
    "ResourceAllocationStrategy",
    "IntegrationType",
    "OptimizationLevel",
    "IntegrationStatus",
    
    # Factory functions
    "create_default_optimization_config",
    "create_performance_metrics",
    "create_performance_report",
    "create_integration_task",
    
    # Validation functions
    "validate_optimization_config",
    "validate_integration_task",
    
    # Constants
    "DEFAULT_COORDINATION_STRATEGIES",
    "RESOURCE_ALLOCATION_WEIGHTS",
    "OPTIMIZATION_MULTIPLIERS",
    
    # Main interface functions
    "create_enhanced_integration_coordinator",
    "get_enhanced_integration_coordinator"
]
