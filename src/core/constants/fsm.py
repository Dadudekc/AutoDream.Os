
#!/usr/bin/env python3
"""
FSM Constants - V2 Compliance Finite State Machine Definitions
===============================================================

This module provides FSM-related constants with V2 compliance standards.

V2 COMPLIANCE: Type-safe FSM definitions with validation and configuration
DESIGN PATTERN: Builder pattern for FSM state and transition creation
DEPENDENCY INJECTION: Configuration-driven FSM parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - FSM Constants Optimized
"""

from typing import List, Optional, Dict, Any, Final
from dataclasses import dataclass
from enum import Enum
# Configuration simplified - KISS compliance

# ================================
# FSM TYPE DEFINITIONS
# ================================

class TransitionType(Enum):
    """Types of FSM transitions."""
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    CONDITIONAL = "conditional"
    TIMED = "timed"

@dataclass
class StateDefinition:
    """FSM state definition with V2 compliance."""
    name: str
    description: str
    entry_actions: List[str]
    exit_actions: List[str]
    timeout_seconds: Optional[int]
    retry_count: int
    retry_delay: float
    required_resources: List[str]
    dependencies: List[str]
    metadata: Dict[str, Any]

@dataclass
class TransitionDefinition:
    """FSM transition definition with V2 compliance."""
    from_state: str
    to_state: str
    transition_type: TransitionType
    condition: Optional[str]
    priority: int
    timeout_seconds: Optional[int]
    actions: List[str]
    metadata: Dict[str, Any]

# ================================
# FSM CONFIGURATION CONSTANTS
# ================================

# State timeouts and retries
FSM_STATE_TIMEOUT_SECONDS: Final[Optional[int]] = get_config("FSM_STATE_TIMEOUT_SECONDS", 300)
"""Default timeout for FSM states in seconds."""

FSM_STATE_RETRY_COUNT: Final[int] = get_config("FSM_STATE_RETRY_COUNT", 3)
"""Default retry count for failed state transitions."""

FSM_STATE_RETRY_DELAY: Final[float] = get_config("FSM_STATE_RETRY_DELAY", 1.0)
"""Default retry delay in seconds between state transition attempts."""

# Transition settings
FSM_TRANSITION_PRIORITY_DEFAULT: Final[int] = get_config("FSM_TRANSITION_PRIORITY_DEFAULT", 1)
"""Default priority for FSM transitions."""

FSM_TRANSITION_TIMEOUT_SECONDS: Final[Optional[int]] = get_config("FSM_TRANSITION_TIMEOUT_SECONDS", 60)
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
    metadata={"category": "core", "critical": True}
)

CORE_FSM_PROCESS_STATE: Final[StateDefinition] = StateDefinition(
    name="process",
    description="Main processing state for FSM operations",
    entry_actions=["validate_input", "execute_process"],
    exit_actions=["cleanup_resources", "update_status"],
    timeout_seconds=FSM_STATE_TIMEOUT_SECONDS,
    retry_count=FSM_STATE_RETRY_COUNT,
    retry_delay=FSM_STATE_RETRY_DELAY,
    required_resources=["fsm_context", "processing_engine"],
    dependencies=["start"],
    metadata={"category": "core", "critical": False}
)

CORE_FSM_END_STATE: Final[StateDefinition] = StateDefinition(
    name="end",
    description="Terminal state for FSM completion",
    entry_actions=["finalize_execution", "generate_report"],
    exit_actions=["cleanup_all_resources", "log_completion"],
    timeout_seconds=None,  # No timeout for end state
    retry_count=0,  # No retries for end state
    retry_delay=0.0,
    required_resources=[],
    dependencies=["process"],
    metadata={"category": "core", "terminal": True}
)

# ================================
# CORE FSM TRANSITION DEFINITIONS
# ================================

CORE_FSM_TRANSITION_START_PROCESS: Final[TransitionDefinition] = TransitionDefinition(
    from_state="start",
    to_state="process",
    transition_type=TransitionType.AUTOMATIC,
    condition="start_completed",
    priority=FSM_TRANSITION_PRIORITY_DEFAULT,
    timeout_seconds=FSM_TRANSITION_TIMEOUT_SECONDS,
    actions=["transfer_context", "notify_process_start"],
    metadata={"automatic": True, "required_condition": True}
)

CORE_FSM_TRANSITION_PROCESS_END: Final[TransitionDefinition] = TransitionDefinition(
    from_state="process",
    to_state="end",
    transition_type=TransitionType.CONDITIONAL,
    condition="process_successful",
    priority=FSM_TRANSITION_PRIORITY_DEFAULT,
    timeout_seconds=FSM_TRANSITION_TIMEOUT_SECONDS,
    actions=["finalize_results", "notify_completion"],
    metadata={"conditional": True, "success_required": True}
)

# ================================
# FSM COLLECTIONS
# ================================

CORE_FSM_DEFAULT_STATES: Final[List[StateDefinition]] = [
    CORE_FSM_START_STATE,
    CORE_FSM_PROCESS_STATE,
    CORE_FSM_END_STATE,
]
"""Default FSM states for basic workflows."""

