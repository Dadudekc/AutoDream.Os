"""
Discord Bot Components
======================

Modular Discord bot components for V2 compliance.
"""

from .core.discord_bot import EnhancedDiscordAgentBot
from .commands.basic_commands import setup_basic_commands

__all__ = [
    'EnhancedDiscordAgentBot',
    'setup_basic_commands'
]

