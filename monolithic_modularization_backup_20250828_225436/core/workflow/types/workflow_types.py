#!/usr/bin/env python3
"""
Workflow Types - Unified Core Data Structures
============================================

Core workflow data structures consolidated from multiple implementations.
Provides backward compatibility and unified interface.

Author: Agent-3 (Workflow Unification)
License: MIT
"""

# Re-export from workflow_models for backward compatibility
from .workflow_models import (
    WorkflowStep,
    WorkflowExecution,
    WorkflowTask,
    WorkflowDefinition,
    WorkflowCondition,
    AgentCapabilityInfo,
    ResourceRequirement
)

# Re-export from workflow_enums for backward compatibility
from .workflow_enums import (
    WorkflowStatus,
    TaskStatus,
    WorkflowType,
    TaskPriority,
    OptimizationStrategy,
    AgentCapability
)

# Legacy compatibility aliases
# These maintain backward compatibility with existing code
WorkflowOptimization = WorkflowDefinition  # Legacy alias
OptimizationStrategy = OptimizationStrategy  # Legacy alias

__all__ = [
    # Core data structures
    "WorkflowStep",
    "WorkflowExecution",
    "WorkflowTask",
    "WorkflowDefinition",
    "WorkflowCondition",
    "AgentCapabilityInfo",
    "ResourceRequirement",
    
    # Enums and status
    "WorkflowStatus",
    "TaskStatus",
    "WorkflowType",
    "TaskPriority",
    "OptimizationStrategy",
    "AgentCapability",
    
    # Legacy compatibility
    "WorkflowOptimization"
]
