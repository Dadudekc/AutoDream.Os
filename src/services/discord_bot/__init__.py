"""
Discord Bot Components
======================

Modular Discord bot components for V2 compliance.
"""

from .core.discord_bot import EnhancedDiscordAgentBot
from .commands.basic_commands import setup_basic_commands
from .commands.agent_commands import setup_agent_commands
from .commands.devlog_commands import setup_devlog_commands
from .commands.messaging_commands import setup_messaging_commands
from .commands.system_commands import setup_system_commands

__all__ = [
    'EnhancedDiscordAgentBot',
    'setup_basic_commands',
    'setup_agent_commands', 
    'setup_devlog_commands',
    'setup_messaging_commands',
    'setup_system_commands'
]

