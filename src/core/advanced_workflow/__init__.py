"""
Advanced Workflow Package - V2 Compliant Refactored Structure

This package contains the refactored advanced workflow engine components,
each following V2 standards (≤300 LOC) and Single Responsibility Principle.

Components:
- workflow_types.py: Type definitions and enums
- workflow_core.py: Core workflow logic and data models
- workflow_validation.py: Validation logic and error handling
- workflow_cli.py: CLI interface for testing and management

Note: For workflow execution, use the modular workflow system:
- src.core.workflow.workflow_execution.WorkflowExecutionEngine
"""

from .workflow_types import (
    WorkflowType,
    WorkflowPriority,
    OptimizationStrategy,
    WorkflowStatus,
)
from .workflow_core import (
    WorkflowStep,
    WorkflowExecution,
    WorkflowOptimization,
    V2Workflow,
    AIResponse,
)
from .workflow_core import (
    WorkflowDefinitionManager,
)
from .workflow_validation import WorkflowValidator
from .workflow_cli import WorkflowCLI

__all__ = [
    # Types and enums
    "WorkflowType",
    "WorkflowPriority", 
    "OptimizationStrategy",
    "WorkflowStatus",
    
    # Core data models
    "WorkflowStep",
    "WorkflowExecution",
    "WorkflowOptimization",
    "V2Workflow",
    "AIResponse",
    
    # Core functionality
    "WorkflowDefinitionManager",
    
    # Validation
    "WorkflowValidator",
    
    # CLI interface
    "WorkflowCLI",
]

# Backward compatibility - use modular workflow system
# For AdvancedWorkflowEngine functionality, use:
# from src.core.workflow.workflow_execution import WorkflowExecutionEngine
