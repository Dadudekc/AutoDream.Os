"""
Discord Commander Bot
=====================

Main Discord bot implementation using modular components.
Refactored into modular components for V2 compliance.

Features:
- Rich Discord embeds for better user experience
- Comprehensive command system with error handling
- Real-time agent status monitoring
- Swarm coordination capabilities
- Interactive help system
"""

# DEPRECATED: Use bot_v2.py instead
# This file maintained for backward compatibility only

from .bot_main import (
    BotManager,
    DiscordCommanderBot,
    create_bot_configuration,
    create_discord_bot,
    run_bot,
)
from .bot_models import BotConfiguration, BotCore, CommandContext, EmbedBuilder
from .commands import CommandManager

# Re-export main classes for backward compatibility
__all__ = [
    "BotConfiguration",
    "BotCore",
    "BotStatus",
    "CommandContext",
    "EmbedBuilder",
    "CommandManager",
    "DiscordCommanderBot",
    "BotManager",
    "create_discord_bot",
    "create_bot_configuration",
    "run_bot",
]
