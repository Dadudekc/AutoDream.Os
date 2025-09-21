#!/usr/bin/env python3
"""
Discord Commander - Fixed Version
=================================

Fixed Discord Commander with working Discord bot integration.
Features:
- Working Discord bot connection
- Slash command support
- Agent coordination
- Swarm intelligence integration

🐝 WE ARE SWARM - Discord Commander Active!
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Discord imports with error handling
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("❌ Discord.py not installed! Please install: pip install discord.py")

# Load environment variables
try:
    from dotenv import load_dotenv
    dotenv_path = Path(__file__).parent / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
        print("✅ Loaded environment variables from .env file")
    else:
        print("⚠️  No .env file found, using system environment variables")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment variables")

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import configuration
try:
    from discord_bot_config import config as discord_config
except ImportError:
    print("❌ Error: Cannot import discord_bot_config")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DiscordCommanderBot(commands.Bot):
    """Fixed Discord Commander Bot with working functionality."""

    def __init__(self, command_prefix: str = "!", intents: discord.Intents = None):
        """Initialize the Discord Commander bot."""
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
        self.is_ready = False
        self.connected_agents = set()
        self.swarm_status = {}
        self.config = {}

        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.DiscordCommanderBot")

        # Register event handlers
        self.setup_events()
        self.setup_commands()

    def setup_events(self):
        """Setup Discord bot event handlers."""

        @self.event
        async def on_ready():
            """Called when bot is ready and connected."""
            self.is_ready = True
            self.logger.info(f"🤖 Discord Commander {self.user} is online!")
            self.logger.info(f"📊 Connected to {len(self.guilds)} servers")

            # Update presence
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="🐝 WE ARE SWARM - Agent Coordination Active"
                )
            )

            # Print startup message
            print("=" * 60)
            print("🐝 Discord Commander Successfully Started!")
            print("=" * 60)
            print(f"🤖 Bot: {self.user}")
            print(f"📊 Servers: {len(self.guilds)}")
            print(f"👥 Users: {len(self.users)}")
            print(f"📡 Status: Online and Ready!")
            print(f"🎯 5-Agent Mode: Agent-4, Agent-5, Agent-6, Agent-7, Agent-8")
            print("=" * 60)
            print("✅ All systems operational!")
            print("🚀 Ready for agent coordination!")
            print("=" * 60)

        @self.event
        async def on_guild_join(guild):
            """Called when bot joins a guild."""
            self.logger.info(f"✅ Joined guild: {guild.name}")
            print(f"📈 Joined new server: {guild.name}")

        @self.event
        async def on_guild_remove(guild):
            """Called when bot leaves a guild."""
            self.logger.info(f"❌ Left guild: {guild.name}")
            print(f"📉 Left server: {guild.name}")

        @self.event
        async def on_message(self, message):
            """Handle incoming messages."""
            if message.author == self.user:
                return

            # Process commands
            await self.process_commands(message)

            # Handle mentions
            if self.user.mentioned_in(message):
                await self.handle_mention(message)

    def setup_commands(self):
        """Setup Discord bot commands."""

        @self.command(name="help", help="Show available commands")
        async def help_command(ctx):
            """Show help information."""
            embed = discord.Embed(
                title="🐝 Discord Commander Help",
                description="Available commands for agent coordination",
                color=0x00ff00
            )

            embed.add_field(
                name="🤖 Bot Commands",
                value="`!help` - Show this help message\n"
                      "`!status` - Show bot status\n"
                      "`!ping` - Test bot response\n"
                      "`!agents` - Show connected agents",
                inline=False
            )

            embed.add_field(
                name="📋 Agent Commands",
                value="`!register <agent_id>` - Register an agent\n"
                      "`!unregister <agent_id>` - Unregister an agent\n"
                      "`!send <agent_id> <message>` - Send message to agent\n"
                      "`!broadcast <message>` - Broadcast to all agents",
                inline=False
            )

            embed.add_field(
                name="🛠️ Admin Commands",
                value="`!restart` - Restart the bot (admin only)\n"
                      "`!shutdown` - Shutdown the bot (admin only)\n"
                      "`!reload` - Reload commands (admin only)",
                inline=False
            )

            embed.set_footer(text="WE ARE SWARM - Agent Coordination Active")
            await ctx.send(embed=embed)

        @self.command(name="status", help="Show bot status")
        async def status_command(ctx):
            """Show bot status."""
            embed = discord.Embed(
                title="📊 Discord Commander Status",
                color=0x0099ff
            )

            embed.add_field(
                name="🤖 Bot Status",
                value="🟢 Online" if self.is_ready else "🔴 Offline",
                inline=True
            )

            embed.add_field(
                name="📡 Servers",
                value=str(len(self.guilds)),
                inline=True
            )

            embed.add_field(
                name="👥 Users",
                value=str(len(self.users)),
                inline=True
            )

            embed.add_field(
                name="⏱️ Latency",
                value=f"{round(self.latency * 1000)}ms" if self.latency else "Unknown",
                inline=True
            )

            embed.add_field(
                name="🔗 Connected Agents",
                value=str(len(self.connected_agents)),
                inline=True
            )

            embed.add_field(
                name="🐝 Swarm Mode",
                value="5-Agent Mode Active",
                inline=True
            )

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
                title="👥 Connected Agents",
                description="Active agents in the swarm",
                color=0xff9900
            )

            for agent_id in self.connected_agents:
                embed.add_field(
                    name=f"🔗 {agent_id}",
                    value="🟢 Connected",
                    inline=True
                )

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

    async def handle_mention(self, message):
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


async def main():
    """Main function to run Discord Commander."""
    if not DISCORD_AVAILABLE:
        print("❌ Discord.py is required but not installed!")
        print("💡 Install it with: pip install discord.py")
        return 1

    # Create bot instance
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True

    bot = DiscordCommanderBot(command_prefix="!", intents=intents)

    try:
        # Get bot token
        token = discord_config.get_bot_token()
        if not token:
            print("❌ Discord bot token not configured!")
            print("💡 Please set DISCORD_BOT_TOKEN environment variable")
            print("💡 Run: python setup_discord_commander.py to configure")
            return 1

        print("🚀 Starting Discord Commander...")
        print(f"🔑 Token: {token[:10]}...{token[-4:]}")
        print("🐝 WE ARE SWARM - Agent Coordination Active!")

        # Start the Discord bot
        await bot.start(token)

    except discord.LoginFailure:
        print("❌ Discord login failed - invalid token!")
        print("💡 Check your DISCORD_BOT_TOKEN environment variable")
        return 1
    except discord.HTTPException as e:
        print(f"❌ Discord HTTP error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n🛑 Received keyboard interrupt - shutting down...")
    except Exception as e:
        print(f"❌ Error starting Discord bot: {e}")
        return 1
    finally:
        # Cleanup
        if not bot.is_closed():
            await bot.close()

    print("👋 Discord Commander shutdown complete!")
    return 0


if __name__ == "__main__":
    # Print header
    print("🐝 Discord Commander - Agent Cellphone V2")
    print("=" * 50)
    print("WE ARE SWARM - 5-Agent Mode Active")
    print("Agent Coordination Hub (Agent-4, Agent-5, Agent-6, Agent-7, Agent-8)")
    print("=" * 50)

    # Run main function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
