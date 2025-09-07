#!/usr/bin/env python3
"""Helper utilities for the FSM execution engine."""

import logging
from typing import Any, Dict, List, Optional

from .state_machine import TransitionDefinition, WorkflowInstance


def evaluate_condition(
    condition: str, context: Dict[str, Any], logger: Optional[logging.Logger] = None
) -> bool:
    """Evaluate a transition condition."""
    try:
        if "==" in condition:
            key, value = condition.split("==")
            return str(context.get(key.strip())) == value.strip()
        if "!=" in condition:
            key, value = condition.split("!=")
            return str(context.get(key.strip())) != value.strip()
        if ">" in condition:
            key, value = condition.split(">")
            return float(context.get(key.strip(), 0)) > float(value.strip())
        if "<" in condition:
            key, value = condition.split("<")
            return float(context.get(key.strip(), 0)) < float(value.strip())
        return condition.strip() in context
    except Exception as e:  # pragma: no cover - defensive
        if logger:
            logger.error(f"Failed to evaluate condition '{condition}': {e}")
        return False


def can_execute_transition(
    transition: TransitionDefinition,
    context: Dict[str, Any],
    logger: Optional[logging.Logger] = None,
) -> bool:
    """Check if a transition can be executed."""
    try:
        if transition.condition:
            return evaluate_condition(transition.condition, context, logger)
        return True
    except Exception as e:  # pragma: no cover - defensive
        if logger:
            logger.error(f"Failed to evaluate transition condition: {e}")
        return False


def build_context(workflow: WorkflowInstance) -> Dict[str, Any]:
    """Build execution context for state handlers."""
    return {
        "workflow_id": workflow.workflow_id,
        "workflow_name": workflow.workflow_name,
        "current_state": workflow.current_state,
        "state_history": workflow.state_history,
        "metadata": workflow.metadata,
        "start_time": workflow.start_time.isoformat(),
        "priority": workflow.priority.value,
    }


def execute_actions(
    workflow_id: str,
    actions: List[str],
    action_type: str,
    logger: Optional[logging.Logger] = None,
) -> None:
    """Execute a list of actions."""
    for action in actions:
        try:
            if logger:
                logger.debug(
                    f"Executing {action_type} action: {action} for workflow {workflow_id}"
                )
            # Action execution logic can be extended here
        except Exception as e:  # pragma: no cover - defensive
            if logger:
                logger.error(f"Failed to execute {action_type} action {action}: {e}")
