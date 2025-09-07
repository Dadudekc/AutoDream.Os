#!/usr/bin/env python3
"""Learning Manager - high-level orchestrator for unified learning engine."""

from datetime import datetime
from typing import Any, Dict, Optional

from ..base_manager import BaseManager
from .models import (
    LearningMode,
    LearningManagerConfig,
    LearningEngineConfig,
)
from .unified_learning_engine import UnifiedLearningEngine
from . import models as learning_models
from .trainer import add_learning_data


class LearningManager(BaseManager):
    """High-level orchestration for learning operations."""

    def __init__(
        self, manager_id: str, name: str = "Learning Manager", description: str = ""
    ):
        super().__init__(manager_id, name, description)
        self.learning_config = LearningManagerConfig(
            manager_id=manager_id,
            name=name,
            description=description,
        )
        self.learning_engine: Optional[UnifiedLearningEngine] = None
        self.logger.info(f"LearningManager initialized: {manager_id}")

    def _on_start(self) -> bool:
        """Initialize the learning engine."""
        try:
            engine_config = LearningEngineConfig(
                max_concurrent_sessions=self.learning_config.max_concurrent_learners,
                session_timeout_minutes=self.learning_config.learning_session_timeout
                // 60,
                learning_rate=self.learning_config.learning_rate,
                batch_size=self.learning_config.batch_size,
                max_iterations=self.learning_config.max_iterations,
                convergence_threshold=self.learning_config.convergence_threshold,
                enable_adaptive_learning=self.learning_config.enable_adaptive_learning,
                enable_collaborative_learning=self.learning_config.enable_collaborative_learning,
            )
            self.learning_engine = UnifiedLearningEngine(engine_config)
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Learning Manager: {e}")
            return False

    def _on_stop(self) -> None:
        """Shutdown learning engine."""
        self.learning_engine = None

    def _on_heartbeat(self) -> None:
        """Heartbeat hook for future monitoring."""
        pass

    def _initialize_resources(self) -> bool:
        """Initialize manager resources."""
        self.logger.info("LearningManager resources initialized")
        return True

    def _cleanup_resources(self) -> None:
        """Cleanup manager resources."""
        self.logger.info("LearningManager resources cleaned up")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from an error."""
        self.logger.warning(f"Recovery attempt for {context}: {error}")
        return False

    # ------------------------------------------------------------------
    # High-level learning operations
    # ------------------------------------------------------------------
    def start_learning_session(
        self, agent_id: str, session_type: str = "general"
    ) -> Optional[str]:
        """Create a new learning session."""
        if not self.learning_engine:
            return None
        return learning_models.create_learning_session(
            self.learning_engine, agent_id, session_type
        )

    def end_learning_session(self, session_id: str) -> bool:
        """End an existing learning session."""
        if not self.learning_engine:
            return False
        return learning_models.end_learning_session(self.learning_engine, session_id)

    def add_learning_data(
        self,
        session_id: str,
        context: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        performance_score: float,
        learning_mode: LearningMode = LearningMode.ADAPTIVE,
    ) -> bool:
        """Add learning data to a session."""
        if not self.learning_engine:
            return False
        return add_learning_data(
            self.learning_engine,
            session_id,
            context,
            input_data,
            output_data,
            performance_score,
            learning_mode,
        )

    def create_learning_goal(
        self,
        title: str,
        description: str,
        target_metrics: Dict[str, float],
        priority: int = 1,
        deadline: Optional[datetime] = None,
    ) -> Optional[str]:
        """Create a learning goal."""
        if not self.learning_engine:
            return None
        return learning_models.create_learning_goal(
            self.learning_engine,
            title,
            description,
            target_metrics,
            priority,
            deadline,
        )

    def update_learning_goal(self, goal_id: str, **kwargs: Any) -> bool:
        """Update a learning goal."""
        if not self.learning_engine:
            return False
        return learning_models.update_learning_goal(
            self.learning_engine, goal_id, **kwargs
        )

    def get_learning_status(self) -> Dict[str, Any]:
        """Get engine status summary."""
        if not self.learning_engine:
            return {"status": "engine_not_initialized"}
        return self.learning_engine.get_engine_status()
