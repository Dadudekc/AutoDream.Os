from __future__ import annotations

"""Core dataclasses and enums for the smooth handoff system.

These lightweight models are intentionally decoupled from the main
system logic so that they can be reused independently and keep each
module focused on a single responsibility.
"""

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
    """Supported handoff types."""

    PHASE_TRANSITION = "phase_transition"
    AGENT_HANDOFF = "agent_handoff"
    CONTRACT_HANDOFF = "contract_handoff"
    WORKFLOW_HANDOFF = "workflow_handoff"
    SYSTEM_HANDOFF = "system_handoff"


@dataclass
class HandoffContext:
    """Context information for a handoff operation."""

    handoff_id: str
    source_phase: str
    target_phase: str
    source_agent: str
    target_agent: Optional[str] = None
    handoff_type: HandoffType = HandoffType.PHASE_TRANSITION
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    priority: str = "medium"


@dataclass
class HandoffProcedure:
    """Definition of a handoff procedure."""

    procedure_id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]
    validation_rules: List[Dict[str, Any]]
    rollback_procedures: List[Dict[str, Any]]
    estimated_duration: float  # seconds
    dependencies: List[str] = field(default_factory=list)
    required_agents: List[str] = field(default_factory=list)


@dataclass
class HandoffExecution:
    """Runtime tracking for an executing handoff."""

    execution_id: str
    handoff_id: str
    procedure_id: str
    status: HandoffStatus = HandoffStatus.PENDING
    current_step: int = 0
    steps_completed: List[int] = field(default_factory=list)
    steps_failed: List[int] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
