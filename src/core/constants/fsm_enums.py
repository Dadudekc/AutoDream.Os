"""
FSM Enums - V2 Compliance Finite State Machine Enumerations
===========================================================

This module provides FSM-related enums with V2 compliance standards.

V2 COMPLIANCE: Type-safe FSM enumerations with validation
DESIGN PATTERN: Enum pattern for FSM type definitions
DEPENDENCY INJECTION: Configuration-driven FSM parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - FSM Enums Optimized
"""

from enum import Enum


class TransitionType(Enum):
    """Types of FSM transitions."""
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    CONDITIONAL = "conditional"
    TIMED = "timed"


class StateStatus(Enum):
    """FSM state status values."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class TransitionStatus(Enum):
    """FSM transition status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FSMErrorType(Enum):
    """FSM error types."""
    STATE_ERROR = "state_error"
    TRANSITION_ERROR = "transition_error"
    TIMEOUT_ERROR = "timeout_error"
    VALIDATION_ERROR = "validation_error"
    CONFIGURATION_ERROR = "configuration_error"
