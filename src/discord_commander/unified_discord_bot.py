#!/usr/bin/env python3
"""
Unified Discord Bot - Single Bot for Agent Messaging
====================================================

Single, unified Discord bot providing complete GUI access to agent messaging system.
Consolidates all Discord functionality into one bot instance.

Features:
- Complete agent messaging GUI
- Real-time swarm status monitoring
- Interactive views, modals, and commands
- Broadcast capabilities
- Single bot instance (no duplication)

Author: Agent-3 (Infrastructure & DevOps) - Discord Consolidation
License: MIT
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()  # Load .env file
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("⚠️  Continuing without .env support...")

# Discord imports
try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("❌ discord.py not installed! Run: pip install discord.py")
    sys.exit(1)

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.discord_commander.discord_gui_controller import DiscordGUIController
from src.services.messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class UnifiedDiscordBot(commands.Bot):
    """Single unified Discord bot for agent messaging system."""

    def __init__(self, token: str, channel_id: int | None = None):
        """Initialize unified Discord bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True

        super().__init__(command_prefix="!", intents=intents, help_command=None)

        self.token = token
        self.channel_id = channel_id
        self.messaging_service = ConsolidatedMessagingService()
        self.gui_controller = DiscordGUIController(self.messaging_service)
        self.logger = logging.getLogger(__name__)

    async def on_ready(self):
        """Bot ready event."""
        self.logger.info(f"✅ Discord Commander Bot ready: {self.user}")
        self.logger.info(f"📊 Guilds: {len(self.guilds)}")
        self.logger.info(f"🤖 Latency: {round(self.latency * 1000, 2)}ms")

        # Set bot presence
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="the swarm 🐝")
        )

        # Send startup message
        await self.send_startup_message()

    async def send_startup_message(self):
        """Send startup message to configured channel."""
        try:
            channel = None

            if self.channel_id:
                channel = self.get_channel(self.channel_id)

            if not channel:
                # Find first available text channel
                for guild in self.guilds:
                    for text_channel in guild.text_channels:
                        channel = text_channel
                        self.logger.info(f"Using channel: {channel.name} ({channel.id})")
                        break
                    if channel:
                        break

            if not channel:
                self.logger.warning("No text channels available for startup message")
                return

            embed = discord.Embed(
                title="🚀 Discord Commander - ONLINE",
                description="**Complete Agent Messaging System Access**",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )

            embed.add_field(
                name="✅ System Status",
                value="Discord GUI Controller active and ready!",
                inline=False,
            )

            embed.add_field(
                name="🎯 Available Commands",
                value=(
                    "• `!gui` - Open messaging GUI\n"
                    "• `!status` - View swarm status\n"
                    "• `!message <agent> <msg>` - Direct message\n"
                    "• `!broadcast <msg>` - Broadcast to all\n"
                    "• `!help` - Full command list"
                ),
                inline=False,
            )

            embed.add_field(
                name="🤖 Bot Info",
                value=f"Guilds: {len(self.guilds)} | Latency: {round(self.latency * 1000, 2)}ms",
                inline=False,
            )

            embed.set_footer(text="🐝 WE. ARE. SWARM. - Agent-3 Infrastructure")

            await channel.send(embed=embed)
            self.logger.info("✅ Startup message sent successfully")

        except Exception as e:
            self.logger.error(f"Error sending startup message: {e}")

    async def setup_hook(self):
        """Setup hook for bot initialization."""
        try:
            # Add messaging commands cog
            await self.add_cog(MessagingCommands(self, self.gui_controller))
            self.logger.info("✅ Messaging commands loaded")
        except Exception as e:
            self.logger.error(f"Error loading commands: {e}")

    async def close(self):
        """Clean shutdown."""
        self.logger.info("🛑 Unified Discord Bot shutting down...")
        await super().close()


