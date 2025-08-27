#!/usr/bin/env python3
"""
Unified Learning Engine - Agent Cellphone V2
===========================================

Consolidated learning engine delegating responsibilities to
model management, training, and evaluation modules.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, Any, Optional, Set, List

from .models import (
    LearningGoal,
    LearningPattern,
    LearningStrategy,
    LearningMetrics,
    LearningSession,
    LearningMode,
    LearningEngineConfig,
)
from .decision_models import (
    DecisionAlgorithm,
    DecisionRule,
    DecisionWorkflow,
    DecisionMetrics,
    DecisionType,
    DecisionResult,
    DecisionContext,
)

from . import model_management, training, evaluation


class UnifiedLearningEngine:
    """Unified learning engine using modular components."""

    def __init__(self, config: Optional[LearningEngineConfig] = None):
        self.config = config or LearningEngineConfig()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        # Core learning components
        self.learning_sessions: Dict[str, LearningSession] = {}
        self.learning_goals: Dict[str, LearningGoal] = {}
        self.learning_metrics: Dict[str, LearningMetrics] = {}
        self.learning_patterns: Dict[str, LearningPattern] = {}
        self.learning_strategies: Dict[str, LearningStrategy] = {}

        # Decision components
        self.decision_algorithms: Dict[str, DecisionAlgorithm] = {}
        self.decision_rules: Dict[str, DecisionRule] = {}
        self.decision_workflows: Dict[str, DecisionWorkflow] = {}
        self.decision_metrics: Dict[DecisionType, Dict[str, Any]] = {}

        # Active learning state
        self.active_sessions: Set[str] = set()
        self.session_locks: Dict[str, bool] = {}

        # Performance tracking
        self.total_learning_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0
        self.startup_time = datetime.now()

        self.logger.info(
            f"UnifiedLearningEngine initialized: {self.config.engine_id}"
        )
        self._initialize_default_components()

    # ------------------------------------------------------------------
    # Model management
    # ------------------------------------------------------------------
    def _initialize_default_components(self) -> None:
        model_management.initialize_default_components(self)

    def create_learning_session(self, agent_id: str, session_type: str = "general") -> str:
        return model_management.create_learning_session(self, agent_id, session_type)

    def end_learning_session(self, session_id: str) -> bool:
        return model_management.end_learning_session(self, session_id)

    def create_learning_goal(
        self,
        title: str,
        description: str,
        target_metrics: Dict[str, float],
        priority: int = 1,
        deadline: Optional[datetime] = None,
    ) -> str:
        return model_management.create_learning_goal(
            self, title, description, target_metrics, priority, deadline
        )

    def update_learning_goal(self, goal_id: str, **kwargs: Any) -> bool:
        return model_management.update_learning_goal(self, goal_id, **kwargs)

    def update_learning_progress(self, goal_id: str, progress: float) -> float:
        return model_management.update_learning_progress(self, goal_id, progress)

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------
    def add_learning_data(
        self,
        session_id: str,
        context: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        performance_score: float,
        learning_mode: LearningMode = LearningMode.ADAPTIVE,
    ) -> bool:
        return training.add_learning_data(
            self,
            session_id,
            context,
            input_data,
            output_data,
            performance_score,
            learning_mode,
        )

    def make_decision(
        self,
        decision_type: DecisionType,
        requester: str,
        parameters: Dict[str, Any],
        context: Optional[DecisionContext] = None,
        algorithm_id: Optional[str] = None,
    ) -> DecisionResult:
        return training.make_decision(
            self, decision_type, requester, parameters, context, algorithm_id
        )

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------
    def identify_learning_patterns(
        self, agent_id: str, session_id: str
    ) -> List[LearningPattern]:
        return evaluation.identify_learning_patterns(self, agent_id, session_id)

    def get_learning_performance_summary(self, agent_id: str) -> Dict[str, Any]:
        return evaluation.get_learning_performance_summary(self, agent_id)

    def get_engine_status(self) -> Dict[str, Any]:
        return evaluation.get_engine_status(self)

    def run_smoke_test(self) -> bool:
        return evaluation.run_smoke_test(self)


