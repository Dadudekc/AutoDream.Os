#!/usr/bin/env python3
"""
Task Recovery - Agent Cellphone V2
==================================

Handles task recovery, error handling, and task deletion.
Single responsibility: Task recovery and error handling.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import json
from dataclasses import dataclass
from enum import Enum

from src.utils.stability_improvements import stability_manager, safe_import


class TaskStatus(Enum):
    """Task status states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """Task data structure."""
    task_id: str
    title: str
    description: str
    assigned_to: str
    created_by: str
    priority: str
    status: TaskStatus
    created_at: str
    due_date: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    dependencies: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class TaskRecovery:
    """
    Task Recovery - Single responsibility: Task recovery and error handling.
    
    This service handles:
    - Task deletion and cleanup
    - Error recovery and task restoration
    - Failed task handling
    - Task dependency resolution
    """

    def __init__(self, workspace_manager):
        """Initialize Task Recovery with workspace manager."""
        self.workspace_manager = workspace_manager
        self.logger = logging.getLogger(__name__)
        self.tasks: Dict[str, Task] = {}
        self.deleted_tasks: Dict[str, Task] = {}  # Backup of deleted tasks

    def delete_task(self, task_id: str) -> bool:
        """Delete a task with recovery backup."""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]

                # Backup task before deletion
                self.deleted_tasks[task_id] = task

                # Remove from file system
                assigned_workspace = self.workspace_manager.get_workspace_info(
                    task.assigned_to
                )
                if assigned_workspace:
                    tasks_path = Path(assigned_workspace.tasks_path)
                    task_file = tasks_path / f"{task_id}.json"

                    if task_file.exists():
                        task_file.unlink()

                # Remove from memory
                del self.tasks[task_id]

                self.logger.info(f"Task deleted: {task_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete task: {e}")
            return False

    def restore_deleted_task(self, task_id: str) -> bool:
        """Restore a previously deleted task."""
        try:
            if task_id in self.deleted_tasks:
                task = self.deleted_tasks[task_id]
                
                # Restore to main tasks
                self.tasks[task_id] = task
                
                # Save to file system
                assigned_workspace = self.workspace_manager.get_workspace_info(
                    task.assigned_to
                )
                if assigned_workspace:
                    tasks_path = Path(assigned_workspace.tasks_path)
                    task_file = tasks_path / f"{task_id}.json"

                    with open(task_file, "w") as f:
                        json.dump(task.__dict__, f, indent=2, default=str)

                # Remove from deleted tasks
                del self.deleted_tasks[task_id]

                self.logger.info(f"Task restored: {task_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to restore task: {e}")
            return False

    def get_deleted_tasks(self) -> List[Task]:
        """Get list of deleted tasks available for restoration."""
        return list(self.deleted_tasks.values())

    def permanently_delete_task(self, task_id: str) -> bool:
        """Permanently delete a task without recovery option."""
        try:
            if task_id in self.deleted_tasks:
                del self.deleted_tasks[task_id]
                self.logger.info(f"Task permanently deleted: {task_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to permanently delete task: {e}")
            return False

    def cleanup_deleted_tasks(self, days_old: int = 7) -> int:
        """Clean up old deleted tasks."""
        try:
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            removed_count = 0
            to_remove = []

            for task_id, task in self.deleted_tasks.items():
                # Parse created_at timestamp
                try:
                    task_timestamp = datetime.fromisoformat(task.created_at.replace('Z', '+00:00')).timestamp()
                    if task_timestamp < cutoff_date:
                        to_remove.append(task_id)
                except:
                    # If timestamp parsing fails, remove the task
                    to_remove.append(task_id)

            for task_id in to_remove:
                del self.deleted_tasks[task_id]
                removed_count += 1

            self.logger.info(f"Cleaned up {removed_count} old deleted tasks")
            return removed_count
        except Exception as e:
            self.logger.error(f"Failed to cleanup deleted tasks: {e}")
            return 0

    def handle_failed_task(self, task_id: str, error_message: str) -> bool:
        """Handle a task that has failed with error recovery."""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                
                # Update task metadata with error information
                if not task.metadata:
                    task.metadata = {}
                
                task.metadata["last_error"] = error_message
                task.metadata["error_timestamp"] = datetime.now().isoformat()
                task.metadata["error_count"] = task.metadata.get("error_count", 0) + 1
                
                # Mark task as failed
                task.status = TaskStatus.FAILED
                
                # Save updated task
                assigned_workspace = self.workspace_manager.get_workspace_info(
                    task.assigned_to
                )
                if assigned_workspace:
                    tasks_path = Path(assigned_workspace.tasks_path)
                    task_file = tasks_path / f"{task_id}.json"

                    with open(task_file, "w") as f:
                        json.dump(task.__dict__, f, indent=2, default=str)

                self.logger.info(f"Task marked as failed: {task_id} - {error_message}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to handle failed task: {e}")
            return False

    def retry_failed_task(self, task_id: str) -> bool:
        """Retry a previously failed task."""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                
                if task.status == TaskStatus.FAILED:
                    # Reset task status to pending
                    task.status = TaskStatus.PENDING
                    
                    # Clear error information
                    if task.metadata:
                        task.metadata.pop("last_error", None)
                        task.metadata.pop("error_timestamp", None)
                    
                    # Save updated task
                    assigned_workspace = self.workspace_manager.get_workspace_info(
                        task.assigned_to
                    )
                    if assigned_workspace:
                        tasks_path = Path(assigned_workspace.tasks_path)
                        task_file = tasks_path / f"{task_id}.json"

                        with open(task_file, "w") as f:
                            json.dump(task.__dict__, f, indent=2, default=str)

                    self.logger.info(f"Task retry initiated: {task_id}")
                    return True
                else:
                    self.logger.warning(f"Task {task_id} is not in failed status")
                    return False
            return False
        except Exception as e:
            self.logger.error(f"Failed to retry task: {e}")
            return False

    def get_failed_tasks(self) -> List[Task]:
        """Get all failed tasks."""
        try:
            return [task for task in self.tasks.values() if task.status == TaskStatus.FAILED]
        except Exception as e:
            self.logger.error(f"Failed to get failed tasks: {e}")
            return []

    def resolve_task_dependencies(self, task_id: str) -> List[str]:
        """Resolve dependencies for a specific task."""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                
                if not task.dependencies:
                    return []
                
                resolved_dependencies = []
                unresolved_dependencies = []
                
                for dep_id in task.dependencies:
                    if dep_id in self.tasks:
                        dep_task = self.tasks[dep_id]
                        if dep_task.status == TaskStatus.COMPLETED:
                            resolved_dependencies.append(dep_id)
                        else:
                            unresolved_dependencies.append(dep_id)
                    else:
                        unresolved_dependencies.append(dep_id)
                
                # Log dependency status
                if unresolved_dependencies:
                    self.logger.info(f"Task {task_id} has unresolved dependencies: {unresolved_dependencies}")
                
                return resolved_dependencies
            return []
        except Exception as e:
            self.logger.error(f"Failed to resolve dependencies for task {task_id}: {e}")
            return []

    def can_task_start(self, task_id: str) -> bool:
        """Check if a task can start based on its dependencies."""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                
                if not task.dependencies:
                    return True
                
                # Check if all dependencies are completed
                for dep_id in task.dependencies:
                    if dep_id in self.tasks:
                        dep_task = self.tasks[dep_id]
                        if dep_task.status != TaskStatus.COMPLETED:
                            return False
                    else:
                        # Dependency task not found
                        return False
                
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to check if task {task_id} can start: {e}")
            return False

    def load_tasks(self, tasks: Dict[str, Task]):
        """Load tasks into the recovery system."""
        self.tasks = tasks
        self.logger.info(f"Loaded {len(tasks)} tasks into recovery system")

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        return self.tasks.get(task_id)

    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get recovery system statistics."""
        try:
            return {
                "total_tasks": len(self.tasks),
                "deleted_tasks": len(self.deleted_tasks),
                "failed_tasks": len(self.get_failed_tasks()),
                "recoverable_tasks": len(self.deleted_tasks),
                "tasks_with_dependencies": len([t for t in self.tasks.values() if t.dependencies]),
                "ready_to_start": len([t for t in self.tasks.values() if self.can_task_start(t.task_id)])
            }
        except Exception as e:
            self.logger.error(f"Failed to get recovery statistics: {e}")
            return {"error": str(e)}
