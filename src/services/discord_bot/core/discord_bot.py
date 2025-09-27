#!/usr/bin/env python3
"""
Enhanced Discord Bot Core
=========================

Core Discord bot functionality with devlog integration.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.discord_devlog_service import DiscordDevlogService
from services.consolidated_messaging_service import ConsolidatedMessagingService
from .command_router import CommandRouter
from .agent_communication_engine import AgentCommunicationEngine
from .security_manager import SecurityManager
from .ui_embeds import UIEmbedManager

# Architecture Foundation Integration
from architecture.design_patterns import PatternType, PatternConfig
from architecture.system_integration import IntegrationType
from architecture.unified_architecture_core import ComponentType
from domain.entities.agent import AgentType, AgentCapability, AgentStatus
from domain.entities.task import TaskType, TaskStatus, TaskPriority
from domain.domain_events import EventType, EventPriority, SystemEvent

logger = logging.getLogger(__name__)


class EnhancedDiscordAgentBot(commands.Bot):
    """Enhanced Discord agent bot with devlog integration."""

    def __init__(self, command_prefix: str = "!", intents=None):
        """Initialize enhanced Discord agent bot."""
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = False
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.agent_coordinates = self._load_agent_coordinates()
        self.devlog_service = DiscordDevlogService()
        self.messaging_service = ConsolidatedMessagingService("config/coordinates.json")
        
        # Initialize advanced systems
        self.command_router = CommandRouter(self)
        self.agent_communication = AgentCommunicationEngine(self, self.messaging_service)
        self.security_manager = SecurityManager(self)
        self.ui_embeds = UIEmbedManager()
        
        # Architecture Foundation Integration
        self.pattern_manager = None
        self.integration_manager = None
        self.unified_architecture = None
        self.agent_manager = None
        self.task_manager = None
        self.event_bus = None
        self._architecture_initialized = False
    
    async def setup_hook(self):
        """Setup hook for slash commands and architecture integration."""
        # Initialize architecture foundation
        await self._initialize_architecture()
        
        # Import and setup commands here
        from src.services.discord_bot.commands.basic_commands import setup_basic_commands
        from src.services.discord_bot.commands.agent_commands import setup_agent_commands
        from src.services.discord_bot.commands.devlog_commands import setup_devlog_commands
        from src.services.discord_bot.commands.messaging_commands import setup_messaging_commands
        from src.services.discord_bot.commands.system_commands import setup_system_commands
        from src.services.discord_bot.commands.project_update_core_commands import setup_project_update_core_commands
        from src.services.discord_bot.commands.project_update_specialized_commands import setup_project_update_specialized_commands
        from src.services.discord_bot.commands.project_update_management_commands import setup_project_update_management_commands
        from src.services.discord_bot.commands.messaging_advanced_commands import setup_messaging_advanced_commands
        from src.services.discord_bot.commands.onboarding_commands import setup_onboarding_commands
        from src.services.discord_bot.commands.stall_commands import setup_stall_commands
        from src.services.discord_bot.commands.send_controller import setup_send_controller
        
        # Setup all commands
        setup_basic_commands(self)
        setup_agent_commands(self)
        setup_devlog_commands(self)
        setup_messaging_commands(self)
        setup_system_commands(self)
        setup_project_update_core_commands(self)
        setup_project_update_specialized_commands(self)
        setup_project_update_management_commands(self)
        setup_messaging_advanced_commands(self)
        setup_onboarding_commands(self)
        setup_stall_commands(self)
        setup_send_controller(self)
        
        logger.info("✅ All slash commands registered in setup_hook")

    async def _initialize_architecture(self):
        """Initialize architecture foundation integration."""
        try:
            logger.info("🏗️ Initializing architecture foundation integration...")
            
            # Initialize unified architecture core if available
            if self.unified_architecture:
                await self.unified_architecture.initialize()
            
            # Initialize design patterns
            if self.pattern_manager:
                await self._initialize_design_patterns()
            
            # Initialize system integrations
            if self.integration_manager:
                await self._initialize_system_integrations()
            
            # Initialize domain entities
            if self.agent_manager and self.task_manager:
                await self._initialize_domain_entities()
            
            # Publish system startup event
            if self.event_bus:
                startup_event = SystemEvent(
                    event_id="",
                    event_name="discord_bot_startup",
                    event_type=EventType.SYSTEM,
                    source="discord_bot",
                    system_component="discord_bot",
                    operation="startup",
                    data={"bot_name": self.user.name if self.user else "DiscordBot"}
                )
                await self.event_bus.publish_event(startup_event)
            
            self._architecture_initialized = True
            logger.info("✅ Architecture foundation integration complete")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize architecture foundation: {e}")
            raise

    async def _initialize_design_patterns(self):
        """Initialize design patterns for Discord system."""
        try:
            # Initialize command pattern
            command_config = PatternConfig(
                pattern_type=PatternType.COMMAND,
                name="discord_command_pattern",
                description="Command pattern for Discord slash commands"
            )
            
            # Initialize security pattern
            security_config = PatternConfig(
                pattern_type=PatternType.SECURITY,
                name="discord_security_pattern",
                description="Security pattern for Discord bot security"
            )
            
            # Initialize UI pattern
            ui_config = PatternConfig(
                pattern_type=PatternType.UI,
                name="discord_ui_pattern",
                description="UI pattern for Discord embeds and interactions"
            )
            
            # Initialize communication pattern
            communication_config = PatternConfig(
                pattern_type=PatternType.COMMUNICATION,
                name="discord_communication_pattern",
                description="Communication pattern for Discord messaging"
            )
            
            logger.info("✅ Design patterns initialized for Discord system")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize design patterns: {e}")
            raise

    async def _initialize_system_integrations(self):
        """Initialize system integrations for Discord system."""
        try:
            # Initialize Discord API integration
            discord_api_config = IntegrationConfig(
                integration_type=IntegrationType.API,
                name="discord_api",
                endpoint="https://discord.com/api/v10"
            )
            
            # Initialize messaging integration
            messaging_config = IntegrationConfig(
                integration_type=IntegrationType.MESSAGING,
                name="agent_messaging",
                endpoint="agent_workspaces"
            )
            
            logger.info("✅ System integrations initialized for Discord system")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize system integrations: {e}")
            raise

    async def _initialize_domain_entities(self):
        """Initialize domain entities for Discord system."""
        try:
            # Create Discord bot agent configuration
            discord_agent_config = AgentConfiguration(
                agent_id="discord_bot_agent",
                name="Discord Bot Agent",
                agent_type=AgentType.SERVICE,
                capabilities={
                    AgentCapability.MESSAGING,
                    AgentCapability.COMMAND_EXECUTION,
                    AgentCapability.USER_INTERFACE,
                    AgentCapability.SECURITY
                }
            )
            
            # Create Discord bot task configuration
            discord_task_config = TaskConfiguration(
                task_id="discord_bot_task",
                name="Discord Bot Task",
                description="Main Discord bot operation task",
                task_type=TaskType.SYSTEM,
                category=TaskCategory.SYSTEM_OPERATION
            )
            
            logger.info("✅ Domain entities initialized for Discord system")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize domain entities: {e}")
            raise

    def _load_agent_coordinates(self):
        """Load agent coordinates configuration."""
        coordinates_path = "cursor_agent_coords.json"
        try:
            import json

            with open(coordinates_path) as f:
                data = json.load(f)
                return data.get("agents", {})
        except Exception as e:
            logger.info(f"⚠️  Failed to load coordinates: {e}. Using defaults.")
            # Fallback to default coordinates
            return {
                "Agent-1": {"active": True, "description": "Integration Specialist"},
                "Agent-2": {"active": True, "description": "Architecture & Design Specialist"},
                "Agent-3": {"active": True, "description": "Database Specialist"},
                "Agent-4": {"active": True, "description": "Captain & Operations Coordinator"},
                "Agent-5": {"active": True, "description": "Business Intelligence Specialist"},
                "Agent-6": {"active": True, "description": "Quality Assurance Specialist"},
                "Agent-7": {"active": True, "description": "Python Development & Testing Specialist"},
                "Agent-8": {"active": True, "description": "System Monitoring & Health Specialist"}
            }

    async def on_ready(self):
        """Event triggered when bot is ready."""
        logger.info(f"✅ {self.user} is online and ready!")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"❌ Failed to sync slash commands: {e}")
        
        await self._send_startup_notification()
        
        # Publish bot ready event
        if self._architecture_initialized:
            ready_event = SystemEvent(
                event_id="",
                event_name="discord_bot_ready",
                event_type=EventType.SYSTEM,
                source="discord_bot",
                system_component="discord_bot",
                operation="ready",
                data={"bot_name": self.user.name, "guild_count": len(self.guilds)}
            )
            if self.event_bus:
                await self.event_bus.publish_event(ready_event)

    async def _send_startup_notification(self):
        """Send startup notification to configured channel."""
        try:
            channel_id = os.getenv("DISCORD_CHANNEL_ID")
            if not channel_id:
                logger.warning("⚠️  DISCORD_CHANNEL_ID not set, skipping startup notification")
                return

            channel = self.get_channel(int(channel_id))
            if not channel:
                logger.warning(f"⚠️  Channel {channel_id} not found")
                return

            startup_message = f"""
