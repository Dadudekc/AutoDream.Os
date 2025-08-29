"""
FSM Package - Finite State Machine System for Phase 2 Workflow Management

This package provides a modular, V2 standards compliant FSM system.
All components follow V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""

from .fsm_core import FSMCore, FSMStateManager, FSMWorkflowManager
from .fsm_states import (
    StateStatus, TransitionType, WorkflowPriority,
    StateDefinition, TransitionDefinition, WorkflowInstance,
    StateExecutionResult, TransitionResult
)
from .fsm_transitions import TransitionManager, TransitionValidator
from .fsm_execution import ExecutionEngine, ExecutionMonitor
from .fsm_orchestrator import FSMOrchestrator

__all__ = [
    # Core components
    'FSMCore',
    'FSMStateManager', 
    'FSMWorkflowManager',
    
    # State definitions
    'StateStatus',
    'TransitionType',
    'WorkflowPriority',
    'StateDefinition',
    'TransitionDefinition',
    'WorkflowInstance',
    'StateExecutionResult',
    'TransitionResult',
    
    # Transition management
    'TransitionManager',
    'TransitionValidator',
    
    # Execution engine
    'ExecutionEngine',
    'ExecutionMonitor',
    
    # Main orchestrator
    'FSMOrchestrator'
]

# Version information
__version__ = "2.0.0"
__author__ = "Agent-5 (Coding Standards Implementation)"
__status__ = "V2 Standards Compliant"
