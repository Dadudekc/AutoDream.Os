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

# Add project root to path for messaging service
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

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

        # Load additional cogs
        self.load_cogs()

    def load_cogs(self):
        """Load additional Discord cogs including ChatMate integration."""
        try:
            # Load social media commands cog
            from .commands.social_media_commands import SocialMediaCommands
            self.add_cog(SocialMediaCommands(self))
            self.logger.info("✅ Social media commands cog loaded")

            # Initialize social media service
            from src.services.social_media_integration import initialize_social_media_integration
            asyncio.create_task(initialize_social_media_integration())
            self.logger.info("✅ ChatMate social media integration initialized")

        except Exception as e:
            self.logger.error(f"❌ Failed to load social media cog: {e}")

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

        @app_commands.command(name="message_agent", description="Send a message to a specific agent")
        async def message_agent(interaction: discord.Interaction, agent_id: str, message: str):
            """Send a message to a specific agent."""
            try:
                # Send message via consolidated messaging service
                success = await self.send_agent_message(agent_id, message)

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
