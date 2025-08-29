"""Data model helpers for FSM definitions."""

from dataclasses import dataclass
from typing import List, Tuple

from .constants import DEFAULT_STATES, DEFAULT_TRANSITIONS


@dataclass(frozen=True)
class StateDefinition:
    """Definition of a workflow state."""

    name: str


@dataclass(frozen=True)
class TransitionDefinition:
    """Definition of a state transition."""

    source: str
    target: str


def load_default_definitions() -> (
    Tuple[List[StateDefinition], List[TransitionDefinition]]
):
    """Build default state and transition definitions from constants."""

    states = [StateDefinition(name) for name in DEFAULT_STATES]
    transitions = [
        TransitionDefinition(src, tgt)
        for src, targets in DEFAULT_TRANSITIONS.items()
        for tgt in targets
    ]
    return states, transitions
