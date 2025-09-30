"""
Task Core - V2 Compliant
========================

Core Task entity with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from .task_enums import TaskPriority, TaskStatus, TaskType

logger = logging.getLogger(__name__)


@dataclass
class TaskCore:
    """Core Task entity with essential functionality."""

    task_id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.NORMAL
    task_type: TaskType = TaskType.DEVELOPMENT

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    due_date: datetime | None = None

    # Assignment
    assigned_to: str | None = None
    assigned_by: str | None = None

    # Progress tracking
    progress: int = 0
    estimated_hours: float | None = None
    actual_hours: float | None = None

    # Metadata
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def update_status(self, new_status: TaskStatus) -> None:
        """Update task status and timestamp."""
        self.status = new_status
        self.updated_at = datetime.now()
        logger.info(f"Task {self.task_id} status updated to {new_status.value}")

    def update_progress(self, progress: int) -> None:
        """Update task progress."""
        if 0 <= progress <= 100:
            self.progress = progress
            self.updated_at = datetime.now()
            logger.info(f"Task {self.task_id} progress updated to {progress}%")
        else:
            raise ValueError("Progress must be between 0 and 100")

    def assign_to(self, agent_id: str, assigned_by: str) -> None:
        """Assign task to agent."""
        self.assigned_to = agent_id
        self.assigned_by = assigned_by
        self.updated_at = datetime.now()
        logger.info(f"Task {self.task_id} assigned to {agent_id} by {assigned_by}")

    def add_tag(self, tag: str) -> None:
        """Add tag to task."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        """Remove tag from task."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata key-value pair."""
        self.metadata[key] = value
        self.updated_at = datetime.now()

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value."""
        return self.metadata.get(key, default)

    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.due_date and self.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            return datetime.now() > self.due_date
        return False

    def time_remaining(self) -> timedelta | None:
        """Get time remaining until due date."""
        if self.due_date and self.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            return self.due_date - datetime.now()
        return None

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "task_type": self.task_type.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "assigned_to": self.assigned_to,
            "assigned_by": self.assigned_by,
            "progress": self.progress,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "tags": self.tags,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskCore":
        """Create task from dictionary."""
        task = cls()
        task.task_id = data.get("task_id", str(uuid4()))
        task.title = data.get("title", "")
        task.description = data.get("description", "")
        task.status = TaskStatus(data.get("status", "pending"))
        task.priority = TaskPriority(data.get("priority", "normal"))
        task.task_type = TaskType(data.get("task_type", "development"))

        # Parse timestamps
        if data.get("created_at"):
            task.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            task.updated_at = datetime.fromisoformat(data["updated_at"])
        if data.get("due_date"):
            task.due_date = datetime.fromisoformat(data["due_date"])

        task.assigned_to = data.get("assigned_to")
        task.assigned_by = data.get("assigned_by")
        task.progress = data.get("progress", 0)
        task.estimated_hours = data.get("estimated_hours")
        task.actual_hours = data.get("actual_hours")
        task.tags = data.get("tags", [])
        task.metadata = data.get("metadata", {})

        return task
