"""
Task Entity - V2 Compliant (Simplified)
======================================

Core Task entity with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Integration Specialist)
License: MIT
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority enumeration."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(Enum):
    """Task type enumeration."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    SYSTEM = "system"


class TaskCategory(Enum):
    """Task category enumeration."""

    SYSTEM_OPERATION = "system_operation"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    INTEGRATION = "integration"
    MONITORING = "monitoring"


@dataclass
class TaskRequirements:
    """Task requirements and constraints."""

    required_skills: list[str] = field(default_factory=list)
    estimated_duration: timedelta | None = None
    max_retries: int = 3
    dependencies: list[str] = field(default_factory=list)


@dataclass
class TaskProgress:
    """Task progress tracking."""

    percentage_complete: float = 0.0
    current_phase: str = "initialization"
    milestones: list[str] = field(default_factory=list)
    completed_milestones: list[str] = field(default_factory=list)
    last_update: datetime | None = None
    notes: list[str] = field(default_factory=list)


@dataclass
class TaskMetrics:
    """Task performance metrics."""

    time_created: datetime = field(default_factory=datetime.now)
    time_started: datetime | None = None
    time_completed: datetime | None = None
    total_duration: timedelta | None = None
    retry_count: int = 0
    error_count: int = 0
    last_error: str | None = None


