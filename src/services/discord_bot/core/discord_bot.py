#!/usr/bin/env python3
"""
Enhanced Discord Agent Bot Core
===============================

Core Discord bot implementation for the Discord Commander system.
Provides enhanced functionality for agent coordination and communication.

V2 Compliance: ≤400 lines, 3 classes, 8 functions
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Dict, Any, Optional, List
import logging
import asyncio
import sys
from datetime import datetime
from pathlib import Path

<<<<<<< HEAD
# Import logging system
from src.services.discord_bot.core.command_logger import command_logger
from src.services.discord_bot.core.command_wrapper import safe_command
from src.services.discord_bot.core.logging_config import setup_discord_logging

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
=======
# Add project root to path for messaging service
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
>>>>>>> origin/develop

logger = logging.getLogger(__name__)


class EnhancedDiscordAgentBot(commands.Bot):
    """
    Enhanced Discord Bot for Agent Coordination and Communication.

    This bot provides:
    - Agent-to-agent messaging through Discord
    - Swarm coordination capabilities
    - Task assignment and status tracking
    - Integration with the agent messaging system
    """

    def __init__(self, command_prefix: str = "!", intents: discord.Intents = None):
        """Initialize the enhanced Discord agent bot."""
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
<<<<<<< HEAD
            intents.members = False
        super().__init__(command_prefix=command_prefix, intents=intents)
        
        # Setup logging system
        setup_discord_logging()
        self.agent_coordinates = self._load_agent_coordinates()
        self.devlog_service = DiscordDevlogService()
        
        # Initialize messaging service with proper error handling
        try:
            self.messaging_service = ConsolidatedMessagingService("config/coordinates.json")
        except Exception as e:
            logger.error(f"Failed to initialize messaging service: {e}")
            self.messaging_service = None
        
        # Initialize advanced systems with proper error handling
        try:
            self.command_router = CommandRouter(self)
            self.agent_communication = AgentCommunicationEngine(self, self.messaging_service)
            self.security_manager = SecurityManager(self)
            self.ui_embeds = UIEmbedManager()
        except Exception as e:
            logger.error(f"Failed to initialize advanced systems: {e}")
            self.command_router = None
            self.agent_communication = None
            self.security_manager = None
            self.ui_embeds = None
        
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
        from src.services.discord_bot.commands.admin_commands import setup_admin_commands
        from src.services.discord_bot.commands.send_controller import setup_send_controller
        
        # Setup consolidated commands for vibe coders
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
        setup_admin_commands(self)
        setup_send_controller(self)
        
        logger.info("[SUCCESS] All slash commands registered in setup_hook")

    async def _initialize_architecture(self):
        """Initialize architecture foundation integration."""
        try:
            logger.info("[INIT] Initializing architecture foundation integration...")
            
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
            logger.info("[SUCCESS] Architecture foundation integration complete")
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize architecture foundation: {e}")
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
            
            logger.info("[SUCCESS] Design patterns initialized for Discord system")
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize design patterns: {e}")
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
            
            logger.info("[SUCCESS] System integrations initialized for Discord system")
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize system integrations: {e}")
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
            
            logger.info("[SUCCESS] Domain entities initialized for Discord system")
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize domain entities: {e}")
            raise
=======
            intents.members = True
            intents.guilds = True

        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            help_command=None
        )

        # Bot state
        self.agent_id = "Discord-Commander"
        self.is_ready = False
        self.connected_agents = set()
        self.swarm_status = {}
        self.config = {}  # Bot configuration

        # Messaging integration
        self.messaging_provider = None
        self.command_handler = None

        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.EnhancedDiscordAgentBot")

        # Register event handlers
        self.setup_events()

        # Setup slash commands
        self.setup_slash_commands()

    def setup_slash_commands(self):
        """Setup Discord slash commands."""

        @app_commands.command(name="agent_status", description="Get status of a specific agent")
        async def agent_status(interaction: discord.Interaction, agent_id: str):
            """Get status of a specific agent."""
            try:
                # Get agent status from messaging service
                from src.services.consolidated_messaging_service import ConsolidatedMessagingService
                messaging_service = ConsolidatedMessagingService()

                # Check if agent is active
                is_active = agent_id in messaging_service.agent_data and messaging_service.agent_data[agent_id].get("active", True)

                embed = discord.Embed(
                    title=f"🐝 Agent {agent_id} Status",
                    color=0x00ff00 if is_active else 0xff0000,
                    timestamp=datetime.utcnow()
                )

                embed.add_field(name="Status", value="✅ Active" if is_active else "❌ Inactive", inline=True)
                embed.add_field(name="Agent ID", value=agent_id, inline=True)
                embed.set_footer(text="WE ARE SWARM - Discord Commander")

                await interaction.response.send_message(embed=embed)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to get agent status: {str(e)}",
                    color=0xff0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
>>>>>>> origin/develop

        @app_commands.command(name="message_agent", description="Send a message to a specific agent")
        async def message_agent(interaction: discord.Interaction, agent_id: str, message: str):
            """Send a message to a specific agent."""
            try:
                # Send message via consolidated messaging service
                success = await self.send_agent_message(agent_id, message)

<<<<<<< HEAD
            with open(coordinates_path) as f:
                data = json.load(f)
                return data.get("agents", {})
        except Exception as e:
            logger.info(f"[WARNING] Failed to load coordinates: {e}. Using defaults.")
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
        logger.info(f"[SUCCESS] {self.user} is online and ready!")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"[SUCCESS] Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"[ERROR] Failed to sync slash commands: {e}")
        
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
                logger.warning("[WARNING] DISCORD_CHANNEL_ID not set, skipping startup notification")
                return

            channel = self.get_channel(int(channel_id))
            if not channel:
                logger.warning(f"[WARNING] Channel {channel_id} not found")
                return

            startup_message = f"""🚀 **SWARM COMMANDER ONLINE** 🚀

