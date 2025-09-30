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
    AgentCoordinatesLoader,
    AgentStatusChecker,
    ConsolidatedMessagingServiceCore,
    CoordinationRequest,
    ENHANCED_VALIDATION_AVAILABLE,
    MessageProtocolChecker,
)
from src.services.consolidated_messaging_service_utils import (
    AgentOnboarder,
    create_agent_onboarder,
    create_message_formatter,
    create_message_sender,
    create_message_validator,
    MessageFormatter,
    MessageSender,
    MessageValidator,
)
from src.services.consolidated_messaging_service_main import (
    build_parser,
    ConsolidatedMessagingService,
    main,
)

# Re-export main components for backward compatibility
__all__ = [
    'ConsolidatedMessagingService',
    'ConsolidatedMessagingServiceCore',
    'MessageFormatter',
    'MessageValidator',
    'MessageSender',
    'AgentOnboarder',
    'CoordinationRequest',
    'MessageProtocolChecker',
    'AgentCoordinatesLoader',
    'AgentStatusChecker',
    'ENHANCED_VALIDATION_AVAILABLE',
    'create_message_formatter',
    'create_message_validator',
    'create_message_sender',
    'create_agent_onboarder',
    'build_parser',
    'main',
]

if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
