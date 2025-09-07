<<<<<<< HEAD
#!/usr/bin/env python3
"""
FSM Constants - V2 Compliance Finite State Machine Definitions (V2 Refactored)
==============================================================================

V2 Refactored FSM module with modular architecture and V2 compliance standards.

V2 COMPLIANCE: Type-safe FSM definitions with validation and configuration
DESIGN PATTERN: Builder pattern for FSM state and transition creation
DEPENDENCY INJECTION: Configuration-driven FSM parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - FSM Refactored Optimized
"""

# V2 Refactored - Backward Compatibility Wrapper
from .fsm_refactored import *

# Maintain backward compatibility
__all__ = [
    # Enums
    "TransitionType",
    "StateStatus",
    "TransitionStatus",
    "FSMErrorType",
    # Models
    "StateDefinition",
    "TransitionDefinition",
    "FSMConfiguration",
    "FSMError",
    # Constants
    "FSM_STATE_TIMEOUT_SECONDS",
    "FSM_STATE_RETRY_COUNT",
    "FSM_STATE_RETRY_DELAY",
    "FSM_TRANSITION_PRIORITY_DEFAULT",
    "FSM_TRANSITION_TIMEOUT_SECONDS",
    "CORE_FSM_START_STATE",
    "CORE_FSM_PROCESS_STATE",
    "CORE_FSM_COMPLETE_STATE",
    "CORE_FSM_ERROR_STATE",
    # Utilities
    "validate_fsm_constants",
    "create_custom_state",
    "create_custom_transition",
    "get_fsm_config_summary",
]
=======
from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
FSM Constants - Finite State Machine Definitions

This module provides FSM-related constants.

Agent: Agent-6 (Performance Optimization Manager)
Mission: Autonomous Cleanup - V2 Compliance
Status: SSOT Consolidation in Progress
"""

from ..fsm.fsm_core import StateDefinition, TransitionDefinition, TransitionType

# Core FSM definitions
CORE_FSM_START_STATE = StateDefinition(
    name="start",
    description="Starting state",
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
    name="process",
    description="Processing state",
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
    name="end",
    description="Ending state",
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
    from_state="start",
    to_state="process",
    transition_type=TransitionType.AUTOMATIC,
    condition=None,
    priority=1,
    timeout_seconds=None,
    actions=[],
    metadata={},
)

CORE_FSM_TRANSITION_PROCESS_END = TransitionDefinition(
    from_state="process",
    to_state="end",
    transition_type=TransitionType.AUTOMATIC,
    condition=None,
    priority=1,
    timeout_seconds=None,
    actions=[],
    metadata={},
)
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
