"""
SSOT (Single Source of Truth) Package - Canonical Implementation

This package provides the core SSOT functionality for the Agent Cellphone V2 system.
All imports now use the canonical implementations for consistency and maintainability.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Version: 3.0.0 - Canonical Implementation
License: MIT
"""

# Import canonical implementations
    SSOTExecutionCoordinator,
    get_ssot_execution_coordinator,
    create_ssot_execution_coordinator,
)
    SSOTValidationSystem,
    get_ssot_validation_system,
    create_ssot_validation_system,
)

# Import core models and types
    ExecutionPhase,
    ExecutionResult,
    ExecutionStatus,
    ExecutionTask,
    CoordinationContext,
    ExecutionMetrics,
)
    ValidationLevel,
    ValidationResult,
    ValidationTest,
    ValidationSuite,
    ValidationReport,
    ValidationMetrics,
)

# Import coordination components

# Import types and enums
    SSOTComponentType,
    SSOTIntegrationStatus,
    SSOTSystemHealth,
)

# Define package version
__version__ = "3.0.0"

# Define what's available when importing the package
__all__ = [
    # Canonical implementations
    "SSOTExecutionCoordinator",
    "get_ssot_execution_coordinator",
    "create_ssot_execution_coordinator",
    "SSOTValidationSystem",
    "get_ssot_validation_system",
    "create_ssot_validation_system",
    
    # Core models
    "ExecutionTask",
    "ExecutionResult",
    "ExecutionPhase",
    "ExecutionStatus",
    "CoordinationContext",
    "ExecutionMetrics",
    
    # Validation models
    "ValidationLevel",
    "ValidationResult",
    "ValidationTest",
    "ValidationSuite",
    "ValidationReport",
    "ValidationMetrics",
    
    # Coordination components
    "SSOTCoordinationManager",
    "SSOTIntegrationCoordinator",
    
    # Types and enums
    "SSOTComponentType",
    "SSOTIntegrationStatus",
    "SSOTSystemHealth",
]

# Package metadata
__title__ = "SSOT Package - Canonical Implementation"
__description__ = "Single Source of Truth package for Agent Cellphone V2 - Canonical Implementation"
__author__ = "Agent-3"
__email__ = "agent3@agentcellphone.com"

