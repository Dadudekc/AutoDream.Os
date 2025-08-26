#!/usr/bin/env python3
"""
Unified Learning Models - Agent Cellphone V2
===========================================

CONSOLIDATED learning models eliminating duplication across multiple implementations.
Follows V2 standards: 400 LOC, OOP design, SRP.

**Author:** V2 Consolidation Specialist
**Created:** Current Sprint
**Status:** ACTIVE - CONSOLIDATION IN PROGRESS
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
import uuid


class LearningMode(Enum):
    """Unified learning modes consolidating all implementations"""
    REINFORCEMENT = "reinforcement"
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    ADAPTIVE = "adaptive"
    COLLABORATIVE = "collaborative"
    AUTONOMOUS = "autonomous"
    TRANSFER = "transfer"
    META = "meta"


class IntelligenceLevel(Enum):
    """Unified intelligence levels consolidating all implementations"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    MASTER = "master"
    AUTONOMOUS = "autonomous"


class LearningStatus(Enum):
    """Unified learning status states"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


@dataclass
class LearningGoal:
    """Unified learning goal structure"""
    goal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    target_metrics: Dict[str, float] = field(default_factory=dict)
    deadline: Optional[datetime] = None
    priority: int = 1  # 1-5 scale
    status: LearningStatus = LearningStatus.NOT_STARTED
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.goal_id:
            self.goal_id = str(uuid.uuid4())


@dataclass
class LearningProgress:
    """Unified learning progress tracking"""
    progress_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    goal_id: str = ""
    current_metrics: Dict[str, float] = field(default_factory=dict)
    completion_percentage: float = 0.0
    milestones_achieved: List[str] = field(default_factory=list)
    obstacles_encountered: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.progress_id:
            self.progress_id = str(uuid.uuid4())


@dataclass
class LearningData:
    """Unified learning data structure consolidating all implementations"""
    data_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    context: str = ""
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    performance_score: float = 0.0
    learning_mode: LearningMode = LearningMode.ADAPTIVE
    intelligence_level: IntelligenceLevel = IntelligenceLevel.INTERMEDIATE
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.data_id:
            self.data_id = str(uuid.uuid4())


@dataclass
class LearningPattern:
    """Unified learning pattern identification"""
    pattern_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    pattern_type: str = ""
    confidence_score: float = 0.0
    supporting_data: List[str] = field(default_factory=list)
    discovered_at: datetime = field(default_factory=datetime.now)
    last_observed: datetime = field(default_factory=datetime.now)
    frequency: int = 1
    
    def __post_init__(self):
        if not self.pattern_id:
            self.pattern_id = str(uuid.uuid4())


@dataclass
class LearningStrategy:
    """Unified learning strategy definition"""
    strategy_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    learning_mode: LearningMode = LearningMode.ADAPTIVE
    parameters: Dict[str, Any] = field(default_factory=dict)
    success_criteria: Dict[str, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    
    def __post_init__(self):
        if not self.strategy_id:
            self.strategy_id = str(uuid.uuid4())


@dataclass
class LearningMetrics:
    """Unified learning performance metrics"""
    metrics_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    metric_name: str = ""
    values: List[float] = field(default_factory=list)
    timestamps: List[datetime] = field(default_factory=list)
    average_value: float = 0.0
    trend: str = "stable"  # improving, declining, stable
    last_updated: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.metrics_id:
            self.metrics_id = str(uuid.uuid4())
        self._calculate_average()
        self._determine_trend()
    
    def _calculate_average(self):
        """Calculate average metric value"""
        if self.values:
            self.average_value = sum(self.values) / len(self.values)
    
    def _determine_trend(self):
        """Determine metric trend"""
        if len(self.values) >= 2:
            if self.values[-1] > self.values[0]:
                self.trend = "improving"
            elif self.values[-1] < self.values[0]:
                self.trend = "declining"
            else:
                self.trend = "stable"


@dataclass
class LearningSession:
    """Unified learning session tracking"""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    learning_goals: List[str] = field(default_factory=list)
    strategies_used: List[str] = field(default_factory=list)
    performance_summary: Dict[str, float] = field(default_factory=dict)
    session_data: List[LearningData] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
    
    def end_session(self):
        """End the learning session and calculate duration"""
        self.end_time = datetime.now()
        if self.start_time:
            self.duration_seconds = (self.end_time - self.start_time).total_seconds()
    
    def add_learning_data(self, data: LearningData):
        """Add learning data to the session"""
        self.session_data.append(data)
    
    def get_performance_summary(self) -> Dict[str, float]:
        """Calculate performance summary from session data"""
        if not self.session_data:
            return {}
        
        total_score = sum(data.performance_score for data in self.session_data)
        avg_score = total_score / len(self.session_data)
        
        return {
            "total_data_points": len(self.session_data),
            "average_performance": avg_score,
            "session_duration": self.duration_seconds,
            "goals_attempted": len(self.learning_goals)
        }


@dataclass
class LearningConfiguration:
    """Unified learning configuration settings"""
    config_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    default_learning_mode: LearningMode = LearningMode.ADAPTIVE
    target_intelligence_level: IntelligenceLevel = IntelligenceLevel.INTERMEDIATE
    learning_rate: float = 0.1
    batch_size: int = 32
    max_iterations: int = 1000
    convergence_threshold: float = 0.001
    adaptive_parameters: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.config_id:
            self.config_id = str(uuid.uuid4())
    
    def update_parameter(self, key: str, value: Any):
        """Update a configuration parameter"""
        if hasattr(self, key):
            setattr(self, key, value)
            self.updated_at = datetime.now()
        else:
            self.adaptive_parameters[key] = value
            self.updated_at = datetime.now()
    
    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Get a configuration parameter"""
        if hasattr(self, key):
            return getattr(self, key)
        return self.adaptive_parameters.get(key, default)


# Utility functions for learning models
def create_learning_goal(
    title: str,
    description: str,
    target_metrics: Dict[str, float],
    priority: int = 1,
    deadline: Optional[datetime] = None
) -> LearningGoal:
    """Create a new learning goal with validation"""
    if priority < 1 or priority > 5:
        raise ValueError("Priority must be between 1 and 5")
    
    return LearningGoal(
        title=title,
        description=description,
        target_metrics=target_metrics,
        priority=priority,
        deadline=deadline
    )


def create_learning_session(
    agent_id: str,
    learning_goals: List[str],
    strategies: List[str]
) -> LearningSession:
    """Create a new learning session"""
    return LearningSession(
        agent_id=agent_id,
        learning_goals=learning_goals,
        strategies_used=strategies
    )


def validate_learning_data(data: LearningData) -> bool:
    """Validate learning data structure"""
    if not data.agent_id:
        return False
    if not data.context:
        return False
    if data.performance_score < 0 or data.performance_score > 100:
        return False
    return True


def merge_learning_metrics(metrics_list: List[LearningMetrics]) -> LearningMetrics:
    """Merge multiple learning metrics into one"""
    if not metrics_list:
        raise ValueError("Cannot merge empty metrics list")
    
    base_metrics = metrics_list[0]
    merged_metrics = LearningMetrics(
        metrics_id=str(uuid.uuid4()),
        agent_id=base_metrics.agent_id,
        metric_name=base_metrics.metric_name
    )
    
    # Combine all values and timestamps
    for metrics in metrics_list:
        merged_metrics.values.extend(metrics.values)
        merged_metrics.timestamps.extend(metrics.timestamps)
    
    # Recalculate averages and trends
    merged_metrics._calculate_average()
    merged_metrics._determine_trend()
    
    return merged_metrics

