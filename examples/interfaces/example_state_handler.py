"""Example FSM state and transition handlers."""

from typing import Any, Dict

from src.core.fsm.fsm_core_v2 import (
    StateExecutionResult,
    StateHandler,
    TransitionHandler,
)


class IdleState(StateHandler):
    """Idle state that performs no work."""

    def execute(self, context: Dict[str, Any]) -> StateExecutionResult:
        return StateExecutionResult(success=True, context=context)

    def can_transition(self, context: Dict[str, Any]) -> bool:
        return True


class AlwaysTransition(TransitionHandler):
    """Transition that always evaluates to ``True``."""

    def evaluate(self, context: Dict[str, Any]) -> bool:
        return True

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return context
