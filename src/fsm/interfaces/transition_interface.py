"""
Transition Interface - Abstract Transition Logic
Captain Agent-3: FSM Core V2 Modularization
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class ITransitionManager(ABC):
    """Abstract interface for transition management"""
    
    @abstractmethod
    def get_available_transitions(self, current_state: str) -> List[str]:
        """Get available transitions from current state"""
        pass
    
    @abstractmethod
    def execute_transition(self, from_state: str, to_state: str, context: Dict[str, Any]) -> bool:
        """Execute state transition"""
        pass
    
    @abstractmethod
    def validate_transition(self, from_state: str, to_state: str) -> bool:
        """Validate transition possibility"""
        pass

class ITransitionDefinition(ABC):
    """Abstract interface for transition definitions"""
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate transition definition"""
        pass
    
    @abstractmethod
    def get_conditions(self) -> Dict[str, Any]:
        """Get transition conditions"""
        pass
