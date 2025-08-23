"""
Inbox Manager - Compatibility Layer

This module now uses the V2 Comprehensive Messaging System through the compatibility layer
to maintain backward compatibility while eliminating duplication.

DEPRECATED: Use src.core.v2_comprehensive_messaging_system directly for new code.
"""

# Import from compatibility layer to maintain old interface
from .communication_compatibility_layer import (
    # Enums
    MessageType, MessagePriority, MessageStatus,
    # Classes
    InboxManager,
    # Dataclasses
    Message,
    # Functions
    create_message
)

# Re-export for backward compatibility
__all__ = [
    'MessageType', 'MessagePriority', 'MessageStatus',
    'InboxManager', 'Message', 'create_message'
]

# Deprecation warning
import warnings
warnings.warn(
    "inbox_manager.py is deprecated. Use v2_comprehensive_messaging_system directly.",
    DeprecationWarning,
    stacklevel=2
)
