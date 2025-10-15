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

from src.discord_commander.core import DiscordConfig
from src.discord_commander.messaging_commands import MessagingCommands
from src.discord_commander.messaging_controller import DiscordMessagingController
from src.services.messaging_infrastructure import ConsolidatedMessagingService

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

        # Cog already loaded in setup_hook
        self.logger.info("Bot ready and commands loaded!")

        # C-057: Send startup intro message to Captain
        await self.send_startup_intro()

    async def send_startup_intro(self):
        """C-057: Send startup intro message to Captain at work."""
        try:
            # Get configured channel from environment or use default
            channel_id = self.config.channel_id

            if not channel_id:
                self.logger.warning("No command channel configured, skipping intro message")
                return

            # Convert channel_id to int if it's a string
            try:
                channel_id = int(channel_id)
            except (ValueError, TypeError):
                self.logger.error(f"Invalid channel ID format: {channel_id}")
                return

            channel = self.get_channel(channel_id)

            if not channel:
                # Try to find first available text channel
                self.logger.warning(
                    f"Could not find channel {channel_id}, using first text channel"
                )
                for guild in self.guilds:
                    for text_channel in guild.text_channels:
                        channel = text_channel
                        self.logger.info(f"Using channel: {channel.name} ({channel.id})")
                        break
                    if channel:
                        break

                if not channel:
                    self.logger.error("No text channels available")
                    return

            # Create intro embed
            embed = discord.Embed(
                title="🚀 C-057 Discord View Controller - ONLINE",
                description="**First Autonomous Mission Complete!**",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )

            embed.add_field(
                name="✅ Mission Status",
                value="Discord View Controller successfully deployed and running!",
                inline=False,
            )

            embed.add_field(
                name="🐝 Autonomous Execution",
                value="Built autonomously by Agent-2 (Architecture), Agent-1 (Integration), Agent-7 (Discord), Agent-3 (Infrastructure)",
                inline=False,
            )

            embed.add_field(
                name="🎯 Features Available",
                value="• `!agent <name> <message>` - Send message to agents\n• `!agent_interact` - Interactive messaging UI\n• `!swarm_status` - View swarm status\n• `!broadcast <message>` - Message all agents\n• `!help_messaging` - Full command list",
                inline=False,
            )

            embed.add_field(
                name="📊 System Info",
                value=f"Bot: {self.user.name}\nGuilds: {len(self.guilds)}\nLatency: {round(self.latency * 1000, 2)}ms",
                inline=False,
            )

            embed.set_footer(text="C-057 Autonomous Mission | 🐝 WE. ARE. SWARM. ⚡️")

            await channel.send(embed=embed)
            self.logger.info("C-057 startup intro message sent successfully!")

        except Exception as e:
            self.logger.error(f"Failed to send startup intro: {e}")

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
            await self.add_cog(MessagingCommands(self, self.messaging_controller))
            self.logger.info("Messaging commands cog added successfully")
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
            await self.bot.start(self.config.bot_token)

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