**We're online and ready to command the swarm!** 🐝

**Commander Status:**
- **Name**: {self.user.name} | **ID**: {self.user.id} | **Latency**: {round(self.latency * 1000)}ms
- **Guilds**: {len(self.guilds)} | **Agents**: {len(self.agent_coordinates)} configured
- **Architecture**: ✅ V2_SWARM Foundation | **Patterns**: ✅ Active | **Integrations**: ✅ Active

**Available Commands:** `/ping`, `/commands`, `/swarm-help`, `/status`, `/agents`, `/swarm`, `/devlog`, `/send`, `/agent-devlog`, `/test-devlog`, `/msg-status`, `/agent-channels`, `/info`

**Ready for swarm coordination!** 🐝 *Use `/commands` for complete list*"""
            
            await channel.send(startup_message)
            logger.info("[SUCCESS] Startup notification sent")

        except Exception as e:
            logger.error(f"[ERROR] Failed to send startup notification: {e}")
=======
                if success:
                    embed = discord.Embed(
                        title="✅ Message Sent",
                        description=f"Message sent to **{agent_id}**",
                        color=0x00ff00,
                        timestamp=datetime.utcnow()
                    )
                    embed.add_field(name="Message", value=message[:100] + "..." if len(message) > 100 else message, inline=False)
                    embed.set_footer(text="WE ARE SWARM - Discord Commander")
                else:
                    embed = discord.Embed(
                        title="❌ Message Failed",
                        description=f"Failed to send message to **{agent_id}**",
                        color=0xff0000
                    )

                await interaction.response.send_message(embed=embed)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to send message: {str(e)}",
                    color=0xff0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        @app_commands.command(name="swarm_status", description="Get current swarm status")
        async def swarm_status(interaction: discord.Interaction):
            """Get current swarm status."""
            try:
                status = self.get_swarm_status()

                embed = discord.Embed(
                    title="🐝 Swarm Status",
                    description="Current status of the agent swarm",
                    color=0x0099ff,
                    timestamp=datetime.utcnow()
                )

                for key, value in status.items():
                    embed.add_field(name=key.replace("_", " ").title(), value=str(value), inline=True)

                embed.set_footer(text="WE ARE SWARM - Discord Commander")
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to get swarm status: {str(e)}",
                    color=0xff0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        # Register commands with the bot
        self.tree.add_command(agent_status)
        self.tree.add_command(message_agent)
        self.tree.add_command(swarm_status)

        self.logger.info("✅ Slash commands registered")

    def setup_events(self):
        """Setup Discord bot event handlers."""
        # Event handlers are defined as methods below
        pass

    async def on_ready(self):
        """Called when bot is ready and connected."""
        self.is_ready = True
        self.logger.info(f"🤖 Discord Commander {self.user} is online!")

        # Update presence
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="🐝 WE ARE SWARM - Agent Coordination Active"
            )
        )

        # Sync slash commands after bot is ready
        try:
            synced = await self.tree.sync()
            self.logger.info(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            self.logger.warning(f"⚠️  Failed to sync slash commands: {e}")

    async def on_guild_join(self, guild):
        """Called when bot joins a guild."""
        self.logger.info(f"✅ Joined guild: {guild.name}")
        await self._broadcast_system_message(
            f"🤖 Discord Commander has joined {guild.name}",
            color=0x00ff00
        )

    async def on_guild_remove(self, guild):
        """Called when bot leaves a guild."""
        self.logger.info(f"❌ Left guild: {guild.name}")

    async def on_member_join(self, member):
        """Called when a member joins."""
        if not member.bot:
            self.logger.info(f"👋 Member joined: {member.display_name}")
>>>>>>> origin/develop

    async def on_message(self, message):
        """Handle incoming messages."""
        if message.author == self.user:
            return

        # Process commands
        await self.process_commands(message)

        # Handle mentions
        if self.user.mentioned_in(message):
            await self._handle_mention(message)

    async def _handle_mention(self, message):
        """Handle bot mentions."""
        try:
<<<<<<< HEAD
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
                    if not interaction.response.is_done():
                        await interaction.response.send_message(
                            "You are currently blocked from using commands.",
                            ephemeral=True
                        )
                    return
                
                # Check rate limits
                command_name = interaction.command.name if interaction.command else "unknown"
                if not await self.security_manager.check_rate_limit(
                    str(interaction.user.id), command_name, str(interaction.channel.id), interaction
                ):
                    if not interaction.response.is_done():
                        await interaction.response.send_message(
                            "Rate limit exceeded. Please wait before using commands again.",
                            ephemeral=True
                        )
                    return
                
                # Route command through command router
                if interaction.command:
                    await self.command_router.route_command(interaction, command_name)
        
        except Exception as e:
            logger.error(f"Error handling interaction: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "An error occurred while processing your request.",
                        ephemeral=True
                    )
            except:
                pass
=======
            # Simple response to mentions
            response = "🐝 **Discord Commander Active!**\n\n"
            response += f"**WE ARE SWARM** - Ready to coordinate agents!\n"
            response += f"Use `{self.command_prefix}help` to see available commands."

            await message.channel.send(response)

        except Exception as e:
            self.logger.error(f"Error handling mention: {e}")
            await message.channel.send("❌ Error processing mention")

    async def _broadcast_system_message(self, message: str, color: int = 0x0099ff):
        """Broadcast system message to all connected channels."""
        try:
            # Create embed
            embed = discord.Embed(
                title="🐝 Discord Commander System Message",
                description=message,
                color=color,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="WE ARE SWARM - Agent Coordination Active")

            # This would need to track channels to broadcast to
            # For now, just log the message
            self.logger.info(f"System Message: {message}")

        except Exception as e:
            self.logger.error(f"Error broadcasting system message: {e}")

    def get_swarm_status(self) -> Dict[str, Any]:
        """Get current swarm status."""
        return {
            "commander_status": "Active" if self.is_ready else "Offline",
            "connected_agents": len(self.connected_agents),
            "guild_count": len(self.guilds),
            "latency": round(self.latency * 1000) if self.latency and not str(self.latency).lower() == 'nan' else 0,
            "uptime": "Unknown",  # Would need to track startup time
            "last_activity": datetime.utcnow().isoformat()
        }

    async def send_agent_message(self, agent_id: str, message: str) -> bool:
        """Send message to specific agent via consolidated messaging service."""
        try:
            # Import and use consolidated messaging service
            from src.services.consolidated_messaging_service import ConsolidatedMessagingService

            messaging_service = ConsolidatedMessagingService()
            success = messaging_service.send_message(agent_id, message, "Discord-Commander")

            if success:
                self.logger.info(f"✅ Message sent to {agent_id} via Discord Commander")
                return True
            else:
                self.logger.error(f"❌ Failed to send message to {agent_id}")
                return False

        except Exception as e:
            self.logger.error(f"Error sending message to {agent_id}: {e}")
            return False

    async def broadcast_to_agents(self, message: str, agent_ids: List[str] = None) -> Dict[str, bool]:
        """Broadcast message to multiple agents."""
        try:
            results = {}

            if agent_ids is None:
                agent_ids = list(self.connected_agents)

            for agent_id in agent_ids:
                results[agent_id] = await self.send_agent_message(agent_id, message)

            return results

        except Exception as e:
            self.logger.error(f"Error broadcasting to agents: {e}")
            return {"error": str(e)}


class DiscordAgentInterface:
    """Interface for Discord agent communication."""

    def __init__(self, bot: EnhancedDiscordAgentBot):
        """Initialize Discord agent interface."""
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.DiscordAgentInterface")

    async def register_agent(self, agent_id: str, channel_id: str = None):
        """Register an agent with the Discord system."""
        try:
            self.bot.connected_agents.add(agent_id)
            self.logger.info(f"✅ Registered agent: {agent_id}")

            if channel_id:
                # Could set up agent-specific channel
                pass

        except Exception as e:
            self.logger.error(f"Error registering agent {agent_id}: {e}")

    async def unregister_agent(self, agent_id: str):
        """Unregister an agent from the Discord system."""
        try:
            self.bot.connected_agents.discard(agent_id)
            self.logger.info(f"❌ Unregistered agent: {agent_id}")

        except Exception as e:
            self.logger.error(f"Error unregistering agent {agent_id}: {e}")

    async def send_agent_notification(self, agent_id: str, notification: Dict[str, Any]):
        """Send notification to specific agent."""
        try:
            message = f"📨 **Notification for {agent_id}**\n\n"
            for key, value in notification.items():
                message += f"**{key}:** {value}\n"

            await self.bot.send_agent_message(agent_id, message)

        except Exception as e:
            self.logger.error(f"Error sending notification to {agent_id}: {e}")


class DiscordSwarmCoordinator:
    """Coordinates swarm activities through Discord."""

    def __init__(self, bot: EnhancedDiscordAgentBot):
        """Initialize Discord swarm coordinator."""
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.DiscordSwarmCoordinator")

    async def coordinate_task_assignment(self, task_data: Dict[str, Any]):
        """Coordinate task assignment through Discord."""
        try:
            # Broadcast task assignment to relevant agents
            message = "📋 **New Task Assignment**\n\n"
            message += f"**Task:** {task_data.get('title', 'Unknown')}\n"
            message += f"**Priority:** {task_data.get('priority', 'Normal')}\n"
            message += f"**Assigned to:** {', '.join(task_data.get('agents', []))}\n"

            if 'description' in task_data:
                message += f"\n**Description:** {task_data['description']}"

            await self.bot.broadcast_to_agents(message, task_data.get('agents'))

        except Exception as e:
            self.logger.error(f"Error coordinating task assignment: {e}")

    async def broadcast_swarm_status(self):
        """Broadcast current swarm status."""
        try:
            status = self.bot.get_swarm_status()
            message = "📊 **Swarm Status Update**\n\n"

            for key, value in status.items():
                message += f"**{key}:** {value}\n"

            await self.bot.broadcast_to_agents(message)

        except Exception as e:
            self.logger.error(f"Error broadcasting swarm status: {e}")


# Create bot instance
def create_discord_commander() -> EnhancedDiscordAgentBot:
    """Create and configure Discord Commander bot instance."""
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True

    bot = EnhancedDiscordAgentBot(command_prefix="!", intents=intents)

    # Add interfaces and coordinators
    bot.agent_interface = DiscordAgentInterface(bot)
    bot.swarm_coordinator = DiscordSwarmCoordinator(bot)

    return bot


if __name__ == "__main__":
    # Test the Discord Commander
    print("🐝 Discord Commander - Enhanced Discord Agent Bot")
    print("=" * 50)

    bot = create_discord_commander()
    print(f"✅ Discord Commander created: {bot.agent_id}")
    print(f"✅ Agent Interface: {bot.agent_interface}")
    print(f"✅ Swarm Coordinator: {bot.swarm_coordinator}")
    print(f"✅ Ready for deployment!")

    # Note: Bot will only run when provided with a valid Discord token
    print("\n⚠️  To run the bot, set DISCORD_BOT_TOKEN environment variable")
    print("⚠️  And use: asyncio.run(bot.start('your_token_here'))")
>>>>>>> origin/develop
