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

# Import all components from refactored modules
from .bot_core import (
    BotConfiguration,
    BotCore,
    BotStatus,
    CommandContext,
    EmbedBuilder
)
from .bot_commands import CommandManager
from .bot_main import (
    DiscordCommanderBot,
    BotManager,
    create_discord_bot,
    create_bot_configuration,
    run_bot
)

# Re-export main classes for backward compatibility
__all__ = [
    'BotConfiguration',
    'BotCore',
    'BotStatus',
    'CommandContext',
    'EmbedBuilder',
    'CommandManager',
    'DiscordCommanderBot',
    'BotManager',
    'create_discord_bot',
    'create_bot_configuration',
    'run_bot'
]