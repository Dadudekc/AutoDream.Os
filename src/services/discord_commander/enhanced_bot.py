#!/usr/bin/env python3
"""
Enhanced Discord Commander Bot
==============================

Enhanced Discord bot with messaging controller integration.
Provides easy agent interaction through Discord views and commands.

Features:
- Discord views for intuitive agent messaging
- Real-time swarm status monitoring
- Interactive agent selection and communication
- Broadcast messaging capabilities
- Seamless integration with swarm messaging system

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import asyncio
import logging
import sys
from pathlib import Path

# Discord imports with error handling
try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.discord_commander.core import DiscordConfig
from src.services.discord_commander.messaging_commands import MessagingCommands
from src.services.discord_commander.messaging_controller import DiscordMessagingController
from src.services.messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class EnhancedDiscordCommanderBot(commands.Bot):
    """Enhanced Discord Commander Bot with messaging integration."""

    def __init__(self, config: DiscordConfig):
        """Initialize the enhanced Discord bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        super().__init__(command_prefix="!", intents=intents, help_command=None)

        self.config = config
        self.messaging_service = ConsolidatedMessagingService()
        self.messaging_controller = DiscordMessagingController(self.messaging_service)
        self.logger = logging.getLogger(__name__)

    async def on_ready(self):
        """Bot ready event."""
        self.logger.info(f"Enhanced Discord Commander Bot ready: {self.user}")

        # Set bot status
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="the swarm 🤖")
        )

        # Messaging commands are already loaded via setup_hook
        self.logger.info("Messaging commands already loaded via setup_hook")

        # Send online message to all guilds
        for guild in self.guilds:
            try:
                # Find a general or first available text channel
                channel = None
                for ch in guild.text_channels:
                    if (
                        ch.name in ["general", "bot-commands", "swarm"]
                        or "general" in ch.name.lower()
                    ):
                        channel = ch
                        break

                if not channel and guild.text_channels:
                    channel = guild.text_channels[0]

                if channel:
                    embed = discord.Embed(
                        title="🤖 Swarm Commander Online",
                        description="Enhanced Discord Messaging Bot is ready for agent communication!",
                        color=discord.Color.green(),
                        timestamp=discord.utils.utcnow(),
                    )
                    embed.add_field(
                        name="Available Commands",
                        value="`!help_messaging` - Get help with all commands\n`!agent_interact` - Interactive agent messaging\n`!swarm_status` - View swarm status",
                        inline=False,
                    )
                    embed.add_field(
                        name="Quick Start",
                        value="Use `!agent_interact` to start messaging agents through Discord!",
                        inline=False,
                    )
                    await channel.send(embed=embed)
                    self.logger.info(f"Sent online message to {guild.name} in #{channel.name}")

            except Exception as e:
                self.logger.error(f"Failed to send online message to {guild.name}: {e}")

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Handle command errors."""
        self.logger.error(f"Command error: {error}")

        if isinstance(error, commands.CommandNotFound):
            return

        embed = discord.Embed(
            title="❌ Command Error",
            description=f"An error occurred: {str(error)}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
        )

        try:
            await ctx.send(embed=embed)
        except:
            pass

    async def setup_hook(self):
        """Setup hook for bot initialization."""
        # Add messaging commands cog
        try:
            cog = MessagingCommands(self, self.messaging_controller)
            await self.add_cog(cog)
            self.logger.info("Messaging commands cog added successfully")
            self.logger.info(f"Available commands: {[cmd.name for cmd in self.commands]}")
        except Exception as e:
            self.logger.error(f"Failed to add messaging commands cog: {e}")

    async def close(self):
        """Clean shutdown."""
        self.logger.info("Enhanced Discord Commander Bot shutting down...")
        await super().close()


class EnhancedBotManager:
    """Manager for the enhanced Discord bot."""

    def __init__(self):
        """Initialize the bot manager."""
        self.config = DiscordConfig()
        self.bot = None
        self.logger = logging.getLogger(__name__)

    async def start_bot(self) -> bool:
        """Start the enhanced Discord bot."""
        try:
            self.logger.info("Starting Enhanced Discord Commander Bot...")

            # Validate configuration
            config_issues = self.config.validate()
            if config_issues:
                self.logger.error(f"Configuration issues: {config_issues}")
                return False

            # Create bot instance
            self.bot = EnhancedDiscordCommanderBot(self.config)

            # Start bot
            await self.bot.start(self.config.token)

        except Exception as e:
            self.logger.error(f"Failed to start bot: {e}")
            return False

    async def stop_bot(self):
        """Stop the enhanced Discord bot."""
        try:
            if self.bot:
                self.logger.info("Stopping Enhanced Discord Commander Bot...")
                await self.bot.close()
                self.bot = None
        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")

    def get_bot_status(self) -> dict:
        """Get bot status information."""
        if not self.bot:
            return {"status": "stopped", "guilds": 0, "users": 0}

        try:
            return {
                "status": "running",
                "guilds": len(self.bot.guilds),
                "users": len(self.bot.users),
                "latency": round(self.bot.latency * 1000, 2),
            }
        except:
            return {"status": "error", "guilds": 0, "users": 0}


async def main():
    """Main function to run the enhanced Discord bot."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    manager = EnhancedBotManager()

    try:
        await manager.start_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
    finally:
        await manager.stop_bot()


if __name__ == "__main__":
    if not DISCORD_AVAILABLE:
        print("❌ Discord.py not available. Install with: pip install discord.py")
        sys.exit(1)

    asyncio.run(main())
