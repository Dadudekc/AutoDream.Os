"""
Memory Integrations Module - V2_SWARM
=====================================

Integration points for memory leak prevention across services.

Author: Agent-7 (Web Development Expert)
License: MIT
"""

from .messaging_checks import (
    CoordinationRequestPurger,
    FileResourceGuard,
    MessageSizeValidator,
    MessagingInstrumentation,
    MessagingMemoryIntegration,
)

__all__ = [
    'FileResourceGuard',
    'MessageSizeValidator',
    'MessagingInstrumentation',
    'CoordinationRequestPurger',
    'MessagingMemoryIntegration',
]

