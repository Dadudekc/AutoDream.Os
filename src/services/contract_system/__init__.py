"""
Contract System Package - V2 Compliant Module
=============================================

Comprehensive contract system for agent task management.
Provides task assignment, completion tracking, and status monitoring.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .manager import ContractManager
from .storage import ContractStorage
from .models import Contract, Task, TaskType, PriorityLevel, TaskStatus

__all__ = [
    'ContractManager',
    'ContractStorage', 
    'Contract',
    'Task',
    'TaskType',
    'PriorityLevel',
    'TaskStatus'
]
