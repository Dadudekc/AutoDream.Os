"""
Coordination Models - KISS Simplified
=====================================

Simplified data models for swarm coordination.
KISS PRINCIPLE: Keep It Simple, Stupid - removed overengineering.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-6 - Gaming & Entertainment Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class CoordinationStrategy(Enum):
    """Simple coordination strategy types."""

    COLLABORATIVE = "collaborative"
    INDEPENDENT = "independent"
    HIERARCHICAL = "hierarchical"


class TaskPriority(Enum):
    """Simple task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(Enum):
    """Simple task status states."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class CoordinationTask:
    """Simple coordination task model."""

    task_id: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    assigned_agent: Optional[str] = None
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CoordinationResult:
    """Simple coordination result model."""

    result_id: str
    task_id: str
    success: bool
    message: str
    timestamp: datetime = None
    data: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.data is None:
            self.data = {}


@dataclass
class AgentCoordinationStatus:
    """Simple agent coordination status model."""

    agent_id: str
    status: str
    current_tasks: List[str] = None
    last_activity: datetime = None
    capabilities: List[str] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.current_tasks is None:
            self.current_tasks = []
        if self.last_activity is None:
            self.last_activity = datetime.now()
        if self.capabilities is None:
            self.capabilities = []


@dataclass
class CoordinationMetrics:
    """Simple coordination metrics model."""

    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    active_agents: int = 0
    average_completion_time: float = 0.0
    last_updated: datetime = None

    def __post_init__(self):
        """Initialize default values."""
        if self.last_updated is None:
            self.last_updated = datetime.now()

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_tasks == 0:
            return 0.0
        return self.completed_tasks / self.total_tasks


# Factory functions for backward compatibility
def create_coordination_task(
    task_id: str, description: str, priority: TaskPriority = TaskPriority.MEDIUM
) -> CoordinationTask:
    """Create a coordination task."""
    return CoordinationTask(
        task_id=task_id,
        description=description,
        priority=priority,
        status=TaskStatus.PENDING,
    )


def create_coordination_result(
    result_id: str, task_id: str, success: bool, message: str
) -> CoordinationResult:
    """Create a coordination result."""
    return CoordinationResult(
        result_id=result_id, task_id=task_id, success=success, message=message
    )


def create_agent_coordination_status(
    agent_id: str, status: str = "active"
) -> AgentCoordinationStatus:
    """Create an agent coordination status."""
    return AgentCoordinationStatus(agent_id=agent_id, status=status)


def create_coordination_metrics() -> CoordinationMetrics:
    """Create coordination metrics."""
    return CoordinationMetrics()
