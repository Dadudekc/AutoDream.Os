#!/usr/bin/env python3
"""
Integrated Discord Bot Service - Fixed for 5-Agent Mode

This service provides a Discord bot integrated with the consolidated messaging service.
Fixed to work properly with 5-agent testing mode without architecture dependencies.

Author: Agent-2 (Discord System Migration - Fixed)
Date: 2025-01-19
Version: 3.0.0 (Fixed)
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import messaging service for integration
try:
    from services.messaging.core.messaging_service import MessagingService
except ImportError:
    # Fallback for direct execution
    from messaging.core.messaging_service import MessagingService

logger = logging.getLogger(__name__)


class IntegratedDiscordBotService:
    """Integrated Discord bot service with consolidated messaging."""

    def __init__(self):
        """Initialize Discord bot service."""
        self.bot = None
        self.messaging_service = None
        self.is_initialized = False
        self.logger = logging.getLogger(f"{__name__}.IntegratedDiscordBotService")

    async def initialize(self) -> bool:
        """Initialize the Discord bot service."""
        try:
            self.logger.info("🚀 Initializing Integrated Discord Bot Service...")

            # Initialize messaging service
            await self._initialize_messaging_service()

            # Initialize Discord bot
            await self._initialize_discord_bot()

            # Setup slash commands
            await self._setup_slash_commands()

            self.is_initialized = True
            self.logger.info("✅ Integrated Discord Bot Service initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Integrated Discord Bot Service: {e}")
            return False

    async def _initialize_messaging_service(self):
        """Initialize messaging service integration."""
        try:
            self.logger.info("🔗 Initializing messaging service integration...")
            self.messaging_service = MessagingService("config/coordinates.json")
            self.logger.info("✅ Messaging service integration complete")

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize messaging service: {e}")
            raise

    async def _initialize_discord_bot(self):
        """Initialize the Discord bot."""
        try:
            self.logger.info("🤖 Initializing Discord bot...")

            # Create bot instance with proper intents
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            intents.guilds = True

            self.bot = commands.Bot(command_prefix="!", intents=intents)

            # Setup event handlers
            await self._setup_event_handlers()

            # Setup messaging integration
            self.bot.messaging_service = self.messaging_service

            self.logger.info("✅ Discord bot initialized")

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Discord bot: {e}")
            raise

    async def _setup_event_handlers(self):
        """Setup Discord bot event handlers."""

        @self.bot.event
        async def on_ready():
            """Called when bot is ready and connected."""
            self.logger.info(f"🤖 Discord Commander is online as {self.bot.user}")

            # Update presence for 5-agent mode
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="🐝 5-Agent Mode - WE ARE SWARM"
                )
            )

        @self.bot.event
        async def on_message(message):
            """Handle incoming messages."""
            if message.author == self.bot.user:
                return

            # Process commands
            await self.bot.process_commands(message)

    async def _setup_slash_commands(self):
        """Setup Discord slash commands."""

        @self.bot.tree.command(name="swarm_status", description="Get current swarm status")
        async def swarm_status(interaction: discord.Interaction):
            """Get current swarm status."""
            try:
                embed = discord.Embed(
                    title="🐝 Swarm Status Report",
                    description="5-Agent Testing Mode Active",
                    color=0x00ff00,
                    timestamp=discord.utils.utcnow()
                )

                # Messaging service status
                messaging_status = "✅ Connected" if self.messaging_service else "❌ Disconnected"
                embed.add_field(name="Messaging Service", value=messaging_status, inline=True)

                # Discord bot status
                bot_status = "✅ Online" if self.bot.is_ready() else "❌ Offline"
                embed.add_field(name="Discord Bot", value=bot_status, inline=True)

                # 5-agent mode info
                embed.add_field(
                    name="Active Agents",
                    value="Agent-4, Agent-5, Agent-6, Agent-7, Agent-8",
                    inline=False
                )

                embed.set_footer(text="WE ARE SWARM - Discord Commander")
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                self.logger.error(f"Error getting swarm status: {e}")
                await interaction.response.send_message("❌ Error getting swarm status")

        @self.bot.tree.command(name="send_to_agent", description="Send message to specific agent")
        async def send_to_agent(interaction: discord.Interaction, agent: str, message: str):
            """Send message to specific agent."""
            try:
                if not self.messaging_service:
                    await interaction.response.send_message("❌ Messaging service not available")
                    return

                # Validate agent ID
                valid_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
                if agent not in valid_agents:
                    await interaction.response.send_message(
                        f"❌ Invalid agent. Valid agents: {', '.join(valid_agents)}"
                    )
                    return

                # Send message through messaging service
                success = self.messaging_service.send_message(
                    agent_id=agent,
                    message=f"[Discord] {message}",
                    from_agent=f"Discord-{interaction.user.name}"
                )

                if success:
                    embed = discord.Embed(
                        title="✅ Message Sent",
                        description=f"Sent to {agent}: {message}",
                        color=0x00ff00
                    )
                else:
                    embed = discord.Embed(
                        title="❌ Message Failed",
                        description=f"Could not send message to {agent}",
                        color=0xff0000
                    )

                embed.set_footer(text="WE ARE SWARM - Agent Communication")
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                self.logger.error(f"Error sending message: {e}")
                await interaction.response.send_message("❌ Error sending message")

        @self.bot.tree.command(name="broadcast", description="Broadcast message to all agents")
        async def broadcast(interaction: discord.Interaction, message: str):
            """Broadcast message to all agents."""
            try:
                if not self.messaging_service:
                    await interaction.response.send_message("❌ Messaging service not available")
                    return

                # Send to all 5 active agents
                agent_ids = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
                results = {}

                for agent_id in agent_ids:
                    results[agent_id] = self.messaging_service.send_message(
                        agent_id=agent_id,
                        message=f"[Discord Broadcast] {message}",
                        from_agent=f"Discord-{interaction.user.name}"
                    )

                successful = sum(1 for result in results.values() if result)
                total = len(results)

                embed = discord.Embed(
                    title="📡 Broadcast Results",
                    description=f"Message: {message}",
                    color=0x0099ff
                )

                embed.add_field(
                    name="Successful",
                    value=f"{successful}/{total}",
                    inline=True
                )

                embed.add_field(
                    name="Failed",
                    value=f"{total - successful}/{total}",
                    inline=True
                )

                embed.set_footer(text="WE ARE SWARM - Swarm Communication")
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                self.logger.error(f"Error broadcasting message: {e}")
                await interaction.response.send_message("❌ Error broadcasting message")

        @self.bot.tree.command(name="agent_list", description="List all available agents")
        async def agent_list(interaction: discord.Interaction):
            """List all available agents."""
            try:
                agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

                embed = discord.Embed(
                    title="🤖 Available Agents",
                    description=f"**5-Agent Testing Mode Active**\nTotal: {len(agents)} agents",
                    color=0x0099ff
                )

                for i, agent in enumerate(agents, 1):
                    embed.add_field(
                        name=f"Agent {i}",
                        value=agent,
                        inline=True
                    )

                embed.set_footer(text="WE ARE SWARM - Agent Network")
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                self.logger.error(f"Error listing agents: {e}")
                await interaction.response.send_message("❌ Error listing agents")

        @self.bot.tree.command(name="system_check", description="Check system integration status")
        async def system_check(interaction: discord.Interaction):
            """Check system integration status."""
            try:
                embed = discord.Embed(
                    title="🔧 System Integration Check",
                    description="Discord Commander System Status",
                    color=0x0099ff,
                    timestamp=discord.utils.utcnow()
                )

                # Bot status
                embed.add_field(
                    name="Discord Bot",
                    value="✅ Online" if self.bot.is_ready() else "❌ Offline",
                    inline=True
                )

                # Messaging service status
                messaging_status = "✅ Connected" if self.messaging_service else "❌ Disconnected"
                embed.add_field(
                    name="Messaging Service",
                    value=messaging_status,
                    inline=True
                )

                # 5-agent mode info
                embed.add_field(
                    name="Agent Mode",
                    value="5-Agent Testing Mode",
                    inline=False
                )

                embed.set_footer(text="WE ARE SWARM - System Check Complete")
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                self.logger.error(f"Error checking system: {e}")
                await interaction.response.send_message("❌ Error checking system")
    
    async def _initialize_discord_bot(self):
        """Initialize the Discord bot."""
        try:
            self.logger.info("🤖 Initializing Discord bot...")

            # Create bot instance
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            intents.guilds = True

            self.bot = commands.Bot(command_prefix="!", intents=intents)

            # No architecture dependencies needed for basic functionality

            # Setup messaging integration
            self.bot.messaging_service = self.messaging_service
            self.logger.info("✅ Discord bot initialized with messaging service integration")

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Discord bot: {e}")
            raise
    
    # System integration is handled through messaging service
    # No additional integration needed for basic functionality
    
    async def start(self) -> None:
        """Start the Discord bot service."""
        try:
            if not self.bot:
                raise RuntimeError("Discord bot not initialized")

            self.logger.info("🚀 Starting Discord Commander...")

            # Get bot token
            token = os.getenv("DISCORD_BOT_TOKEN")
            if not token:
                raise RuntimeError("DISCORD_BOT_TOKEN environment variable not set")

            # Sync slash commands
            try:
                synced = await self.bot.tree.sync()
                self.logger.info(f"✅ Synced {len(synced)} slash commands")
            except Exception as e:
                self.logger.error(f"❌ Failed to sync slash commands: {e}")

            # Start the bot
            await self.bot.start(token)

        except discord.LoginFailure:
            self.logger.error("❌ Invalid Discord bot token!")
            raise
        except Exception as e:
            self.logger.error(f"❌ Failed to start Discord Commander: {e}")
            raise
    
    async def stop(self) -> None:
        """Stop the Discord bot service."""
        try:
            if self.bot:
                self.logger.info("🛑 Stopping Discord Commander...")
                await self.bot.close()

            self.logger.info("✅ Discord Commander stopped")

        except Exception as e:
            self.logger.error(f"❌ Failed to stop Discord Commander: {e}")

    def get_status(self) -> dict:
        """Get the status of the Discord bot service."""
        return {
            "service_initialized": self.is_initialized,
            "bot_ready": self.bot.user is not None if self.bot else False,
            "guild_count": len(self.bot.guilds) if self.bot and self.bot.guilds else 0,
            "messaging_service_connected": self.messaging_service is not None
        }


async def main():
    """Main function to run the integrated Discord bot service."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and initialize service
    service = IntegratedDiscordBotService()
    
    try:
        # Initialize service
        success = await service.initialize()
        if not success:
            logger.error("❌ Failed to initialize service")
            return
        
        # Start service
        await service.start()
        
# Start the bot with proper token handling
    except Exception as e:
        logger.error(f"❌ Service error: {e}")
    finally:
        # Stop service
        await service.stop()


if __name__ == "__main__":
    asyncio.run(main())
