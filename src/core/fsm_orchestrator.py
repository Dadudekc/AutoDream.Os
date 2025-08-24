#!/usr/bin/env python3
"""
FSM Orchestrator - V2 Core FSM Management System

This module orchestrates FSM tasks and workflows.
Follows Single Responsibility Principle - FSM orchestration only.
Architecture: Single Responsibility Principle - FSM orchestration only
LOC: Target 200 lines (under 200 limit)
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json
import threading
import time

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels"""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(Enum):
    """Task status states"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class FSMTask:
    """FSM task definition"""

    task_id: str
    title: str
    description: str
    assigned_agent: str
    priority: TaskPriority
    status: TaskStatus
    created_at: str
    updated_at: str
    completed_at: Optional[str]
    metadata: Dict[str, Any]


class FSMOrchestrator:
    """
    Orchestrates FSM tasks and workflows

    Responsibilities:
    - FSM task creation and management
    - Task assignment and tracking
    - Workflow orchestration
    - Task status monitoring
    """

    def __init__(self, workspace_manager, inbox_manager):
        self.workspace_manager = workspace_manager
        self.inbox_manager = inbox_manager
        self.tasks: Dict[str, FSMTask] = {}
        self.logger = logging.getLogger(f"{__name__}.FSMOrchestrator")
        self.monitoring = False
        self.monitor_thread = None

        # Load existing tasks
        self._load_tasks()

    def create_task(
        self,
        title: str,
        description: str,
        assigned_agent: str,
        priority: TaskPriority = TaskPriority.NORMAL,
    ) -> str:
        """Create a new FSM task"""
        try:
            task_id = f"TASK-{len(self.tasks) + 1:03d}"
            current_time = datetime.now().isoformat()

            task = FSMTask(
                task_id=task_id,
                title=title,
                description=description,
                assigned_agent=assigned_agent,
                priority=priority,
                status=TaskStatus.PENDING,
                created_at=current_time,
                updated_at=current_time,
                completed_at=None,
                metadata={},
            )

            self.tasks[task_id] = task
            self._save_task(task)

            self.logger.info(f"Created FSM task {task_id} for {assigned_agent}")
            return task_id

        except Exception as e:
            self.logger.error(f"Failed to create FSM task: {e}")
            return ""

    def get_task(self, task_id: str) -> Optional[FSMTask]:
        """Get task by ID"""
        return self.tasks.get(task_id)

    def get_tasks_by_agent(self, agent_id: str) -> List[FSMTask]:
        """Get all tasks assigned to an agent"""
        return [task for task in self.tasks.values() if task.assigned_agent == agent_id]

    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update task status"""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.status = status
                task.updated_at = datetime.now().isoformat()

                if status == TaskStatus.COMPLETED:
                    task.completed_at = datetime.now().isoformat()

                if metadata:
                    task.metadata.update(metadata)

                self._save_task(task)
                self.logger.info(f"Updated task {task_id} status to {status.value}")
                return True

            return False

        except Exception as e:
            self.logger.error(f"Failed to update task status: {e}")
            return False

    def start_monitoring(self):
        """Start FSM monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop, daemon=True
            )
            self.monitor_thread.start()
            self.logger.info("FSM monitoring started")

    def stop_monitoring(self):
        """Stop FSM monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        self.logger.info("FSM monitoring stopped")

    def _monitor_loop(self):
        """FSM monitoring loop"""
        while self.monitoring:
            try:
                # Check for stalled tasks
                current_time = datetime.now()
                for task in self.tasks.values():
                    if task.status == TaskStatus.IN_PROGRESS and task.updated_at:
                        updated_time = datetime.fromisoformat(task.updated_at)
                        if (
                            current_time - updated_time
                        ).total_seconds() > 3600:  # 1 hour
                            self.logger.warning(f"Task {task.task_id} may be stalled")

                time.sleep(60)  # Check every minute

            except Exception as e:
                self.logger.error(f"FSM monitoring error: {e}")
                time.sleep(60)

    def _save_task(self, task: FSMTask):
        """Save task to file"""
        try:
            task_dir = Path("fsm_data") / "tasks"
            task_dir.mkdir(parents=True, exist_ok=True)

            task_file = task_dir / f"{task.task_id}.json"
            task_data = {
                "task_id": task.task_id,
                "title": task.title,
                "description": task.description,
                "assigned_agent": task.assigned_agent,
                "priority": task.priority.value,
                "status": task.status.value,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "completed_at": task.completed_at,
                "metadata": task.metadata,
            }

            with open(task_file, "w") as f:
                json.dump(task_data, f, indent=2)

        except Exception as e:
            self.logger.error(f"Failed to save task {task.task_id}: {e}")

    def _load_tasks(self):
        """Load existing tasks from files"""
        try:
            task_dir = Path("fsm_data") / "tasks"
            if not task_dir.exists():
                return

            for task_file in task_dir.glob("*.json"):
                try:
                    with open(task_file, "r") as f:
                        task_data = json.load(f)

                    task = FSMTask(
                        task_id=task_data["task_id"],
                        title=task_data["title"],
                        description=task_data["description"],
                        assigned_agent=task_data["assigned_agent"],
                        priority=TaskPriority(task_data["priority"]),
                        status=TaskStatus(task_data["status"]),
                        created_at=task_data["created_at"],
                        updated_at=task_data["updated_at"],
                        completed_at=task_data.get("completed_at"),
                        metadata=task_data.get("metadata", {}),
                    )

                    self.tasks[task.task_id] = task

                except Exception as e:
                    self.logger.error(f"Failed to load task from {task_file}: {e}")

        except Exception as e:
            self.logger.error(f"Failed to load tasks: {e}")

    def get_system_summary(self) -> Dict[str, Any]:
        """Get FSM system summary"""
        return {
            "total_tasks": len(self.tasks),
            "pending_tasks": len(
                [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
            ),
            "in_progress_tasks": len(
                [t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]
            ),
            "completed_tasks": len(
                [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]
            ),
            "failed_tasks": len(
                [t for t in self.tasks.values() if t.status == TaskStatus.FAILED]
            ),
            "monitoring_active": self.monitoring,
        }
