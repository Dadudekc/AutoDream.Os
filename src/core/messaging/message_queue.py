"""
Message Queue - Compatibility Layer

This module now uses the V2 Comprehensive Messaging System through the compatibility layer
to maintain backward compatibility while eliminating duplication.

DEPRECATED: Use src.core.v2_comprehensive_messaging_system directly for new code.
"""

# Import from compatibility layer to maintain old interface
from ..communication_compatibility_layer import (
    # Enums
    MessageType, MessagePriority, MessageStatus,
    # Dataclasses
    Message
)

# Re-export for backward compatibility
__all__ = [
    'MessageType', 'MessagePriority', 'MessageStatus', 'Message'
]

# Deprecation warning
import warnings
warnings.warn(
    "message_queue.py is deprecated. Use v2_comprehensive_messaging_system directly.",
    DeprecationWarning,
    stacklevel=2
)
