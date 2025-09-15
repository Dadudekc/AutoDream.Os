#!/usr/bin/env python3
""""
FSM Constants - Finite State Machine Definitions

This module provides FSM-related constants.

Agent: Agent-6 (Performance Optimization Manager)
Mission: Autonomous Cleanup - V2 Compliance
Status: SSOT Consolidation in Progress
""""

from .fsm_models import StateDefinition, TransitionDefinition, TransitionType

# Core FSM definitions
CORE_FSM_START_STATE = StateDefinition(
    name="start","
    description="Starting state","
    entry_actions=[],
    exit_actions=[],
    timeout_seconds=None,
    retry_count=0,
    retry_delay=0.0,
    required_resources=[],
    dependencies=[],
    metadata={},
)

CORE_FSM_PROCESS_STATE = StateDefinition(
    name="process","
    description="Processing state","
    entry_actions=[],
    exit_actions=[],
    timeout_seconds=None,
    retry_count=0,
    retry_delay=0.0,
    required_resources=[],
    dependencies=[],
    metadata={},
)

CORE_FSM_END_STATE = StateDefinition(
    name="end","
    description="Ending state","
    entry_actions=[],
    exit_actions=[],
    timeout_seconds=None,
    retry_count=0,
    retry_delay=0.0,
    required_resources=[],
    dependencies=[],
    metadata={},
)

CORE_FSM_DEFAULT_STATES = [
    CORE_FSM_START_STATE,
    CORE_FSM_PROCESS_STATE,
    CORE_FSM_END_STATE,
]

CORE_FSM_TRANSITION_START_PROCESS = TransitionDefinition(
    from_state="start","
    to_state="process","
    transition_type=TransitionType.AUTOMATIC,
    condition=None,
    priority=1,
    timeout_seconds=None,
    actions=[],
    metadata={},
)

CORE_FSM_TRANSITION_PROCESS_END = TransitionDefinition(
    from_state="process","
    to_state="end","
    transition_type=TransitionType.AUTOMATIC,
    condition=None,
    priority=1,
    timeout_seconds=None,
    actions=[],
    metadata={},
)
