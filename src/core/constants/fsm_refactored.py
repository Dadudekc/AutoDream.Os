"""
FSM Refactored - V2 Compliance Finite State Machine (Refactored)
================================================================

Refactored FSM module with modular architecture and V2 compliance standards.

V2 COMPLIANCE: Type-safe FSM definitions with validation and configuration
DESIGN PATTERN: Builder pattern for FSM state and transition creation
DEPENDENCY INJECTION: Configuration-driven FSM parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - FSM Refactored Optimized
"""

# Import all FSM components
from .fsm_enums import (
    TransitionType, StateStatus, TransitionStatus, FSMErrorType
)
from .fsm_models import (
    StateDefinition, TransitionDefinition, FSMConfiguration, FSMError
)
from .fsm_constants import (
    FSM_STATE_TIMEOUT_SECONDS, FSM_STATE_RETRY_COUNT, FSM_STATE_RETRY_DELAY,
    FSM_TRANSITION_PRIORITY_DEFAULT, FSM_TRANSITION_TIMEOUT_SECONDS,
    CORE_FSM_START_STATE, CORE_FSM_PROCESS_STATE, CORE_FSM_COMPLETE_STATE, CORE_FSM_ERROR_STATE
)
from .fsm_utilities import (
    validate_fsm_constants, create_custom_state, create_custom_transition, get_fsm_config_summary
)

# Re-export all public components for backward compatibility
__all__ = [
    # Enums
    'TransitionType', 'StateStatus', 'TransitionStatus', 'FSMErrorType',
    # Models
    'StateDefinition', 'TransitionDefinition', 'FSMConfiguration', 'FSMError',
    # Constants
    'FSM_STATE_TIMEOUT_SECONDS', 'FSM_STATE_RETRY_COUNT', 'FSM_STATE_RETRY_DELAY',
    'FSM_TRANSITION_PRIORITY_DEFAULT', 'FSM_TRANSITION_TIMEOUT_SECONDS',
    'CORE_FSM_START_STATE', 'CORE_FSM_PROCESS_STATE', 'CORE_FSM_COMPLETE_STATE', 'CORE_FSM_ERROR_STATE',
    # Utilities
    'validate_fsm_constants', 'create_custom_state', 'create_custom_transition', 'get_fsm_config_summary'
]
