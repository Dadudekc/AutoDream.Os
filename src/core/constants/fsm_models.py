#!/usr/bin/env python3
"""
FSM Models - V2 Compliance Refactored
====================================

FSM-related data models with V2 compliance standards.
Refactored into modular architecture for better maintainability.
V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from .fsm.configuration_models import FSMConfiguration

# Import modular components
from .fsm.state_models import StateDefinition
from .fsm.transition_models import TransitionDefinition
from .fsm_enums import FSMErrorType, StateStatus, TransitionStatus, TransitionType

# Re-export for backward compatibility
__all__ = [
    "StateDefinition",
    "TransitionDefinition",
    "FSMConfiguration",
    "FSMErrorType",
    "StateStatus",
    "TransitionStatus",
    "TransitionType",
]
