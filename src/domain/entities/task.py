"""
Task Entity - V2 Compliant (Refactored)
======================================

Refactored Task entity importing from modular components.
Maintains backward compatibility while achieving V2 compliance.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
from .task_enums import TaskStatus, TaskPriority, TaskType
from .task_core import TaskCore

# Backward compatibility - export main classes
__all__ = ["TaskStatus", "TaskPriority", "TaskType", "TaskCore"]

# For backward compatibility, alias TaskCore as Task
Task = TaskCore
