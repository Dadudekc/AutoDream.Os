"""Workflow definition utilities for the FSM package."""




def get_default_definitions() -> (
    Tuple[List[StateDefinition], List[TransitionDefinition]]
):
    """Return default states and transitions used across the project."""
    return DEFAULT_STATES, DEFAULT_TRANSITIONS


__all__ = ["get_default_definitions"]
