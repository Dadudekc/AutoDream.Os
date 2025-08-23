#!/usr/bin/env python3
"""
Workflow Package - V2 Core Workflow Automation System

This package provides modular workflow automation following V2 coding standards.
Each module has ≤300 lines and follows single responsibility principle.

Modules:
- workflow_types: Data models and enums (≤100 lines)
- workflow_orchestrator: Main orchestration logic (≤200 lines)  
- workflow_executor: Task execution engine (≤200 lines)
- workflow_planner: Execution planning and optimization (≤200 lines)
- workflow_cli: CLI interface for testing (≤100 lines)

Author: Agent-4 (Quality Assurance)
License: MIT
"""

from .workflow_types import (
    WorkflowStatus, TaskStatus, TaskPriority, WorkflowType,
    WorkflowTask, WorkflowCondition, WorkflowExecution,
    AgentCapability, ResourceRequirement
)

from .workflow_orchestrator import WorkflowOrchestrator
from .workflow_executor import WorkflowExecutor
from .workflow_planner import WorkflowPlanner
from .workflow_cli import WorkflowCLI

__version__ = "2.0.0"
__author__ = "Agent-4 (Quality Assurance)"

__all__ = [
    # Types and enums
    "WorkflowStatus", "TaskStatus", "TaskPriority", "WorkflowType",
    "WorkflowTask", "WorkflowCondition", "WorkflowExecution",
    "AgentCapability", "ResourceRequirement",
    
    # Core classes
    "WorkflowOrchestrator", "WorkflowExecutor", "WorkflowPlanner", "WorkflowCLI"
]
