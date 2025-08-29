#!/usr/bin/env python3
"""Transition management mixin for FSM core."""

from typing import Any, Dict, List

from .common import TransitionDefinition, can_execute_transition


class TransitionManager:
    """Provides transition management operations."""

    def add_transition(self, transition_def: TransitionDefinition) -> bool:
        """Add a new transition to the FSM."""
        try:
            if transition_def.from_state not in self.states:
                self.logger.error(f"From state {transition_def.from_state} not found")
                return False

            if transition_def.to_state not in self.states:
                self.logger.error(f"To state {transition_def.to_state} not found")
                return False

            self.transitions[transition_def.from_state].append(transition_def)
            self.logger.info(
                f"✅ Added transition: {transition_def.from_state} -> {transition_def.to_state}"
            )
            return True

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to add transition: {e}")
            return False

    def remove_transition(self, from_state: str, to_state: str) -> bool:
        """Remove a transition from the FSM."""
        try:
            if from_state not in self.transitions:
                return False

            transitions = self.transitions[from_state]
            for i, transition in enumerate(transitions):
                if transition.to_state == to_state:
                    del transitions[i]
                    self.logger.info(
                        f"✅ Removed transition: {from_state} -> {to_state}"
                    )
                    return True

            return False

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to remove transition: {e}")
            return False

    def get_transitions(self, from_state: str) -> List[TransitionDefinition]:
        """Get all transitions from a state."""
        return self.transitions.get(from_state, [])

    def get_available_transitions(
        self, current_state: str, context: Dict[str, Any]
    ) -> List[TransitionDefinition]:
        """Get available transitions from current state."""
        available: List[TransitionDefinition] = []

        for transition in self.get_transitions(current_state):
            if can_execute_transition(transition, context, self.logger):
                available.append(transition)

        available.sort(key=lambda t: t.priority, reverse=True)
        return available


__all__ = ["TransitionManager"]
