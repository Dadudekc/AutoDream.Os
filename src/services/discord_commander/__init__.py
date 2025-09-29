"""
Discord Commander Package
========================

Modular Discord Commander with clean architecture and V2 compliance.
Clean separation of concerns with focused components.

Components:
- core: Core Discord functionality and configuration
- commands: Command handlers and management
- bot: Main bot implementation

Usage:
    from src.services.discord_commander import DiscordCommanderBot
    bot = DiscordCommanderBot()
    await bot.initialize()
"""

from .bot import DiscordCommanderBot
from .commands import AgentCommands, CommandManager, SwarmCommands, SystemCommands
from .core import (
    DiscordCommandRegistry,
    DiscordConfig,
    DiscordConnectionManager,
    DiscordEventManager,
    DiscordStatusMonitor,
)

__all__ = [
    "DiscordConfig",
    "DiscordConnectionManager",
    "DiscordCommandRegistry",
    "DiscordEventManager",
    "DiscordStatusMonitor",
    "AgentCommands",
    "SystemCommands",
    "SwarmCommands",
    "CommandManager",
    "DiscordCommanderBot",
]

__version__ = "2.0.0"
__author__ = "Agent-2 (Architecture & Design Specialist)"
__description__ = "V2 Compliant Discord Commander System"
