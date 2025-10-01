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

__all__ = ['AgentControlCommands', 'AgentCommands', 'CommandManager', 'SwarmCommands']

