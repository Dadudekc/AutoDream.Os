"""
Execution Runner - Task Execution Logic
=======================================
Task execution and thread management extracted for V2 compliance.

Author: Agent-5 (extracted from base_execution_manager.py)
License: MIT
"""

from __future__ import annotations

import threading
import uuid
from datetime import datetime
from typing import Any

from ..contracts import ManagerContext, ManagerResult


class ExecutionRunner:
    """Handles task execution and thread management."""

    def __init__(self, tasks: dict, executions: dict, execution_threads: dict, task_executor):
        """Initialize execution runner."""
        self.tasks = tasks
        self.executions = executions
        self.execution_threads = execution_threads
        self.task_executor = task_executor

    def execute_task(
        self,
        context: ManagerContext,
        task_id: str | None,
        task_data: dict[str, Any],
        task_status_enum: Any,
    ) -> ManagerResult:
        """Execute a task."""
        try:
            if task_id and task_id not in self.tasks:
                return ManagerResult(
                    success=False,
                    data={},
                    message=f"Task not found: {task_id}",
                    errors=[f"Task not found: {task_id}"],
                )
            task = self.tasks[task_id] if task_id else {}
            execution_id = str(uuid.uuid4())
            execution = {
                "execution_id": execution_id,
                "task_id": task_id,
                "started_at": datetime.now().isoformat(),
                "status": "running",
                "result": None,
            }
            self.executions[execution_id] = execution
            if task_id:
                task["status"] = task_status_enum.RUNNING
                task["started_at"] = execution["started_at"]
            # Execute task in thread
            thread = threading.Thread(
                target=self.task_executor.execute_task_thread,
                args=(
                    context,
                    execution_id,
                    task,
                    task_data,
                    self.tasks,
                    self.executions,
                    task_status_enum,
                ),
            )
            thread.daemon = True
            thread.start()
            if task_id:
                self.execution_threads[task_id] = thread
            return ManagerResult(
                success=True,
                data={"execution_id": execution_id, "task_id": task_id},
                message=f"Task execution started: {execution_id}",
                errors=[],
            )
        except Exception as e:
            return ManagerResult(
                success=False, data={}, message=f"Failed to execute task: {e}", errors=[str(e)]
            )

    def get_execution_status(
        self, context: ManagerContext, execution_id: str | None
    ) -> ManagerResult:
        """Get execution status."""
        try:
            if not execution_id:
                return ManagerResult(
                    success=False,
                    data={},
                    message="Execution ID is required",
                    errors=["Execution ID is required"],
                )
            execution = self.executions.get(execution_id)
            if not execution:
                return ManagerResult(
                    success=False,
                    data={},
                    message=f"Execution not found: {execution_id}",
                    errors=[f"Execution not found: {execution_id}"],
                )
            return ManagerResult(
                success=True,
                data=execution,
                message=f"Execution status: {execution['status']}",
                errors=[],
            )
        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                message=f"Failed to get execution status: {e}",
                errors=[str(e)],
            )
