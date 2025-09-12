"""
Agent Communication Package - Core Messaging Infrastructure
=========================================================

This package provides the core agent communication infrastructure for V2_SWARM.
It consolidates agent-to-agent messaging, status tracking, and coordination operations.

Modules:
- agent_communication_engine_base: Base classes and utilities
- agent_communication_engine_core: Core messaging functionality
- agent_communication_engine_operations: High-level operations and orchestration

Author: Agent-4 (Captain - Discord Integration Coordinator)
License: MIT
"""

try:
    from .agent_communication_engine_base import AgentCommunicationEngineBase
    from .agent_communication_engine_core import AgentCommunicationEngineCore
    from .agent_communication_engine_operations import AgentCommunicationEngineOperations
except ImportError:
    # Fallback for direct execution
    from agent_communication_engine_base import AgentCommunicationEngineBase
    from agent_communication_engine_core import AgentCommunicationEngineCore
    from agent_communication_engine_operations import AgentCommunicationEngineOperations

__all__ = [
    "AgentCommunicationEngineBase",
    "AgentCommunicationEngineCore",
    "AgentCommunicationEngineOperations",
]