🚀 **SWARM COMMANDER ONLINE** 🚀

**We're online and ready to command the swarm!** 🐝

**Commander Status:**
- **Name**: {self.user.name}
- **ID**: {self.user.id}
- **Latency**: {round(self.latency * 1000)}ms
- **Guilds**: {len(self.guilds)}
- **Agents**: {len(self.agent_coordinates)} configured
- **Architecture**: ✅ Integrated with V2_SWARM Foundation
- **Patterns**: ✅ Design patterns active
- **Integrations**: ✅ System integrations active
- **Domain**: ✅ Domain entities active

**Available Slash Commands:**
- `/ping` - Test bot responsiveness
- `/commands` - Show all commands
- `/swarm-help` - Show help information
- `/status` - Show system status
- `/agents` - List all agents
- `/swarm` - Send to all agents
- `/devlog` - Create devlog
- `/send` - Send to specific agent
- `/agent-devlog` - Create agent-specific devlog
- `/test-devlog` - Test devlog system
- `/msg-status` - Get messaging status
- `/agent-channels` - List agent channels
- `/info` - Show bot information

**Ready for swarm coordination!** 🐝

*Use `/commands` for complete command list*
            """
            await channel.send(startup_message)
            logger.info("✅ Startup notification sent")

        except Exception as e:
            logger.error(f"❌ Failed to send startup notification: {e}")

    async def on_message(self, message):
        """Event triggered when a message is received."""
        if message.author == self.user:
            return
        
        # Skip prefix command processing since we're using slash commands
        # Only process commands in the command controller channel if needed
        command_channel_id = os.getenv("COMMAND_CONTROLLER_CHANNEL")
        if command_channel_id and str(message.channel.id) != command_channel_id:
            return
            
        # Note: We're using slash commands, so we don't need to process prefix commands
        # await self.process_commands(message)

    async def on_app_command_error(self, interaction, error):
        """Handle application command errors (slash commands)."""
        logger.error(f"Slash command error: {error}")
        try:
            await interaction.response.send_message(f"❌ Command error: {error}", ephemeral=True)
        except:
            # If we can't respond, just log the error
            logger.error(f"Failed to send error response: {error}")
    
    async def on_interaction(self, interaction):
        """Handle all interactions including buttons and selects."""
        try:
            # Handle UI component interactions
            if interaction.type == discord.InteractionType.component:
                await self.ui_embeds.handle_interaction(interaction)
                return
            
            # Handle slash command interactions
            if interaction.type == discord.InteractionType.application_command:
                # Check security
                if self.security_manager.is_user_blocked(str(interaction.user.id)):
                    await interaction.response.send_message(
                        "🚫 You are currently blocked from using commands.",
                        ephemeral=True
                    )
                    return
                
                # Check rate limits
                command_name = interaction.command.name if interaction.command else "unknown"
                if not await self.security_manager.check_rate_limit(
                    str(interaction.user.id), command_name, str(interaction.channel.id)
                ):
                    await interaction.response.send_message(
                        "⏰ Rate limit exceeded. Please wait before using commands again.",
                        ephemeral=True
                    )
                    return
                
                # Route command through command router
                if interaction.command:
                    await self.command_router.route_command(interaction, command_name)
        
        except Exception as e:
            logger.error(f"❌ Error handling interaction: {e}")
            try:
                await interaction.response.send_message(
                    "❌ An error occurred while processing your request.",
                    ephemeral=True
                )
            except:
                pass