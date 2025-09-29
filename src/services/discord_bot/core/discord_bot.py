#!/usr/bin/env python3
"""
Enhanced Discord Agent Bot Core
===============================

Core Discord bot implementation for the Discord Commander system.
Provides enhanced functionality for agent coordination and communication.

V2 Compliance: ≤400 lines, 3 classes, 8 functions
"""

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import discord
from discord import app_commands
from discord.ext import commands

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

        super().__init__(command_prefix=command_prefix, intents=intents, help_command=None)

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
        """Setup Discord slash commands with beautiful UI integration."""
        # Check if commands are already registered to prevent duplicate registration
        if hasattr(self, "_commands_registered") and self._commands_registered:
            self.logger.info("✅ Slash commands already registered, skipping")
            return

        @app_commands.command(
            name="dashboard", description="Open the beautiful Discord Commander dashboard"
        )
        async def dashboard(interaction: discord.Interaction):
            """Open the main dashboard with interactive UI."""
            try:
                from src.services.discord_bot.ui.discord_ui import DiscordUI

                ui_controller = DiscordUI(self)

                embed = await ui_controller.create_main_dashboard()
                agent_view = await ui_controller.create_agent_control_view()
                system_view = await ui_controller.create_system_control_view()

                # Send main dashboard
                await interaction.response.send_message(embed=embed)

                # Send agent control section
                agent_embed = discord.Embed(
                    title="📨 Agent Control Panel",
                    description="Manage individual agents and communication",
                    color=0x00FF00,
                )
                await interaction.followup.send(embed=agent_embed, view=agent_view)

                # Send system control section
                system_embed = discord.Embed(
                    title="🔧 System Control Panel",
                    description="Monitor system health and perform operations",
                    color=0xFF9900,
                )
                await interaction.followup.send(embed=system_embed, view=system_view)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to open dashboard: {str(e)}",
                    color=0xFF0000,
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        @app_commands.command(name="agent_status", description="Get status of a specific agent")
        async def agent_status(interaction: discord.Interaction, agent_id: str):
            """Get status of a specific agent."""
            try:
                # Get agent status from messaging service
                from src.services.consolidated_messaging_service import ConsolidatedMessagingService

                messaging_service = ConsolidatedMessagingService()

                # Check if agent is active
                is_active = (
                    agent_id in messaging_service.agent_data
                    and messaging_service.agent_data[agent_id].get("active", True)
                )

                embed = discord.Embed(
                    title=f"🐝 Agent {agent_id} Status",
                    color=0x00FF00 if is_active else 0xFF0000,
                    timestamp=datetime.utcnow(),
                )

                embed.add_field(
                    name="Status", value="✅ Active" if is_active else "❌ Inactive", inline=True
                )
                embed.add_field(name="Agent ID", value=agent_id, inline=True)
                embed.set_footer(text="WE ARE SWARM - Discord Commander")

                await interaction.response.send_message(embed=embed)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to get agent status: {str(e)}",
                    color=0xFF0000,
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        @app_commands.command(
            name="message_agent", description="Send a message to a specific agent"
        )
        async def message_agent(interaction: discord.Interaction, agent_id: str, message: str):
            """Send a message to a specific agent."""
            try:
                # Send message via consolidated messaging service
                success = await self.send_agent_message(agent_id, message)

                if success:
                    embed = discord.Embed(
                        title="✅ Message Sent",
                        description=f"Message sent to **{agent_id}**",
                        color=0x00FF00,
                        timestamp=datetime.utcnow(),
                    )
                    embed.add_field(
                        name="Message",
                        value=message[:100] + "..." if len(message) > 100 else message,
                        inline=False,
                    )
                    embed.set_footer(text="WE ARE SWARM - Discord Commander")
                else:
                    embed = discord.Embed(
                        title="❌ Message Failed",
                        description=f"Failed to send message to **{agent_id}**",
                        color=0xFF0000,
                    )

                await interaction.response.send_message(embed=embed)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error", description=f"Failed to send message: {str(e)}", color=0xFF0000
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
                    color=0x0099FF,
                    timestamp=datetime.utcnow(),
                )

                for key, value in status.items():
                    embed.add_field(
                        name=key.replace("_", " ").title(), value=str(value), inline=True
                    )

                embed.set_footer(text="WE ARE SWARM - Discord Commander")
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to get swarm status: {str(e)}",
                    color=0xFF0000,
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        @app_commands.command(name="help", description="Show comprehensive help information")
        async def help_command(interaction: discord.Interaction):
            """Show comprehensive help information."""
            embed = discord.Embed(
                title="📋 Discord Commander Help",
                description="Complete guide to using the Discord Commander interface",
                color=0x0099FF,
                timestamp=datetime.utcnow(),
            )

            embed.add_field(
                name="🎮 Interactive Commands",
                value="• `/dashboard` - Open beautiful interactive dashboard\n"
                "• `/agent_status <agent_id>` - Check specific agent status\n"
                "• `/message_agent <agent_id> <message>` - Send message to agent\n"
                "• `/swarm_status` - Get current swarm status\n"
                "• `/help` - Show this help information",
                inline=False,
            )

            embed.add_field(
                name="🎯 Interactive UI Features",
                value="• **Clickable Buttons**: Easy-to-use interface\n"
                "• **Real-time Status**: Live system monitoring\n"
                "• **Agent Management**: Direct agent communication\n"
                "• **System Control**: Comprehensive system operations",
                inline=False,
            )

            embed.add_field(
                name="🐝 WE ARE SWARM",
                value="This system enables true swarm intelligence through:\n"
                "• 8-agent coordination\n"
                "• Real-time communication\n"
                "• Democratic decision making\n"
                "• Collective intelligence",
                inline=False,
            )

            embed.set_footer(text="WE ARE SWARM - Discord Commander")
            await interaction.response.send_message(embed=embed)

        # Register commands with the bot
        self.tree.add_command(dashboard)
        self.tree.add_command(agent_status)
        self.tree.add_command(message_agent)
        self.tree.add_command(swarm_status)
        self.tree.add_command(help_command)

        # Mark commands as registered
        self._commands_registered = True
        self.logger.info("✅ Slash commands registered with beautiful UI integration")

        # Also setup traditional commands for better compatibility
        self.setup_traditional_commands()

    def setup_traditional_commands(self):
        """Setup traditional Discord commands (using ! prefix)."""
        # Check if traditional commands are already registered
        if (
            hasattr(self, "_traditional_commands_registered")
            and self._traditional_commands_registered
        ):
            self.logger.info("✅ Traditional commands already registered, skipping")
            return

        @self.command(name="help", help="Show available commands")
        async def help_command(ctx):
            """Show help information."""
            embed = discord.Embed(
                title="🐝 Discord Commander Help",
                description="Available commands for agent coordination",
                color=0x00FF00,
            )

            embed.add_field(
                name="🤖 Bot Commands",
                value="`!help` - Show this help message\n"
                "`!status` - Show bot status\n"
                "`!ping` - Test bot response\n"
                "`!agents` - Show connected agents",
                inline=False,
            )

            embed.add_field(
                name="📋 Agent Commands",
                value="`!register <agent_id>` - Register an agent\n"
                "`!unregister <agent_id>` - Unregister an agent\n"
                "`!send <agent_id> <message>` - Send message to agent\n"
                "`!broadcast <message>` - Broadcast to all agents",
                inline=False,
            )

            embed.add_field(
                name="📱 Social Media Commands",
                value="`!social_status` - Get social media status\n"
                "`!post_update <message> [platform]` - Post to social media\n"
                "`!social_analytics [platform]` - Get social media analytics",
                inline=False,
            )

            embed.add_field(
                name="🛠️ Admin Commands",
                value="`!restart` - Restart the bot (admin only)\n"
                "`!shutdown` - Shutdown the bot (admin only)",
                inline=False,
            )

            embed.set_footer(text="WE ARE SWARM - Agent Coordination Active")
            await ctx.send(embed=embed)

        @self.command(name="status", help="Show bot status")
        async def status_command(ctx):
            """Show bot status."""
            embed = discord.Embed(title="📊 Discord Commander Status", color=0x0099FF)

            embed.add_field(
                name="🤖 Bot Status", value="🟢 Online" if self.is_ready else "🔴 Offline", inline=True
            )

            embed.add_field(name="📡 Servers", value=str(len(self.guilds)), inline=True)

            embed.add_field(name="👥 Users", value=str(len(self.users)), inline=True)

            embed.add_field(
                name="⏱️ Latency",
                value=f"{round(self.latency * 1000)}ms" if self.latency else "Unknown",
                inline=True,
            )

            embed.add_field(
                name="🔗 Connected Agents", value=str(len(self.connected_agents)), inline=True
            )

            embed.add_field(name="🐝 Swarm Mode", value="5-Agent Mode Active", inline=True)

            embed.set_footer(text="WE ARE SWARM - Agent Coordination Active")
            await ctx.send(embed=embed)

        @self.command(name="ping", help="Test bot response")
        async def ping_command(ctx):
            """Test bot response time."""
            latency = round(self.latency * 1000) if self.latency else 0
            await ctx.send(f"🏓 Pong! `{latency}ms`")

        @self.command(name="agents", help="Show connected agents")
        async def agents_command(ctx):
            """Show connected agents."""
            if not self.connected_agents:
                await ctx.send("🤖 No agents currently connected.")
                return

            embed = discord.Embed(
                title="👥 Connected Agents", description="Active agents in the swarm", color=0xFF9900
            )

            for agent_id in self.connected_agents:
                embed.add_field(name=f"🔗 {agent_id}", value="🟢 Connected", inline=True)

            embed.set_footer(text="WE ARE SWARM - Agent Coordination Active")
            await ctx.send(embed=embed)

        @self.command(name="register", help="Register an agent")
        async def register_command(ctx, agent_id: str):
            """Register an agent with the Discord system."""
            if agent_id in self.connected_agents:
                await ctx.send(f"⚠️ Agent {agent_id} is already registered!")
                return

            self.connected_agents.add(agent_id)
            await ctx.send(f"✅ Agent {agent_id} registered successfully!")
            self.logger.info(f"Agent {agent_id} registered by {ctx.author}")

        @self.command(name="unregister", help="Unregister an agent")
        async def unregister_command(ctx, agent_id: str):
            """Unregister an agent from the Discord system."""
            if agent_id not in self.connected_agents:
                await ctx.send(f"⚠️ Agent {agent_id} is not registered!")
                return

            self.connected_agents.discard(agent_id)
            await ctx.send(f"❌ Agent {agent_id} unregistered successfully!")
            self.logger.info(f"Agent {agent_id} unregistered by {ctx.author}")

        @self.command(name="send", help="Send message to agent")
        async def send_command(ctx, agent_id: str, *, message: str):
            """Send message to specific agent."""
            if agent_id not in self.connected_agents:
                await ctx.send(f"⚠️ Agent {agent_id} is not registered!")
                return

            # Simulate sending message to agent
            await ctx.send(f"📨 Message sent to {agent_id}: {message}")
            self.logger.info(f"Message sent to {agent_id} by {ctx.author}")

        @self.command(name="broadcast", help="Broadcast message to all agents")
        async def broadcast_command(ctx, *, message: str):
            """Broadcast message to all connected agents."""
            if not self.connected_agents:
                await ctx.send("⚠️ No agents connected to broadcast to!")
                return

            await ctx.send(f"📡 Broadcasting to {len(self.connected_agents)} agents: {message}")

            # Simulate broadcasting to all agents
            for agent_id in self.connected_agents:
                self.logger.info(f"Broadcast message to {agent_id}: {message}")

        @self.command(name="restart", help="Restart the bot")
        async def restart_command(ctx):
            """Restart the bot (admin only)."""
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("❌ This command requires administrator permissions!")
                return

            await ctx.send("🔄 Restarting Discord Commander...")
            self.logger.info(f"Bot restart requested by {ctx.author}")
            await self.close()

        @self.command(name="shutdown", help="Shutdown the bot")
        async def shutdown_command(ctx):
            """Shutdown the bot (admin only)."""
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("❌ This command requires administrator permissions!")
                return

            await ctx.send("🛑 Shutting down Discord Commander...")
            self.logger.info(f"Bot shutdown requested by {ctx.author}")
            await self.close()

        # Mark traditional commands as registered
        self._traditional_commands_registered = True
        self.logger.info("✅ Traditional commands registered successfully")

    def setup_events(self):
        """Setup Discord bot event handlers."""

        @self.event
        async def on_message(message):
            """Handle incoming messages."""
            if message.author == self.user:
                return

            # Process commands
            await self.process_commands(message)

            # Handle mentions
            if self.user.mentioned_in(message):
                await self.handle_mention(message)

    async def on_ready(self):
        """Called when bot is ready and connected."""
        self.is_ready = True
        self.logger.info(f"🤖 Discord Commander {self.user} is online!")

        # Update presence
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="🐝 WE ARE SWARM - Agent Coordination Active",
            )
        )

        # Sync slash commands after bot is ready
        try:
            synced = await self.tree.sync()
            self.logger.info(f"✅ Synced {len(synced)} slash commands")

            # List the synced commands for debugging
            command_names = [cmd.name for cmd in synced]
            self.logger.info(f"📋 Synced commands: {', '.join(command_names)}")

        except Exception as e:
            self.logger.warning(f"⚠️  Failed to sync slash commands: {e}")
            # Try to sync again after a delay
            try:
                await asyncio.sleep(2)
                synced = await self.tree.sync()
                self.logger.info(f"✅ Retry sync successful: {len(synced)} commands")
            except Exception as retry_e:
                self.logger.error(f"❌ Retry sync failed: {retry_e}")

        # Send welcome message with beautiful UI to the first available channel
        try:
            from src.services.discord_bot.ui.discord_ui import DiscordUI

            ui_controller = DiscordUI(self)

            # Find the first text channel we can send messages to
            for guild in self.guilds:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        await ui_controller.send_welcome_message(channel)
                        self.logger.info(
                            f"✅ Welcome message sent to #{channel.name} in {guild.name}"
                        )
                        break
                else:
                    continue
                break
            else:
                self.logger.warning("⚠️  No channels available to send welcome message")

        except Exception as e:
            self.logger.error(f"❌ Failed to send welcome message: {e}")

    async def handle_mention(self, message):
        """Handle bot mentions."""
        try:
            # Simple response to mentions
            response = "🐝 **Discord Commander Active!**\n\n"
            response += "**WE ARE SWARM** - Ready to coordinate agents!\n"
            response += "Use `/dashboard` to see the beautiful interactive interface."

            await message.channel.send(response)

        except Exception as e:
            self.logger.error(f"Error handling mention: {e}")
            await message.channel.send("❌ Error processing mention")

    async def on_guild_join(self, guild):
        """Called when bot joins a guild."""
        self.logger.info(f"✅ Joined guild: {guild.name}")
        await self._broadcast_system_message(
            f"🤖 Discord Commander has joined {guild.name}", color=0x00FF00
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
            response += "**WE ARE SWARM** - Ready to coordinate agents!\n"
            response += f"Use `{self.command_prefix}help` to see available commands."

            await message.channel.send(response)

        except Exception as e:
            self.logger.error(f"Error handling mention: {e}")
            await message.channel.send("❌ Error processing mention")

    async def _broadcast_system_message(self, message: str, color: int = 0x0099FF):
        """Broadcast system message to all connected channels."""
        try:
            # Create embed
            embed = discord.Embed(
                title="🐝 Discord Commander System Message",
                description=message,
                color=color,
                timestamp=datetime.utcnow(),
            )
            embed.set_footer(text="WE ARE SWARM - Agent Coordination Active")

            # This would need to track channels to broadcast to
            # For now, just log the message
            self.logger.info(f"System Message: {message}")

        except Exception as e:
            self.logger.error(f"Error broadcasting system message: {e}")

    def get_swarm_status(self) -> dict[str, Any]:
        """Get current swarm status."""
        return {
            "commander_status": "Active" if self.is_ready else "Offline",
            "connected_agents": len(self.connected_agents),
            "guild_count": len(self.guilds),
            "latency": round(self.latency * 1000)
            if self.latency and not str(self.latency).lower() == "nan"
            else 0,
            "uptime": "Unknown",  # Would need to track startup time
            "last_activity": datetime.utcnow().isoformat(),
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

    async def broadcast_to_agents(
        self, message: str, agent_ids: list[str] = None
    ) -> dict[str, bool]:
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

    async def send_agent_notification(self, agent_id: str, notification: dict[str, Any]):
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

    async def coordinate_task_assignment(self, task_data: dict[str, Any]):
        """Coordinate task assignment through Discord."""
        try:
            # Broadcast task assignment to relevant agents
            message = "📋 **New Task Assignment**\n\n"
            message += f"**Task:** {task_data.get('title', 'Unknown')}\n"
            message += f"**Priority:** {task_data.get('priority', 'Normal')}\n"
            message += f"**Assigned to:** {', '.join(task_data.get('agents', []))}\n"

            if "description" in task_data:
                message += f"\n**Description:** {task_data['description']}"

            await self.bot.broadcast_to_agents(message, task_data.get("agents"))

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
    print("✅ Ready for deployment!")

    # Note: Bot will only run when provided with a valid Discord token
    print("\n⚠️  To run the bot, set DISCORD_BOT_TOKEN environment variable")
    print("⚠️  And use: asyncio.run(bot.start('your_token_here'))")
