"""Data models and enums for handoff operations."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time


class HandoffStatus(Enum):
    """Possible states for a handoff execution."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLBACK = "rollback"


class HandoffType(Enum):
    """Kinds of handoff that the system can process."""

    PHASE_TRANSITION = "phase_transition"
    AGENT_HANDOFF = "agent_handoff"


@dataclass
class HandoffContext:
    """Context information for initiating a handoff."""

    handoff_id: str
    source_phase: str
    target_phase: str
    source_agent: str
    target_agent: Optional[str] = None
    handoff_type: HandoffType = HandoffType.PHASE_TRANSITION
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class HandoffProcedure:
    """Definition of a handoff procedure."""

    procedure_id: str
    name: str
    steps: List[Dict[str, Any]]
    validation_rules: List[Dict[str, Any]]
    rollback_procedures: List[Dict[str, Any]]
    description: str = ""
    estimated_duration: float = 0.0


@dataclass
class HandoffExecution:
    """Runtime tracking information for a handoff."""

    execution_id: str
    handoff_id: str
    procedure_id: str
    status: HandoffStatus
    current_step: int
    steps_completed: List[int] = field(default_factory=list)
    steps_failed: List[int] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    error_details: Optional[str] = None
