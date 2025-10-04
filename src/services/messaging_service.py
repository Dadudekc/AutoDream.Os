#!/usr/bin/env python3
"""
Consolidated Messaging Service - SSOT for All Messaging
=======================================================

Single Source of Truth messaging service that consolidates all messaging functionality.
Refactored into modular components for V2 compliance.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""
from src.services.messaging_cli import ConsolidatedMessagingCLI

# Import all components from refactored modules
from src.services.messaging_service_core import (
    ENHANCED_VALIDATION_AVAILABLE,
    AgentCoordinatesLoader,
    AgentStatusChecker,
    ConsolidatedMessagingServiceCore,
    CoordinationRequest,
    MessageProtocolChecker,
    ScreenshotManager,
    ScreenshotTrigger,
)
from src.services.messaging_service_main import ConsolidatedMessagingService
from src.services.messaging_service_utils import (
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
    "ScreenshotManager",
    "ScreenshotTrigger",
    "ENHANCED_VALIDATION_AVAILABLE",
    "create_message_formatter",
    "create_message_validator",
    "create_message_sender",
    "create_agent_onboarder",
    "ConsolidatedMessagingCLI",
]

if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(level=logging.INFO)
    cli = ConsolidatedMessagingCLI()
    sys.exit(cli.main())
