#!/usr/bin/env python3
"""
FSM Bridge - Task State Management
===================================

Bridges message-task system with Core FSM constants.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

from enum import Enum


class TaskState(str, Enum):
    """Task state constants aligned with Core FSM."""

    TODO = "todo"
    DOING = "doing"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskEvent(str, Enum):
    """Task event constants."""

    CREATE = "create"
    START = "start"
    BLOCK = "block"
    UNBLOCK = "unblock"
    COMPLETE = "complete"
    CANCEL = "cancel"


def initial_state() -> TaskState:
    """Get initial state for new task."""
    return TaskState.TODO


def transition_on_create() -> tuple[TaskState, TaskEvent]:
    """Get state and event when task is created."""
    return TaskState.TODO, TaskEvent.CREATE


def transition_to_doing(current_state: TaskState | None = None) -> tuple[TaskState, TaskEvent]:
    """Transition to DOING state."""
    if current_state == TaskState.BLOCKED:
        return TaskState.DOING, TaskEvent.UNBLOCK
    return TaskState.DOING, TaskEvent.START


def transition_to_blocked(
    reason: str | None = None,
) -> tuple[TaskState, TaskEvent]:
    """Transition to BLOCKED state."""
    return TaskState.BLOCKED, TaskEvent.BLOCK


def transition_to_done() -> tuple[TaskState, TaskEvent]:
    """Transition to DONE state."""
    return TaskState.DONE, TaskEvent.COMPLETE


def transition_to_cancelled() -> tuple[TaskState, TaskEvent]:
    """Transition to CANCELLED state."""
    return TaskState.CANCELLED, TaskEvent.CANCEL


def is_terminal_state(state: TaskState) -> bool:
    """Check if state is terminal (no further transitions)."""
    return state in (TaskState.DONE, TaskState.CANCELLED)


def can_transition(from_state: TaskState, to_state: TaskState) -> bool:
    """
    Check if transition is valid.

    Args:
        from_state: Current state
        to_state: Target state

    Returns:
        True if transition is allowed
    """
    # Terminal states cannot transition
    if is_terminal_state(from_state):
        return False

    # Valid transition matrix
    valid_transitions = {
        TaskState.TODO: {TaskState.DOING, TaskState.CANCELLED},
        TaskState.DOING: {TaskState.BLOCKED, TaskState.DONE, TaskState.CANCELLED},
        TaskState.BLOCKED: {TaskState.DOING, TaskState.CANCELLED},
    }

    return to_state in valid_transitions.get(from_state, set())


def get_transition_event(from_state: TaskState, to_state: TaskState) -> TaskEvent | None:
    """
    Get event for state transition.

    Args:
        from_state: Current state
        to_state: Target state

    Returns:
        Event or None if invalid transition
    """
    if not can_transition(from_state, to_state):
        return None

    # Map transitions to events
    transition_events = {
        (TaskState.TODO, TaskState.DOING): TaskEvent.START,
        (TaskState.DOING, TaskState.BLOCKED): TaskEvent.BLOCK,
        (TaskState.DOING, TaskState.DONE): TaskEvent.COMPLETE,
        (TaskState.BLOCKED, TaskState.DOING): TaskEvent.UNBLOCK,
        (TaskState.TODO, TaskState.CANCELLED): TaskEvent.CANCEL,
        (TaskState.DOING, TaskState.CANCELLED): TaskEvent.CANCEL,
        (TaskState.BLOCKED, TaskState.CANCELLED): TaskEvent.CANCEL,
    }

    return transition_events.get((from_state, to_state))
