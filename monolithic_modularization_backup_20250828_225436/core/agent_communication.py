"""Compatibility wrapper for agent communication classes.

This module re-exports communication primitives so legacy imports
(`src.core.agent_communication`) continue to work.
"""

from .communication_compatibility_layer import (
    AgentCommunicationProtocol,
    MessageType,
    UnifiedMessagePriority,
    InboxManager,
)

__all__ = [
    "AgentCommunicationProtocol",
    "MessageType",
    "UnifiedMessagePriority",
    "InboxManager",
]
