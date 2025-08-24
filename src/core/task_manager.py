#!/usr/bin/env python3
"""
Task Manager - Agent Cellphone V2
================================

Manages agent task management with strict OOP design.
Follows Single Responsibility Principle with extracted modules.
"""

import logging
from typing import Dict, List, Optional, Any

from src.utils.stability_improvements import stability_manager, safe_import
from src.core.tasks.scheduling import TaskScheduler, Task, TaskPriority, TaskStatus
from src.core.tasks.execution import TaskExecutor
from src.core.tasks.monitoring import TaskMonitor
from src.core.tasks.recovery import TaskRecovery


class TaskManager:
    """
    Task Manager - Orchestrates extracted task management modules.
    
    This service coordinates:
    - Task scheduling and assignment (TaskScheduler)
    - Task execution and workflow (TaskExecutor)
    - Task monitoring and status (TaskMonitor)
    - Task recovery and error handling (TaskRecovery)
    """

    def __init__(self, workspace_manager):
        """Initialize Task Manager with extracted modules."""
        self.workspace_manager = workspace_manager
        self.logger = self._setup_logging()
        
        # Initialize extracted modules
        self.scheduler = TaskScheduler(workspace_manager)
        self.executor = TaskExecutor()
        self.monitor = TaskMonitor(workspace_manager)
        self.recovery = TaskRecovery(workspace_manager)
        
        self.status = "initialized"
        
        # Load tasks into all modules
        self._sync_modules()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("TaskManager")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _sync_modules(self):
        """Synchronize tasks across all modules."""
        try:
            # Get tasks from scheduler
            scheduler_tasks = self.scheduler.tasks
            
            # Load into monitor and recovery
            self.monitor.load_tasks(scheduler_tasks)
            self.recovery.load_tasks(scheduler_tasks)
            
            self.logger.info("Task modules synchronized successfully")
        except Exception as e:
            self.logger.error(f"Failed to sync modules: {e}")

    # Task Scheduling Methods (delegated to TaskScheduler)
    def create_task(self, *args, **kwargs):
        """Create a new task using TaskScheduler."""
        return self.scheduler.create_task(*args, **kwargs)

    def assign_task(self, *args, **kwargs):
        """Reassign a task using TaskScheduler."""
        return self.scheduler.assign_task(*args, **kwargs)

    def get_tasks(self, *args, **kwargs):
        """Get tasks using TaskScheduler."""
        return self.scheduler.get_tasks(*args, **kwargs)

    def get_task(self, *args, **kwargs):
        """Get a specific task using TaskScheduler."""
        return self.scheduler.get_task(*args, **kwargs)

    # Task Execution Methods (delegated to TaskExecutor)
    def get_development_tasks(self):
        """Get all development tasks using TaskExecutor."""
        return self.executor.get_all_tasks()

    def claim_development_task(self, *args, **kwargs):
        """Claim a development task using TaskExecutor."""
        return self.executor.claim_task(*args, **kwargs)

    def start_development_task(self, *args, **kwargs):
        """Start work on a development task using TaskExecutor."""
        return self.executor.start_task_work(*args, **kwargs)

    def complete_development_task(self, *args, **kwargs):
        """Complete a development task using TaskExecutor."""
        return self.executor.complete_task(*args, **kwargs)

    def get_development_statistics(self):
        """Get development task statistics using TaskExecutor."""
        return self.executor.get_task_statistics()

    # Task Monitoring Methods (delegated to TaskMonitor)
    def update_task_status(self, *args, **kwargs):
        """Update task status using TaskMonitor."""
        return self.monitor.update_task_status(*args, **kwargs)

    def get_task_status(self, *args, **kwargs):
        """Get task status using TaskMonitor."""
        return self.monitor.get_task_status(*args, **kwargs)

    def get_task_status_summary(self):
        """Get task status summary using TaskMonitor."""
        return self.monitor.get_task_status_summary()

    def get_overdue_tasks(self):
        """Get overdue tasks using TaskMonitor."""
        return self.monitor.get_overdue_tasks()

    def get_task_progress_report(self, *args, **kwargs):
        """Get task progress report using TaskMonitor."""
        return self.monitor.get_task_progress_report(*args, **kwargs)

    # Task Recovery Methods (delegated to TaskRecovery)
    def delete_task(self, *args, **kwargs):
        """Delete a task using TaskRecovery."""
        return self.recovery.delete_task(*args, **kwargs)

    def restore_deleted_task(self, *args, **kwargs):
        """Restore a deleted task using TaskRecovery."""
        return self.recovery.restore_deleted_task(*args, **kwargs)

    def get_deleted_tasks(self):
        """Get deleted tasks using TaskRecovery."""
        return self.recovery.get_deleted_tasks()

    def handle_failed_task(self, *args, **kwargs):
        """Handle a failed task using TaskRecovery."""
        return self.recovery.handle_failed_task(*args, **kwargs)

    def retry_failed_task(self, *args, **kwargs):
        """Retry a failed task using TaskRecovery."""
        return self.recovery.retry_failed_task(*args, **kwargs)

    def get_failed_tasks(self):
        """Get failed tasks using TaskRecovery."""
        return self.recovery.get_failed_tasks()

    def resolve_task_dependencies(self, *args, **kwargs):
        """Resolve task dependencies using TaskRecovery."""
        return self.recovery.resolve_task_dependencies(*args, **kwargs)

    def can_task_start(self, *args, **kwargs):
        """Check if task can start using TaskRecovery."""
        return self.recovery.can_task_start(*args, **kwargs)

    # Convenience Methods
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall task system status."""
        try:
            scheduler_status = self.scheduler.get_system_status()
            monitor_summary = self.monitor.get_task_status_summary()
            recovery_stats = self.recovery.get_recovery_statistics()
            
            return {
                "status": self.status,
                "scheduler": scheduler_status,
                "monitor": monitor_summary,
                "recovery": recovery_stats,
                "modules": {
                    "scheduler": "active",
                    "executor": "active", 
                    "monitor": "active",
                    "recovery": "active"
                }
            }
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"status": "error", "error": str(e)}

    def get_priority_distribution(self):
        """Get priority distribution using TaskScheduler."""
        return self.scheduler.get_priority_distribution()

    def get_recovery_statistics(self):
        """Get recovery statistics using TaskRecovery."""
        return self.recovery.get_recovery_statistics()

    def cleanup_old_tasks(self, days_old: int = 30):
        """Clean up old tasks using TaskExecutor."""
        return self.executor.cleanup_completed_tasks(days_old)

    def cleanup_deleted_tasks(self, days_old: int = 7):
        """Clean up old deleted tasks using TaskRecovery."""
        return self.recovery.cleanup_deleted_tasks(days_old)

    def export_tasks(self):
        """Export tasks using TaskExecutor."""
        return self.executor.export_tasks()

    def import_tasks(self, tasks_data):
        """Import tasks using TaskExecutor."""
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

    # Create workspace manager first
    from workspace_manager import WorkspaceManager

    workspace_manager = WorkspaceManager()

    # Create task manager
    task_manager = TaskManager(workspace_manager)

    if args.init or not any(
        [args.init, args.create, args.status, args.tasks, args.update, args.test]
    ):
        print("📋 Task Manager - Agent Cellphone V2")
        print("Manager initialized successfully with extracted modules")

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
        if task_id:
            print(f"✅ Task created successfully: {task_id}")
        else:
            print("❌ Failed to create task")

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
            # Test task creation
            task_id = task_manager.create_task(
                "Test Task",
                "Test description",
                "Agent-1",
                "TestAgent",
                TaskPriority.HIGH,
            )
            print(f"Task creation test: {'✅ Success' if task_id else '❌ Failed'}")

            # Test task retrieval
            tasks = task_manager.get_tasks("Agent-1")
            print(f"Task retrieval test: {'✅ Success' if tasks else '❌ Failed'}")

            # Test status update
            if task_id:
                success = task_manager.update_task_status(
                    task_id, TaskStatus.IN_PROGRESS
                )
                print(f"Status update test: {'✅ Success' if success else '❌ Failed'}")

            # Test system status
            system_status = task_manager.get_system_status()
            print(f"System status test: {'✅ Success' if system_status else '❌ Failed'}")

        except Exception as e:
            print(f"❌ Task manager test failed: {e}")


if __name__ == "__main__":
    main()
