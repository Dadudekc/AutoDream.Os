"""
Discord Commander Commands Module
==================================

Slash commands for Discord bot agent control.

Author: Agent-7 (Web Development Expert)
License: MIT
"""

from .agent_control import AgentControlCommands

# Import the actual CommandManager from commands.py
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import DiscordCommandManager from the commands.py file directly
import sys
from pathlib import Path
commands_path = Path(__file__).parent.parent / "commands.py"
sys.path.insert(0, str(commands_path.parent))

try:
    from commands import DiscordCommandManager
    CommandManager = DiscordCommandManager
except ImportError:
    # Fallback to AgentControlCommands if DiscordCommandManager not available
    CommandManager = AgentControlCommands

# Aliases for backward compatibility
AgentCommands = AgentControlCommands
SwarmCommands = AgentControlCommands
SystemCommands = AgentControlCommands

__all__ = [
    "AgentControlCommands",
    "AgentCommands",
    "CommandManager",
    "SwarmCommands",
    "SystemCommands",
]
