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
from typing import Dict, List, Any, Optional, Set, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:  # pragma: no cover - for type checking only
    from .unified_learning_engine import UnifiedLearningEngine

from ..base_manager import ManagerConfig
from .decision_models import (
    DecisionAlgorithm,
    DecisionRule,
    DecisionPriority,
    DecisionType,
)


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
    learning_modes: List[LearningMode] = field(default_factory=list)
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
    session_type: str = "general"
    created_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    status: LearningStatus = LearningStatus.NOT_STARTED
    learning_goals: List[str] = field(default_factory=list)
    strategies_used: List[str] = field(default_factory=list)
    performance_summary: Dict[str, float] = field(default_factory=dict)
    session_data: List[LearningData] = field(default_factory=list)
    total_duration: float = 0.0

    def __post_init__(self):
        if not self.session_id:
            self.session_id = str(uuid.uuid4())

    def end_session(self):
        """End the learning session and calculate duration"""
        self.ended_at = datetime.now()
        self.status = LearningStatus.COMPLETED
        self.total_duration = (self.ended_at - self.created_at).total_seconds()

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
            "session_duration": self.total_duration,
            "goals_attempted": len(self.learning_goals),
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


@dataclass
class LearningManagerConfig(ManagerConfig):
    """Extended configuration for the learning manager"""

    max_concurrent_learners: int = 50
    learning_session_timeout: int = 3600  # seconds
    enable_adaptive_learning: bool = True
    enable_collaborative_learning: bool = True
    learning_rate: float = 0.1
    batch_size: int = 32
    max_iterations: int = 1000
    convergence_threshold: float = 0.001
    auto_cleanup_inactive_sessions: bool = True
    cleanup_interval_minutes: int = 30


@dataclass
class LearningEngineConfig:
    """Configuration for the unified learning engine"""

    engine_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    max_concurrent_sessions: int = 10
    session_timeout_minutes: int = 60
    learning_rate: float = 0.1
    batch_size: int = 32
    max_iterations: int = 1000
    convergence_threshold: float = 0.001
    enable_adaptive_learning: bool = True
    enable_collaborative_learning: bool = True
    log_level: str = "INFO"
    created_at: datetime = field(default_factory=datetime.now)


# Engine-related model management utilities


def initialize_default_components(engine: "UnifiedLearningEngine") -> None:
    """Initialize default learning strategies, algorithms, and rules."""
    try:
        _initialize_default_strategies(engine)
        _initialize_default_algorithms(engine)
        _initialize_default_rules(engine)
        engine.logger.info("✅ Default components initialized successfully")
    except Exception as exc:  # pragma: no cover - log warning only
        engine.logger.warning(f"⚠️ Failed to initialize some default components: {exc}")


def _initialize_default_strategies(engine: "UnifiedLearningEngine") -> None:
    """Populate default learning strategies."""
    default_strategies = [
        LearningStrategy(
            strategy_id="adaptive_learning",
            name="Adaptive Learning",
            description="Dynamically adjusts learning approach based on performance",
            learning_modes=[LearningMode.ADAPTIVE],
            parameters={"adaptation_rate": 0.1, "performance_threshold": 0.8},
        ),
        LearningStrategy(
            strategy_id="collaborative_learning",
            name="Collaborative Learning",
            description="Learns from multiple agents and shared experiences",
            learning_modes=[LearningMode.COLLABORATIVE],
            parameters={"collaboration_threshold": 0.6, "max_collaborators": 5},
        ),
        LearningStrategy(
            strategy_id="reinforcement_learning",
            name="Reinforcement Learning",
            description="Learns through trial and error with reward feedback",
            learning_modes=[LearningMode.REINFORCEMENT],
            parameters={"exploration_rate": 0.2, "learning_rate": 0.1},
        ),
    ]

    for strategy in default_strategies:
        engine.learning_strategies[strategy.strategy_id] = strategy


def _initialize_default_algorithms(engine: "UnifiedLearningEngine") -> None:
    """Populate default decision algorithms."""
    default_algorithms = [
        DecisionAlgorithm(
            algorithm_id="rule_based",
            name="Rule-Based Decision Making",
            description="Makes decisions based on predefined rules and logic",
            decision_types=[
                DecisionType.TASK_ASSIGNMENT,
                DecisionType.PRIORITY_DETERMINATION,
            ],
            is_active=True,
            performance_metrics={"success_rate": 85.0, "response_time_ms": 50},
        ),
        DecisionAlgorithm(
            algorithm_id="machine_learning",
            name="Machine Learning Decision Making",
            description="Uses trained models for intelligent decision making",
            decision_types=[
                DecisionType.LEARNING_STRATEGY,
                DecisionType.RESOURCE_ALLOCATION,
            ],
            is_active=True,
            performance_metrics={"success_rate": 92.0, "response_time_ms": 150},
        ),
        DecisionAlgorithm(
            algorithm_id="collaborative",
            name="Collaborative Decision Making",
            description="Consults multiple agents for consensus decisions",
            decision_types=[
                DecisionType.COMPLEX_DECISION,
                DecisionType.STRATEGIC_PLANNING,
            ],
            is_active=True,
            performance_metrics={"success_rate": 88.0, "response_time_ms": 300},
        ),
    ]

    for algorithm in default_algorithms:
        engine.decision_algorithms[algorithm.algorithm_id] = algorithm


