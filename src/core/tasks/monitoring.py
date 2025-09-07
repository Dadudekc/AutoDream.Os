#!/usr/bin/env python3
"""
Task Monitor - Agent Cellphone V2
=================================

Handles task monitoring, status tracking, and status updates.
Single responsibility: Task monitoring and status tracking.
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


class TaskMonitor:
    """
    Task Monitor - Single responsibility: Task monitoring and status tracking.
    
    This service handles:
    - Task status updates and tracking
    - Task status reporting and statistics
    - Task status queries and filtering
    - Task status persistence
    """

    def __init__(self, workspace_manager):
        """Initialize Task Monitor with workspace manager."""
        self.workspace_manager = workspace_manager
        self.logger = logging.getLogger(__name__)
        self.tasks: Dict[str, Task] = {}

    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update task status."""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                old_status = task.status
                task.status = status

                # Update timestamps
                if status == TaskStatus.IN_PROGRESS and not task.started_at:
                    task.started_at = datetime.now().isoformat()
                elif status == TaskStatus.COMPLETED:
                    task.completed_at = datetime.now().isoformat()

                # Update file
                assigned_workspace = self.workspace_manager.get_workspace_info(
                    task.assigned_to
                )
                if assigned_workspace:
                    tasks_path = Path(assigned_workspace.tasks_path)
                    task_file = tasks_path / f"{task_id}.json"

                    with open(task_file, "w") as f:
                        json.dump(task.__dict__, f, indent=2, default=str)

                    self.logger.info(
                        f"Task status updated: {task_id} {old_status.value} -> {status.value}"
                    )
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update task status: {e}")
            return False

    def get_task_status(self, agent_id: str) -> Dict[str, Any]:
        """Get task status for an agent."""
        try:
            tasks = [t for t in self.tasks.values() if t.assigned_to == agent_id]

            status_counts = {}
            for status in TaskStatus:
                status_counts[status.value] = len(
                    [t for t in tasks if t.status == status]
                )

            # Count by priority (assuming priority is stored as string)
            priority_counts = {}
            for task in tasks:
                priority = task.priority
                priority_counts[priority] = priority_counts.get(priority, 0) + 1

            pending_tasks = [t for t in tasks if t.status == TaskStatus.PENDING]
            critical_tasks = [t for t in tasks if t.priority == "critical"]

            return {
                "agent_id": agent_id,
                "total_tasks": len(tasks),
                "status_counts": status_counts,
                "priority_counts": priority_counts,
                "pending_count": len(pending_tasks),
                "critical_count": len(critical_tasks),
                "overdue_count": len(
                    [
                        t
                        for t in tasks
                        if t.due_date and t.due_date < datetime.now().isoformat()
                    ]
                ),
            }

        except Exception as e:
            self.logger.error(f"Failed to get task status for {agent_id}: {e}")
            return {"agent_id": agent_id, "error": str(e)}

    def get_task_status_summary(self) -> Dict[str, Any]:
        """Get overall task status summary."""
        try:
            total_tasks = len(self.tasks)
            status_summary = {}
            
            for status in TaskStatus:
                count = len([t for t in self.tasks.values() if t.status == status])
                status_summary[status.value] = count

            # Priority summary
            priority_summary = {}
            for task in self.tasks.values():
                priority = task.priority
                priority_summary[priority] = priority_summary.get(priority, 0) + 1

            # Agent summary
            agent_summary = {}
            for task in self.tasks.values():
                agent = task.assigned_to
                agent_summary[agent] = agent_summary.get(agent, 0) + 1

            return {
                "total_tasks": total_tasks,
                "status_summary": status_summary,
                "priority_summary": priority_summary,
                "agent_summary": agent_summary,
                "active_agents": len(agent_summary),
            }

        except Exception as e:
            self.logger.error(f"Failed to get task status summary: {e}")
            return {"error": str(e)}

    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks."""
        try:
            current_time = datetime.now().isoformat()
            overdue_tasks = []
            
            for task in self.tasks.values():
                if task.due_date and task.due_date < current_time:
                    if task.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
                        overdue_tasks.append(task)
            
            return overdue_tasks
        except Exception as e:
            self.logger.error(f"Failed to get overdue tasks: {e}")
            return []

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with a specific status."""
        try:
            return [task for task in self.tasks.values() if task.status == status]
        except Exception as e:
            self.logger.error(f"Failed to get tasks by status {status}: {e}")
            return []

    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Get all tasks with a specific priority."""
        try:
            return [task for task in self.tasks.values() if task.priority == priority]
        except Exception as e:
            self.logger.error(f"Failed to get tasks by priority {priority}: {e}")
            return []

    def get_tasks_by_agent(self, agent_id: str) -> List[Task]:
        """Get all tasks assigned to a specific agent."""
        try:
            return [task for task in self.tasks.values() if task.assigned_to == agent_id]
        except Exception as e:
            self.logger.error(f"Failed to get tasks by agent {agent_id}: {e}")
            return []

    def get_task_progress_report(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed progress report for an agent."""
        try:
            agent_tasks = self.get_tasks_by_agent(agent_id)
            
            if not agent_tasks:
                return {
                    "agent_id": agent_id,
                    "message": "No tasks assigned",
                    "progress": 0.0
                }

            total_tasks = len(agent_tasks)
            completed_tasks = len([t for t in agent_tasks if t.status == TaskStatus.COMPLETED])
            in_progress_tasks = len([t for t in agent_tasks if t.status == TaskStatus.IN_PROGRESS])
            pending_tasks = len([t for t in agent_tasks if t.status == TaskStatus.PENDING])
            blocked_tasks = len([t for t in agent_tasks if t.status == TaskStatus.BLOCKED])

            progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

            return {
                "agent_id": agent_id,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "in_progress_tasks": in_progress_tasks,
                "pending_tasks": pending_tasks,
                "blocked_tasks": blocked_tasks,
                "progress_percentage": round(progress_percentage, 2),
                "completion_rate": f"{completed_tasks}/{total_tasks}"
            }

        except Exception as e:
            self.logger.error(f"Failed to get progress report for {agent_id}: {e}")
            return {"agent_id": agent_id, "error": str(e)}

    def load_tasks(self, tasks: Dict[str, Task]):
        """Load tasks into the monitor."""
        self.tasks = tasks
        self.logger.info(f"Loaded {len(tasks)} tasks into monitor")

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        return self.tasks.get(task_id)

