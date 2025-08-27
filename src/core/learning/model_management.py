#!/usr/bin/env python3
"""Model management utilities for UnifiedLearningEngine."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from .models import (
    LearningStrategy,
    LearningMode,
    LearningSession,
    LearningStatus,
    LearningGoal,
)
from .decision_models import (
    DecisionAlgorithm,
    DecisionRule,
    DecisionPriority,
    DecisionType,
)


def initialize_default_components(engine: "UnifiedLearningEngine") -> None:
    """Initialize default learning strategies, algorithms, and rules."""
    try:
        _initialize_default_strategies(engine)
        _initialize_default_algorithms(engine)
        _initialize_default_rules(engine)
        engine.logger.info("\u2705 Default components initialized successfully")
    except Exception as exc:  # pragma: no cover - log warning only
        engine.logger.warning(f"\u26a0\ufe0f Failed to initialize some default components: {exc}")


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
            decision_types=[DecisionType.TASK_ASSIGNMENT, DecisionType.PRIORITY_DETERMINATION],
            is_active=True,
            performance_metrics={"success_rate": 85.0, "response_time_ms": 50},
        ),
        DecisionAlgorithm(
            algorithm_id="machine_learning",
            name="Machine Learning Decision Making",
            description="Uses trained models for intelligent decision making",
            decision_types=[DecisionType.LEARNING_STRATEGY, DecisionType.RESOURCE_ALLOCATION],
            is_active=True,
            performance_metrics={"success_rate": 92.0, "response_time_ms": 150},
        ),
        DecisionAlgorithm(
            algorithm_id="collaborative",
            name="Collaborative Decision Making",
            description="Consults multiple agents for consensus decisions",
            decision_types=[DecisionType.COMPLEX_DECISION, DecisionType.STRATEGIC_PLANNING],
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


def create_learning_session(engine: "UnifiedLearningEngine", agent_id: str, session_type: str = "general") -> str:
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

        engine.logger.info(f"Created learning session: {session_id} for agent: {agent_id}")
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


def update_learning_goal(engine: "UnifiedLearningEngine", goal_id: str, **kwargs: Any) -> bool:
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


def update_learning_progress(engine: "UnifiedLearningEngine", goal_id: str, progress: float) -> float:
    """Update progress for a learning goal."""
    try:
        if goal_id not in engine.learning_goals:
            raise ValueError(f"Goal {goal_id} not found")
        goal = engine.learning_goals[goal_id]
        goal.current_progress = min(1.0, max(0.0, progress))
        goal.updated_at = datetime.now()
        if goal.current_progress >= 1.0:
            goal.status = LearningStatus.COMPLETED
            goal.completed_at = datetime.now()
            engine.logger.info(f"Learning goal completed: {goal_id}")
        return goal.current_progress
    except Exception as exc:  # pragma: no cover - log and default
        engine.logger.error(f"Failed to update learning progress: {exc}")
        return 0.0
