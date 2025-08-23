#!/usr/bin/env python3
"""
Decision Types - Agent Cellphone V2
===================================

Defines decision-related enums and dataclasses.
Follows V2 standards: ≤50 LOC, SRP, OOP principles.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


class DecisionType(Enum):
    """Types of decisions the system can make"""

    TASK_ASSIGNMENT = "task_assignment"
    RESOURCE_ALLOCATION = "resource_allocation"
    PRIORITY_DETERMINATION = "priority_determination"
    CONFLICT_RESOLUTION = "conflict_resolution"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    AGENT_COORDINATION = "agent_coordination"


class DecisionStatus(Enum):
    """Decision processing status"""

    PENDING = "pending"
    ANALYZING = "analyzing"
    COLLABORATING = "collaborating"
    DECIDED = "decided"
    IMPLEMENTED = "implemented"
    FAILED = "failed"


class DecisionPriority(Enum):
    """Decision priority levels"""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5


@dataclass
class DecisionRequest:
    """Decision request data structure"""

    decision_id: str
    decision_type: DecisionType
    requester: str
    timestamp: float
    parameters: Dict[str, Any]
    priority: DecisionPriority
    deadline: Optional[float]
    collaborators: List[str]


@dataclass
class DecisionResult:
    """Decision result data structure"""

    decision_id: str
    decision_type: DecisionType
    timestamp: float
    decision: Any
    confidence: float
    reasoning: str
    collaborators: List[str]
    implementation_plan: List[str]


@dataclass
class DecisionContext:
    """Context information for decision making"""

    available_resources: Dict[str, Any]
    agent_capabilities: Dict[str, List[str]]
    current_workload: Dict[str, float]
    system_constraints: Dict[str, Any]
    historical_data: Dict[str, Any]
