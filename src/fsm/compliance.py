"""High-level orchestrator for FSM compliance tasks."""

from typing import Iterable, Tuple, Dict, Any

from .compliance_rules import validate_states, validate_transitions
from .state_manager import StateManager
from .compliance_reporting import generate_report


class ComplianceOrchestrator:
    """Coordinate validation, state management, and reporting."""

    def __init__(self) -> None:
        self.state_manager = StateManager()

    def run(
        self, states: Iterable[str], transitions: Iterable[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """Validate the FSM definition and return a compliance report."""

        validate_states(states)
        validate_transitions(transitions)
        for state in states:
            self.state_manager.set_state(state, {})
        return generate_report(states, transitions)


__all__ = ["ComplianceOrchestrator"]
