#!/usr/bin/env python3
"""
Task Manager - Agent Cellphone V2
================================

Unified Task Manager consolidating all task management functionality.
Follows Single Responsibility Principle with extracted modules.
Eliminates duplication by consolidating workflow and general task management.
"""

import logging
import uuid
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any

from src.core.base_manager import BaseManager
from src.core.tasks.scheduler import TaskScheduler, Task, TaskPriority, TaskStatus
from src.core.tasks.executor import TaskExecutor
from src.core.tasks.monitoring import TaskMonitor
from src.core.tasks.recovery import TaskRecovery


class TaskManager(BaseManager):
    """
    Unified Task Manager - Orchestrates all task management functionality.

    Consolidates:
    - General task management (scheduling, execution, monitoring, recovery)
    - Workflow task management (creation, assignment, dependency management)
    - Contract-based task management (contract integration, threading support)
    - Agent capability management

    Inherits from BaseManager for unified lifecycle management, monitoring,
    and error handling while coordinating specialized task components.
    """

    def __init__(self, workspace_manager):
        """Initialize Unified Task Manager with BaseManager inheritance."""
        super().__init__(
            manager_id="task_manager",
            name="Unified Task Manager",
            description="Orchestrates all task management with consolidated functionality",
        )

        self.workspace_manager = workspace_manager

        # Initialize extracted modules
        self.scheduler = TaskScheduler(workspace_manager)
        self.executor = TaskExecutor()
        self.monitor = TaskMonitor(workspace_manager)
        self.recovery = TaskRecovery(workspace_manager)

        # Workflow task management (consolidated from duplicate)
        self.workflow_tasks: Dict[str, Dict[str, Any]] = {}
        self.task_assignments: Dict[str, str] = {}  # task_id -> agent_id
        self.task_dependencies: Dict[str, List[str]] = {}  # task_id -> [dependency_ids]
        self.agent_capabilities: Dict[str, Dict[str, Any]] = {}

        # Contract-based task management (consolidated from perpetual motion)
        self.contract_tasks: Dict[str, Dict[str, Any]] = {}
        self.completed_contract_tasks: Dict[str, Dict[str, Any]] = {}
        self._contract_task_lock = threading.Lock()

        self._sync_modules()

    def _sync_modules(self):
        """Synchronize tasks across all modules."""
        try:
            scheduler_tasks = self.scheduler.tasks
            self.monitor.load_tasks(scheduler_tasks)
            self.recovery.load_tasks(scheduler_tasks)
            self.logger.info("Task modules synchronized successfully")
        except Exception as e:
            self.logger.error(f"Failed to sync modules: {e}")

    # Contract-based Task Management (Consolidated from perpetual motion)
    def create_contract_task(self, contract_data: Dict[str, Any]) -> str:
        """
        Create a new task from contract data.

        Args:
            contract_data: Contract information for task creation

        Returns:
            Task ID of the created task
        """
        try:
            task_id = str(uuid.uuid4())
            task_data = {
                "task_id": task_id,
                "contract_id": contract_data.get("contract_id", ""),
                "title": contract_data.get("title", "Untitled Contract Task"),
                "description": contract_data.get("description", ""),
                "assignee": contract_data.get("assignee", None),
                "state": "new",
                "created_at": datetime.now(),
                "estimated_hours": contract_data.get("estimated_hours", 0),
                "actual_hours": 0,
                "priority": contract_data.get("priority", "medium"),
                "type": "contract",
            }

            with self._contract_task_lock:
                self.contract_tasks[task_id] = task_data

            self.logger.info(f"Contract task created: {task_id}")
            return task_id

        except Exception as e:
            self.logger.error(f"Failed to create contract task: {e}")
            return ""

    def update_contract_task_status(
        self, task_id: str, status: str, details: Dict[str, Any] = None
    ) -> bool:
        """
        Update contract task status.

        Args:
            task_id: ID of the task to update
            status: New status for the task
            details: Additional details to update

        Returns:
            True if update successful, False otherwise
        """
        try:
            with self._contract_task_lock:
                if task_id in self.contract_tasks:
                    self.contract_tasks[task_id]["state"] = status
                    if details:
                        self.contract_tasks[task_id].update(details)
                    self.logger.info(
                        f"Contract task {task_id} status updated to {status}"
                    )
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update contract task status: {e}")
            return False

    def complete_contract_task(
        self, task_id: str, completion_data: Dict[str, Any] = None
    ) -> bool:
        """
        Mark contract task as completed.

        Args:
            task_id: ID of the task to complete
            completion_data: Additional completion information

        Returns:
            True if completion successful, False otherwise
        """
        try:
            with self._contract_task_lock:
                if task_id in self.contract_tasks:
                    task = self.contract_tasks.pop(task_id)
                    task["state"] = "completed"
                    task["completed_at"] = datetime.now()
                    if completion_data:
                        task.update(completion_data)
                    self.completed_contract_tasks[task_id] = task
                    self.logger.info(f"Contract task {task_id} completed successfully")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to complete contract task: {e}")
            return False

    def get_active_contract_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all active contract tasks."""
        with self._contract_task_lock:
            return self.contract_tasks.copy()

    def get_completed_contract_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all completed contract tasks."""
        with self._contract_task_lock:
            return self.completed_contract_tasks.copy()

    # Workflow Task Management (Consolidated from duplicate)
    def create_workflow_task(self, task_definition: Dict[str, Any]) -> str:
        """
        Create new workflow task.

        Args:
            task_definition: Task definition dictionary

        Returns:
            Task ID of the created task
        """
        try:
            task_id = str(uuid.uuid4())
            task = {
                "task_id": task_id,
                "title": task_definition.get("title", "Untitled Task"),
                "description": task_definition.get("description", ""),
                "status": "PENDING",
                "priority": task_definition.get("priority", "MEDIUM"),
                "type": task_definition.get("type", "GENERAL"),
                "dependencies": task_definition.get("dependencies", []),
                "created_at": datetime.now().isoformat(),
                "assigned_agent": None,
                "assignment_time": None,
            }

            self.workflow_tasks[task_id] = task

            # Initialize dependencies
            if task["dependencies"]:
                self.task_dependencies[task_id] = task["dependencies"].copy()

            self.logger.info(f"Workflow task created successfully: {task_id}")
            return task_id

        except Exception as e:
            self.logger.error(f"Failed to create workflow task: {e}")
            raise

    def assign_workflow_task(self, task_id: str, agent_id: str) -> bool:
        """
        Assign workflow task to an agent.

        Args:
            task_id: ID of the task to assign
            agent_id: ID of the agent to assign to

        Returns:
            True if assignment successful, False otherwise
        """
        try:
            if task_id not in self.workflow_tasks:
                self.logger.error(f"Workflow task not found: {task_id}")
                return False

            # Check if task is already assigned
            if task_id in self.task_assignments:
                self.logger.warning(
                    f"Task {task_id} is already assigned to {self.task_assignments[task_id]}"
                )
                return False

            # Assign task
            self.task_assignments[task_id] = agent_id
            self.workflow_tasks[task_id]["status"] = "ASSIGNED"
            self.workflow_tasks[task_id]["assigned_agent"] = agent_id
            self.workflow_tasks[task_id]["assignment_time"] = datetime.now().isoformat()

            self.logger.info(f"Workflow task {task_id} assigned to agent {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to assign workflow task: {e}")
            return False

    def get_workflow_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow task by ID."""
        return self.workflow_tasks.get(task_id)

    def get_all_workflow_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all workflow tasks."""
        return self.workflow_tasks.copy()

    def update_workflow_task_status(self, task_id: str, status: str) -> bool:
        """Update workflow task status."""
        try:
            if task_id in self.workflow_tasks:
                self.workflow_tasks[task_id]["status"] = status
                self.logger.info(f"Workflow task {task_id} status updated to {status}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update workflow task status: {e}")
            return False

    def get_agent_workflow_tasks(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all workflow tasks assigned to a specific agent."""
        try:
            agent_tasks = []
            for task_id, assignment in self.task_assignments.items():
                if assignment == agent_id:
                    task = self.workflow_tasks.get(task_id)
                    if task:
                        agent_tasks.append(task)
            return agent_tasks
        except Exception as e:
            self.logger.error(f"Failed to get agent workflow tasks: {e}")
            return []

    # BaseManager abstract method implementations
    def _on_start(self) -> bool:
        """Task manager specific startup logic."""
        try:
            self.logger.info("Starting Unified Task Manager...")
            self._sync_modules()
            self.logger.info("Unified Task Manager started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Unified Task Manager: {e}")
            return False

    def _on_stop(self):
        """Task manager specific shutdown logic."""
        try:
            self.logger.info("Stopping Unified Task Manager...")
            self.logger.info("Unified Task Manager stopped successfully")
        except Exception as e:
            self.logger.error(f"Error during Unified Task Manager shutdown: {e}")

    def _on_heartbeat(self):
        """Task manager specific heartbeat logic."""
        try:
            system_status = self.get_system_status()
            if system_status.get("status") == "error":
                self.logger.warning("Task system health check failed")
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")

    def _on_initialize_resources(self) -> bool:
        """Task manager specific resource initialization."""
        try:
            self._sync_modules()
            return True
        except Exception as e:
            self.logger.error(f"Resource initialization failed: {e}")
            return False

    def _on_cleanup_resources(self):
        """Task manager specific resource cleanup."""
        try:
            pass  # No specific cleanup needed
        except Exception as e:
            self.logger.error(f"Resource cleanup error: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Task manager specific recovery logic."""
        try:
            self.logger.info(f"Attempting recovery for {context}: {error}")
            self._sync_modules()
            return True
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False

    # Task delegation methods - consolidated by module
    def create_task(self, *args, **kwargs):
        return self.scheduler.create_task(*args, **kwargs)

    def assign_task(self, *args, **kwargs):
        return self.scheduler.assign_task(*args, **kwargs)

    def get_tasks(self, *args, **kwargs):
        return self.scheduler.get_tasks(*args, **kwargs)

    def get_task(self, *args, **kwargs):
        return self.scheduler.get_task(*args, **kwargs)

    def get_development_tasks(self):
        return self.executor.get_all_tasks()

    def claim_development_task(self, *args, **kwargs):
        return self.executor.claim_task(*args, **kwargs)

    def start_development_task(self, *args, **kwargs):
        return self.executor.start_task_work(*args, **kwargs)

    def complete_development_task(self, *args, **kwargs):
        return self.executor.complete_task(*args, **kwargs)

    def get_development_statistics(self):
        return self.executor.get_task_statistics()

    def update_task_status(self, *args, **kwargs):
        return self.monitor.update_task_status(*args, **kwargs)

    def get_task_status(self, *args, **kwargs):
        return self.monitor.get_task_status(*args, **kwargs)

    def get_task_status_summary(self):
        return self.monitor.get_task_status_summary()

    def get_overdue_tasks(self):
        return self.monitor.get_overdue_tasks()

    def get_task_progress_report(self, *args, **kwargs):
        return self.monitor.get_task_progress_report(*args, **kwargs)

    def delete_task(self, *args, **kwargs):
        return self.recovery.delete_task(*args, **kwargs)

    def restore_deleted_task(self, *args, **kwargs):
        return self.recovery.restore_deleted_task(*args, **kwargs)

    def get_deleted_tasks(self):
        return self.recovery.get_deleted_tasks()

    def handle_failed_task(self, *args, **kwargs):
        return self.recovery.handle_failed_task(*args, **kwargs)

    def retry_failed_task(self, *args, **kwargs):
        return self.recovery.retry_failed_task(*args, **kwargs)

    def get_failed_tasks(self):
        return self.recovery.get_failed_tasks()

    def resolve_task_dependencies(self, *args, **kwargs):
        return self.recovery.resolve_task_dependencies(*args, **kwargs)

    def can_task_start(self, *args, **kwargs):
        return self.recovery.can_task_start(*args, **kwargs)

    # Convenience methods
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall task system status."""
        try:
            return {
                "status": self.status,
                "scheduler": self.scheduler.get_system_status(),
                "monitor": self.monitor.get_task_status_summary(),
                "recovery": self.recovery.get_recovery_statistics(),
                "modules": {
                    "scheduler": "active",
                    "executor": "active",
                    "monitor": "active",
                    "recovery": "active",
                },
            }
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"status": "error", "error": str(e)}

    def get_priority_distribution(self):
        return self.scheduler.get_priority_distribution()

    def get_recovery_statistics(self):
        return self.recovery.get_recovery_statistics()

    def cleanup_old_tasks(self, days_old: int = 30):
        return self.executor.cleanup_completed_tasks(days_old)

    def cleanup_deleted_tasks(self, days_old: int = 7):
        return self.recovery.cleanup_deleted_tasks(days_old)

    def export_tasks(self):
        return self.executor.export_tasks()

    def import_tasks(self, tasks_data):
        return self.executor.import_tasks(tasks_data)


def main():
    """CLI interface for Task Manager testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Task Manager Testing Interface")
    parser.add_argument("--init", action="store_true", help="Initialize task manager")
    parser.add_argument(
        "--create",
        nargs=5,
        metavar=("TITLE", "DESCRIPTION", "ASSIGNED_TO", "CREATED_BY", "PRIORITY"),
        help="Create task",
    )
    parser.add_argument(
        "--status", metavar="AGENT_ID", help="Show task status for agent"
    )
    parser.add_argument("--tasks", metavar="AGENT_ID", help="Show tasks for agent")
    parser.add_argument(
        "--update", nargs=2, metavar=("TASK_ID", "STATUS"), help="Update task status"
    )
    parser.add_argument("--test", action="store_true", help="Run task manager tests")

    args = parser.parse_args()

    # Create workspace manager and task manager
    from workspace_manager import WorkspaceManager

    workspace_manager = WorkspaceManager()
    task_manager = TaskManager(workspace_manager)

    if args.init or not any(
        [args.init, args.create, args.status, args.tasks, args.update, args.test]
    ):
        print("📋 Task Manager - Agent Cellphone V2")
        print("Manager initialized successfully with BaseManager inheritance")

    if args.create:
        title, description, assigned_to, created_by, priority = args.create
        task_priority = (
            TaskPriority(priority.lower())
            if priority.lower() in [p.value for p in TaskPriority]
            else TaskPriority.NORMAL
        )
        task_id = task_manager.create_task(
            title, description, assigned_to, created_by, task_priority
        )
        print(
            f"✅ Task created successfully: {task_id}"
            if task_id
            else "❌ Failed to create task"
        )

    if args.status:
        status = task_manager.get_task_status(args.status)
        print(f"📊 Task Status for {args.status}:")
        for key, value in status.items():
            print(f"  {key}: {value}")

    if args.tasks:
        tasks = task_manager.get_tasks(args.tasks)
        print(f"📋 Tasks for {args.tasks}:")
        for task in tasks:
            print(
                f"  {task.task_id}: {task.title} (Priority: {task.priority.value}, Status: {task.status.value})"
            )

    if args.update:
        task_id, status = args.update
        task_status = (
            TaskStatus(status.lower())
            if status.lower() in [s.value for s in TaskStatus]
            else TaskStatus.PENDING
        )
        success = task_manager.update_task_status(task_id, task_status)
        print(f"Task status update: {'✅ Success' if success else '❌ Failed'}")

    if args.test:
        print("🧪 Running task manager tests...")
        try:
            task_id = task_manager.create_task(
                "Test Task",
                "Test description",
                "Agent-1",
                "TestAgent",
                TaskPriority.HIGH,
            )
            print(f"Task creation test: {'✅ Success' if task_id else '❌ Failed'}")

            tasks = task_manager.get_tasks("Agent-1")
            print(f"Task retrieval test: {'✅ Success' if tasks else '❌ Failed'}")

            if task_id:
                success = task_manager.update_task_status(
                    task_id, TaskStatus.IN_PROGRESS
                )
                print(f"Status update test: {'✅ Success' if success else '❌ Failed'}")

            system_status = task_manager.get_system_status()
            print(f"System status test: {'✅ Success' if system_status else '❌ Failed'}")
        except Exception as e:
            print(f"❌ Task manager test failed: {e}")


if __name__ == "__main__":
    main()
