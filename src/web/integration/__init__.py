"""
This package provides the infrastructure for cross-agent communication,
coordination, and integration across all agent systems.
"""

# Core communication classes
from .cross_agent_protocol import (
    CrossAgentCommunicator,
    AgentMessage,
    AgentResponse,
    MessagePriority,
    PROTOCOL_VERSION,
    MESSAGE_TYPES,
    COMMAND_CATEGORIES,
)

from .authentication import AuthenticationManager
from .routing import MessageRouter, MessageValidator
from .handshake import HandshakeNegotiator

__all__ = [
    "CrossAgentCommunicator",
    "AgentMessage",
    "AgentResponse",
    "MessagePriority",
    "AuthenticationManager",
    "MessageRouter",
    "MessageValidator",
    "HandshakeNegotiator",
    "PROTOCOL_VERSION",
    "MESSAGE_TYPES",
    "COMMAND_CATEGORIES",
]
