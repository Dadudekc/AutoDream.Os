#!/usr/bin/env python3
"""
FSM System - Finite State Machine for Agent States
=================================================

FSM system for managing agent state transitions.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from enum import Enum

logger = logging.getLogger(__name__)

class AgentState(Enum):
    """Agent state enumeration."""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"

class FSMTransition:
    """FSM transition definition."""
    
    def __init__(self, from_state: AgentState, to_state: AgentState, 
                 condition: str = None):
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert transition to dictionary."""
        return {
            "from_state": self.from_state.value,
            "to_state": self.to_state.value,
            "condition": self.condition,
            "timestamp": self.timestamp.isoformat()
        }

class AgentFSM:
    """Finite State Machine for agent state management."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.current_state = AgentState.IDLE
        self.previous_state = None
        self.transitions: List[FSMTransition] = []
        self.state_history: List[Dict] = []
        self._initialize_transitions()
    
    def _initialize_transitions(self) -> None:
        """Initialize valid state transitions."""
        self.valid_transitions = {
            AgentState.IDLE: {AgentState.WORKING, AgentState.ERROR},
            AgentState.WORKING: {AgentState.IDLE, AgentState.WAITING, AgentState.ERROR, AgentState.COMPLETED},
            AgentState.WAITING: {AgentState.WORKING, AgentState.IDLE, AgentState.ERROR},
            AgentState.ERROR: {AgentState.IDLE, AgentState.WORKING},
            AgentState.COMPLETED: {AgentState.IDLE, AgentState.WORKING}
        }
    
    def can_transition_to(self, target_state: AgentState) -> bool:
        """Check if transition to target state is valid."""
        return target_state in self.valid_transitions.get(self.current_state, set())
    
    def transition_to(self, target_state: AgentState, condition: str = None) -> bool:
        """Transition to target state if valid."""
        if not self.can_transition_to(target_state):
            logger.warning(f"Invalid transition from {self.current_state.value} to {target_state.value}")
            return False
        
        self.previous_state = self.current_state
        self.current_state = target_state
        
        transition = FSMTransition(self.previous_state, target_state, condition)
        self.transitions.append(transition)
        
        # Record state history
        self.state_history.append({
            "state": target_state.value,
            "timestamp": datetime.now().isoformat(),
            "condition": condition
        })
        
        logger.info(f"Agent {self.agent_id} transitioned from {self.previous_state.value} to {target_state.value}")
        return True
    
    def get_state_info(self) -> Dict:
        """Get current state information."""
        return {
            "agent_id": self.agent_id,
            "current_state": self.current_state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "transition_count": len(self.transitions),
            "last_transition": self.transitions[-1].to_dict() if self.transitions else None
        }
    
    def to_dict(self) -> Dict:
        """Convert FSM to dictionary."""
        return {
            "agent_id": self.agent_id,
            "current_state": self.current_state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "transitions": [t.to_dict() for t in self.transitions],
            "state_history": self.state_history
        }

class FSMManager:
    """Manager for agent FSMs."""
    
    def __init__(self, fsm_file: str = "agent_fsms.json"):
        self.fsm_file = Path(fsm_file)
        self.fsms: Dict[str, AgentFSM] = {}
        self._load_fsms()
    
    def _load_fsms(self) -> None:
        """Load FSMs from file."""
        try:
            if self.fsm_file.exists():
                with open(self.fsm_file, encoding="utf-8") as f:
                    data = json.load(f)
                    for fsm_data in data.get("fsms", []):
                        fsm = self._create_fsm_from_dict(fsm_data)
                        self.fsms[fsm.agent_id] = fsm
                logger.info(f"Loaded {len(self.fsms)} FSMs")
        except Exception as e:
            logger.error(f"Error loading FSMs: {e}")
    
    def _create_fsm_from_dict(self, data: Dict) -> AgentFSM:
        """Create FSM from dictionary."""
        fsm = AgentFSM(data["agent_id"])
        fsm.current_state = AgentState(data["current_state"])
        if data.get("previous_state"):
            fsm.previous_state = AgentState(data["previous_state"])
        fsm.state_history = data.get("state_history", [])
        return fsm
    
    def _save_fsms(self) -> None:
        """Save FSMs to file."""
        try:
            data = {
                "fsms": [fsm.to_dict() for fsm in self.fsms.values()],
                "last_updated": datetime.now().isoformat()
            }
            with open(self.fsm_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving FSMs: {e}")
    
    def get_or_create_fsm(self, agent_id: str) -> AgentFSM:
        """Get existing FSM or create new one."""
        if agent_id not in self.fsms:
            self.fsms[agent_id] = AgentFSM(agent_id)
            self._save_fsms()
        return self.fsms[agent_id]
    
    def transition_agent(self, agent_id: str, target_state: AgentState, 
                        condition: str = None) -> bool:
        """Transition agent to target state."""
        fsm = self.get_or_create_fsm(agent_id)
        success = fsm.transition_to(target_state, condition)
        if success:
            self._save_fsms()
        return success
    
    def get_agent_state(self, agent_id: str) -> Optional[AgentState]:
        """Get current state of agent."""
        fsm = self.fsms.get(agent_id)
        return fsm.current_state if fsm else None

