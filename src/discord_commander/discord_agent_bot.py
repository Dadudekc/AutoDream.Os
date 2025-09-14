#!/usr/bin/env python3
"""
Discord Agent Bot - V2 Compliant Refactored Module
==================================================

Refactored Discord Agent Bot for V2_SWARM with modular architecture.
V2 COMPLIANT: Main bot coordinator under 200 lines.

Features:
- Modular component integration
- Command processing delegation
- Security policy enforcement
- Rate limiting integration

Author: Agent-3 (Quality Assurance Co-Captain) - V2 Refactoring
License: MIT
"""

# Import the refactored Discord Agent Bot
from .discord_agent_bot_refactored import (
    DiscordAgentBotRefactored as DiscordAgentBot,
    DiscordAgentBotManager,
    get_discord_bot_manager,
    start_discord_agent_bot,
    test_discord_bot_connection
)

# Re-export all public interfaces for backward compatibility
__all__ = [
    "DiscordAgentBot",
    "DiscordAgentBotManager", 
    "get_discord_bot_manager",
    "start_discord_agent_bot",
    "test_discord_bot_connection"
]