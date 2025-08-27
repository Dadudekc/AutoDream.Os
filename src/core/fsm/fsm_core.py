#!/usr/bin/env python3
"""Compatibility wrapper for FSM core components."""

try:  # pragma: no cover - allow standalone import
    from .state_machine import (
        StateHandler,
        TransitionHandler,
        StateStatus,
        TransitionType,
        WorkflowPriority,
        StateDefinition,
        TransitionDefinition,
        WorkflowInstance,
        StateExecutionResult,
    )
    from .execution_engine import FSMCore
except Exception:  # pragma: no cover - fallback for direct execution
    from state_machine import (
        StateHandler,
        TransitionHandler,
        StateStatus,
        TransitionType,
        WorkflowPriority,
        StateDefinition,
        TransitionDefinition,
        WorkflowInstance,
        StateExecutionResult,
    )
    from execution_engine import FSMCore

FSMCoreV2 = FSMCore
FiniteStateMachine = FSMCore
WorkflowEngine = FSMCore

__all__ = [
    "FSMCore",
    "FSMCoreV2",
    "FiniteStateMachine",
    "WorkflowEngine",
    "StateHandler",
    "TransitionHandler",
    "StateStatus",
    "TransitionType",
    "WorkflowPriority",
    "StateDefinition",
    "TransitionDefinition",
    "WorkflowInstance",
    "StateExecutionResult",
]
