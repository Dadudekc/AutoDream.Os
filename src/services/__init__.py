"""
Agent Cellphone V2 Services
===========================

Core services for the multi-agent swarm intelligence system.
This module provides access to all system services including the new ChatMate integration.

V2 Compliance: Modular design, comprehensive service architecture
"""

# Core services
from .consolidated_messaging_service import ConsolidatedMessagingService
from .discord_bot_integrated import IntegratedDiscordBotService
from .social_media_integration import get_social_media_service, initialize_social_media_integration

# Discord bot services
from .discord_bot import EnhancedDiscordAgentBot

# Analytics and monitoring
from .agent_devlog_automation import AgentDevlogAutomation
from .agent_devlog_posting import AgentDevlogPoster

# Quality assurance
from .test_discord_commander import DiscordCommanderTester

__all__ = [
    'ConsolidatedMessagingService',
    'IntegratedDiscordBotService',
    'get_social_media_service',
    'initialize_social_media_integration',
    'EnhancedDiscordAgentBot',
    'AgentDevlogAutomation',
    'AgentDevlogPoster',
    'DiscordCommanderTester'
]
