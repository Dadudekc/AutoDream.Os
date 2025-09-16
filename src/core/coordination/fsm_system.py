#!/usr/bin/env python3
"""
FSM System - Finite State Machine for Agent State Management
===========================================================

Finite State Machine system for agent state management and workflow coordination.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Finite State Machine states for agents."""

    UNINITIALIZED = "uninitialized"
    ONBOARDING = "onboarding"
    IDLE = "idle"
    CONTRACT_NEGOTIATION = "contract_negotiation"
    TASK_EXECUTION = "task_execution"
    COLLABORATION = "collaboration"
    PROGRESS_REPORTING = "progress_reporting"
    CYCLE_COMPLETION = "cycle_completion"
    ERROR_RECOVERY = "error_recovery"


class AgentFSM:
    """Finite State Machine for agent state management."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.current_state = AgentState.UNINITIALIZED
        self.previous_state = None
        self.state_history = []
        self.transition_count = 0

    def transition_to(self, new_state: AgentState):
        """Transition to a new state."""
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self.state_history.append(
                {
                    "timestamp": datetime.now(),
                    "from": self.previous_state.value if self.previous_state else None,
                    "to": new_state.value,
                }
            )
            self.transition_count += 1
            logger.info(
                f"🔄 {self.agent_id} FSM: {self.previous_state.value if self.previous_state else 'None'} → {new_state.value}"
            )

    def get_state_info(self):
        """Get current state information."""
        return {
            "agent_id": self.agent_id,
            "current_state": self.current_state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "transition_count": self.transition_count,
            "state_history_count": len(self.state_history),
        }

