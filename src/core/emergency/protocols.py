"""Protocol definitions for emergency response system."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ProtocolStatus(Enum):
    """Protocol activation status."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    ESCALATED = "escalated"
    COMPLETED = "completed"
    FAILED = "failed"


class ProtocolPriority(Enum):
    """Protocol priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ResponseAction:
    """Emergency response action definition."""
    action: str
    description: str
    priority: ProtocolPriority
    timeout: int  # seconds
    required: bool = True
    completed: bool = False
    completion_time: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None


@dataclass
class EscalationProcedure:
    """Protocol escalation procedure."""
    level: ProtocolPriority
    action: str
    timeout: int  # seconds
    description: str
    triggered: bool = False
    trigger_time: Optional[datetime] = None


@dataclass
class RecoveryProcedure:
    """Protocol recovery procedure."""
    action: str
    description: str
    validation_criteria: List[str]
    required: bool = True
    completed: bool = False
    completion_time: Optional[datetime] = None
    validation_results: Optional[Dict[str, bool]] = None


@dataclass
class EmergencyProtocol:
    """Emergency response protocol definition."""
    name: str
    description: str
    activation_conditions: List[str]
    response_actions: List[ResponseAction]
    escalation_procedures: List[EscalationProcedure]
    recovery_procedures: List[RecoveryProcedure]
    validation_criteria: List[str]
    documentation_requirements: List[str]
    status: ProtocolStatus = ProtocolStatus.INACTIVE
    activated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    activation_source: Optional[str] = None


@dataclass
class ProtocolExecution:
    """Protocol execution tracking."""
    protocol_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: ProtocolStatus = ProtocolStatus.ACTIVE
    actions_completed: int = 0
    total_actions: int = 0
    escalation_level: ProtocolPriority = ProtocolPriority.LOW
    errors: List[str] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)


__all__ = [
    "ProtocolStatus",
    "ProtocolPriority",
    "ResponseAction",
    "EscalationProcedure",
    "RecoveryProcedure",
    "EmergencyProtocol",
    "ProtocolExecution",
]
