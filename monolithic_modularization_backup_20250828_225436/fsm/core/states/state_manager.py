"""
State Manager - FSM Core V2 Modularization
Captain Agent-3: State Management Implementation
"""

import logging
from typing import Dict, Any, Optional
from ..interfaces.state_interface import IStateManager

class StateManager(IStateManager):
    """Concrete state manager implementation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.states = {}
        self.state_history = []
    
    def get_state(self, state_id: str) -> Optional[Dict[str, Any]]:
        """Get state by ID"""
        return self.states.get(state_id)
    
    def set_state(self, state_id: str, state_data: Dict[str, Any]) -> bool:
        """Set state data"""
        try:
            self.states[state_id] = state_data
            self.state_history.append({
                "state_id": state_id,
                "action": "set",
                "timestamp": "2025-08-28T22:45:00.000000Z"
            })
            return True
        except Exception as e:
            self.logger.error(f"Failed to set state: {e}")
            return False
    
    def transition_to(self, from_state: str, to_state: str, context: Dict[str, Any]) -> bool:
        """Transition between states"""
        try:
            if from_state in self.states and to_state in self.states:
                self.state_history.append({
                    "from_state": from_state,
                    "to_state": to_state,
                    "context": context,
                    "timestamp": "2025-08-28T22:45:00.000000Z"
                })
                return True
            return False
        except Exception as e:
            self.logger.error(f"State transition failed: {e}")
            return False
