#!/usr/bin/env python3
"""
Workflow Package - V2 Core Workflow System
=========================================

Refactored workflow system following V2 coding standards.
Split from monolithic advanced_workflow_engine.py into focused modules.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from .workflow_types import (
    WorkflowType, WorkflowPriority, OptimizationStrategy,
    WorkflowStep, WorkflowExecution, WorkflowOptimization,
    V2Workflow, AIResponse
)

from .workflow_core import (
    WorkflowDefinitionManager, WorkflowStateManager, WorkflowOptimizationManager
)

from .workflow_execution import WorkflowExecutionEngine

from .workflow_cli import WorkflowCLI, run_smoke_test

__all__ = [
    # Types and enums
    'WorkflowType', 'WorkflowPriority', 'OptimizationStrategy',
    'WorkflowStep', 'WorkflowExecution', 'WorkflowOptimization',
    'V2Workflow', 'AIResponse',
    
    # Core management
    'WorkflowDefinitionManager', 'WorkflowStateManager', 'WorkflowOptimizationManager',
    
    # Execution engine
    'WorkflowExecutionEngine',
    
    # CLI interface
    'WorkflowCLI', 'run_smoke_test'
]

__version__ = "2.0.0"
__author__ = "Agent-2 (Architecture & Design Specialist)"
