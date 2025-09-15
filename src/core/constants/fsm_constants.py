#!/usr/bin/env python3
"""
FSM Constants - V2 Compliance Finite State Machine Constants
===========================================================

This module provides FSM-related constants with V2 compliance standards.

V2 COMPLIANCE: Type-safe FSM constants with validation
DESIGN PATTERN: Constants pattern for FSM configuration
DEPENDENCY INJECTION: Configuration-driven FSM parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - FSM Constants Optimized
"""

from typing import Any, Final

from .fsm_models import StateDefinition


def get_config(key: str, default: Any) -> Any:
    """Get configuration value with fallback."""
    # Simplified configuration - KISS compliance
    import os

    return os.getenv(key, default)


# ================================
# FSM CONFIGURATION CONSTANTS
# ================================

# State timeouts and retries
FSM_STATE_TIMEOUT_SECONDS: Final[int | None] = get_config("FSM_STATE_TIMEOUT_SECONDS", 300)

FSM_STATE_RETRY_COUNT: Final[int] = get_config("FSM_STATE_RETRY_COUNT", 3)

FSM_STATE_RETRY_DELAY: Final[float] = get_config("FSM_STATE_RETRY_DELAY", 1.0)

# Transition settings
FSM_TRANSITION_PRIORITY_DEFAULT: Final[int] = get_config("FSM_TRANSITION_PRIORITY_DEFAULT", 1)
"""Default priority for FSM transitions."""

FSM_TRANSITION_TIMEOUT_SECONDS: Final[int | None] = get_config("FSM_TRANSITION_TIMEOUT_SECONDS", 60)
"""Default timeout for FSM transitions in seconds."""

# ================================
# CORE FSM STATE DEFINITIONS
# ================================

CORE_FSM_START_STATE: Final[StateDefinition] = StateDefinition(
    name="start",
    description="Starting state for FSM execution",
    entry_actions=["log_start", "initialize_context"],
    exit_actions=["validate_initialization"],
    timeout_seconds=FSM_STATE_TIMEOUT_SECONDS,
    retry_count=FSM_STATE_RETRY_COUNT,
    retry_delay=FSM_STATE_RETRY_DELAY,
    required_resources=["fsm_context"],
    dependencies=[],
    metadata={"category": "core", "critical": True},
)

CORE_FSM_PROCESS_STATE: Final[StateDefinition] = StateDefinition(
    name="process",
    description="Processing state for FSM execution",
    entry_actions=["log_process_start", "validate_input"],
    exit_actions=["log_process_end", "cleanup_resources"],
    timeout_seconds=FSM_STATE_TIMEOUT_SECONDS,
    retry_count=FSM_STATE_RETRY_COUNT,
    retry_delay=FSM_STATE_RETRY_DELAY,
    required_resources=["processing_context", "input_data"],
    dependencies=["start"],
    metadata={"category": "core", "critical": True},
)

CORE_FSM_COMPLETE_STATE: Final[StateDefinition] = StateDefinition(
    name="complete",
    description="Completion state for FSM execution",
    entry_actions=["log_completion", "finalize_results"],
    exit_actions=["cleanup_all", "notify_completion"],
    timeout_seconds=FSM_STATE_TIMEOUT_SECONDS,
    retry_count=FSM_STATE_RETRY_COUNT,
    retry_delay=FSM_STATE_RETRY_DELAY,
    required_resources=["completion_context"],
    dependencies=["process"],
    metadata={"category": "core", "critical": True},
)

CORE_FSM_ERROR_STATE: Final[StateDefinition] = StateDefinition(
    name="error",
    description="Error state for FSM execution",
    entry_actions=["log_error", "handle_error"],
    exit_actions=["cleanup_error", "notify_error"],
    timeout_seconds=FSM_STATE_TIMEOUT_SECONDS,
    retry_count=FSM_STATE_RETRY_COUNT,
    retry_delay=FSM_STATE_RETRY_DELAY,
    required_resources=["error_context"],
    dependencies=[],
    metadata={"category": "core", "critical": True},
)
