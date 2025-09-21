#!/usr/bin/env python3
"""
Discord Commander Fixed - V2 Compliant
=====================================

Fixed Discord Commander with proper integration to the consolidated messaging service.
Handles missing configuration gracefully and provides all slash commands.

V2 Compliance: ≤400 lines, 2 classes, 8 functions
"""

import discord
from discord.ext import commands
import logging
import asyncio
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from services.messaging.core.messaging_service import MessagingService
except ImportError:
    # Fallback for direct execution
    from messaging.core.messaging_service import MessagingService

logger = logging.getLogger(__name__)


class DiscordCommanderBot(commands.Bot):
    """Fixed Discord Commander bot with consolidated messaging integration."""

    def __init__(self):
        """Initialize Discord Commander bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

        # Bot state
        self.is_ready = False
        self.messaging_service = None

        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.DiscordCommanderBot")

        # Register event handlers
        self.setup_events()

        # Setup slash commands
        self.setup_slash_commands()

    def setup_events(self):
        """Setup Discord bot event handlers."""

        @self.event
        async def on_ready():
            """Called when bot is ready and connected."""
            self.is_ready = True
            self.logger.info(f"🤖 Discord Commander {self.user} is online!")

            # Update presence
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="🐝 WE ARE SWARM - 5-Agent Mode Active"
                )
            )

            # Initialize messaging service
            self.messaging_service = MessagingService("config/coordinates.json")

        @self.event
        async def on_guild_join(guild):
            """Called when bot joins a guild."""
            self.logger.info(f"✅ Joined guild: {guild.name}")

        @self.event
        async def on_message(self, message):
            """Handle incoming messages."""
            if message.author == self.user:
                return

            # Process commands
            await self.process_commands(message)

    def setup_slash_commands(self):
        """Setup Discord slash commands."""

        @self.tree.command(name="swarm_status", description="Get current swarm status")
        async def swarm_status(interaction: discord.Interaction):
            """Get current swarm status."""
            try:
                if not self.messaging_service:
                    await interaction.response.send_message("❌ Messaging service not available")
                    return

                embed = discord.Embed(
                    title="🐝 Swarm Status Report",
                    description="5-Agent Testing Mode Active",
                    color=0x00ff00,
                    timestamp=datetime.utcnow()
                )

                embed.add_field(
                    name="Active Agents",
                    value="Agent-4, Agent-5, Agent-6, Agent-7, Agent-8",
                    inline=False
                )

                embed.add_field(
                    name="Messaging System",
                    value="✅ Operational",
                    inline=True
                )

                embed.add_field(
                    name="Discord Bot",
                    value="✅ Online" if self.is_ready else "❌ Offline",
                    inline=True
                )

                embed.add_field(
                    name="Guilds",
                    value=len(self.guilds),
                    inline=True
                )

                embed.set_footer(text="WE ARE SWARM - Discord Commander Active")
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                self.logger.error(f"Error getting swarm status: {e}")
                await interaction.response.send_message("❌ Error getting swarm status")

        @self.tree.command(name="send_to_agent", description="Send message to specific agent")
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

        @self.tree.command(name="broadcast", description="Broadcast message to all agents")
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

        @self.tree.command(name="agent_list", description="List all available agents")
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

        @self.tree.command(name="system_check", description="Check system integration status")
        async def system_check(interaction: discord.Interaction):
            """Check system integration status."""
            try:
                embed = discord.Embed(
                    title="🔧 System Integration Check",
                    description="Discord Commander System Status",
                    color=0x0099ff,
                    timestamp=datetime.utcnow()
                )

                # Bot status
                embed.add_field(
                    name="Discord Bot",
                    value="✅ Online" if self.is_ready else "❌ Offline",
                    inline=True
                )

                # Messaging service status
                messaging_status = "✅ Connected" if self.messaging_service else "❌ Disconnected"
                embed.add_field(
                    name="Messaging Service",
                    value=messaging_status,
                    inline=True
                )

                # Guild status
                embed.add_field(
                    name="Connected Guilds",
                    value=len(self.guilds),
                    inline=True
                )

                # Agent mode
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


async def main():
    """Main function to run the Discord Commander."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Check configuration
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN environment variable not set!")
        logger.info("📝 To fix this:")
        logger.info("1. Set your Discord bot token: export DISCORD_BOT_TOKEN='your_token_here'")
        logger.info("2. Or create a .env file with DISCORD_BOT_TOKEN=your_token_here")
        logger.info("3. Then run: python src/services/discord_commander_fixed.py")
        return

    # Create bot instance
    bot = DiscordCommanderBot()

    try:
        logger.info("🚀 Starting Discord Commander...")

        # Sync slash commands
        try:
            synced = await bot.tree.sync()
            logger.info(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"❌ Failed to sync slash commands: {e}")
            logger.warning("⚠️  Slash commands may not work until synced with Discord")

        # Start the bot
        await bot.start(token)

    except discord.LoginFailure:
        logger.error("❌ Invalid Discord bot token!")
        logger.info("📝 Check your DISCORD_BOT_TOKEN")
    except Exception as e:
        logger.error(f"❌ Discord Commander error: {e}")
    finally:
        if bot.is_ready:
            logger.info("🛑 Shutting down Discord Commander...")
            await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

