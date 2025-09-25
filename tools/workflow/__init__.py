"""
Agent Workflow Package
======================

Modular workflow automation and management for agents.
V2 Compliance: Clean, focused, and maintainable components.

Components:
- core: Core workflow data structures and validation
- automation: Automated task execution
- manager: Workflow management and coordination

Usage:
    from tools.workflow import WorkflowManager, WorkflowDefinition
    manager = WorkflowManager()
    workflow = manager.create_workflow(...)
"""

from .core import (
    WorkflowStep,
    WorkflowDefinition,
    WorkflowValidator,
    WorkflowScheduler,
    WorkflowStatusTracker
)

from .automation import WorkflowAutomation
from .manager import WorkflowManager

__all__ = [
    "WorkflowStep",
    "WorkflowDefinition", 
    "WorkflowValidator",
    "WorkflowScheduler",
    "WorkflowStatusTracker",
    "WorkflowAutomation",
    "WorkflowManager"
]

__version__ = "2.0.0"
__author__ = "Agent-2 (Architecture & Design Specialist)"
__description__ = "V2 Compliant Agent Workflow System"




