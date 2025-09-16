#!/usr/bin/env python3
"""Swarm Communication Enums and Models"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class SwarmDecisionType(Enum):
    """Types of decisions that can be made by the swarm"""
    MISSION_ASSIGNMENT = "mission_assignment"
    ARCHITECTURE_CHANGE = "architecture_change"
    QUALITY_STANDARD_UPDATE = "quality_standard_update"
    RESOURCE_ALLOCATION = "resource_allocation"
    PHASE_TRANSITION = "phase_transition"
    EMERGENCY_RESPONSE = "emergency_response"


class QCStandard(Enum):
    """Quality control standards for the swarm"""
    V2_COMPLIANCE = "v2_compliance"
    SOLID_PRINCIPLES = "solid_principles"
    TEST_COVERAGE = "test_coverage"
    PERFORMANCE_METRICS = "performance_metrics"
    SECURITY_AUDIT = "security_audit"
    CODE_REVIEW = "code_review"


class SwarmAgentStatus(Enum):
    """Status of swarm agents"""
    ACTIVE = "active"
    COORDINATING = "coordinating"
    EXECUTING = "executing"
    REVIEWING = "reviewing"
    VOTING = "voting"
    IDLE = "idle"


class DecisionStatus(Enum):
    """Status of swarm decisions"""
    PENDING = "pending"
    VOTING = "voting"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"


@dataclass
class SwarmAgent:
    """Represents a swarm agent"""
    agent_id: str
    specialty: str
    status: SwarmAgentStatus = SwarmAgentStatus.ACTIVE
    last_activity: Optional[datetime] = None
    capabilities: Set[str] = field(default_factory=set)
    current_mission: Optional[str] = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SwarmDecision:
    """Represents a swarm decision"""
    decision_id: str
    decision_type: SwarmDecisionType
    description: str
    proposer: str
    status: DecisionStatus = DecisionStatus.PENDING
    votes: Dict[str, bool] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    implementation_notes: Optional[str] = None


@dataclass
class QCStandardResult:
    """Result of a quality control standard check"""
    standard: QCStandard
    passed: bool
    score: float
    details: Dict[str, Any]
    checked_at: datetime = field(default_factory=datetime.now)
    checked_by: Optional[str] = None


@dataclass
class SwarmCommunicationMetrics:
    """Metrics for swarm communication"""
    active_agents: int = 0
    total_decisions: int = 0
    pending_decisions: int = 0
    approved_decisions: int = 0
    rejected_decisions: int = 0
    average_voting_time_hours: float = 0.0
    qc_checks_performed: int = 0
    qc_pass_rate: float = 0.0
    communication_uptime_hours: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)



