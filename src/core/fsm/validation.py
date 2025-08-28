"""Compliance validation utilities for FSM workflows."""
from typing import List
from .fsm_core import StateDefinition, TransitionDefinition


def validate_workflow(
    states: List[StateDefinition], transitions: List[TransitionDefinition]
) -> bool:
    """Ensure transitions reference valid states."""
    state_names = {state.name for state in states}
    if not state_names:
        return False
    for transition in transitions:
        if (
            transition.from_state not in state_names
            or transition.to_state not in state_names
        ):
            return False
    return True


__all__ = ["validate_workflow"]
