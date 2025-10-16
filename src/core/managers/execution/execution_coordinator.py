"""
Execution Coordinator - Phase-2 V2 Compliance Refactoring
=========================================================

Coordinates between task and protocol managers.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations

from typing import Any

from ..contracts import ManagerContext, ManagerResult
from .base_execution_manager import BaseExecutionManager
from .protocol_manager import ProtocolManager
from .task_executor import TaskExecutor


class ExecutionCoordinator(BaseExecutionManager):
    """Coordinates execution operations between task and protocol managers."""

    def __init__(self):
        """Initialize execution coordinator."""
        super().__init__()
        # Note: BaseExecutionManager already has task_executor and protocol_manager
        # These are just aliases for backward compatibility
        self.task_manager = self.task_executor
        self.protocol_manager_instance = ProtocolManager()

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize all execution components."""
        try:
            # Initialize base manager
            base_success = super().initialize(context)

            # Initialize specialized managers
            task_success = self.task_manager.initialize(context)
            protocol_success = self.protocol_manager.initialize(context)

            # Sync shared state
            self._sync_managers()

            success = base_success and task_success and protocol_success

            if success:
                context.logger("Execution Coordinator initialized with specialized managers")

            return success

        except Exception as e:
            context.logger(f"Failed to initialize Execution Coordinator: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute operation using appropriate manager."""
        try:
            # Route to appropriate manager based on operation
            if operation in [
                "create_task",
                "execute_task",
                "cancel_task",
                "list_tasks",
                "get_task_status",
            ]:
                return self.task_manager.execute(context, operation, payload)
            elif operation in [
                "register_protocol",
                "execute_protocol",
                "list_protocols",
                "enable_protocol",
                "disable_protocol",
            ]:
                return self.protocol_manager.execute(context, operation, payload)
            elif operation in ["get_execution_status"]:
                return super().execute(context, operation, payload)
            else:
                return super().execute(context, operation, payload)

        except Exception as e:
            context.logger(f"Error executing operation {operation}: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup all execution components."""
        try:
            # Cleanup specialized managers
            task_success = self.task_manager.cleanup(context)
            protocol_success = self.protocol_manager.cleanup(context)

            # Cleanup base manager
            base_success = super().cleanup(context)

            success = base_success and task_success and protocol_success

            if success:
                context.logger("Execution Coordinator cleaned up")

            return success

        except Exception as e:
            context.logger(f"Error cleaning up Execution Coordinator: {e}")
            return False

    def get_status(self) -> dict[str, Any]:
        """Get consolidated status from all managers."""
        try:
            base_status = super().get_status()
            task_status = self.task_manager.get_status()
            protocol_status = self.protocol_manager.get_status()

            return {
                **base_status,
                "task_manager": task_status,
                "protocol_manager": protocol_status,
                "coordinator_active": True,
                "v2_compliant": True,
            }

        except Exception:
            return {
                "error": "Failed to get status",
                "v2_compliant": True,
            }

    def _sync_managers(self):
        """Sync shared state between managers."""
        # Share the same data structures
        self.task_manager.tasks = self.tasks
        self.task_manager.protocols = self.protocols
        self.task_manager.executions = self.executions
        self.task_manager.task_queue = self.task_queue
        self.task_manager.execution_threads = self.execution_threads

        self.protocol_manager.tasks = self.tasks
        self.protocol_manager.protocols = self.protocols
        self.protocol_manager.executions = self.executions
        self.protocol_manager.task_queue = self.task_queue
        self.protocol_manager.execution_threads = self.execution_threads

    # Public methods for backward compatibility
    def create_task(
        self,
        context: ManagerContext,
        task_type: str,
        priority: int = 5,
        data: dict[str, Any] | None = None,
    ) -> ManagerResult:
        """Create a new task (public method)."""
        payload = {
            "task_type": task_type,
            "priority": priority,
            "data": data or {},
        }
        return self.task_manager.execute(context, "create_task", payload)

    def execute_protocol(
        self, context: ManagerContext, protocol_name: str, payload: dict[str, Any] | None = None
    ) -> ManagerResult:
        """Execute a protocol (public method)."""
        exec_payload = {
            "protocol_name": protocol_name,
            **(payload or {}),
        }
        return self.protocol_manager.execute(context, "execute_protocol", exec_payload)

    def get_task_status(self, context: ManagerContext, task_id: str) -> ManagerResult:
        """Get task status (public method)."""
        payload = {"task_id": task_id}
        return self.task_manager.execute(context, "get_task_status", payload)
