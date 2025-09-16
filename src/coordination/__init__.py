#!/usr/bin/env python3
"""
Coordination Module
===================

Modularized coordination system for agent onboarding and management.
Replaces the original integrated_onboarding_coordination_system.py (966 lines)
with 4 V2-compliant modules (≤400 lines each).

Modules:
- onboarding_coordinator.py: Agent onboarding and contract management
- coordination_service.py: FSM and state management
- agent_instructions.py: Agent-specific instructions and prompts
- coordination_factory.py: System orchestration and factory pattern

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from .agent_instructions import AgentInstructions
from .coordination_factory import CoordinationFactory, IntegratedOnboardingCoordinationSystem
from .coordination_service import AgentFSM, CoordinationService
from .onboarding_coordinator import AgentContract, AgentState, ContractType, OnboardingCoordinator

__version__ = "2.0.0"
__author__ = "Agent-2 (Architecture & Design Specialist)"

__all__ = [
    # Enums
    "AgentState",
    "ContractType",
    # Core Classes
    "AgentContract",
    "AgentFSM",
    "OnboardingCoordinator",
    "CoordinationService",
    "AgentInstructions",
    "CoordinationFactory",
    "IntegratedOnboardingCoordinationSystem",
]
