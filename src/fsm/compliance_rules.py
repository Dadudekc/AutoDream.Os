"""Compliance rule validators for FSM definitions."""

from typing import Iterable, Tuple

from .constants import DEFAULT_STATES, DEFAULT_TRANSITIONS


def validate_states(states: Iterable[str]) -> bool:
    """Ensure all provided states exist in the defaults."""

    unknown = set(states) - set(DEFAULT_STATES)
    if unknown:
        raise ValueError(f"Unknown states: {sorted(unknown)}")
    return True


def validate_transitions(transitions: Iterable[Tuple[str, str]]) -> bool:
    """Validate that transitions use known states and allowed paths."""

    for source, target in transitions:
        if source not in DEFAULT_STATES:
            raise ValueError(f"Unknown source state: {source}")
        if target not in DEFAULT_STATES:
            raise ValueError(f"Unknown target state: {target}")
        allowed = DEFAULT_TRANSITIONS.get(source, ())
        if target not in allowed:
            raise ValueError(f"Invalid transition: {source} -> {target}")
    return True


__all__ = ["validate_states", "validate_transitions"]
