#!/usr/bin/env python3
"""
Workflow Package - Unified Workflow Management System
===================================================

Consolidated workflow system replacing 15+ duplicate implementations.
Follows V2 standards: NO duplicate implementations, unified architecture only.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

# Core workflow engine - Single entry point for all workflow operations
from .base_workflow_engine import BaseWorkflowEngine

# Core workflow components - only import what exists
from .core import (
    WorkflowEngine,
    # WorkflowExecutor,  # REMOVED - module deleted
    # WorkflowPlanner,   # REMOVED - module deleted
    WorkflowMonitor
)

# Specialized workflow managers
from .managers import (
    WorkflowManager,
    TaskManager,
    ResourceManager
)

# Unified data models and types
from .types import (
    WorkflowStep,
    WorkflowExecution,
    WorkflowTask,
    WorkflowDefinition,
    WorkflowCondition,
    AgentCapabilityInfo,
    ResourceRequirement,
    WorkflowStatus,
    TaskStatus,
    TaskType,
    WorkflowType,
    TaskPriority,
    OptimizationStrategy,
    AgentCapability
)

# Legacy compatibility aliases
# These maintain backward compatibility with existing code
from .types.workflow_types import WorkflowOptimization

__all__ = [
    # Primary entry point - Use this for all workflow operations
    "BaseWorkflowEngine",
    
    # Core components
    "WorkflowEngine",
    # "WorkflowExecutor",  # REMOVED - module deleted
    # "WorkflowPlanner",  # REMOVED - module deleted
    "WorkflowMonitor",
    
    # Specialized managers
    "WorkflowManager",
    "TaskManager",
    "ResourceManager",
    
    # Data models
    "WorkflowStep",
    "WorkflowExecution",
    "WorkflowTask",
    "WorkflowDefinition",
    "WorkflowCondition",
    "AgentCapabilityInfo",
    "ResourceRequirement",
    
    # Enums and types
    "WorkflowStatus",
    "TaskStatus",
    "TaskType",
    "WorkflowType",
    "TaskPriority",
    "OptimizationStrategy",
    "AgentCapability",
    
    # Legacy compatibility
    "WorkflowOptimization"
]

# Version information
__version__ = "2.0.0"
__author__ = "Agent-3 (Integration & Testing)"
__description__ = "Unified workflow engine system consolidating multiple implementations"
