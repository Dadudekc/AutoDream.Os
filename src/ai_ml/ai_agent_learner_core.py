from __future__ import annotations

"""Core learning utilities for the AI agent.

This module contains lightweight dataclasses and a small manager used by
:mod:`ai_agent_learner`. It keeps track of learning goals and progress
without any external dependencies so it can be easily tested.
"""

from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass
class LearningGoal:
    """Represents a single learning objective."""

    name: str
    description: str = ""


@dataclass
class LearningProgress:
    """Tracks progress toward a :class:`LearningGoal`."""

    goal: LearningGoal
    progress: float = 0.0  # value between 0 and 1

    def update(self, value: float) -> float:
        """Update progress ensuring it stays within ``0`` and ``1``."""

        self.progress = max(0.0, min(1.0, value))
        return self.progress


class LearnerCore:
    """Central manager coordinating learning goals."""

    def __init__(self) -> None:
        self._goals: Dict[str, LearningProgress] = {}

    # Goal management -----------------------------------------------------
    def add_goal(self, goal: LearningGoal) -> None:
        """Register a new learning goal."""

        self._goals[goal.name] = LearningProgress(goal)

    def update_progress(self, goal_name: str, value: float) -> float:
        """Update progress for a given goal.

        Raises
        ------
        KeyError
            If the goal does not exist.
        """

        if goal_name not in self._goals:
            raise KeyError(f"Unknown goal: {goal_name}")
        return self._goals[goal_name].update(value)

    def progress_report(self) -> Dict[str, float]:
        """Return a mapping of goal names to progress values."""

        return {name: lp.progress for name, lp in self._goals.items()}

    def overall_progress(self) -> float:
        """Average progress across all goals."""

        if not self._goals:
            return 0.0
        return sum(lp.progress for lp in self._goals.values()) / len(self._goals)

    def goals(self) -> Iterable[LearningGoal]:
        """Iterate over registered goals."""

        return (lp.goal for lp in self._goals.values())


__all__ = [
    "LearningGoal",
    "LearningProgress",
    "LearnerCore",
]
