#!/usr/bin/env python3
"""State management mixin for FSM core."""

from typing import List, Optional

from .common import StateDefinition


class StateManager:
    """Provides state management operations."""

    def add_state(self, state_def: StateDefinition) -> bool:
        """Add a new state to the FSM."""
        try:
            if state_def.name in self.states:
                self.logger.warning(f"State {state_def.name} already exists, updating")

            self.states[state_def.name] = state_def
            self.logger.info(f"✅ Added state: {state_def.name}")
            return True

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to add state {state_def.name}: {e}")
            return False

    def remove_state(self, state_name: str) -> bool:
        """Remove a state from the FSM."""
        try:
            if state_name not in self.states:
                self.logger.warning(f"State {state_name} not found")
                return False

            for workflow in self.workflows.values():
                if workflow.current_state == state_name:
                    self.logger.error(
                        f"Cannot remove state {state_name} - in use by workflow {workflow.workflow_id}"
                    )
                    return False

            del self.states[state_name]
            self.logger.info(f"✅ Removed state: {state_name}")
            return True

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to remove state {state_name}: {e}")
            return False

    def get_state(self, state_name: str) -> Optional[StateDefinition]:
        """Get state definition by name."""
        return self.states.get(state_name)

    def list_states(self) -> List[str]:
        """List all available states."""
        return list(self.states.keys())


__all__ = ["StateManager"]
