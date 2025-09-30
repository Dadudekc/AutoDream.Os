#!/usr/bin/env python3
"""
Consolidated Messaging Service - SSOT for All Messaging
=======================================================

Single Source of Truth messaging service that consolidates all messaging functionality.
Refactored into modular components for V2 compliance.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

# Import all components from refactored modules
from src.services.consolidated_messaging_service_core import (
    ENHANCED_VALIDATION_AVAILABLE,
    AgentCoordinatesLoader,
    AgentStatusChecker,
    ConsolidatedMessagingServiceCore,
    CoordinationRequest,
    MessageProtocolChecker,
)
from src.services.consolidated_messaging_service_main import (
    ConsolidatedMessagingService,
    build_parser,
    main,
)
from src.services.consolidated_messaging_service_utils import (
    AgentOnboarder,
    MessageFormatter,
    MessageSender,
    MessageValidator,
    create_agent_onboarder,
    create_message_formatter,
    create_message_sender,
    create_message_validator,
)

# Re-export main components for backward compatibility
__all__ = [
    "ConsolidatedMessagingService",
    "ConsolidatedMessagingServiceCore",
    "MessageFormatter",
    "MessageValidator",
    "MessageSender",
    "AgentOnboarder",
    "CoordinationRequest",
    "MessageProtocolChecker",
    "AgentCoordinatesLoader",
    "AgentStatusChecker",
    "ENHANCED_VALIDATION_AVAILABLE",
    "create_message_formatter",
    "create_message_validator",
    "create_message_sender",
    "create_agent_onboarder",
    "build_parser",
    "main",
]

if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
