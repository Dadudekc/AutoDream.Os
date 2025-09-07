from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .enums import TaskPriority, TaskStatus, TaskType, TaskCategory


@dataclass
class TaskDependency:
    """Task dependency information."""

    task_id: str
    dependency_type: str  # "required", "optional", "parallel"
    condition: str = "completed"  # "completed", "successful", "any"
    timeout: Optional[int] = None  # seconds to wait for dependency


@dataclass
class TaskResource:
    """Resource requirements for a task."""

    cpu_cores: int = 1
    memory_mb: int = 512
    storage_mb: int = 100
    network_bandwidth: Optional[int] = None  # MB/s
    gpu_required: bool = False
    special_hardware: List[str] = field(default_factory=list)


@dataclass
class TaskConstraint:
    """Constraints that must be satisfied for task execution."""

    deadline: Optional[datetime] = None
    max_execution_time: Optional[int] = None  # seconds
    retry_limit: int = 3
    priority_boost: bool = False
    exclusive_execution: bool = False


@dataclass
class TaskMetadata:
    """Additional metadata for task tracking and analysis."""

    tags: List[str] = field(default_factory=list)
    source: str = "unknown"
    estimated_complexity: str = "medium"
    business_value: str = "normal"
    risk_level: str = "low"


@dataclass
class Task:
    """Core task definition with all necessary attributes."""

    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    content: str = ""
    task_type: TaskType = TaskType.COMPUTATION
    category: TaskCategory = TaskCategory.USER
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING

    # Assignment and ownership
    assigned_agent: Optional[str] = None
    created_by: str = "system"
    assigned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Timing and execution
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    execution_time: Optional[float] = None  # seconds
    retry_count: int = 0

    # Dependencies and relationships
    dependencies: List[TaskDependency] = field(default_factory=list)
    dependent_tasks: List[str] = field(default_factory=list)

    # Resources and constraints
    resources: TaskResource = field(default_factory=TaskResource)
    constraints: TaskConstraint = field(default_factory=TaskConstraint)
    metadata: TaskMetadata = field(default_factory=TaskMetadata)

    # Results and error handling
    result: Optional[Any] = None
    error_message: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None

    def is_ready_to_execute(self) -> bool:
        """Check if task is ready to execute."""
        if self.status != TaskStatus.PENDING:
            return False

        # Check dependencies
        for dep in self.dependencies:
            if dep.condition == "completed" and dep.task_id not in self.completed_tasks:
                return False

        return True

    def is_expired(self) -> bool:
        """Check if task has expired."""
        if not self.constraints.deadline:
            return False
        return datetime.now() > self.constraints.deadline

    def complete_execution(self, result: Any = None):
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now()
        if self.started_at:
            self.execution_time = (self.completed_at - self.started_at).total_seconds()
