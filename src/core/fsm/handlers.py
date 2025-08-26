#!/usr/bin/env python3
"""Concrete FSM handlers executing state actions and transition checks."""

from datetime import datetime
import time
from typing import Any, Callable, Dict

from .models import StateExecutionResult, StateHandler, StateStatus, TransitionHandler


class ConcreteStateHandler(StateHandler):
    """State handler that runs an action and validates context."""

    def __init__(self, action: Callable[[Dict[str, Any]], None], check: Callable[[Dict[str, Any]], bool]):
        self._action = action
        self._check = check

    def execute(self, context: Dict[str, Any]) -> StateExecutionResult:
        """Execute the configured action then validate state."""
        self._action(context)
        success = self._check(context)
        status = StateStatus.COMPLETED if success else StateStatus.FAILED
        return StateExecutionResult(
            state_name=context.get("current_state", "unknown"),
            execution_time=0.0,
            status=status,
            output=context.copy(),
            error_message=None if success else "state check failed",
            metadata={},
            timestamp=datetime.now(),
        )

    def can_transition(self, context: Dict[str, Any]) -> bool:
        """Check if context satisfies requirements for transition."""
        return self._check(context)


class ConditionalTransitionHandler(TransitionHandler):
    """Transition handler evaluating a condition and applying a state change."""

    def __init__(self, condition: Callable[[Dict[str, Any]], bool], target_state: str):
        self._condition = condition
        self._target_state = target_state

    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Return True if transition is allowed."""
        return self._condition(context)

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply state change when condition is met."""
        allowed = self.evaluate(context)
        if allowed:
            context["current_state"] = self._target_state
        return {"allowed": allowed, "current_state": context.get("current_state")}
