#!/usr/bin/env python3
"""
Command Handlers Refactored - V2 Compliance Module
==================================================

Main refactored entry point for Discord command handlers.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

from .command_handlers_core import DiscordCommandHandlersCore
from .command_handlers_operations import DiscordCommandHandlersOperations


class DiscordCommandHandlers(
    DiscordCommandHandlersCore, DiscordCommandHandlersOperations
):
    """Unified Discord command handlers with core and operations functionality."""

    def __init__(self, swarm_status: SwarmStatus):
        """Initialize unified Discord command handlers."""
        DiscordCommandHandlersCore.__init__(self, swarm_status)
        DiscordCommandHandlersOperations.__init__(self, swarm_status)
