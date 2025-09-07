#!/usr/bin/env python3
"""
Unified Decision Models - Agent Cellphone V2
===========================================

CONSOLIDATED decision models eliminating duplication across multiple implementations.
Follows V2 standards: 400 LOC, OOP design, SRP.

**Author:** V2 Consolidation Specialist
**Created:** Current Sprint
**Status:** ACTIVE - CONSOLIDATION IN PROGRESS
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Set, Callable
from datetime import datetime
import uuid


class DecisionType(Enum):
    """Unified decision types consolidating all implementations"""
    TASK_ASSIGNMENT = "task_assignment"
    RESOURCE_ALLOCATION = "resource_allocation"
    PRIORITY_DETERMINATION = "priority_determination"
    CONFLICT_RESOLUTION = "conflict_resolution"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    AGENT_COORDINATION = "agent_coordination"
    LEARNING_STRATEGY = "learning_strategy"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    RISK_ASSESSMENT = "risk_assessment"
    QUALITY_ASSURANCE = "quality_assurance"


class DecisionPriority(Enum):
    """Unified decision priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


class DecisionStatus(Enum):
    """Unified decision status states"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"
    REQUIRES_APPROVAL = "requires_approval"


class DecisionConfidence(Enum):
    """Unified decision confidence levels"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    CERTAIN = "certain"


@dataclass
class DecisionRequest:
    """Unified decision request structure"""
    decision_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    decision_type: DecisionType = DecisionType.TASK_ASSIGNMENT
    requester: str = ""
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    parameters: Dict[str, Any] = field(default_factory=dict)
    priority: DecisionPriority = DecisionPriority.MEDIUM
    deadline: Optional[float] = None
    collaborators: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.decision_id:
            self.decision_id = str(uuid.uuid4())


@dataclass
class DecisionResult:
    """Unified decision result structure"""
    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    decision_id: str = ""
    outcome: str = ""
    confidence: DecisionConfidence = DecisionConfidence.MEDIUM
    reasoning: str = ""
    alternatives_considered: List[str] = field(default_factory=list)
    impact_assessment: Dict[str, Any] = field(default_factory=dict)
    execution_plan: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def __post_init__(self):
        if not self.result_id:
            self.result_id = str(uuid.uuid4())


@dataclass
class DecisionContext:
    """Unified decision context structure"""
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    environment_state: Dict[str, Any] = field(default_factory=dict)
    available_resources: Dict[str, Any] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    historical_data: Dict[str, Any] = field(default_factory=dict)
    risk_factors: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def __post_init__(self):
        if not self.context_id:
            self.context_id = str(uuid.uuid4())


@dataclass
class DecisionAlgorithm:
    """Unified decision algorithm definition"""
    algorithm_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    decision_types: List[DecisionType] = field(default_factory=list)
    implementation: Optional[Callable] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.algorithm_id:
            self.algorithm_id = str(uuid.uuid4())


@dataclass
class DecisionRule:
    """Unified decision rule definition"""
    rule_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    condition: str = ""
    action: str = ""
    priority: int = 1
    decision_types: List[DecisionType] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.rule_id:
            self.rule_id = str(uuid.uuid4())

@dataclass
class DecisionWorkflow:
    """Unified decision workflow definition"""
    workflow_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    decision_points: List[str] = field(default_factory=list)
    required_approvals: List[str] = field(default_factory=list)
    timeout_seconds: int = 3600  # 1 hour default
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.workflow_id:
            self.workflow_id = str(uuid.uuid4())
    
    def add_step(self, step_name: str, step_type: str, parameters: Dict[str, Any]):
        """Add a step to the workflow"""
        step = {
            "step_id": str(uuid.uuid4()),
            "name": step_name,
            "type": step_type,
            "parameters": parameters,
            "order": len(self.steps)
        }
        self.steps.append(step)
    
    def add_decision_point(self, decision_id: str, conditions: Dict[str, Any]):
        """Add a decision point to the workflow"""
        decision_point = {
            "decision_id": decision_id,
            "conditions": conditions,
            "order": len(self.decision_points)
        }
        self.decision_points.append(decision_point)


