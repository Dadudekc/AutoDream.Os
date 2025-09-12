# Discord Commander V2 - Complete Integration
# ===========================================

try:
    from .agent_communication_engine_base import AgentCommunicationEngineBase
    from .agent_communication_engine_core import AgentCommunicationEngineCore
    from .agent_communication_engine_operations import AgentCommunicationEngineOperations
    from .agent_communication_engine_refactored import (
        AgentCommunicationEngine,
        create_agent_communication_engine,
    )
    from .discord_commander import (
        DiscordCommander,
        get_discord_commander,
        start_discord_devlog_monitoring,
    )
    from .discord_commander_models import (
        AgentCommand,
        CommandResult,
        CommunicationStats,
        DiscordMessage,
        create_command_result,
    )
    from .discord_webhook_integration import DiscordWebhookIntegration
except ImportError:
    # Fallback for direct execution
    from agent_communication_engine_base import AgentCommunicationEngineBase
    from agent_communication_engine_core import AgentCommunicationEngineCore
    from agent_communication_engine_operations import AgentCommunicationEngineOperations
    from agent_communication_engine_refactored import (
        AgentCommunicationEngine,
        create_agent_communication_engine,
    )
    from discord_commander_models import (
        AgentCommand,
        CommandResult,
        CommunicationStats,
        DiscordMessage,
        create_command_result,
    )
    from discord_webhook_integration import DiscordWebhookIntegration

    from discord_commander import (
        DiscordCommander,
        get_discord_commander,
        start_discord_devlog_monitoring,
    )

__all__ = [
    # Base classes
    "AgentCommunicationEngineBase",
    # Core engines
    "AgentCommunicationEngineCore",
    "AgentCommunicationEngineOperations",
    "AgentCommunicationEngine",
    # Factory functions
    "create_agent_communication_engine",
    # Data models
    "CommandResult",
    "DiscordMessage",
    "AgentCommand",
    "CommunicationStats",
    # Factory functions for models
    "create_command_result",
    # Discord integration
    "DiscordWebhookIntegration",
    "DiscordCommander",
    # Global access functions
    "get_discord_commander",
    "start_discord_devlog_monitoring",
]
