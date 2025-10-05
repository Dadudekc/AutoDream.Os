#!/usr/bin/env python3
"""
Thea Services Package - V3 Autonomous Agent Communication
=======================================================

Complete package for autonomous agent-to-Thea communication.
Removes human-in-the-loop and enables agents to coordinate with
external entity with aligned values.

Modules:
- agent_thea_automation: Core automation system
- agent_thea_coordinator: Agent coordination protocol
- agent_thea_interface: Simple agent interface
- thea_communication_interface: Legacy interface
- thea_communication_core: Core communication functionality
- thea_browser_manager: Browser automation
- thea_login_handler_refactored: Authentication handling
- thea_cookie_manager: Session management
- thea_login_detector: Login state detection

Usage:
    # Simple agent interface
    from src.services.thea import AgentTheaInterface

    thea = AgentTheaInterface("Agent-1")
    thea.start_communication()
    thea.send_status_update("Task completed")

    # Advanced coordination
    from src.services.thea import AgentTheaCoordinator

    coordinator = AgentTheaCoordinator()
    coordinator.start_coordination()
"""

# Note: Advanced agent modules not yet implemented
# from .agent_thea_automation import (
#     AgentTheaAutomation,
#     MessagePriority,
#     MessageStatus,
#     AgentMessage
# )

# from .agent_thea_coordinator import (
#     AgentTheaCoordinator,
#     TheaRecommendation
# )

# from .agent_thea_interface import (
#     AgentTheaInterface,
#     TheaResponse
# )

from .thea_browser_manager import TheaBrowserManager
from .thea_communication_core import TheaCommunicationCore

# Legacy components (V2 compliant)
from .thea_communication_interface import TheaCommunicationInterface
from .thea_cookie_manager import TheaCookieManager
from .thea_login_detector import TheaLoginDetector
from .thea_login_handler_refactored import TheaLoginHandler, create_thea_login_handler


# Convenience functions (using available components)
def create_cookie_manager():
    """Create cookie manager instance."""
    return TheaCookieManager()


def create_login_detector():
    """Create login detector instance."""
    return TheaLoginDetector()


def create_browser_manager():
    """Create browser manager instance."""
    return TheaBrowserManager()


__all__ = [
    # Available components
    "TheaCommunicationInterface",
    "TheaCommunicationCore",
    "TheaBrowserManager",
    "TheaCookieManager",
    "TheaLoginDetector",
    "TheaLoginHandler",
    "create_thea_login_handler",
    # Convenience functions
    "create_cookie_manager",
    "create_login_detector",
    "create_browser_manager",
]
