"""Core FSM state definitions and enums."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Any, Dict, List, Optional


class StateStatus(Enum):
    """State execution status."""

    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class TransitionType(Enum):
    """Types of state transitions."""

    AUTOMATIC = "automatic"
    MANUAL = "manual"
    CONDITIONAL = "conditional"
    TIMEOUT = "timeout"
    ERROR = "error"


class WorkflowPriority(Enum):
    """Workflow priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class StateDefinition:
    """State definition structure."""

    name: str
    description: str
    entry_actions: List[str]
    exit_actions: List[str]
    timeout_seconds: Optional[float]
    retry_count: int
    retry_delay: float
    required_resources: List[str]
    dependencies: List[str]
    metadata: Dict[str, Any]


@dataclass
class TransitionDefinition:
    """Transition definition structure."""

    from_state: str
    to_state: str
    transition_type: TransitionType
    condition: Optional[str]
    priority: int
    timeout_seconds: Optional[float]
    actions: List[str]
    metadata: Dict[str, Any]


@dataclass
class WorkflowInstance:
    """Workflow instance tracking."""

    workflow_id: str
    workflow_name: str
    current_state: str
    created_at: datetime
    last_transition: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: StateStatus = StateStatus.PENDING
    metadata: Dict[str, Any] = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


@dataclass
class StateExecutionResult:
    """Result of state execution."""

    state_name: str
    success: bool
    execution_time: float
    error_message: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


@dataclass
class TransitionResult:
    """Result of state transition."""

    from_state: str
    to_state: str
    success: bool
    transition_time: float
    error_message: Optional[str] = None
    executed_actions: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self) -> None:
        if self.executed_actions is None:
            self.executed_actions = []
        if self.metadata is None:
            self.metadata = {}


__all__ = [
    "StateStatus",
    "TransitionType",
    "WorkflowPriority",
    "StateDefinition",
    "TransitionDefinition",
    "WorkflowInstance",
    "StateExecutionResult",
    "TransitionResult",
]
