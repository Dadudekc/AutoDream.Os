"""
🎯 FSM INTERFACES - CONSOLIDATED
Agent-7 - Interface Systems Consolidation Specialist

Consolidated FSM interface definitions.
Source: src/fsm/interfaces/

Agent: Agent-7 (Interface Systems Consolidation Specialist)
Mission: CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders
Priority: CRITICAL - Above all other work
Status: IMPLEMENTATION PHASE 1 - Unified Interface System

Author: Agent-7 - Quality Completion Optimization Manager
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum


class StateStatus(Enum):
    """State status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    TRANSITIONING = "transitioning"
    ERROR = "error"


class TransitionType(Enum):
    """Transition type enumeration."""
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    CONDITIONAL = "conditional"
    TIMEOUT = "timeout"


class StateInterface(ABC):
    """
    Interface for FSM state management.
    
    Provides unified state management functionality across all FSM implementations.
    """
    
    @abstractmethod
    def enter_state(self, context: Dict[str, Any]) -> bool:
        """Enter the state with given context."""
        pass
    
    @abstractmethod
    def exit_state(self, context: Dict[str, Any]) -> bool:
        """Exit the state with given context."""
        pass
    
    @abstractmethod
    def execute_state(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute state logic with given context."""
        pass
    
    @abstractmethod
    def get_state_status(self) -> StateStatus:
        """Get current state status."""
        pass
    
    @abstractmethod
    def can_transition_to(self, target_state: str) -> bool:
        """Check if transition to target state is allowed."""
        pass
    
    @abstractmethod
    def get_available_transitions(self) -> List[str]:
        """Get list of available transitions from this state."""
        pass


class TransitionInterface(ABC):
    """
    Interface for FSM transition management.
    
    Provides unified transition functionality across all FSM implementations.
    """
    
    @abstractmethod
    def execute_transition(self, from_state: str, to_state: str, context: Dict[str, Any]) -> bool:
        """Execute transition from one state to another."""
        pass
    
    @abstractmethod
    def validate_transition(self, from_state: str, to_state: str, context: Dict[str, Any]) -> bool:
        """Validate if transition is allowed."""
        pass
    
    @abstractmethod
    def get_transition_type(self) -> TransitionType:
        """Get the type of this transition."""
        pass
    
    @abstractmethod
    def get_transition_conditions(self) -> Dict[str, Any]:
        """Get conditions required for this transition."""
        pass
    
    @abstractmethod
    def get_transition_actions(self) -> List[Callable]:
        """Get actions to execute during this transition."""
        pass


class WorkflowInterface(ABC):
    """
    Interface for FSM workflow management.
    
    Provides unified workflow functionality across all FSM implementations.
    """
    
    @abstractmethod
    def start_workflow(self, initial_context: Dict[str, Any]) -> str:
        """Start a new workflow instance."""
        pass
    
    @abstractmethod
    def stop_workflow(self, workflow_id: str) -> bool:
        """Stop a workflow instance."""
        pass
    
    @abstractmethod
    def pause_workflow(self, workflow_id: str) -> bool:
        """Pause a workflow instance."""
        pass
    
    @abstractmethod
    def resume_workflow(self, workflow_id: str) -> bool:
        """Resume a paused workflow instance."""
        pass
    
    @abstractmethod
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of workflow instance."""
        pass
    
    @abstractmethod
    def get_workflow_history(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get history of workflow instance."""
        pass
    
    @abstractmethod
    def add_workflow_listener(self, workflow_id: str, listener: Callable) -> bool:
        """Add listener to workflow events."""
        pass
    
    @abstractmethod
    def remove_workflow_listener(self, workflow_id: str, listener: Callable) -> bool:
        """Remove listener from workflow events."""
        pass
