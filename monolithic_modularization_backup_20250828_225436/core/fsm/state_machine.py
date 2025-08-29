#!/usr/bin/env python3
"""State machine definitions for the FSM system."""

from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional


# ============================================================================
# ENUMS
# ============================================================================


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


# ============================================================================
# DATA MODELS
# ============================================================================


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
    state_history: List[Dict[str, Any]]
    start_time: datetime
    last_update: datetime
    status: StateStatus
    priority: WorkflowPriority
    metadata: Dict[str, Any]
    error_count: int
    retry_count: int


@dataclass
class StateExecutionResult:
    """Result of state execution."""

    state_name: str
    execution_time: float
    status: StateStatus
    output: Dict[str, Any]
    error_message: Optional[str]
    metadata: Dict[str, Any]
    timestamp: datetime


# ============================================================================
# BASE HANDLERS
# ============================================================================


class StateHandler(ABC):
    """Abstract base class for state handlers."""

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> StateExecutionResult:
        """Execute the state logic."""

    @abstractmethod
    def can_transition(self, context: Dict[str, Any]) -> bool:
        """Check if transition to this state is allowed."""


class TransitionHandler(ABC):
    """Abstract base class for transition handlers."""

    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate transition condition."""

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute transition actions."""


__all__ = [
    "StateStatus",
    "TransitionType",
    "WorkflowPriority",
    "StateDefinition",
    "TransitionDefinition",
    "WorkflowInstance",
    "StateExecutionResult",
    "StateHandler",
    "TransitionHandler",
]
