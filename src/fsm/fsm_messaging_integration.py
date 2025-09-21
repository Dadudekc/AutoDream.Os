#!/usr/bin/env python3
"""
FSM Messaging Integration
=========================

Integrates FSM state management with the messaging system for enhanced
agent coordination and state tracking.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .fsm_registry import AgentState, SwarmState, read_agent_state

logger = logging.getLogger(__name__)


@dataclass
class FSMTransition:
    """FSM state transition record."""
    agent_id: str
    from_state: str
    to_state: str
    timestamp: str
    reason: str
    metadata: Dict[str, Any]


class FSMMessagingIntegration:
    """Integrates FSM state management with messaging system."""
    
    def __init__(self):
        """Initialize FSM messaging integration."""
        self.transition_log = []
        self.state_cache = {}
    
    def get_agent_fsm_state(self, agent_id: str) -> Optional[str]:
        """Get current FSM state for agent."""
        return read_agent_state(agent_id)
    
    def validate_state_transition(self, agent_id: str, from_state: str, to_state: str) -> bool:
        """Validate if state transition is allowed."""
        # Define valid transitions based on FSM spec
        valid_transitions = {
            AgentState.ONBOARDING: [AgentState.ACTIVE, AgentState.ERROR, AgentState.SHUTDOWN],
            AgentState.ACTIVE: [
                AgentState.CONTRACT_EXECUTION_ACTIVE, 
                AgentState.PAUSED, 
                AgentState.ERROR, 
                AgentState.SHUTDOWN
            ],
            AgentState.CONTRACT_EXECUTION_ACTIVE: [
                AgentState.SURVEY_MISSION_COMPLETED, 
                AgentState.ACTIVE, 
                AgentState.ERROR, 
                AgentState.SHUTDOWN
            ],
            AgentState.SURVEY_MISSION_COMPLETED: [
                AgentState.ACTIVE, 
                AgentState.ERROR, 
                AgentState.SHUTDOWN
            ],
            AgentState.PAUSED: [AgentState.ACTIVE, AgentState.ERROR, AgentState.SHUTDOWN],
            AgentState.ERROR: [AgentState.RESET, AgentState.SHUTDOWN],
            AgentState.RESET: [AgentState.ACTIVE, AgentState.ERROR, AgentState.SHUTDOWN],
        }
        
        if from_state in valid_transitions:
            return to_state in valid_transitions[from_state]
        return False
    
    def record_state_transition(self, agent_id: str, from_state: str, to_state: str, 
                              reason: str, metadata: Dict[str, Any] = None) -> bool:
        """Record a state transition."""
        if not self.validate_state_transition(agent_id, from_state, to_state):
            logger.warning(f"Invalid state transition: {agent_id} {from_state} -> {to_state}")
            return False
        
        transition = FSMTransition(
            agent_id=agent_id,
            from_state=from_state,
            to_state=to_state,
            timestamp=datetime.now().isoformat(),
            reason=reason,
            metadata=metadata or {}
        )
        
        self.transition_log.append(transition)
        self.state_cache[agent_id] = to_state
        
        # Log transition
        logger.info(f"FSM Transition: {agent_id} {from_state} -> {to_state} ({reason})")
        
        return True
    
    def get_agent_status_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive agent status including FSM state."""
        current_state = self.get_agent_fsm_state(agent_id)
        
        return {
            "agent_id": agent_id,
            "fsm_state": current_state,
            "last_transition": self._get_last_transition(agent_id),
            "state_history": self._get_state_history(agent_id),
            "is_valid_state": current_state in [state.value for state in AgentState],
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_last_transition(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get last transition for agent."""
        agent_transitions = [t for t in self.transition_log if t.agent_id == agent_id]
        if agent_transitions:
            last = agent_transitions[-1]
            return {
                "from_state": last.from_state,
                "to_state": last.to_state,
                "timestamp": last.timestamp,
                "reason": last.reason
            }
        return None
    
    def _get_state_history(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get state history for agent."""
        agent_transitions = [t for t in self.transition_log if t.agent_id == agent_id]
        return [
            {
                "from_state": t.from_state,
                "to_state": t.to_state,
                "timestamp": t.timestamp,
                "reason": t.reason
            }
            for t in agent_transitions
        ]
    
    def generate_fsm_status_message(self, agent_id: str) -> str:
        """Generate FSM status message for agent."""
        status = self.get_agent_status_summary(agent_id)
        
        message = f"""🤖 FSM STATUS REPORT - {agent_id}

**Current State:** {status['fsm_state']}
**State Valid:** {'✅' if status['is_valid_state'] else '❌'}
**Last Updated:** {status['timestamp']}

**State History:**"""
        
        if status['state_history']:
            for transition in status['state_history'][-3:]:  # Last 3 transitions
                message += f"\n• {transition['from_state']} → {transition['to_state']} ({transition['reason']})"
        else:
            message += "\n• No transitions recorded"
        
        return message


def create_fsm_enhanced_message(agent_id: str, base_message: str, 
                              fsm_integration: FSMMessagingIntegration) -> str:
    """Create FSM-enhanced message with state information."""
    fsm_status = fsm_integration.generate_fsm_status_message(agent_id)
    
    return f"""{base_message}

---
🤖 FSM STATE INFORMATION
{fsm_status}

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"""






