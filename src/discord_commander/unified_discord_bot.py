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
from src.services.messaging_infrastructure import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


# Confirmation Views for Shutdown/Restart Commands
class ConfirmShutdownView(discord.ui.View):
    """Confirmation view for shutdown command."""

    def __init__(self):
        super().__init__(timeout=30)
        self.confirmed = False

    @discord.ui.button(label="✅ Confirm Shutdown", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm shutdown button."""
        self.confirmed = True
        await interaction.response.send_message("✅ Shutdown confirmed", ephemeral=True)
        self.stop()

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel shutdown button."""
        self.confirmed = False
        await interaction.response.send_message("❌ Cancelled", ephemeral=True)
        self.stop()


class ConfirmRestartView(discord.ui.View):
    """Confirmation view for restart command."""

    def __init__(self):
        super().__init__(timeout=30)
        self.confirmed = False

    @discord.ui.button(label="🔄 Confirm Restart", style=discord.ButtonStyle.primary)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm restart button."""
        self.confirmed = True
        await interaction.response.send_message("✅ Restart confirmed", ephemeral=True)
        self.stop()

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel restart button."""
        self.confirmed = False
        await interaction.response.send_message("❌ Cancelled", ephemeral=True)
        self.stop()


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
            
            # Add swarm showcase commands cog
            from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
            await self.add_cog(SwarmShowcaseCommands(self))
            self.logger.info("✅ Swarm showcase commands loaded")
            
            # Add GitHub book viewer cog (WOW FACTOR!)
            from src.discord_commander.github_book_viewer import GitHubBookCommands
            await self.add_cog(GitHubBookCommands(self))
            self.logger.info("✅ GitHub Book Viewer loaded - WOW FACTOR READY!")
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
                "`!broadcast <msg>` - Broadcast to all agents\n"
                "`!shutdown` - Gracefully shutdown bot (admin only)\n"
                "`!restart` - Restart bot (admin only)"
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

    @commands.command(name="shutdown", description="Gracefully shutdown the bot")
    @commands.has_permissions(administrator=True)
    async def shutdown_cmd(self, ctx: commands.Context):
        """Gracefully shutdown the Discord bot."""
        # Confirmation embed
        embed = discord.Embed(
            title="🛑 Shutdown Requested",
            description="Are you sure you want to shutdown the bot?",
            color=discord.Color.red(),
        )

        # Create confirmation view
        view = ConfirmShutdownView()
        message = await ctx.send(embed=embed, view=view)

        # Wait for user confirmation (30 second timeout)
        await view.wait()

        if view.confirmed:
            # Announce shutdown
            shutdown_embed = discord.Embed(
                title="👋 Bot Shutting Down",
                description="Gracefully closing connections...",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=shutdown_embed)

            # Log shutdown
            self.logger.info("🛑 Shutdown command received - closing bot")

            # Close bot gracefully
            await self.close()
        else:
            await message.edit(content="❌ Shutdown cancelled", embed=None, view=None)

    @commands.command(name="restart", description="Restart the Discord bot")
    @commands.has_permissions(administrator=True)
    async def restart_cmd(self, ctx: commands.Context):
        """Restart the Discord bot."""
        # Confirmation embed
        embed = discord.Embed(
            title="🔄 Restart Requested",
            description="Bot will shutdown and restart. Continue?",
            color=discord.Color.blue(),
        )

        # Create confirmation view
        view = ConfirmRestartView()
        message = await ctx.send(embed=embed, view=view)

        # Wait for user confirmation (30 second timeout)
        await view.wait()

        if view.confirmed:
            # Announce restart
            restart_embed = discord.Embed(
                title="🔄 Bot Restarting",
                description="Shutting down... Will be back in 5-10 seconds!",
                color=discord.Color.blue(),
            )
            await ctx.send(embed=restart_embed)

            # Log restart
            self.logger.info("🔄 Restart command received - restarting bot")

            # Create restart flag file
            restart_flag_path = Path(__file__).parent.parent.parent / ".discord_bot_restart"
            restart_flag_path.write_text("RESTART_REQUESTED")

            # Close bot (restart logic handled by run script)
            await self.close()
        else:
            await message.edit(content="❌ Restart cancelled", embed=None, view=None)


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
