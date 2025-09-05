#!/usr/bin/env python3
"""
Discord Commander Package
=========================

Modular Discord commander system.
V2 COMPLIANT: Clean, focused, modular architecture.

@version 1.0.0 - V2 COMPLIANCE MODULAR PACKAGE
@license MIT
"""

# Import main orchestrator
from .discord_commander_orchestrator import (
    DiscordCommanderOrchestrator,
    create_discord_commander_orchestrator
)

# Import individual engines
from .configuration_manager import (
    DiscordConfigurationManager,
    create_discord_configuration_manager
)

from .command_handlers import (
    DiscordCommandHandlers,
    create_discord_command_handlers
)

from .agent_communication_engine import (
    AgentCommunicationEngine,
    create_agent_communication_engine
)

from .discord_integration_engine import (
    DiscordIntegrationEngine,
    create_discord_integration_engine
)

# Import models
from .discord_commander_models import (
    CommandStatus,
    AgentStatus,
    CommandResult,
    SwarmStatus,
    DiscordConfig,
    AgentMessage,
    DiscordEmbed,
    DiscordCommanderState,
    CommandHistory,
    ChannelConfig,
    create_command_result,
    create_swarm_status,
    create_discord_config,
    create_agent_message,
    create_discord_embed,
    create_command_history
)

# Export all public interfaces
__all__ = [
    # Main orchestrator
    'DiscordCommanderOrchestrator',
    'create_discord_commander_orchestrator',
    
    # Individual engines
    'DiscordConfigurationManager',
    'create_discord_configuration_manager',
    'DiscordCommandHandlers',
    'create_discord_command_handlers',
    'AgentCommunicationEngine',
    'create_agent_communication_engine',
    'DiscordIntegrationEngine',
    'create_discord_integration_engine',
    
    # Models
    'CommandStatus',
    'AgentStatus',
    'CommandResult',
    'SwarmStatus',
    'DiscordConfig',
    'AgentMessage',
    'DiscordEmbed',
    'DiscordCommanderState',
    'CommandHistory',
    'ChannelConfig',
    'create_command_result',
    'create_swarm_status',
    'create_discord_config',
    'create_agent_message',
    'create_discord_embed',
    'create_command_history'
]