class Task:
    """
    Core Task entity representing a work item in the system.

    Simplified version focusing on essential functionality.
    """

    def __init__(
        self,
        task_id: str,
        title: str,
        description: str,
        task_type: TaskType,
        priority: TaskPriority = TaskPriority.NORMAL,
        requirements: TaskRequirements | None = None,
        assigned_agent: str | None = None,
    ):
        """Initialize a new Task."""
        self._id = task_id
        self._title = title
        self._description = description
        self._task_type = task_type
        self._priority = priority
        self._status = TaskStatus.PENDING
        self._requirements = requirements or TaskRequirements()
        self._progress = TaskProgress()
        self._metrics = TaskMetrics()
        self._assigned_agent = assigned_agent
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._tags: list[str] = []

        logger.info(f"Task created: {self._title} ({self._task_type.value})")

    # Properties
    @property
    def id(self) -> str:
        """Get the task ID."""
        return self._id

    @property
    def title(self) -> str:
        """Get the task title."""
        return self._title

    @property
    def description(self) -> str:
        """Get the task description."""
        return self._description

    @property
    def task_type(self) -> TaskType:
        """Get the task type."""
        return self._task_type

    @property
    def priority(self) -> TaskPriority:
        """Get the task priority."""
        return self._priority

    @property
    def status(self) -> TaskStatus:
        """Get the current task status."""
        return self._status

    @property
    def requirements(self) -> TaskRequirements:
        """Get the task requirements."""
        return self._requirements

    @property
    def progress(self) -> TaskProgress:
        """Get the task progress."""
        return self._progress

    @property
    def metrics(self) -> TaskMetrics:
        """Get the task metrics."""
        return self._metrics

    @property
    def assigned_agent(self) -> str | None:
        """Get the assigned agent ID."""
        return self._assigned_agent

    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get the last update timestamp."""
        return self._updated_at

    @property
    def tags(self) -> list[str]:
        """Get the task tags."""
        return self._tags.copy()

    # Task lifecycle methods
    def assign_to_agent(self, agent_id: str) -> bool:
        """Assign the task to an agent."""
        if self._status != TaskStatus.PENDING:
            logger.warning(f"Task {self._id} is not in pending status")
            return False

        self._assigned_agent = agent_id
        self._status = TaskStatus.IN_PROGRESS
        self._metrics.time_started = datetime.now()
        self._progress.current_phase = "execution"
        self._progress.last_update = datetime.now()
        self._updated_at = datetime.now()
        logger.info(f"Task {self._id} assigned to agent {agent_id}")
        return True

    def complete(self, success: bool = True) -> None:
        """Complete the task."""
        if self._status != TaskStatus.IN_PROGRESS:
            logger.warning(f"Task {self._id} is not in progress")
            return

        self._status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
        self._metrics.time_completed = datetime.now()
        self._progress.percentage_complete = (
            100.0 if success else self._progress.percentage_complete
        )
        self._progress.current_phase = "completed" if success else "failed"
        self._progress.last_update = datetime.now()

        if self._metrics.time_started:
            self._metrics.total_duration = self._metrics.time_completed - self._metrics.time_started

        self._updated_at = datetime.now()
        logger.info(f"Task {self._id} completed (success: {success})")

    def cancel(self, reason: str = "") -> None:
        """Cancel the task."""
        self._status = TaskStatus.CANCELLED
        self._progress.current_phase = "cancelled"
        self._progress.last_update = datetime.now()
        self._updated_at = datetime.now()
        if reason:
            self._progress.notes.append(f"Cancelled: {reason}")
        logger.info(f"Task {self._id} cancelled: {reason}")

    # Progress methods
    def update_progress(self, percentage: float, phase: str = None, note: str = None) -> None:
        """Update task progress."""
        if not 0 <= percentage <= 100:
            raise ValueError("Progress percentage must be between 0 and 100")

        self._progress.percentage_complete = percentage
        if phase:
            self._progress.current_phase = phase
        if note:
            self._progress.notes.append(f"{datetime.now().isoformat()}: {note}")

        self._progress.last_update = datetime.now()
        self._updated_at = datetime.now()
        logger.debug(f"Task {self._id} progress updated: {percentage}%")

    def add_milestone(self, milestone: str) -> None:
        """Add a milestone to the task."""
        self._progress.milestones.append(milestone)
        self._updated_at = datetime.now()
        logger.debug(f"Milestone added to task {self._id}: {milestone}")

    def complete_milestone(self, milestone: str) -> None:
        """Mark a milestone as completed."""
        if (
            milestone in self._progress.milestones
            and milestone not in self._progress.completed_milestones
        ):
            self._progress.completed_milestones.append(milestone)
            self._updated_at = datetime.now()
            logger.debug(f"Milestone completed for task {self._id}: {milestone}")

    def retry(self, error_message: str = "") -> bool:
        """Retry the task after failure."""
        if self._metrics.retry_count >= self._requirements.max_retries:
            logger.warning(f"Task {self._id} exceeded max retries")
            return False

        self._metrics.retry_count += 1
        self._metrics.error_count += 1
        if error_message:
            self._metrics.last_error = error_message
            self._progress.notes.append(f"Retry {self._metrics.retry_count}: {error_message}")

        self._status = TaskStatus.IN_PROGRESS
        self._progress.current_phase = "retry"
        self._progress.last_update = datetime.now()
        self._updated_at = datetime.now()
        logger.info(f"Task {self._id} retry {self._metrics.retry_count}")
        return True

    # Utility methods
    def add_tag(self, tag: str) -> None:
        """Add a tag to the task."""
        if tag not in self._tags:
            self._tags.append(tag)
            self._updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the task."""
        if tag in self._tags:
            self._tags.remove(tag)
            self._updated_at = datetime.now()

    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        if not self._requirements.estimated_duration:
            return False

        expected_completion = self._created_at + self._requirements.estimated_duration
        return datetime.now() > expected_completion and self._status not in [
            TaskStatus.COMPLETED,
            TaskStatus.CANCELLED,
        ]

    def get_estimated_completion(self) -> datetime | None:
        """Get estimated completion time."""
        if not self._requirements.estimated_duration:
            return None

        if self._metrics.time_started:
            return self._metrics.time_started + self._requirements.estimated_duration
        else:
            return self._created_at + self._requirements.estimated_duration

    # Serialization methods
    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary representation."""
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "task_type": self._task_type.value,
            "priority": self._priority.value,
            "status": self._status.value,
            "assigned_agent": self._assigned_agent,
            "requirements": {
                "required_skills": self._requirements.required_skills,
                "estimated_duration": self._requirements.estimated_duration.total_seconds()
                if self._requirements.estimated_duration
                else None,
                "max_retries": self._requirements.max_retries,
                "dependencies": self._requirements.dependencies,
            },
            "progress": {
                "percentage_complete": self._progress.percentage_complete,
                "current_phase": self._progress.current_phase,
                "milestones": self._progress.milestones,
                "completed_milestones": self._progress.completed_milestones,
                "last_update": self._progress.last_update.isoformat()
                if self._progress.last_update
                else None,
                "notes": self._progress.notes,
            },
            "metrics": {
                "time_created": self._metrics.time_created.isoformat(),
                "time_started": self._metrics.time_started.isoformat()
                if self._metrics.time_started
                else None,
                "time_completed": self._metrics.time_completed.isoformat()
                if self._metrics.time_completed
                else None,
                "total_duration": self._metrics.total_duration.total_seconds()
                if self._metrics.total_duration
                else None,
                "retry_count": self._metrics.retry_count,
                "error_count": self._metrics.error_count,
                "last_error": self._metrics.last_error,
            },
            "tags": self._tags,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Create task from dictionary representation."""
        requirements_data = data["requirements"]
        if requirements_data.get("estimated_duration"):
            requirements_data["estimated_duration"] = timedelta(
                seconds=requirements_data["estimated_duration"]
            )

        task = cls(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            task_type=TaskType(data["task_type"]),
            priority=TaskPriority(data["priority"]),
            requirements=TaskRequirements(**requirements_data),
            assigned_agent=data.get("assigned_agent"),
        )

        task._status = TaskStatus(data["status"])
        task._tags = data["tags"]
        task._created_at = datetime.fromisoformat(data["created_at"])
        task._updated_at = datetime.fromisoformat(data["updated_at"])

        # Restore progress
        progress_data = data["progress"]
        task._progress = TaskProgress(
            percentage_complete=progress_data["percentage_complete"],
            current_phase=progress_data["current_phase"],
            milestones=progress_data["milestones"],
            completed_milestones=progress_data["completed_milestones"],
            last_update=datetime.fromisoformat(progress_data["last_update"])
            if progress_data["last_update"]
            else None,
            notes=progress_data["notes"],
        )

        # Restore metrics
        metrics_data = data["metrics"]
        task._metrics = TaskMetrics(
            time_created=datetime.fromisoformat(metrics_data["time_created"]),
            time_started=datetime.fromisoformat(metrics_data["time_started"])
            if metrics_data["time_started"]
            else None,
            time_completed=datetime.fromisoformat(metrics_data["time_completed"])
            if metrics_data["time_completed"]
            else None,
            total_duration=timedelta(seconds=metrics_data["total_duration"])
            if metrics_data["total_duration"]
            else None,
            retry_count=metrics_data["retry_count"],
            error_count=metrics_data["error_count"],
            last_error=metrics_data["last_error"],
        )

        return task

    def __str__(self) -> str:
        """String representation of the task."""
        return f"Task({self._title}, {self._task_type.value}, {self._status.value})"

    def __repr__(self) -> str:
        """Detailed string representation of the task."""
        return (
            f"Task(id='{self._id}', title='{self._title}', "
            f"type={self._task_type.value}, status={self._status.value})"
        )


