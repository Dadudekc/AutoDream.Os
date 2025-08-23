#!/usr/bin/env python3
"""
Decision Types - Agent Cellphone V2
===================================

Enums and data classes for autonomous decision making.
Follows V2 standards: ≤100 LOC, single responsibility, clean data structures.

Author: Agent-1 (Foundation & Testing Specialist)
License: MIT
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Any
from datetime import datetime


class DecisionType(Enum):
    """Types of decisions the autonomous engine can make"""
    TASK_ASSIGNMENT = "task_assignment"
    RESOURCE_ALLOCATION = "resource_allocation"
    PRIORITY_DETERMINATION = "priority_determination"
    CONFLICT_RESOLUTION = "conflict_resolution"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    AGENT_COORDINATION = "agent_coordination"
    LEARNING_ADAPTATION = "learning_adaptation"
    STRATEGIC_PLANNING = "strategic_planning"


class DecisionConfidence(Enum):
    """Confidence levels for autonomous decisions"""
    LOW = "low"      # 0-33% confidence (requires human review)
    MEDIUM = "medium"  # 34-66% confidence (can proceed with monitoring)
    HIGH = "high"    # 67-100% confidence (fully autonomous execution)


class LearningMode(Enum):
    """Learning modes for the autonomous system"""
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    REINFORCEMENT = "reinforcement"
    TRANSFER = "transfer"
    ACTIVE = "active"


class IntelligenceLevel(Enum):
    """Intelligence levels for decision making"""
    BASIC = "basic"           # Rule-based decisions
    INTERMEDIATE = "intermediate"  # Pattern recognition
    ADVANCED = "advanced"     # Predictive modeling
    EXPERT = "expert"         # Deep learning
    AUTONOMOUS = "autonomous" # Self-improving


@dataclass
class DecisionContext:
    """Context information for decision making"""
    decision_id: str
    decision_type: str
    timestamp: str
    agent_id: str
    context_data: Dict[str, Any]
    constraints: List[str]
    objectives: List[str]
    risk_factors: List[str]


@dataclass
class DecisionResult:
    """Result of a decision"""
    decision_id: str
    decision_type: str
    selected_option: str
    confidence: str
    reasoning: str
    alternatives: List[str]
    expected_outcome: str
    risk_assessment: str
    timestamp: str


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


def create_decision_context(
    decision_type: str,
    agent_id: str,
    context_data: Dict[str, Any],
    constraints: List[str] = None,
    objectives: List[str] = None,
    risk_factors: List[str] = None
) -> DecisionContext:
    """Create a decision context with default values"""
    return DecisionContext(
        decision_id=f"decision_{int(datetime.now().timestamp())}",
        decision_type=decision_type,
        timestamp=datetime.now().isoformat(),
        agent_id=agent_id,
        context_data=context_data or {},
        constraints=constraints or [],
        objectives=objectives or [],
        risk_factors=risk_factors or []
    )


def create_learning_data(
    input_features: List[float],
    output_target: Any,
    context: str,
    performance_metric: float = 0.0,
    feedback_score: float = 0.0
) -> LearningData:
    """Create learning data with default values"""
    return LearningData(
        input_features=input_features,
        output_target=output_target,
        context=context,
        timestamp=datetime.now().isoformat(),
        performance_metric=performance_metric,
        feedback_score=feedback_score
    )


def create_agent_capability(
    agent_id: str,
    skills: List[str],
    experience_level: float = 0.0,
    learning_rate: float = 0.1,
    specialization: str = "general",
    availability: bool = True
) -> AgentCapability:
    """Create agent capability with default values"""
    return AgentCapability(
        agent_id=agent_id,
        skills=skills,
        experience_level=experience_level,
        performance_history=[],
        learning_rate=learning_rate,
        specialization=specialization,
        availability=availability
    )


if __name__ == "__main__":
    # Smoke test for decision types
    print("🧪 Testing Decision Types Module...")
    
    # Test enum values
    assert DecisionType.TASK_ASSIGNMENT.value == "task_assignment"
    assert DecisionConfidence.HIGH.value == "high"
    assert LearningMode.REINFORCEMENT.value == "reinforcement"
    assert IntelligenceLevel.ADVANCED.value == "advanced"
    
    # Test data class creation
    context = create_decision_context(
        "test_type", "test_agent", {"test": "data"}
    )
    assert context.decision_type == "test_type"
    assert context.agent_id == "test_agent"
    
    # Test learning data creation
    learning_data = create_learning_data([0.1, 0.2], "success", "test")
    assert len(learning_data.input_features) == 2
    assert learning_data.output_target == "success"
    
    # Test agent capability creation
    capability = create_agent_capability("test_agent", ["python", "ai"])
    assert capability.agent_id == "test_agent"
    assert "python" in capability.skills
    
    print("✅ Decision Types Module smoke test PASSED!")
