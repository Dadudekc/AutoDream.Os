"""
This package provides the infrastructure for cross-agent communication,
coordination, and integration across all agent systems.
"""

# Core communication classes - only import what exists
from .authentication import AuthenticationManager
from .handshake import HandshakeNegotiator
from .logging_utils import get_logger

__all__ = [
    "AuthenticationManager",
    "HandshakeNegotiator",
    "get_logger",
]
