"""Shared FSM constants for states and transitions."""

from typing import Dict, Tuple

# Single source of truth for default workflow states
DEFAULT_STATES: Tuple[str, ...] = (
    "pending",
    "in_progress",
    "completed",
    "failed",
)

# Allowed transitions between states
DEFAULT_TRANSITIONS: Dict[str, Tuple[str, ...]] = {
    "pending": ("in_progress",),
    "in_progress": ("completed", "failed"),
    "completed": (),
    "failed": (),
}
