#!/usr/bin/env python3
"""
Decision Types - Agent Cellphone V2
===================================

CONSOLIDATED decision-related enums and dataclasses.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

CONSOLIDATION STATUS:
- ✅ Core decision types maintained
- ❌ REMOVED: LearningMode (unified with src/core/learning/)
- ❌ REMOVED: DataIntegrityLevel (not decision-specific)
- ✅ Clean decision type definitions
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


class DecisionType(Enum):
    """Types of decisions the system can make"""

    TASK_ASSIGNMENT = "task_assignment"
    RESOURCE_ALLOCATION = "resource_allocation"
    PRIORITY_DETERMINATION = "priority_determination"
    CONFLICT_RESOLUTION = "conflict_resolution"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    AGENT_COORDINATION = "agent_coordination"
    STRATEGIC_PLANNING = "strategic_planning"


class DecisionConfidence(Enum):
    """Confidence levels for autonomous decisions"""
    LOW = "low"      # 0-33% confidence (requires human review)
    MEDIUM = "medium"  # 34-66% confidence (can proceed with monitoring)
    HIGH = "high"    # 67-100% confidence (fully autonomous execution)


class IntelligenceLevel(Enum):
    """Intelligence levels for decision making"""
    BASIC = "basic"           # Rule-based decisions
    INTERMEDIATE = "intermediate"  # Pattern recognition
    ADVANCED = "advanced"     # Predictive modeling
    EXPERT = "expert"         # Deep learning
    AUTONOMOUS = "autonomous" # Self-improving


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


@dataclass
class LearningData:
    """Data for learning and adaptation"""
    input_features: List[float]
    output_target: Any
    context: str
    timestamp: str
    performance_metric: float
    feedback_score: float


@dataclass
class AgentCapability:
    """Agent capability information"""
    agent_id: str
    skills: List[str]
    experience_level: float
    performance_history: List[float]
    learning_rate: float
    specialization: str
    availability: bool


@dataclass
class DecisionAlgorithm:
    """Decision algorithm definition"""
    algorithm_id: str
    name: str
    description: str
    decision_types: List[DecisionType]
    confidence_threshold: float
    execution_timeout: float
    version: str
    is_active: bool


@dataclass
class DecisionRule:
    """Decision rule definition"""
    rule_id: str
    name: str
    description: str
    condition: str
    action: str
    priority: DecisionPriority
    is_active: bool


@dataclass
class DecisionWorkflow:
    """Decision workflow definition"""
    workflow_id: str
    name: str
    description: str
    steps: List[str]
    decision_types: List[DecisionType]
    is_active: bool


@dataclass
class DecisionMetrics:
    """Decision performance metrics"""
    total_decisions: int
    successful_decisions: int
    failed_decisions: int
    average_confidence: float
    average_execution_time: float
    last_updated: datetime


@dataclass
class DecisionCollaboration:
    """Decision collaboration data"""
    collaboration_id: str
    participants: List[str]
    decision_type: DecisionType
    collaboration_mode: str
    start_time: datetime
    end_time: Optional[datetime]
