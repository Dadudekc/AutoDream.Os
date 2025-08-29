#!/usr/bin/env python3
"""
FSM utility types and data structures.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


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

    def __post_init__(self) -> None:
        if self.evidence is None:
            self.evidence = []
        if self.metadata is None:
            self.metadata = {}

    def add_evidence(self, agent_id: str, evidence: Dict[str, Any]) -> None:
        """Add evidence to the task."""
        self.evidence.append(
            {
                "timestamp": datetime.now().isoformat(),
                "agent_id": agent_id,
                "evidence": evidence,
            }
        )
        self.updated_at = datetime.now().isoformat()

    def update_state(self, new_state: TaskState) -> None:
        """Update task state."""
        self.state = new_state
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        task_dict = asdict(self)
        task_dict["state"] = self.state.value
        task_dict["priority"] = self.priority.value
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
