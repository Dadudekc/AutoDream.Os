"""
Base Execution Manager - Phase-2 V2 Compliance Refactoring
==========================================================
Base class for execution management. Refactored to <200 lines.
Author: Agent-3, Refactored: Agent-5 | License: MIT
"""

from __future__ import annotations

import threading
from typing import Any

from ..contracts import ExecutionManager, ManagerContext, ManagerResult
from .execution_operations import ExecutionOperations, TaskStatus
from .execution_runner import ExecutionRunner
from .protocol_manager import ProtocolManager
from .task_executor import TaskExecutor


class BaseExecutionManager(ExecutionManager):
    """Base execution manager with common functionality."""

    def __init__(self):
        """Initialize base execution manager."""
        self.tasks: dict[str, dict[str, Any]] = {}
        self.executions: dict[str, dict[str, Any]] = {}
        self.task_queue: list[str] = []
        self.execution_threads: dict[str, threading.Thread] = {}
        self.max_concurrent_tasks = 5
        self.task_timeout = 300
        # Initialize subcomponents
        self.task_executor = TaskExecutor()
        self.protocol_manager = ProtocolManager()
        self.operations = ExecutionOperations(self.tasks, self.task_queue)
        self.runner = ExecutionRunner(
            self.tasks, self.executions, self.execution_threads, self.task_executor
        )

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize execution manager."""
        try:
            self.protocol_manager.register_default_protocols()
            self._start_task_processor()
            context.logger("Base Execution Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize execution manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute operation."""
        try:
            if operation == "execute_task":
                return self.runner.execute_task(
                    context, payload.get("task_id"), payload.get("task_data", {}), TaskStatus
                )
            elif operation == "register_protocol":
                return self.register_protocol(
                    context, payload.get("protocol_name"), payload.get("protocol_data", {})
                )
            elif operation == "get_execution_status":
                return self.runner.get_execution_status(context, payload.get("execution_id"))
            elif operation == "create_task":
                return self.operations.create_task(context, payload)
            elif operation == "cancel_task":
                return self.operations.cancel_task(context, payload)
            elif operation == "list_tasks":
                return self.operations.list_tasks(context, payload)
            elif operation == "list_protocols":
                return self._list_protocols(context, payload)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    message=f"Unknown operation: {operation}",
                    errors=[f"Unknown operation: {operation}"],
                )
        except Exception as e:
            return ManagerResult(
                success=False, data={}, message=f"Execution error: {e}", errors=[str(e)]
            )

    def execute_task(
        self, context: ManagerContext, task_id: str | None, task_data: dict[str, Any]
    ) -> ManagerResult:
        """Execute a task."""
        return self.runner.execute_task(context, task_id, task_data, TaskStatus)

    def register_protocol(
        self, context: ManagerContext, protocol_name: str | None, protocol_data: dict[str, Any]
    ) -> ManagerResult:
        """Register an execution protocol."""
        try:
            if not protocol_name:
                return ManagerResult(
                    success=False,
                    data={},
                    message="Protocol name is required",
                    errors=["Protocol name is required"],
                )
            protocol_type = protocol_data.get("type", "routine")
            priority = protocol_data.get("priority", 1)
            timeout = protocol_data.get("timeout", 300)
            success = self.protocol_manager.register_protocol(
                protocol_name, protocol_type, priority, timeout
            )
            if success:
                return ManagerResult(
                    success=True,
                    data={"protocol_name": protocol_name},
                    message=f"Protocol registered: {protocol_name}",
                    errors=[],
                )
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    message=f"Failed to register protocol: {protocol_name}",
                    errors=["Registration failed"],
                )
        except Exception as e:
            return ManagerResult(
                success=False, data={}, message=f"Failed to register protocol: {e}", errors=[str(e)]
            )

    def get_execution_status(self, context: ManagerContext, execution_id: str | None) -> ManagerResult:
        """Get execution status."""
        return self.runner.get_execution_status(context, execution_id)

    def _list_protocols(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """List all protocols."""
        try:
            protocols = self.protocol_manager.list_protocols()
            return ManagerResult(
                success=True,
                data={"protocols": protocols, "count": len(protocols)},
                message=f"Found {len(protocols)} protocols",
                errors=[],
            )
        except Exception as e:
            return ManagerResult(
                success=False, data={}, message=f"Failed to list protocols: {e}", errors=[str(e)]
            )

    def _start_task_processor(self) -> None:
        """Start background task processor."""
        pass  # Placeholder
