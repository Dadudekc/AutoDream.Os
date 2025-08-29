#!/usr/bin/env python3
"""
Task Scheduler - Agent Cellphone V2
==================================

Handles task scheduling, prioritization, and assignment.
Single responsibility: Task scheduling and priority management.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import json

from src.config import TASK_ID_TIMESTAMP_FORMAT
from src.utils.stability_improvements import stability_manager, safe_import
from .logger import get_task_logger


class TaskPriority(Enum):
    """Task priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


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
    priority: TaskPriority
    status: TaskStatus
    created_at: str
    due_date: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    dependencies: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class TaskScheduler:
    """
    Task Scheduler - Single responsibility: Task scheduling and priority management.

    This service handles:
    - Task creation and assignment
    - Task prioritization and scheduling
    - Task dependencies and relationships
    - Task assignment to agents
    """

    def __init__(self, workspace_manager):
        """Initialize Task Scheduler with workspace manager."""
        self.workspace_manager = workspace_manager
        self.logger = get_task_logger("TaskScheduler")
        self.tasks: Dict[str, Task] = {}
        self.status = "initialized"

        # Load existing tasks
        self._load_tasks()

    def _load_tasks(self):
        """Load existing tasks from all workspaces."""
        try:
            for workspace in self.workspace_manager.get_all_workspaces():
                tasks_path = Path(workspace.tasks_path)
                if tasks_path.exists():
                    for task_file in tasks_path.glob("*.json"):
                        try:
                            with open(task_file, "r") as f:
                                task_data = json.load(f)
                                task = Task(**task_data)
                                self.tasks[task.task_id] = task
                        except Exception as e:
                            self.logger.error(
                                f"Failed to load task from {task_file}: {e}"
                            )

            self.logger.info(f"Loaded {len(self.tasks)} existing tasks")
        except Exception as e:
            self.logger.error(f"Failed to load tasks: {e}")

    def _generate_task_id(self, title: str, assigned_to: str) -> str:
        """Generate unique task ID."""
        timestamp = datetime.now().strftime(TASK_ID_TIMESTAMP_FORMAT)
        safe_title = "".join(
            c for c in title if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        safe_title = safe_title.replace(" ", "_")[:20]
        return f"{safe_title}_{assigned_to}_{timestamp}"

    def create_task(
        self,
        title: str,
        description: str,
        assigned_to: str,
        created_by: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        due_date: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Create a new task."""
        try:
            # Generate task ID
            task_id = self._generate_task_id(title, assigned_to)

            # Create task
            task = Task(
                task_id=task_id,
                title=title,
                description=description,
                assigned_to=assigned_to,
                created_by=created_by,
                priority=priority,
                status=TaskStatus.PENDING,
                created_at=datetime.now().isoformat(),
                due_date=due_date,
                dependencies=dependencies or [],
                metadata=metadata or {},
            )

            # Store task
            self.tasks[task_id] = task

            # Save to assigned agent's workspace
            assigned_workspace = self.workspace_manager.get_workspace_info(assigned_to)
            if assigned_workspace:
                tasks_path = Path(assigned_workspace.tasks_path)
                task_file = tasks_path / f"{task_id}.json"

                with open(task_file, "w") as f:
                    json.dump(task.__dict__, f, indent=2, default=str)

                self.logger.info(f"Task created: {task_id} assigned to {assigned_to}")
                return task_id
            else:
                self.logger.error(f"Assigned agent workspace not found: {assigned_to}")
                return None

        except Exception as e:
            self.logger.error(f"Failed to create task: {e}")
            return None

    def assign_task(self, task_id: str, new_agent: str) -> bool:
        """Reassign a task to a different agent."""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                old_agent = task.assigned_to

                # Check if new agent workspace exists
                new_workspace = self.workspace_manager.get_workspace_info(new_agent)
                if not new_workspace:
                    self.logger.error(f"New agent workspace not found: {new_agent}")
                    return False

                # Remove from old workspace
                old_workspace = self.workspace_manager.get_workspace_info(old_agent)
                if old_workspace:
                    old_task_file = Path(old_workspace.tasks_path) / f"{task_id}.json"
                    if old_task_file.exists():
                        old_task_file.unlink()

                # Update task
                task.assigned_to = new_agent
                task.status = TaskStatus.PENDING  # Reset status for new agent

                # Save to new workspace
                new_task_file = Path(new_workspace.tasks_path) / f"{task_id}.json"
                with open(new_task_file, "w") as f:
                    json.dump(task.__dict__, f, indent=2, default=str)

                self.logger.info(
                    f"Task reassigned: {task_id} {old_agent} -> {new_agent}"
                )
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to reassign task: {e}")
            return False

    def get_tasks(
        self,
        agent_id: str,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> List[Task]:
        """Get tasks for an agent with optional filtering."""
        try:
            tasks = []
            for task in self.tasks.values():
                if task.assigned_to == agent_id:
                    if status and task.status != status:
                        continue
                    if priority and task.priority != priority:
                        continue
                    tasks.append(task)

            # Sort by priority and creation time
            priority_order = {
                TaskPriority.CRITICAL: 0,
                TaskPriority.HIGH: 1,
                TaskPriority.NORMAL: 2,
                TaskPriority.LOW: 3,
            }

            tasks.sort(key=lambda t: (priority_order[t.priority], t.created_at))
            return tasks

        except Exception as e:
            self.logger.error(f"Failed to get tasks for {agent_id}: {e}")
            return []

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        return self.tasks.get(task_id)

    def get_priority_distribution(self) -> Dict[str, int]:
        """Get distribution of tasks by priority."""
        distribution = {}
        for priority in TaskPriority:
            distribution[priority.name] = len(
                [t for t in self.tasks.values() if t.priority == priority]
            )
        return distribution

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall task system status."""
        try:
            total_tasks = len(self.tasks)
            pending_tasks = len(
                [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
            )
            critical_tasks = len(
                [t for t in self.tasks.values() if t.priority == TaskPriority.CRITICAL]
            )
            overdue_tasks = len(
                [
                    t
                    for t in self.tasks.values()
                    if t.due_date and t.due_date < datetime.now().isoformat()
                ]
            )

            return {
                "status": self.status,
                "total_tasks": total_tasks,
                "pending_tasks": pending_tasks,
                "critical_tasks": critical_tasks,
                "overdue_tasks": overdue_tasks,
                "active_agents": len(set(t.assigned_to for t in self.tasks.values())),
            }

        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"status": "error", "error": str(e)}
