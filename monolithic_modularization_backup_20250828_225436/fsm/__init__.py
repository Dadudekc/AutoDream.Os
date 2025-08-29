"""
FSM Core V2 - Modular Architecture
Captain Agent-3: FSM Core V2 Modularization Implementation
"""

__version__ = "2.0.0"
__author__ = "Captain Agent-3"
__status__ = "MODULARIZED"

# Core imports
from .core.engine.execution_engine import ExecutionEngine
from .core.states.state_manager import StateManager
from .core.transitions.transition_manager import TransitionManager
from .core.workflows.workflow_manager import WorkflowManager

# Interface imports
from .interfaces.state_interface import IStateManager
from .interfaces.transition_interface import ITransitionManager
from .interfaces.workflow_interface import IWorkflowManager

# Utility imports
from .utils.config import FSMConfig

__all__ = [
    "ExecutionEngine",
    "StateManager", 
    "TransitionManager",
    "WorkflowManager",
    "IStateManager",
    "ITransitionManager",
    "IWorkflowManager",
    "FSMConfig"
]

# Main FSM Core V2 class
class FSMCoreV2:
    """Main entry point for modular FSM Core V2"""
    
    def __init__(self):
        self.state_manager = StateManager()
        self.transition_manager = TransitionManager()
        self.workflow_manager = WorkflowManager()
        self.execution_engine = ExecutionEngine()
        self.config = FSMConfig()
    
    def initialize(self) -> bool:
        """Initialize FSM Core V2"""
        return True
    
    def get_state_manager(self) -> StateManager:
        """Get state manager instance"""
        return self.state_manager
    
    def get_transition_manager(self) -> TransitionManager:
        """Get transition manager instance"""
        return self.transition_manager
    
    def get_workflow_manager(self) -> WorkflowManager:
        """Get workflow manager instance"""
        return self.workflow_manager
