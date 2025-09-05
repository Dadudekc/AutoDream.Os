"""
FSM Models - V2 Compliance Refactored
====================================

FSM-related data models with V2 compliance standards.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from .fsm_enums import TransitionType, StateStatus, TransitionStatus, FSMErrorType

# Import modular components
from .fsm.state_models import StateDefinition
from .fsm.transition_models import TransitionDefinition
from .fsm.configuration_models import FSMConfiguration

# Re-export for backward compatibility
__all__ = [
    'StateDefinition',
    'TransitionDefinition',
    'FSMConfiguration',
    'TransitionType',
    'StateStatus',
    'TransitionStatus',
    'FSMErrorType'
]

# Backward compatibility - create aliases
StateDefinition = StateDefinition
TransitionDefinition = TransitionDefinition
FSMConfiguration = FSMConfiguration