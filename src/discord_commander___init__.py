#!/usr/bin/env python3
"""
Discord Commander Main Class - V2 Compliant Redirect
====================================================

V2 COMPLIANT: Modular architecture with clean separation of concerns.
Original monolithic implementation refactored into focused modules.

@version 2.0.0 - V2 COMPLIANCE MODULAR REFACTOR
@license MIT
"""

# Import the new modular orchestrator
from .discord_commander import (
    DiscordCommanderOrchestrator,
    create_discord_commander_orchestrator,
    CommandResult,
    SwarmStatus,
    DiscordConfig,
    AgentMessage,
    DiscordEmbed
)

# Re-export for backward compatibility
DiscordCommander = DiscordCommanderOrchestrator

# Export all public interfaces
__all__ = [
    'DiscordCommander',
    'DiscordCommanderOrchestrator',
    'create_discord_commander_orchestrator',
    'CommandResult',
    'SwarmStatus',
    'DiscordConfig',
    'AgentMessage',
    'DiscordEmbed'
]