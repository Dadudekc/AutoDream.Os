#!/usr/bin/env python3
"""
Discord Commander Command Handlers - KISS Simplified
===================================================

Backward compatibility wrapper for Discord command handlers.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

# Import all components from refactored modules
from .command_handlers_refactored import *

# Re-export all components for backward compatibility
__all__ = ["DiscordCommandHandlers"]
