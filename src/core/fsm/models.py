#!/usr/bin/env python3
"""
FSM Models - V2 Modular Architecture
====================================

Data models and structures for the FSM system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4I - FSM System Modularization
License: MIT
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime


# ============================================================================
# CORE FSM ENUMS
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


class TaskState(Enum):
    """Task state enumeration."""
    NEW = "new"
    ONBOARDING = "onboarding"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class BridgeState(Enum):
    """Bridge state enumeration."""
    IDLE = "idle"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


# ============================================================================
# CORE FSM DATA MODELS
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
# TASK MANAGEMENT DATA MODELS
# ============================================================================

@dataclass
class FSMTask:
    """FSM task data structure."""
    id: str
    title: str
    description: str
    state: TaskState
    priority: TaskPriority
    assigned_agent: str
    created_at: str
    updated_at: str
    evidence: List[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []
        if self.metadata is None:
            self.metadata = {}

    def add_evidence(self, agent_id: str, evidence: Dict[str, Any]):
        """Add evidence to the task."""
        self.evidence.append({
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "evidence": evidence,
        })
        self.updated_at = datetime.now().isoformat()

    def update_state(self, new_state: TaskState):
        """Update task state."""
        self.state = new_state
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "state": self.state.value,
            "priority": self.priority.value,
            "assigned_agent": self.assigned_agent,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "evidence": self.evidence,
            "metadata": self.metadata
        }
        return task_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FSMTask":
        """Create task from dictionary."""
        data["state"] = TaskState(data["state"])
        data["priority"] = TaskPriority(data["priority"])
        return cls(**data)


@dataclass
class FSMUpdate:
    """FSM update message structure."""
    update_id: str
    task_id: str
    agent_id: str
    state: TaskState
    summary: str
    timestamp: str
    evidence: Optional[Dict[str, Any]] = None


@dataclass
class FSMCommunicationEvent:
    """FSM communication event structure."""
    event_id: str
    event_type: str
    source_agent: str
    target_agent: str
    message: str
    timestamp: str
    metadata: Dict[str, Any] = None


# ============================================================================
# ABSTRACT BASE CLASSES
# ============================================================================

class StateHandler:
    """Abstract base class for state handlers."""
    
    def execute(self, context: Dict[str, Any]) -> StateExecutionResult:
        """Execute the state logic."""
        raise NotImplementedError
    
    def can_transition(self, context: Dict[str, Any]) -> bool:
        """Check if transition to this state is allowed."""
        raise NotImplementedError


class TransitionHandler:
    """Abstract base class for transition handlers."""
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate transition condition."""
        raise NotImplementedError
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute transition actions."""
        raise NotImplementedError

