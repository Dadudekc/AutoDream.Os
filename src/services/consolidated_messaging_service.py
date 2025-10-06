#!/usr/bin/env python3
"""
🚨 DEPRECATED: Backward Compatibility Shim
==========================================

This module was consolidated during Pass-2 and is kept for backward compatibility only.
Use `src.services.messaging_service` instead.

This shim redirects all imports to the new canonical messaging service structure.

Author: Agent-4 (Captain) - BC Shim for Consolidation Pass-2
License: MIT
"""

import warnings

# Issue deprecation warning
warnings.warn(
    "Deprecated: import src.services.messaging_service instead of consolidated_messaging_service",
    DeprecationWarning,
    stacklevel=2,
)

# Import everything from the canonical messaging service
from src.services.messaging_service import (  # noqa: F401
    # Main service classes
    ConsolidatedMessagingService,
    ConsolidatedMessagingServiceCore,
    
    # Component classes
    MessageFormatter,
    MessageValidator,
    MessageSender,
    AgentOnboarder,
    
    # Data models
    CoordinationRequest,
    MessageProtocolChecker,
    AgentCoordinatesLoader,
    AgentStatusChecker,
    ScreenshotManager,
    ScreenshotTrigger,
    
    # Configuration
    ENHANCED_VALIDATION_AVAILABLE,
    
    # Factory functions
    create_message_formatter,
    create_message_validator,
    create_message_sender,
    create_agent_onboarder,
)

# Re-export everything for backward compatibility
__all__ = [
    # Main service classes
    "ConsolidatedMessagingService",
    "ConsolidatedMessagingServiceCore",
    
    # Component classes
    "MessageFormatter",
    "MessageValidator", 
    "MessageSender",
    "AgentOnboarder",
    
    # Data models
    "CoordinationRequest",
    "MessageProtocolChecker",
    "AgentCoordinatesLoader",
    "AgentStatusChecker",
    "ScreenshotManager",
    "ScreenshotTrigger",
    
    # Configuration
    "ENHANCED_VALIDATION_AVAILABLE",
    
    # Factory functions
    "create_message_formatter",
    "create_message_validator",
    "create_message_sender",
    "create_agent_onboarder",
]

