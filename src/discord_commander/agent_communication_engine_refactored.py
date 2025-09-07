#!/usr/bin/env python3
"""
Agent Communication Engine Refactored - V2 Compliance Module
============================================================

Main refactored entry point for agent communication engine.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

from .agent_communication_engine_core import AgentCommunicationEngineCore
from .agent_communication_engine_operations import AgentCommunicationEngineOperations


class AgentCommunicationEngine(
    AgentCommunicationEngineCore, AgentCommunicationEngineOperations
):
    """Unified agent communication engine with core and operations functionality."""

    def __init__(self) -> None:
        """Initialize unified agent communication engine."""
        super().__init__()


# Factory function for dependency injection
def create_agent_communication_engine() -> AgentCommunicationEngine:
    """Factory function to create agent communication engine"""
    return AgentCommunicationEngine()


# Export for DI
__all__ = ["AgentCommunicationEngine", "create_agent_communication_engine"]
