"""
Execution Management Package - Phase-2 V2 Compliance Refactoring
===============================================================

Specialized execution components for better SRP compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from .base_execution_manager import BaseExecutionManager
from .task_manager import TaskManager
from .protocol_manager import ProtocolManager
from .execution_coordinator import ExecutionCoordinator

__all__ = [
    "BaseExecutionManager",
    "TaskManager",
    "ProtocolManager", 
    "ExecutionCoordinator",
]
