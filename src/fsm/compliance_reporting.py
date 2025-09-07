"""Reporting helpers for FSM compliance orchestrator."""

from typing import Dict, Iterable, List, Tuple


def generate_report(
    states: Iterable[str], transitions: Iterable[Tuple[str, str]]
) -> Dict[str, object]:
    """Generate a simple report summarizing states and transitions."""

    state_list: List[str] = list(states)
    transition_list: List[Tuple[str, str]] = list(transitions)
    return {
        "states": state_list,
        "transitions": transition_list,
        "state_count": len(state_list),
        "transition_count": len(transition_list),
    }


__all__ = ["generate_report"]