class MessagingCommands(commands.Cog):
    """Commands for agent messaging."""

    def __init__(self, bot: UnifiedDiscordBot, gui_controller: DiscordGUIController):
        """Initialize messaging commands."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="gui", description="Open messaging GUI")
    async def gui(self, ctx: commands.Context):
        """Open interactive messaging GUI."""
        try:
            embed = discord.Embed(
                title="🤖 Agent Messaging Control Panel",
                description="Use the controls below to interact with the swarm",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )

            embed.add_field(
                name="📋 Instructions",
                value=(
                    "1. Select an agent from dropdown to send message\n"
                    "2. Click 'Broadcast' to message all agents\n"
                    "3. Click 'Status' to view swarm status\n"
                    "4. Click 'Refresh' to reload agent list"
                ),
                inline=False,
            )

            view = self.gui_controller.create_main_gui()
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            self.logger.error(f"Error opening GUI: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="status", description="View swarm status")
    async def status(self, ctx: commands.Context):
        """View swarm status."""
        try:
            view = self.gui_controller.create_status_gui()

            # Import status reader to create embed
            from src.discord_commander.status_reader import StatusReader

            status_reader = StatusReader()

            # Create status embed
            main_view = self.gui_controller.create_main_gui()
            embed = await main_view._create_status_embed(status_reader)

            await ctx.send(embed=embed, view=view)

        except Exception as e:
            self.logger.error(f"Error showing status: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="message", description="Send message to agent")
    async def message(self, ctx: commands.Context, agent_id: str, *, message: str):
        """Send direct message to agent."""
        try:
            success = await self.gui_controller.send_message(
                agent_id=agent_id, message=message, priority="regular"
            )

            if success:
                embed = discord.Embed(
                    title="✅ Message Sent",
                    description=f"Delivered to **{agent_id}**",
                    color=discord.Color.green(),
                )
                embed.add_field(name="Message", value=message[:500], inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Failed to send message to {agent_id}")

        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="broadcast", description="Broadcast to all agents")
    async def broadcast(self, ctx: commands.Context, *, message: str):
        """Broadcast message to all agents."""
        try:
            success = await self.gui_controller.broadcast_message(
                message=message, priority="regular"
            )

            if success:
                embed = discord.Embed(
                    title="✅ Broadcast Sent",
                    description="Delivered to all agents",
                    color=discord.Color.green(),
                )
                embed.add_field(name="Message", value=message[:500], inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Failed to broadcast message")

        except Exception as e:
            self.logger.error(f"Error broadcasting: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="help", description="Show help information")
    async def help_cmd(self, ctx: commands.Context):
        """Show help information."""
        embed = discord.Embed(
            title="🤖 Discord Bot Help",
            description="Complete command reference for agent messaging",
            color=discord.Color.blue(),
        )

        embed.add_field(
            name="📋 Main Commands",
            value=(
                "`!gui` - Open interactive messaging GUI\n"
                "`!status` - View swarm status dashboard\n"
                "`!message <agent> <msg>` - Send direct message\n"
                "`!broadcast <msg>` - Broadcast to all agents"
            ),
            inline=False,
        )

        embed.add_field(
            name="🎯 GUI Features",
            value=(
                "• Agent selection dropdown\n"
                "• Interactive message composition\n"
                "• **Shift+Enter for line breaks** ✨\n"
                "• Priority selection (regular/urgent)\n"
                "• Real-time status monitoring\n"
                "• Broadcast capabilities"
            ),
            inline=False,
        )

        embed.add_field(
            name="📊 Examples",
            value=(
                "`!message Agent-1 Check your inbox`\n"
                "`!broadcast Team update: All systems go!`\n"
                "`!gui` (opens full GUI interface)"
            ),
            inline=False,
        )

        embed.set_footer(text="🐝 WE. ARE. SWARM.")

        await ctx.send(embed=embed)


async def main():
    """Main function to run the unified Discord bot."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Get token from environment
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN not set in environment!")
        print("   Set it with: $env:DISCORD_BOT_TOKEN='your_token' (Windows)")
        print("   Or add to .env file")
        sys.exit(1)

    # Get channel ID (optional)
    channel_id = os.getenv("DISCORD_CHANNEL_ID")
    if channel_id:
        try:
            channel_id = int(channel_id)
        except ValueError:
            print(f"⚠️  Invalid DISCORD_CHANNEL_ID: {channel_id}")
            channel_id = None

    # Create and run bot
    bot = UnifiedDiscordBot(token=token, channel_id=channel_id)

    try:
        print("🚀 Starting Discord Commander...")
        print("🐝 WE. ARE. SWARM.")
        await bot.start(token)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")
        logger.error(f"Bot crashed: {e}", exc_info=True)
    finally:
        await bot.close()


if __name__ == "__main__":
    if not DISCORD_AVAILABLE:
        print("❌ discord.py not available. Install with: pip install discord.py")
        sys.exit(1)

    asyncio.run(main())
