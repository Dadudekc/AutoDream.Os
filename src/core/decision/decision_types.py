#!/usr/bin/env python3
"""
Decision Types - Agent Cellphone V2
===================================

CONSOLIDATED decision-related enums and dataclasses.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

**SSOT IMPLEMENTATION**: All decision-related classes are consolidated here
to eliminate duplication and provide a single source of truth.

CONSOLIDATION STATUS:
- ✅ Core decision types maintained
- ❌ REMOVED: LearningMode (unified with src/core/learning/)
- ❌ REMOVED: DataIntegrityLevel (not decision-specific)
- ✅ Clean decision type definitions
- ✅ SSOT: Unified DecisionMetrics class
"""

from enum import Enum
from dataclasses import dataclass, field
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
    """
    SSOT: Unified Decision Performance Metrics
    
    This class consolidates all decision metrics functionality into a single
    source of truth, eliminating duplication across the codebase.
    """
    metrics_id: str
    decision_type: DecisionType
    total_decisions: int = 0
    successful_decisions: int = 0
    failed_decisions: int = 0
    average_confidence: float = 0.0
    average_execution_time: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
    
    # Performance tracking
    total_execution_time: float = 0.0
    confidence_history: List[float] = field(default_factory=list)
    execution_time_history: List[float] = field(default_factory=list)
    
    # Alert thresholds
    success_rate_threshold: float = 0.8
    execution_time_threshold: float = 5.0
    confidence_threshold: float = 0.7
    
    def update_metrics(self, success: bool, execution_time: float, confidence: float):
        """Update metrics with new decision result"""
        self.total_decisions += 1
        if success:
            self.successful_decisions += 1
        else:
            self.failed_decisions += 1
            
        self.total_execution_time += execution_time
        self.execution_time_history.append(execution_time)
        self.confidence_history.append(confidence)
        
        # Update averages
        self.average_execution_time = self.total_execution_time / self.total_decisions
        self.average_confidence = sum(self.confidence_history) / len(self.confidence_history)
        
        # Keep history manageable
        if len(self.execution_time_history) > 1000:
            self.execution_time_history = self.execution_time_history[-1000:]
        if len(self.confidence_history) > 1000:
            self.confidence_history = self.confidence_history[-1000:]
            
        self.last_updated = datetime.now()
    
    def get_success_rate(self) -> float:
        """Get current success rate"""
        if self.total_decisions == 0:
            return 0.0
        return self.successful_decisions / self.total_decisions
    
    def get_performance_score(self) -> float:
        """Calculate overall performance score"""
        success_rate = self.get_success_rate()
        time_score = max(0.0, 1.0 - (self.average_execution_time / 10.0))
        confidence_score = self.average_confidence
        
        # Weighted combination
        return (success_rate * 0.4) + (time_score * 0.3) + (confidence_score * 0.3)
    
    def check_alerts(self) -> List[str]:
        """Check for performance alerts"""
        alerts = []
        
        if self.get_success_rate() < self.success_rate_threshold:
            alerts.append(f"Success rate {self.get_success_rate():.2%} below threshold {self.success_rate_threshold:.2%}")
            
        if self.average_execution_time > self.execution_time_threshold:
            alerts.append(f"Average execution time {self.average_execution_time:.2f}s above threshold {self.execution_time_threshold:.2f}s")
            
        if self.average_confidence < self.confidence_threshold:
            alerts.append(f"Average confidence {self.average_confidence:.2f} below threshold {self.confidence_threshold:.2f}")
            
        return alerts
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        return {
            "metrics_id": self.metrics_id,
            "decision_type": self.decision_type.value,
            "total_decisions": self.total_decisions,
            "successful_decisions": self.successful_decisions,
            "failed_decisions": self.failed_decisions,
            "success_rate": self.get_success_rate(),
            "average_execution_time": self.average_execution_time,
            "average_confidence": self.average_confidence,
            "performance_score": self.get_performance_score(),
            "alerts": self.check_alerts(),
            "last_updated": self.last_updated.isoformat()
        }


@dataclass
class DecisionCollaboration:
    """Decision collaboration data"""
    collaboration_id: str
    participants: List[str]
    decision_type: DecisionType
    collaboration_mode: str
    start_time: datetime
    end_time: Optional[datetime]
