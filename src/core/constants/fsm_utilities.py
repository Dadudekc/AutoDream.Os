"""
FSM Utilities - V2 Compliance Finite State Machine Utilities
===========================================================

This module provides FSM-related utility functions with V2 compliance standards.

V2 COMPLIANCE: Type-safe FSM utilities with validation
DESIGN PATTERN: Utility pattern for FSM operations
DEPENDENCY INJECTION: Configuration-driven FSM parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - FSM Utilities Optimized
"""

from typing import List, Optional, Dict, Any
from .fsm_models import StateDefinition, TransitionDefinition, FSMConfiguration, FSMError
from .fsm_enums import TransitionType, FSMErrorType
from .fsm_constants import (
    FSM_STATE_TIMEOUT_SECONDS, FSM_STATE_RETRY_COUNT, FSM_STATE_RETRY_DELAY,
    FSM_TRANSITION_PRIORITY_DEFAULT, FSM_TRANSITION_TIMEOUT_SECONDS
)


def validate_fsm_constants() -> bool:
    """Validate FSM constants configuration - V2 compliance."""
    try:
        # Validate state timeout
        if FSM_STATE_TIMEOUT_SECONDS is not None and FSM_STATE_TIMEOUT_SECONDS <= 0:
            return False
        
        # Validate retry count
        if FSM_STATE_RETRY_COUNT < 0:
            return False
        
        # Validate retry delay
        if FSM_STATE_RETRY_DELAY < 0:
            return False
        
        # Validate transition priority
        if FSM_TRANSITION_PRIORITY_DEFAULT < 0:
            return False
        
        # Validate transition timeout
        if FSM_TRANSITION_TIMEOUT_SECONDS is not None and FSM_TRANSITION_TIMEOUT_SECONDS <= 0:
            return False
        
        return True
    except Exception:
        return False


def create_custom_state(
    name: str,
    description: str,
    entry_actions: List[str] = None,
    exit_actions: List[str] = None,
    timeout_seconds: Optional[int] = None,
    retry_count: int = None,
    retry_delay: float = None,
    required_resources: List[str] = None,
    dependencies: List[str] = None,
    metadata: Dict[str, Any] = None
) -> StateDefinition:
    """Create custom FSM state with V2 compliance."""
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
    transition_type: TransitionType = TransitionType.AUTOMATIC,
    condition: Optional[str] = None,
    priority: int = None,
    timeout_seconds: Optional[int] = None,
    actions: List[str] = None,
    metadata: Dict[str, Any] = None
) -> TransitionDefinition:
    """Create custom FSM transition with V2 compliance."""
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
    """Get FSM configuration summary - V2 compliance."""
    return {
        "state_timeout_seconds": FSM_STATE_TIMEOUT_SECONDS,
        "state_retry_count": FSM_STATE_RETRY_COUNT,
        "state_retry_delay": FSM_STATE_RETRY_DELAY,
        "transition_priority_default": FSM_TRANSITION_PRIORITY_DEFAULT,
        "transition_timeout_seconds": FSM_TRANSITION_TIMEOUT_SECONDS,
        "validation_enabled": True,
        "logging_enabled": True
    }
