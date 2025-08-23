#!/usr/bin/env python3
"""
Task Types and Enums - Advanced Task Management System
=====================================================

Defines the core task structures and enums used throughout the
advanced task management system for type safety and consistency.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, Generic, TypeVar, List, Set
from enum import Enum

T = TypeVar("T")


class TaskPriority(Enum):
    """Task priority levels for scheduling and execution."""

    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """Status of a task in the system."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    BLOCKED = "blocked"


class TaskType(Enum):
    """Types of tasks supported by the system."""

    COMPUTATION = "computation"
    DATA_PROCESSING = "data_processing"
    COMMUNICATION = "communication"
    COORDINATION = "coordination"
    MONITORING = "monitoring"
    ANALYSIS = "analysis"
    OPTIMIZATION = "optimization"
    VALIDATION = "validation"
    SYNCHRONIZATION = "synchronization"
    MAINTENANCE = "maintenance"


class TaskCategory(Enum):
    """Categories for organizing and filtering tasks."""

    SYSTEM = "system"
    USER = "user"
    AUTOMATED = "automated"
    SCHEDULED = "scheduled"
    EMERGENCY = "emergency"
    MAINTENANCE = "maintenance"
    DEVELOPMENT = "development"
    TESTING = "testing"


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
    start_time: Optional[datetime] = None
    max_duration: Optional[int] = None  # seconds
    required_agents: List[str] = field(default_factory=list)
    excluded_agents: List[str] = field(default_factory=list)
    location_constraints: List[str] = field(default_factory=list)
    security_level: Optional[str] = None


@dataclass
class TaskMetadata:
    """Additional task metadata and configuration."""

    version: str = "1.0.0"
    created_by: str = ""
    tags: List[str] = field(default_factory=list)
    description: str = ""
    documentation_url: Optional[str] = None
    estimated_complexity: Optional[int] = None  # 1-10 scale
    risk_level: Optional[str] = None  # "low", "medium", "high"
    compliance_requirements: List[str] = field(default_factory=list)


@dataclass
class Task(Generic[T]):
    """
    Core task structure for the advanced task management system.

    Attributes:
        task_id: Unique identifier for the task
        name: Human-readable task name
        type: Type of task (computation, data_processing, etc.)
        category: Task category for organization
        content: The actual task content (generic type)
        priority: Priority level for scheduling
        status: Current status of the task
        created_at: When the task was created
        started_at: When the task execution began
        completed_at: When the task was completed
        assigned_agent: ID of the agent assigned to the task
        dependencies: List of task dependencies
        resources: Resource requirements for the task
        constraints: Execution constraints
        metadata: Additional task metadata
        progress: Current progress (0-100)
        result: Task execution result
        error_message: Error message if task failed
        retry_count: Number of execution attempts
        max_retries: Maximum retry attempts
        timeout: Task timeout in seconds
        parent_task_id: ID of parent task if this is a subtask
        subtasks: List of subtask IDs
    """

    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    type: TaskType = TaskType.COMPUTATION
    category: TaskCategory = TaskCategory.USER
    content: T = None
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    assigned_agent: Optional[str] = None
    dependencies: List[TaskDependency] = field(default_factory=list)
    resources: TaskResource = field(default_factory=TaskResource)
    constraints: TaskConstraint = field(default_factory=TaskConstraint)
    metadata: TaskMetadata = field(default_factory=TaskMetadata)
    progress: float = 0.0
    result: Optional[Any] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout: Optional[int] = None
    parent_task_id: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Post-initialization validation and setup."""
        if not self.task_id:
            self.task_id = str(uuid.uuid4())

        if not self.created_at:
            self.created_at = datetime.now()

        # Ensure progress is within bounds
        self.progress = max(0.0, min(100.0, self.progress))

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create task from dictionary representation."""
        # Handle datetime fields
        for field_name in ["created_at", "started_at", "completed_at"]:
            if field_name in data and data[field_name]:
                if isinstance(data[field_name], str):
                    data[field_name] = datetime.fromisoformat(data[field_name])

        # Handle enum fields
        for field_name in ["type", "category", "priority", "status"]:
            if field_name in data and isinstance(data[field_name], str):
                enum_class = globals()[f"Task{field_name.title()}"]
                data[field_name] = enum_class(data[field_name])

        return cls(**data)

    def is_ready_to_execute(self) -> bool:
        """Check if task is ready to execute (dependencies satisfied)."""
        if self.status != TaskStatus.PENDING:
            return False

        # Check dependencies
        for dependency in self.dependencies:
            if not self._is_dependency_satisfied(dependency):
                return False

        # Check constraints
        if not self._are_constraints_satisfied():
            return False

        return True

    def _is_dependency_satisfied(self, dependency: TaskDependency) -> bool:
        """Check if a specific dependency is satisfied."""
        # This would typically check with the task manager
        # For now, return True as a placeholder
        return True

    def _are_constraints_satisfied(self) -> bool:
        """Check if all execution constraints are satisfied."""
        # Check deadline
        if self.constraints.deadline and datetime.now() > self.constraints.deadline:
            return False

        # Check start time
        if self.constraints.start_time and datetime.now() < self.constraints.start_time:
            return False

        return True

    def can_retry(self) -> bool:
        """Check if task can be retried."""
        return self.status == TaskStatus.FAILED and self.retry_count < self.max_retries

    def is_expired(self) -> bool:
        """Check if task has expired (timeout exceeded)."""
        if not self.timeout or not self.started_at:
            return False

        elapsed = (datetime.now() - self.started_at).total_seconds()
        return elapsed > self.timeout

    def update_progress(self, progress: float):
        """Update task progress."""
        self.progress = max(0.0, min(100.0, progress))

    def start_execution(self, agent_id: str):
        """Mark task as started."""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now()
        self.assigned_agent = agent_id

    def complete_execution(self, result: Any = None):
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.progress = 100.0
        self.result = result

    def fail_execution(self, error_message: str):
        """Mark task as failed."""
        self.status = TaskStatus.FAILED
        self.error_message = error_message
        self.retry_count += 1

    def cancel_execution(self):
        """Cancel task execution."""
        self.status = TaskStatus.CANCELLED
        if not self.completed_at:
            self.completed_at = datetime.now()

    def get_execution_time(self) -> Optional[float]:
        """Get task execution time in seconds."""
        if not self.started_at:
            return None

        end_time = self.completed_at or datetime.now()
        return (end_time - self.started_at).total_seconds()

    def get_remaining_time(self) -> Optional[float]:
        """Get remaining time before deadline in seconds."""
        if not self.constraints.deadline:
            return None

        remaining = (self.constraints.deadline - datetime.now()).total_seconds()
        return max(0.0, remaining)

    def __str__(self) -> str:
        """String representation of the task."""
        return f"Task({self.task_id}: {self.name} [{self.status.value}])"

    def __repr__(self) -> str:
        """Detailed string representation of the task."""
        return (
            f"Task(task_id='{self.task_id}', name='{self.name}', "
            f"type={self.type.value}, status={self.status.value}, "
            f"priority={self.priority.value}, progress={self.progress}%)"
        )

    def __lt__(self, other):
        """Enable comparison for priority queue ordering."""
        if not isinstance(other, Task):
            return False
        return self.priority.value < other.priority.value

    def __eq__(self, other):
        """Enable equality comparison."""
        if not isinstance(other, Task):
            return False
        return self.task_id == other.task_id
