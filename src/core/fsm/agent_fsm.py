"""
Agent Finite State Machine for the integrated onboarding coordination system.

This module provides the AgentFSM class that manages agent state transitions
and maintains state history for the FSM system.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .agent_state import AgentState


class AgentFSM:
    """Finite State Machine for agent state management."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.current_state = AgentState.UNINITIALIZED
        self.previous_state = None
        self.state_history: List[Dict[str, Any]] = []
        self.transition_count = 0
        self.created_at = datetime.now()
    
    def transition_to(self, new_state: AgentState) -> bool:
        """Transition to a new state."""
        if self._is_valid_transition(self.current_state, new_state):
            self.previous_state = self.current_state
            self.current_state = new_state
            
            # Record transition in history
            transition_record = {
                "timestamp": datetime.now(),
                "from_state": self.previous_state.value if self.previous_state else None,
                "to_state": new_state.value,
                "agent_id": self.agent_id
            }
            self.state_history.append(transition_record)
            self.transition_count += 1
            
            return True
        return False
    
    def _is_valid_transition(self, from_state: AgentState, to_state: AgentState) -> bool:
        """Check if transition is valid."""
        # Define valid transitions
        valid_transitions = {
            AgentState.UNINITIALIZED: [AgentState.ONBOARDING],
            AgentState.ONBOARDING: [AgentState.IDLE, AgentState.ERROR_RECOVERY],
            AgentState.IDLE: [AgentState.CONTRACT_NEGOTIATION, AgentState.COLLABORATION],
            AgentState.CONTRACT_NEGOTIATION: [AgentState.TASK_EXECUTION, AgentState.IDLE],
            AgentState.TASK_EXECUTION: [AgentState.PROGRESS_REPORTING, AgentState.ERROR_RECOVERY],
            AgentState.COLLABORATION: [AgentState.PROGRESS_REPORTING, AgentState.IDLE],
            AgentState.PROGRESS_REPORTING: [AgentState.CYCLE_COMPLETION, AgentState.TASK_EXECUTION],
            AgentState.CYCLE_COMPLETION: [AgentState.IDLE],
            AgentState.ERROR_RECOVERY: [AgentState.IDLE, AgentState.ONBOARDING]
        }
        
        return to_state in valid_transitions.get(from_state, [])
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get current state information."""
        return {
            "agent_id": self.agent_id,
            "current_state": self.current_state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "transition_count": self.transition_count,
            "state_history_count": len(self.state_history),
            "created_at": self.created_at.isoformat()
        }