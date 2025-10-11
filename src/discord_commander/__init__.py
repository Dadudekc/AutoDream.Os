# Discord Commander V2 - Consolidated Integration
# ================================================
# Consolidated from 9→4 files (Agent-3, C-003 Consolidation)

import sys
from pathlib import Path

# Ensure src is in path for imports
if str(Path(__file__).parent.parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    # Consolidated modules (V2 compliant)
    from src.discord_commander.discord_agent_communication import (
        AgentCommunicationEngine,
        create_agent_communication_engine,
    )
    from src.discord_commander.discord_models import (
        AgentCommand,
        CommandResult,
        CommunicationStats,
        DiscordMessage,
        create_command_result,
    )
    from src.discord_commander.discord_service import (
        DiscordService,
        get_discord_service,
        start_discord_devlog_monitoring,
    )
except ImportError:
    # Try relative imports
    try:
        from .discord_agent_communication import (
            AgentCommunicationEngine,
            create_agent_communication_engine,
        )
        from .discord_models import (
            AgentCommand,
            CommandResult,
            CommunicationStats,
            DiscordMessage,
            create_command_result,
        )
        from .discord_service import (
            DiscordService,
            get_discord_service,
            start_discord_devlog_monitoring,
        )
    except ImportError:
        # Last resort: direct imports
        from discord_agent_communication import (
            AgentCommunicationEngine,
            create_agent_communication_engine,
        )
        from discord_models import (
            AgentCommand,
            CommandResult,
            CommunicationStats,
            DiscordMessage,
            create_command_result,
        )
        from discord_service import (
            DiscordService,
            get_discord_service,
            start_discord_devlog_monitoring,
        )

__all__ = [
    # Agent Communication
    "AgentCommunicationEngine",
    "create_agent_communication_engine",
    # Data Models
    "CommandResult",
    "DiscordMessage",
    "AgentCommand",
    "CommunicationStats",
    "create_command_result",
    # Discord Service
    "DiscordService",
    "get_discord_service",
    "start_discord_devlog_monitoring",
]
