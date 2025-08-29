"""Workflow definition utilities for the FSM package."""
from typing import List, Tuple
from .fsm_core import StateDefinition, TransitionDefinition
from .constants import DEFAULT_STATES, DEFAULT_TRANSITIONS


def get_default_definitions() -> (
    Tuple[List[StateDefinition], List[TransitionDefinition]]
):
    """Return default states and transitions used across the project."""
    return DEFAULT_STATES, DEFAULT_TRANSITIONS


__all__ = ["get_default_definitions"]
