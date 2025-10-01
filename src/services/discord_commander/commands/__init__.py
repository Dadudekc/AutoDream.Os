"""
Discord Commander Commands Module
==================================

Slash commands for Discord bot agent control.

Author: Agent-7 (Web Development Expert)
License: MIT
"""

from .agent_control import AgentControlCommands

# Alias for backward compatibility
AgentCommands = AgentControlCommands

__all__ = ['AgentControlCommands', 'AgentCommands']