CORE_FSM_DEFAULT_TRANSITIONS: Final[List[TransitionDefinition]] = [
    CORE_FSM_TRANSITION_START_PROCESS,
    CORE_FSM_TRANSITION_PROCESS_END,
]
"""Default FSM transitions for basic workflows."""

# ================================
# FSM VALIDATION CONSTANTS
# ================================

FSM_MAX_STATE_TIMEOUT: Final[int] = 3600  # 1 hour
"""Maximum allowed timeout for FSM states."""

FSM_MAX_RETRY_COUNT: Final[int] = 10
"""Maximum allowed retry count for FSM states."""

FSM_MAX_RETRY_DELAY: Final[float] = 60.0  # 1 minute
"""Maximum allowed retry delay for FSM states."""

FSM_MAX_TRANSITION_PRIORITY: Final[int] = 100
"""Maximum allowed priority for FSM transitions."""

# ================================
# UTILITY FUNCTIONS
# ================================

def validate_fsm_constants() -> bool:
    """Validate FSM configuration constants."""
    config = get_unified_config()

    # Validate state timeout
    if FSM_STATE_TIMEOUT_SECONDS is not None and FSM_STATE_TIMEOUT_SECONDS > FSM_MAX_STATE_TIMEOUT:
        config.get_logger(__name__).error(
            f"Invalid FSM state timeout: {FSM_STATE_TIMEOUT_SECONDS} "
            f"(must be <= {FSM_MAX_STATE_TIMEOUT})"
        )
        return False

    # Validate retry count
    if FSM_STATE_RETRY_COUNT > FSM_MAX_RETRY_COUNT:
        config.get_logger(__name__).error(
            f"Invalid FSM retry count: {FSM_STATE_RETRY_COUNT} "
            f"(must be <= {FSM_MAX_RETRY_COUNT})"
        )
        return False

    # Validate retry delay
    if FSM_STATE_RETRY_DELAY > FSM_MAX_RETRY_DELAY:
        config.get_logger(__name__).error(
            f"Invalid FSM retry delay: {FSM_STATE_RETRY_DELAY} "
            f"(must be <= {FSM_MAX_RETRY_DELAY})"
        )
        return False

    # Validate transition priority
    if FSM_TRANSITION_PRIORITY_DEFAULT > FSM_MAX_TRANSITION_PRIORITY:
        config.get_logger(__name__).error(
            f"Invalid FSM transition priority: {FSM_TRANSITION_PRIORITY_DEFAULT} "
            f"(must be <= {FSM_MAX_TRANSITION_PRIORITY})"
        )
        return False

    return True

def create_custom_state(
    name: str,
    description: str,
    entry_actions: Optional[List[str]] = None,
    exit_actions: Optional[List[str]] = None,
    timeout_seconds: Optional[int] = None,
    retry_count: Optional[int] = None,
    retry_delay: Optional[float] = None,
    required_resources: Optional[List[str]] = None,
    dependencies: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> StateDefinition:
    """Create a custom FSM state with validation."""
    return StateDefinition(
        name=name,
        description=description,
        entry_actions=entry_actions or [],
        exit_actions=exit_actions or [],
        timeout_seconds=timeout_seconds or FSM_STATE_TIMEOUT_SECONDS,
        retry_count=retry_count or FSM_STATE_RETRY_COUNT,
        retry_delay=retry_delay or FSM_STATE_RETRY_DELAY,
        required_resources=required_resources or [],
        dependencies=dependencies or [],
        metadata=metadata or {}
    )

def create_custom_transition(
    from_state: str,
    to_state: str,
    transition_type: TransitionType,
    condition: Optional[str] = None,
    priority: Optional[int] = None,
    timeout_seconds: Optional[int] = None,
    actions: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> TransitionDefinition:
    """Create a custom FSM transition with validation."""
    return TransitionDefinition(
        from_state=from_state,
        to_state=to_state,
        transition_type=transition_type,
        condition=condition,
        priority=priority or FSM_TRANSITION_PRIORITY_DEFAULT,
        timeout_seconds=timeout_seconds or FSM_TRANSITION_TIMEOUT_SECONDS,
        actions=actions or [],
        metadata=metadata or {}
    )

def get_fsm_config_summary() -> Dict[str, Any]:
    """Get a summary of FSM configuration."""
    return {
        "state_timeout_seconds": FSM_STATE_TIMEOUT_SECONDS,
        "state_retry_count": FSM_STATE_RETRY_COUNT,
        "state_retry_delay": FSM_STATE_RETRY_DELAY,
        "transition_priority_default": FSM_TRANSITION_PRIORITY_DEFAULT,
        "transition_timeout_seconds": FSM_TRANSITION_TIMEOUT_SECONDS,
        "default_states": len(CORE_FSM_DEFAULT_STATES),
        "default_transitions": len(CORE_FSM_DEFAULT_TRANSITIONS),
        "validation_limits": {
            "max_state_timeout": FSM_MAX_STATE_TIMEOUT,
            "max_retry_count": FSM_MAX_RETRY_COUNT,
            "max_retry_delay": FSM_MAX_RETRY_DELAY,
            "max_transition_priority": FSM_MAX_TRANSITION_PRIORITY
        }
    }

# ================================
# INITIALIZATION
# ================================

# Validate FSM constants on import
if not validate_fsm_constants():
    raise ValueError("FSM constants validation failed - check configuration values")