@dataclass
class DecisionCollaboration:
    """Unified decision collaboration tracking"""
    collaboration_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    decision_id: str = ""
    participants: List[str] = field(default_factory=list)
    contributions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    consensus_level: float = 0.0
    conflicts: List[str] = field(default_factory=list)
    resolution_strategy: str = ""
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def __post_init__(self):
        if not self.collaboration_id:
            self.collaboration_id = str(uuid.uuid4())
    
    def add_participant(self, agent_id: str, role: str):
        """Add a participant to the collaboration"""
        if agent_id not in self.participants:
            self.participants.append(agent_id)
            self.contributions[agent_id] = {
                "role": role,
                "contributions": [],
                "confidence": 0.0
            }
    
    def record_contribution(self, agent_id: str, contribution_type: str, content: Any, confidence: float):
        """Record a contribution from a participant"""
        if agent_id in self.contributions:
            contribution = {
                "type": contribution_type,
                "content": content,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat()
            }
            self.contributions[agent_id]["contributions"].append(contribution)
            self.contributions[agent_id]["confidence"] = confidence


# Utility functions for decision models
def create_decision_request(
    decision_type: DecisionType,
    requester: str,
    parameters: Dict[str, Any],
    priority: DecisionPriority = DecisionPriority.MEDIUM,
    deadline: Optional[float] = None,
    collaborators: Optional[List[str]] = None
) -> DecisionRequest:
    """Create a new decision request with validation"""
    return DecisionRequest(
        decision_type=decision_type,
        requester=requester,
        parameters=parameters,
        priority=priority,
        deadline=deadline,
        collaborators=collaborators or []
    )


def create_decision_result(
    decision_id: str,
    outcome: str,
    confidence: DecisionConfidence,
    reasoning: str
) -> DecisionResult:
    """Create a new decision result"""
    return DecisionResult(
        decision_id=decision_id,
        outcome=outcome,
        confidence=confidence,
        reasoning=reasoning
    )


def validate_decision_request(request: DecisionRequest) -> bool:
    """Validate decision request structure"""
    if not request.requester:
        return False
    if not request.parameters:
        return False
    if request.priority.value < 1 or request.priority.value > 5:
        return False
    return True


def calculate_decision_confidence(
    historical_success_rate: float,
    data_quality: float,
    algorithm_performance: float
) -> DecisionConfidence:
    """Calculate decision confidence based on multiple factors"""
    # Weighted average of factors
    confidence_score = (
        historical_success_rate * 0.4 +
        data_quality * 0.3 +
        algorithm_performance * 0.3
    )
    
    if confidence_score >= 0.9:
        return DecisionConfidence.CERTAIN
    elif confidence_score >= 0.8:
        return DecisionConfidence.VERY_HIGH
    elif confidence_score >= 0.7:
        return DecisionConfidence.HIGH
    elif confidence_score >= 0.6:
        return DecisionConfidence.MEDIUM
    elif confidence_score >= 0.5:
        return DecisionConfidence.LOW
    else:
        return DecisionConfidence.VERY_LOW


def merge_decision_contexts(contexts: List[DecisionContext]) -> DecisionContext:
    """Merge multiple decision contexts into one"""
    if not contexts:
        raise ValueError("Cannot merge empty context list")
    
    base_context = contexts[0]
    merged_context = DecisionContext(
        context_id=str(uuid.uuid4()),
        agent_id=base_context.agent_id
    )
    
    # Merge environment states
    for context in contexts:
        merged_context.environment_state.update(context.environment_state)
        merged_context.available_resources.update(context.available_resources)
        merged_context.constraints.extend(context.constraints)
        merged_context.historical_data.update(context.historical_data)
        merged_context.risk_factors.extend(context.risk_factors)
    
    # Remove duplicates
    merged_context.constraints = list(set(merged_context.constraints))
    merged_context.risk_factors = list(set(merged_context.risk_factors))
    
    return merged_context


