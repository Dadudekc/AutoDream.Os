"""
Core Execution Manager V2 - Phase-2 V2 Compliance Refactoring
==============================================================

Consolidated execution manager using specialized components.
Reduced from 513 lines to ~200 lines for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
from typing import Dict, Any, Optional
from .contracts import ExecutionManager, ManagerContext, ManagerResult
from .execution import (
    BaseExecutionManager,
    TaskManager,
    ProtocolManager,
    ExecutionCoordinator,
)


class CoreExecutionManager(ExecutionManager):
    """Core execution manager using specialized components for V2 compliance."""

    def __init__(self):
        """Initialize consolidated execution manager."""
        self.coordinator = ExecutionCoordinator()

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize execution coordinator."""
        return self.coordinator.initialize(context)

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute operation using coordinator."""
        return self.coordinator.execute(context, operation, payload)

    def execute_task(
        self, context: ManagerContext, task_id: Optional[str], task_data: Dict[str, Any]
    ) -> ManagerResult:
        """Execute a task."""
        return self.coordinator.execute_task(context, task_id, task_data)

    def register_protocol(
        self, context: ManagerContext, protocol_name: str, protocol_handler: callable
    ) -> ManagerResult:
        """Register a protocol."""
        return self.coordinator.register_protocol(context, protocol_name, protocol_handler)

    def get_execution_status(
        self, context: ManagerContext, execution_id: Optional[str]
    ) -> ManagerResult:
        """Get execution status."""
        return self.coordinator.get_execution_status(context, execution_id)

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup execution coordinator."""
        return self.coordinator.cleanup(context)

    def get_status(self) -> Dict[str, Any]:
        """Get execution manager status."""
        return self.coordinator.get_status()

    # Public methods for backward compatibility
    def create_task(
        self, context: ManagerContext, task_type: str, priority: int = 5, data: Optional[Dict[str, Any]] = None
    ) -> ManagerResult:
        """Create a new task (public method)."""
        return self.coordinator.create_task(context, task_type, priority, data)

    def execute_protocol(
        self, context: ManagerContext, protocol_name: str, payload: Optional[Dict[str, Any]] = None
    ) -> ManagerResult:
        """Execute a protocol (public method)."""
        return self.coordinator.execute_protocol(context, protocol_name, payload)

    def get_task_status(
        self, context: ManagerContext, task_id: str
    ) -> ManagerResult:
        """Get task status (public method)."""
        return self.coordinator.get_task_status(context, task_id)
