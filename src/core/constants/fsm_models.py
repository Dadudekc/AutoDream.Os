"""
FSM Models - V2 Compliance Finite State Machine Data Models
==========================================================

This module provides FSM-related data models with V2 compliance standards.

V2 COMPLIANCE: Type-safe FSM data models with validation
DESIGN PATTERN: Dataclass pattern for FSM model definitions
DEPENDENCY INJECTION: Configuration-driven FSM parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - FSM Models Optimized
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from .fsm_enums import TransitionType, StateStatus, TransitionStatus, FSMErrorType


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


@dataclass
class FSMConfiguration:
    """FSM configuration with V2 compliance."""
    state_timeout_seconds: Optional[int]
    state_retry_count: int
    state_retry_delay: float
    transition_priority_default: int
    transition_timeout_seconds: Optional[int]
    max_states: int
    max_transitions: int
    validation_enabled: bool
    logging_enabled: bool
    metadata: Dict[str, Any]


@dataclass
class FSMError:
    """FSM error with V2 compliance."""
    error_type: FSMErrorType
    message: str
    state_name: Optional[str]
    transition_name: Optional[str]
    timestamp: str
    metadata: Dict[str, Any]
