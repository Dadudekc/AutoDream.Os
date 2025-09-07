"""Progress tracking utilities for the unified learning engine."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .models import LearningStatus

if TYPE_CHECKING:  # pragma: no cover - for type checkers
    from .unified_learning_engine import UnifiedLearningEngine


def update_learning_progress(
    engine: "UnifiedLearningEngine", goal_id: str, progress: float
) -> float:
    """Update progress for a learning goal.

    Args:
        engine: Active learning engine instance.
        goal_id: Identifier of the goal to update.
        progress: New progress value between 0.0 and 1.0.
    Returns:
        The clamped progress value or 0.0 on failure.
    """
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
    except Exception as exc:  # pragma: no cover - log and return
        engine.logger.error(f"Failed to update learning progress: {exc}")
        return 0.0
