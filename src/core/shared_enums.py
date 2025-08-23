"""
Shared Enums - Compatibility Layer

This module now uses the V2 Comprehensive Messaging System through the compatibility layer
to maintain backward compatibility while eliminating duplication.

DEPRECATED: Use src.core.v2_comprehensive_messaging_system directly for new code.
"""

# Import from compatibility layer to maintain old interface
from .communication_compatibility_layer import (
    # Enums
    MessageType, MessagePriority, MessageStatus, AgentStatus, AgentCapability
)

# Re-export for backward compatibility
__all__ = [
    'MessageType', 'MessagePriority', 'MessageStatus', 'AgentStatus', 'AgentCapability'
]

# Deprecation warning
import warnings
warnings.warn(
    "shared_enums.py is deprecated. Use v2_comprehensive_messaging_system directly.",
    DeprecationWarning,
    stacklevel=2
)
