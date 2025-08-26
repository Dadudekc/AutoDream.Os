#!/usr/bin/env python3
"""
Workflow Managers Module - Specialized Workflow Management
========================================================

Specialized workflow managers inheriting from base classes.
Each manager ≤200 LOC with focused responsibility.

Author: Agent-3 (Workflow Unification)
License: MIT
"""

from .workflow_manager import WorkflowManager
from .task_manager import TaskManager
from .resource_manager import ResourceManager

__all__ = [
    "WorkflowManager",
    "TaskManager",
    "ResourceManager"
]
