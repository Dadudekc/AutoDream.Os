from typing import Dict, Any

        from datetime import datetime
from .fsm_data_models import StateExecutionResult
from abc import ABC, abstractmethod

#!/usr/bin/env python3
"""
FSM Handlers - Abstract Base Classes for State and Transition Handlers
====================================================================

Contains abstract base classes for state and transition handlers.
Follows V2 standards: focused responsibility, clear interfaces.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""




# ============================================================================
# ABSTRACT BASE CLASSES
# ============================================================================


class StateHandler(ABC):
    """Abstract base class for state handlers."""

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> StateExecutionResult:
        """Execute the state logic.

        Args:
            context (Dict[str, Any]): Current FSM context.

        Returns:
            StateExecutionResult: Result of the state execution.
        """
        raise NotImplementedError("execute must be implemented by subclasses")

    @abstractmethod
    def can_transition(self, context: Dict[str, Any]) -> bool:
        """Check if transition to this state is allowed.

        Args:
            context (Dict[str, Any]): Current FSM context.

        Returns:
            bool: True if transition is permitted.
        """
        raise NotImplementedError("can_transition must be implemented by subclasses")

    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validate context before execution.

        Args:
            context (Dict[str, Any]): Current FSM context.

        Returns:
            bool: True if context is valid.
        """
        return isinstance(context, dict) and len(context) > 0

    def pre_execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Pre-execution hook for state preparation.

        Args:
            context (Dict[str, Any]): Current FSM context.

        Returns:
            Dict[str, Any]: Updated context.
        """
        return context

    def post_execute(self, context: Dict[str, Any], result: StateExecutionResult) -> StateExecutionResult:
        """Post-execution hook for state cleanup.

        Args:
            context (Dict[str, Any]): Current FSM context.
            result (StateExecutionResult): Execution result.

        Returns:
            StateExecutionResult: Updated result.
        """
        return result


class TransitionHandler(ABC):
    """Abstract base class for transition handlers."""

    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate transition condition.

        Args:
            context (Dict[str, Any]): Current FSM context.

        Returns:
            bool: True if the transition condition is met.
        """
        raise NotImplementedError("evaluate must be implemented by subclasses")

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute transition actions.

        Args:
            context (Dict[str, Any]): Current FSM context.

        Returns:
            Dict[str, Any]: Updated context after execution.
        """
        raise NotImplementedError("execute must be implemented by subclasses")

    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validate context before evaluation.

        Args:
            context (Dict[str, Any]): Current FSM context.

        Returns:
            bool: True if context is valid.
        """
        return isinstance(context, dict) and len(context) > 0

    def pre_evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Pre-evaluation hook for transition preparation.

        Args:
            context (Dict[str, Any]): Current FSM context.

        Returns:
            Dict[str, Any]: Updated context.
        """
        return context

    def post_execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Post-execution hook for transition cleanup.

        Args:
            context (Dict[str, Any]): Current FSM context.

        Returns:
            Dict[str, Any]: Updated context.
        """
        return context


# ============================================================================
# DEFAULT HANDLER IMPLEMENTATIONS
# ============================================================================


class DefaultStateHandler(StateHandler):
    """Default state handler implementation."""

    def __init__(self, state_name: str):
        """Initialize default state handler."""
        self.state_name = state_name

    def execute(self, context: Dict[str, Any]) -> StateExecutionResult:
        """Execute default state logic."""
        
        # Default implementation - just mark as completed
        return StateExecutionResult(
            state_name=self.state_name,
            execution_time=0.0,
            status="completed",
            output=context,
            error_message=None,
            metadata={"handler": "DefaultStateHandler"},
            timestamp=datetime.now()
        )

    def can_transition(self, context: Dict[str, Any]) -> bool:
        """Default transition permission - always allow."""
        return True


class DefaultTransitionHandler(TransitionHandler):
    """Default transition handler implementation."""

    def __init__(self, from_state: str, to_state: str):
        """Initialize default transition handler."""
        self.from_state = from_state
        self.to_state = to_state

    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Default transition evaluation - always allow."""
        return True

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute default transition actions."""
        # Add transition metadata to context
        context["last_transition"] = {
            "from_state": self.from_state,
            "to_state": self.to_state,
            "timestamp": datetime.now().isoformat()
        }
        return context


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def create_state_handler(handler_class: type, **kwargs) -> StateHandler:
    """Create a state handler instance."""
    try:
        return handler_class(**kwargs)
    except Exception as e:
        # Fallback to default handler
        return DefaultStateHandler("fallback")


def create_transition_handler(handler_class: type, **kwargs) -> TransitionHandler:
    """Create a transition handler instance."""
    try:
        return handler_class(**kwargs)
    except Exception as e:
        # Fallback to default handler
        return DefaultTransitionHandler("unknown", "unknown")


# ============================================================================
# EXPORTS
# ============================================================================


__all__ = [
    "StateHandler",
    "TransitionHandler",
    "DefaultStateHandler",
    "DefaultTransitionHandler",
    "create_state_handler",
    "create_transition_handler",
]
