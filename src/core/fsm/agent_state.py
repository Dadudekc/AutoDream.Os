"""
Agent state enumeration for the integrated onboarding coordination system.

This module provides the AgentState enum that defines all possible states
for agents in the FSM (Finite State Machine) system.
"""

from enum import Enum


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