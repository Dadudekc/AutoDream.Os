"""Reporting helpers for FSM state machines."""

from typing import Dict, List, Tuple

from .constants import DEFAULT_STATES, DEFAULT_TRANSITIONS


def generate_report() -> Dict[str, object]:
    """Generate a simple report summarizing states and transitions."""

    transitions: List[Tuple[str, str]] = [
        (src, tgt) for src, tgts in DEFAULT_TRANSITIONS.items() for tgt in tgts
    ]
    return {
        "states": list(DEFAULT_STATES),
        "transitions": transitions,
        "state_count": len(DEFAULT_STATES),
        "transition_count": len(transitions),
    }
