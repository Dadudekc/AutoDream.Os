"""Cleanup rule helpers for decision management."""

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - for type hints only
    from .decision_tracking import DecisionTracker


def schedule_cleanup(tracker: "DecisionTracker") -> None:
    """Record the last cleanup time."""
    tracker.last_cleanup_time = datetime.now()


def should_cleanup(last_cleanup_time, interval_minutes: int) -> bool:
    """Return True if cleanup should run based on interval."""
    if not last_cleanup_time:
        return True
    elapsed = datetime.now() - last_cleanup_time
    return elapsed.total_seconds() >= interval_minutes * 60


def cleanup_completed_decisions(
    tracker: "DecisionTracker", max_history: int, logger
) -> None:
    """Remove finished decisions and trim history."""
    current_time = datetime.now()
    to_remove = [
        did
        for did, info in tracker.active_decisions.items()
        if info.get("status") in {"completed", "failed"}
    ]
    for decision_id in to_remove:
        tracker.active_decisions.pop(decision_id, None)

    if len(tracker.decision_history) > max_history:
        excess = len(tracker.decision_history) - max_history
        tracker.decision_history = tracker.decision_history[excess:]

    if to_remove:
        logger.info(f"Cleaned up {len(to_remove)} completed decisions")

    tracker.last_cleanup_time = current_time
