"""
State Interface - Abstract State Management
Captain Agent-3: FSM Core V2 Modularization
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IStateManager(ABC):
    """Abstract interface for state management"""
    
    @abstractmethod
    def get_state(self, state_id: str) -> Optional[Dict[str, Any]]:
        """Get state by ID"""
        pass
    
    @abstractmethod
    def set_state(self, state_id: str, state_data: Dict[str, Any]) -> bool:
        """Set state data"""
        pass
    
    @abstractmethod
    def transition_to(self, from_state: str, to_state: str, context: Dict[str, Any]) -> bool:
        """Transition between states"""
        pass

class IStateDefinition(ABC):
    """Abstract interface for state definitions"""
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate state definition"""
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Get state metadata"""
        pass