@dataclass
class TaskConfiguration:
    """Configuration for task management."""

    max_concurrent_tasks: int = 10
    default_timeout: int = 300
    retry_attempts: int = 3
    priority_queue: bool = True
    auto_assignment: bool = True


class TaskManager:
    """Manager for task entities."""

    def __init__(self):
        """Initialize task manager."""
        self._tasks: dict[str, Task] = {}
        self.logger = logging.getLogger(f"{__name__}.TaskManager")

    def create_task(
        self,
        title: str,
        description: str,
        task_type: TaskType,
        priority: TaskPriority = TaskPriority.NORMAL,
    ) -> Task:
        """Create a new task."""
        task_id = f"task_{len(self._tasks) + 1}"
        task = Task(task_id, title, description, task_type, priority)
        self._tasks[task_id] = task
        self.logger.debug(f"Task created: {title}")
        return task

    def get_task(self, task_id: str) -> Task | None:
        """Get a task by ID."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> dict[str, Task]:
        """Get all tasks."""
        return self._tasks.copy()

    def get_tasks_by_status(self, status: TaskStatus) -> list[Task]:
        """Get tasks by status."""
        return [task for task in self._tasks.values() if task.status == status]

    def get_tasks_by_type(self, task_type: TaskType) -> list[Task]:
        """Get tasks by type."""
        return [task for task in self._tasks.values() if task.task_type == task_type]

    def get_tasks_by_priority(self, priority: TaskPriority) -> list[Task]:
        """Get tasks by priority."""
        return [task for task in self._tasks.values() if task.priority == priority]

    def get_pending_tasks(self) -> list[Task]:
        """Get pending tasks."""
        return self.get_tasks_by_status(TaskStatus.PENDING)

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign a task to an agent."""
        task = self.get_task(task_id)
        if task and task.assign_to_agent(agent_id):
            self.logger.info(f"Task {task_id} assigned to {agent_id}")
            return True
        return False

    def complete_task(self, task_id: str, success: bool = True) -> bool:
        """Complete a task."""
        task = self.get_task(task_id)
        if task:
            task.complete(success)
            self.logger.info(f"Task {task_id} completed (success: {success})")
            return True
        return False

    def cancel_task(self, task_id: str, reason: str = "") -> bool:
        """Cancel a task."""
        task = self.get_task(task_id)
        if task:
            task.cancel(reason)
            self.logger.info(f"Task {task_id} cancelled: {reason}")
            return True
        return False

    def cleanup_all(self) -> None:
        """Cleanup all tasks."""
        self._tasks.clear()
        self.logger.info("All tasks cleaned up")

    @property
    def tasks(self) -> dict[str, Task]:
        """Get all tasks."""
        return self._tasks.copy()


# Global task manager
task_manager = TaskManager()
