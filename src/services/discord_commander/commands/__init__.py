"""
Discord Commander Commands Module
==================================

Slash commands for Discord bot agent control.

Author: Agent-7 (Web Development Expert)
License: MIT
"""

from .agent_control import AgentControlCommands

# Aliases for backward compatibility
AgentCommands = AgentControlCommands
CommandManager = AgentControlCommands
SwarmCommands = AgentControlCommands
SystemCommands = AgentControlCommands  # Add missing SystemCommands alias

__all__ = [
    "AgentControlCommands",
    "AgentCommands",
    "CommandManager",
    "SwarmCommands",
    "SystemCommands",
]