def _initialize_default_rules(engine: "UnifiedLearningEngine") -> None:
    """Populate default decision rules."""
    default_rules = [
        DecisionRule(
            rule_id="high_priority_first",
            name="High Priority First",
            description="Always prioritize high priority tasks",
            condition="priority == 'HIGH'",
            action="assign_to_primary_agent",
            priority=DecisionPriority.HIGH,
        ),
        DecisionRule(
            rule_id="expertise_based_assignment",
            name="Expertise-Based Assignment",
            description="Assign tasks based on agent expertise",
            condition="agent_expertise matches task_requirements",
            action="assign_to_expert_agent",
            priority=DecisionPriority.MEDIUM,
        ),
        DecisionRule(
            rule_id="load_balancing",
            name="Load Balancing",
            description="Distribute tasks evenly across available agents",
            condition="agent_load < average_load",
            action="assign_to_least_loaded_agent",
            priority=DecisionPriority.MEDIUM,
        ),
    ]

    for rule in default_rules:
        engine.decision_rules[rule.rule_id] = rule


def create_learning_session(
    engine: "UnifiedLearningEngine",
    agent_id: str,
    session_type: str = "general",
    **_: Any,
) -> str:
    """Create a new learning session for an agent."""
    try:
        if len(engine.active_sessions) >= engine.config.max_concurrent_sessions:
            oldest_session = min(
                engine.active_sessions,
                key=lambda s: engine.learning_sessions[s].created_at,
            )
            end_learning_session(engine, oldest_session)

        session_id = str(uuid.uuid4())
        session = LearningSession(
            session_id=session_id,
            agent_id=agent_id,
            session_type=session_type,
            created_at=datetime.now(),
            status=LearningStatus.ACTIVE,
        )
        engine.learning_sessions[session_id] = session
        engine.active_sessions.add(session_id)
        engine.session_locks[session_id] = False

        engine.logger.info(
            f"Created learning session: {session_id} for agent: {agent_id}"
        )
        engine.total_learning_operations += 1
        engine.successful_operations += 1
        return session_id
    except Exception as exc:  # pragma: no cover - propagate error
        engine.logger.error(f"Failed to create learning session: {exc}")
        engine.total_learning_operations += 1
        engine.failed_operations += 1
        raise


def end_learning_session(engine: "UnifiedLearningEngine", session_id: str) -> bool:
    """End a learning session and clean up resources."""
    try:
        if session_id not in engine.learning_sessions:
            return False
        session = engine.learning_sessions[session_id]
        session.status = LearningStatus.COMPLETED
        session.ended_at = datetime.now()
        engine.active_sessions.discard(session_id)
        engine.session_locks.pop(session_id, None)
        session_duration = (session.ended_at - session.created_at).total_seconds()
        session.total_duration = session_duration
        engine.logger.info(
            f"Ended learning session: {session_id} (duration: {session_duration:.2f}s)"
        )
        return True
    except Exception as exc:  # pragma: no cover - log and return
        engine.logger.error(f"Failed to end learning session: {exc}")
        return False


def create_learning_goal(
    engine: "UnifiedLearningEngine",
    title: str,
    description: str,
    target_metrics: Dict[str, float],
    priority: int = 1,
    deadline: Optional[datetime] = None,
) -> str:
    """Create a new learning goal."""
    try:
        goal_id = str(uuid.uuid4())
        goal = LearningGoal(
            goal_id=goal_id,
            title=title,
            description=description,
            target_metrics=target_metrics,
            priority=priority,
            deadline=deadline,
        )
        engine.learning_goals[goal_id] = goal
        engine.logger.info(f"Created learning goal: {goal_id} - {title}")
        engine.total_learning_operations += 1
        engine.successful_operations += 1
        return goal_id
    except Exception as exc:  # pragma: no cover - propagate
        engine.logger.error(f"Failed to create learning goal: {exc}")
        engine.total_learning_operations += 1
        engine.failed_operations += 1
        raise


def update_learning_goal(
    engine: "UnifiedLearningEngine", goal_id: str, **kwargs: Any
) -> bool:
    """Update an existing learning goal."""
    try:
        if goal_id not in engine.learning_goals:
            raise ValueError(f"Goal {goal_id} not found")
        goal = engine.learning_goals[goal_id]
        for key, value in kwargs.items():
            if hasattr(goal, key):
                setattr(goal, key, value)
        goal.updated_at = datetime.now()
        engine.logger.info(f"Updated learning goal: {goal_id}")
        engine.total_learning_operations += 1
        engine.successful_operations += 1
        return True
    except Exception as exc:  # pragma: no cover - log and return
        engine.logger.error(f"Failed to update learning goal: {exc}")
        engine.total_learning_operations += 1
        engine.failed_operations += 1
        return False
