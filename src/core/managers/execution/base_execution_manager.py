"""
Base Execution Manager - Phase-2 V2 Compliance Refactoring
==========================================================

Base class for execution management with common functionality.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
import asyncio
import threading
import uuid
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from enum import Enum
from ..contracts import ExecutionManager, ManagerContext, ManagerResult
from src.core.constants import get_completion_signal


class TaskStatus(Enum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProtocolType(Enum):
    """Protocol types."""

    EMERGENCY = "emergency"
    ROUTINE = "routine"
    MAINTENANCE = "maintenance"
    RECOVERY = "recovery"


class BaseExecutionManager(ExecutionManager):
    """Base execution manager with common functionality."""

    def __init__(self):
        """Initialize base execution manager."""
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.protocols: Dict[str, Dict[str, Any]] = {}
        self.executions: Dict[str, Dict[str, Any]] = {}
        self.task_queue: List[str] = []
        self.execution_threads: Dict[str, threading.Thread] = {}
        self.max_concurrent_tasks = 5
        self.task_timeout = 300  # 5 minutes

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize execution manager."""
        try:
            # Register default protocols
            self._register_default_protocols()
            
            # Start task processor
            self._start_task_processor()
            
            context.logger("Base Execution Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize execution manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute operation."""
        try:
            if operation == "execute_task":
                return self.execute_task(context, payload.get("task_id"), payload.get("task_data", {}))
            elif operation == "register_protocol":
                return self.register_protocol(context, payload.get("protocol_name"), payload.get("protocol_handler"))
            elif operation == "get_execution_status":
                return self.get_execution_status(context, payload.get("execution_id"))
            elif operation == "create_task":
                return self._create_task(context, payload)
            elif operation == "cancel_task":
                return self._cancel_task(context, payload)
            elif operation == "list_tasks":
                return self._list_tasks(context, payload)
            elif operation == "list_protocols":
                return self._list_protocols(context, payload)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown operation: {operation}",
                )
        except Exception as e:
            context.logger(f"Error executing operation {operation}: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def execute_task(
        self, context: ManagerContext, task_id: Optional[str], task_data: Dict[str, Any]
    ) -> ManagerResult:
        """Execute a task."""
        try:
            if not task_id:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Task ID is required",
                )

            if task_id not in self.tasks:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Task {task_id} not found",
                )

            task = self.tasks[task_id]
            if task["status"] != TaskStatus.PENDING:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Task {task_id} is not in pending status",
                )

            # Update task status
            task["status"] = TaskStatus.RUNNING
            task["started_at"] = datetime.now().isoformat()

            # Create execution record
            execution_id = str(uuid.uuid4())
            execution = {
                "id": execution_id,
                "task_id": task_id,
                "status": "running",
                "started_at": task["started_at"],
                "data": task_data,
            }
            self.executions[execution_id] = execution

            # Execute task in thread
            thread = threading.Thread(
                target=self._execute_task_thread,
                args=(context, execution_id, task, task_data),
            )
            thread.start()
            self.execution_threads[execution_id] = thread

            return ManagerResult(
                success=True,
                data={"execution_id": execution_id, "task_id": task_id},
                metrics={"tasks_executed": 1},
            )

        except Exception as e:
            context.logger(f"Error executing task {task_id}: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def register_protocol(
        self, context: ManagerContext, protocol_name: str, protocol_handler: Callable
    ) -> ManagerResult:
        """Register a protocol."""
        try:
            if not protocol_name or not protocol_handler:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Protocol name and handler are required",
                )

            protocol = {
                "name": protocol_name,
                "handler": protocol_handler,
                "type": ProtocolType.ROUTINE,
                "priority": 5,
                "created_at": datetime.now().isoformat(),
                "enabled": True,
            }

            self.protocols[protocol_name] = protocol

            return ManagerResult(
                success=True,
                data={"protocol_name": protocol_name},
                metrics={"protocols_registered": len(self.protocols)},
            )

        except Exception as e:
            context.logger(f"Error registering protocol {protocol_name}: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def get_execution_status(
        self, context: ManagerContext, execution_id: Optional[str]
    ) -> ManagerResult:
        """Get execution status."""
        try:
            if execution_id:
                if execution_id not in self.executions:
                    return ManagerResult(
                        success=False,
                        data={},
                        metrics={},
                        error=f"Execution {execution_id} not found",
                    )
                executions = {execution_id: self.executions[execution_id]}
            else:
                executions = dict(self.executions)

            # Add duration information
            for exec_id, execution in executions.items():
                duration = self._get_execution_duration(execution)
                execution["duration"] = duration

            return ManagerResult(
                success=True,
                data={"executions": executions},
                metrics={"executions_found": len(executions)},
            )

        except Exception as e:
            context.logger(f"Error getting execution status: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup execution manager."""
        try:
            # Cancel all running tasks
            for task_id, task in self.tasks.items():
                if task["status"] == TaskStatus.RUNNING:
                    task["status"] = TaskStatus.CANCELLED
                    task["cancelled_at"] = datetime.now().isoformat()

            # Wait for threads to finish
            for thread in self.execution_threads.values():
                if thread.is_alive():
                    thread.join(timeout=5.0)

            # Clear data
            self.tasks.clear()
            self.protocols.clear()
            self.executions.clear()
            self.task_queue.clear()
            self.execution_threads.clear()

            context.logger(
                f"Execution manager cleaned up {get_completion_signal()}"
            )
            return True
        except Exception as e:
            context.logger(f"Error cleaning up execution manager: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get execution manager status."""
        return {
            "total_tasks": len(self.tasks),
            "pending_tasks": len([t for t in self.tasks.values() if t["status"] == TaskStatus.PENDING]),
            "running_tasks": len([t for t in self.tasks.values() if t["status"] == TaskStatus.RUNNING]),
            "completed_tasks": len([t for t in self.tasks.values() if t["status"] == TaskStatus.COMPLETED]),
            "failed_tasks": len([t for t in self.tasks.values() if t["status"] == TaskStatus.FAILED]),
            "total_protocols": len(self.protocols),
            "active_executions": len(self.executions),
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "task_timeout": self.task_timeout,
        }

    def _create_task(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Create a new task."""
        try:
            task_id = str(uuid.uuid4())
            task_type = payload.get("task_type", "general")
            priority = payload.get("priority", 5)
            data = payload.get("data", {})

            task = {
                "id": task_id,
                "type": task_type,
                "status": TaskStatus.PENDING,
                "priority": priority,
                "data": data,
                "created_at": datetime.now().isoformat(),
            }

            self.tasks[task_id] = task
            self.task_queue.append(task_id)

            return ManagerResult(
                success=True,
                data={"task_id": task_id},
                metrics={"tasks_created": 1},
            )

        except Exception as e:
            context.logger(f"Error creating task: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _cancel_task(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Cancel a task."""
        try:
            task_id = payload.get("task_id")
            if not task_id or task_id not in self.tasks:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Task ID is required and must exist",
                )

            task = self.tasks[task_id]
            if task["status"] in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Task {task_id} cannot be cancelled",
                )

            task["status"] = TaskStatus.CANCELLED
            task["cancelled_at"] = datetime.now().isoformat()

            # Remove from queue if present
            if task_id in self.task_queue:
                self.task_queue.remove(task_id)

            return ManagerResult(
                success=True,
                data={"task_id": task_id},
                metrics={"tasks_cancelled": 1},
            )

        except Exception as e:
            context.logger(f"Error cancelling task: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _list_tasks(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """List tasks with optional filtering."""
        try:
            status_filter = payload.get("status")
            task_type_filter = payload.get("task_type")

            tasks = dict(self.tasks)

            # Apply filters
            if status_filter:
                tasks = {k: v for k, v in tasks.items() if v["status"].value == status_filter}
            if task_type_filter:
                tasks = {k: v for k, v in tasks.items() if v["type"] == task_type_filter}

            return ManagerResult(
                success=True,
                data={"tasks": tasks},
                metrics={"tasks_found": len(tasks)},
            )

        except Exception as e:
            context.logger(f"Error listing tasks: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _list_protocols(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """List protocols with optional filtering."""
        try:
            protocol_type_filter = payload.get("protocol_type")
            enabled_only = payload.get("enabled_only", False)

            protocols = dict(self.protocols)

            # Apply filters
            if protocol_type_filter:
                protocols = {k: v for k, v in protocols.items() if v.get("type") == protocol_type_filter}
            if enabled_only:
                protocols = {k: v for k, v in protocols.items() if v.get("enabled", True)}

            return ManagerResult(
                success=True,
                data={"protocols": protocols},
                metrics={"protocols_found": len(protocols)},
            )

        except Exception as e:
            context.logger(f"Error listing protocols: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _execute_task_thread(
        self, context: ManagerContext, execution_id: str, task: Dict[str, Any], task_data: Dict[str, Any]
    ) -> None:
        """Execute task in separate thread."""
        try:
            execution = self.executions[execution_id]
            task_type = task["type"]

            # Execute based on task type
            if task_type == "file":
                result = self._execute_file_task(task_data)
            elif task_type == "data":
                result = self._execute_data_task(task_data)
            elif task_type == "api":
                result = self._execute_api_task(task_data)
            else:
                result = {"status": "completed", "message": f"General task {task_type} completed"}

            # Update execution
            execution["status"] = "completed"
            execution["completed_at"] = datetime.now().isoformat()
            execution["result"] = result

            # Update task
            task["status"] = TaskStatus.COMPLETED
            task["completed_at"] = execution["completed_at"]
            task["result"] = result

        except Exception as e:
            context.logger(f"Error executing task thread: {e}")
            
            # Update execution
            execution = self.executions[execution_id]
            execution["status"] = "failed"
            execution["failed_at"] = datetime.now().isoformat()
            execution["error"] = str(e)

            # Update task
            task["status"] = TaskStatus.FAILED
            task["failed_at"] = execution["failed_at"]
            task["error"] = str(e)

    def _execute_file_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file operation task."""
        operation = task_data.get("operation", "read")
        file_path = task_data.get("file_path", "")

        # Simulate file operation
        return {
            "status": "completed",
            "operation": operation,
            "file_path": file_path,
            "message": f"File operation {operation} completed",
        }

    def _execute_data_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data processing task."""
        operation = task_data.get("operation", "process")
        data_size = task_data.get("data_size", 0)

        # Simulate data processing
        return {
            "status": "completed",
            "operation": operation,
            "data_size": data_size,
            "message": f"Data operation {operation} completed",
        }

    def _execute_api_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API call task."""
        url = task_data.get("url", "")
        method = task_data.get("method", "GET")

        # Simulate API call
        return {
            "status": "completed",
            "url": url,
            "method": method,
            "response_code": 200,
            "message": "API call completed",
        }

    def _get_execution_duration(self, execution: Dict[str, Any]) -> Optional[float]:
        """Get execution duration in seconds."""
        try:
            started_at = datetime.fromisoformat(execution["started_at"])
            if "completed_at" in execution:
                completed_at = datetime.fromisoformat(execution["completed_at"])
                return (completed_at - started_at).total_seconds()
            elif "failed_at" in execution:
                failed_at = datetime.fromisoformat(execution["failed_at"])
                return (failed_at - started_at).total_seconds()
            else:
                return (datetime.now() - started_at).total_seconds()
        except Exception:
            return None

    def _register_default_protocols(self) -> None:
        """Register default protocols."""
        # Emergency protocol
        self.protocols["emergency_shutdown"] = {
            "name": "emergency_shutdown",
            "type": ProtocolType.EMERGENCY,
            "steps": [
                "stop_all_tasks",
                "save_state",
                "notify_agents",
                "shutdown_system",
            ],
            "priority": 10,
            "created_at": datetime.now().isoformat(),
            "enabled": True,
        }

        # Routine protocol
        self.protocols["routine_maintenance"] = {
            "name": "routine_maintenance",
            "type": ProtocolType.ROUTINE,
            "steps": [
                "check_system_health",
                "cleanup_temp_files",
                "update_metrics",
                "backup_data",
            ],
            "priority": 5,
            "created_at": datetime.now().isoformat(),
            "enabled": True,
        }

    def _start_task_processor(self) -> None:
        """Start background task processor."""

        def processor():
            while True:
                try:
                    if self.task_queue:
                        task_id = self.task_queue.pop(0)
                        if task_id in self.tasks:
                            task = self.tasks[task_id]
                            if task["status"] == TaskStatus.PENDING:
                                # Auto-execute high priority tasks
                                if task["priority"] >= 8:
                                    self.execute_task(None, task_id, task["data"])
                    threading.Event().wait(1.0)  # Wait 1 second
                except Exception:
                    break

        thread = threading.Thread(target=processor, daemon=True)
        thread.start()
