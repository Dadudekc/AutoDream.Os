from __future__ import annotations

from enum import Enum


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
