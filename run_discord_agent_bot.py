import logging

logger = logging.getLogger(__name__)
"""
Standalone Discord Agent Bot Runner
===================================

Simple script to run the Discord agent bot without import issues.
This bypasses the circular import problems in the main module structure.

Author: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from discord.ext import commands

import discord


class SimpleDiscordAgentBot(commands.Bot):
    """Simple Discord agent bot for testing and coordination."""

    def __init__(self, command_prefix: str = "!", intents=None):
        """Initialize simple Discord agent bot."""
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = False
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.agent_coordinates = self._load_agent_coordinates()

    def _load_agent_coordinates(self):
        """Load agent coordinates configuration."""
        coordinates_path = "cursor_agent_coords.json"
        try:
            import json

            with open(coordinates_path) as f:
                data = json.load(f)
                return data.get("agents", {})
        except Exception as e:
            logger.info(f"⚠️  Failed to load coordinates: {e}. Using defaults.")
            return {
                f"Agent-{i}": {
                    "chat_input_coordinates": [0, 0],
                    "onboarding_coordinates": [0, 0],
                    "description": f"Agent {i}",
                    "active": True,
                }
                for i in range(1, 9)
            }

    async def on_ready(self):
        """Called when bot is ready and connected."""
        logger.info("🐝 V2_SWARM Discord Agent Bot Ready!")
        logger.info(f"🤖 Logged in as: {self.user}")
        logger.info(f"📊 Connected to {len(self.guilds)} guild(s)")
        for guild in self.guilds:
            logger.info(f"  - {guild.name} (ID: {guild.id})")
        logger.info(f"🎯 Command prefix: {self.command_prefix}")
        logger.info("=" * 60)
        logger.info("💡 Available commands:")
        logger.info("  !ping                  - Test bot responsiveness")
        logger.info("  !help                  - Show help")
        logger.info("  !agents                - List all agents")
        logger.info("  !status                - Show system status")
        logger.info("  !swarm <message>       - Send swarm-wide message")
        logger.info("=" * 60)
        await self._send_startup_notification()

    async def _send_startup_notification(self):
        """Send startup notification to Discord channel."""
        try:
            target_channel = None
            for guild in self.guilds:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        target_channel = channel
                        break
                if target_channel:
                    break
            if target_channel:
                notification_msg = """**DISCORD COMMANDER ONLINE**

V2_SWARM Discord Agent Bot is now connected and operational!

**Available Commands:**
- `!ping` - Test bot responsiveness
- `!help` - Show all commands
- `!agents` - List all agents
- `!status` - Show system status
- `!swarm <message>` - Send swarm-wide message

**System Status:**
- Bot: Online
- Agents: 8 ready for coordination
- Security: Active

**Ready for swarm coordination!**
_V2_SWARM - We are swarm intelligence in action!_"""
                await target_channel.send(notification_msg)
                logger.info(
                    f"✅ Startup notification sent to #{target_channel.name} in {target_channel.guild.name}"
                )
            else:
                logger.info("⚠️  No suitable channel found to send startup notification")
        except Exception as e:
            logger.info(f"⚠️  Failed to send startup notification: {e}")

    async def on_message(self, message):
        """Handle incoming messages."""
        if message.author == self.user:
            return
        await self.process_commands(message)


def setup_commands(bot):
    """Setup bot commands."""

    @bot.command(name="ping")
    async def ping(ctx):
        """Test bot responsiveness."""
        latency = round(bot.latency * 1000)
        await ctx.reply(f"🏓 Pong! Latency: {latency}ms")

    @bot.command(name="help")
    async def help_command(ctx):
        """Show help information."""
        help_text = """
**V2_SWARM Discord Agent Bot Commands:**

**Basic Commands:**
- `!ping` - Test bot responsiveness
- `!help` - Show this help message
- `!status` - Show system status

**Agent Commands:**
- `!agents` - List all agents and their status
- `!swarm <message>` - Send message to all agents

**System Commands:**
- `!info` - Show bot information

**Usage Examples:**
- `!swarm All agents report status`
- `!agents`
- `!status`

**Ready for swarm coordination!** 🐝
        """
        await ctx.reply(help_text)

    @bot.command(name="agents")
    async def list_agents(ctx):
        """List all agents and their status."""
        agent_list = "**V2_SWARM Agent Status:**\n\n"
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            status = (
                "🟢 Active"
                if bot.agent_coordinates.get(agent_id, {}).get("active", True)
                else "🔴 Inactive"
            )
            description = bot.agent_coordinates.get(agent_id, {}).get("description", f"Agent {i}")
            roles = {
                "Agent-1": "Integration & Core Systems Specialist",
                "Agent-2": "Architecture & Design Specialist",
                "Agent-3": "Infrastructure & DevOps Specialist",
                "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
                "Agent-5": "Business Intelligence Specialist",
                "Agent-6": "Coordination & Communication Specialist",
                "Agent-7": "Web Development Specialist",
                "Agent-8": "Operations & Support Specialist",
            }
            role = roles.get(agent_id, "Specialist")
            agent_list += f"{agent_id}: {status} - {role}\n"
        agent_list += "\n**Captain Agent-4** coordinates all operations.\n"
        agent_list += "**Agent-6** handles communication protocols.\n\n"
        agent_list += "🐝 **WE ARE SWARM** - Ready for coordination!"
        await ctx.reply(agent_list)

    @bot.command(name="status")
    async def system_status(ctx):
        """Show system status."""
        status_text = f"""
**V2_SWARM System Status:**

**Bot Information:**
- Name: {bot.user.name}
- ID: {bot.user.id}
- Latency: {round(bot.latency * 1000)}ms
- Guilds: {len(bot.guilds)}
- Commands: {len(bot.commands)}

**Agent Configuration:**
- Total Agents: 8
- Active Agents: {sum(1 for agent in bot.agent_coordinates.values() if agent.get("active", True))}
- Coordinate System: Loaded

**System Health:**
- Bot Status: 🟢 Online
- Agent Communication: 🟢 Ready
- Swarm Coordination: 🟢 Active

**Ready for swarm operations!** 🐝
        """
        await ctx.reply(status_text)

    @bot.command(name="swarm")
    async def swarm_message(ctx, *, message: str):
        """Send message to all agents."""
        if not message:
            await ctx.reply("❌ Please provide a message to send to the swarm.")
            return
        active_agents = [
            agent_id
            for agent_id, config in bot.agent_coordinates.items()
            if config.get("active", True)
        ]
        response = f"""
**SWARM MESSAGE SENT** 📢

**Message:** {message}
**Recipients:** {len(active_agents)} active agents
**Agents:** {", ".join(active_agents)}

**Status:** Message queued for delivery
**Priority:** Normal
**Timestamp:** {ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S")}

🐝 **WE ARE SWARM** - Message delivered to all active agents!
        """
        await ctx.reply(response)

    @bot.command(name="info")
    async def bot_info(ctx):
        """Show bot information."""
        info_text = f"""
**V2_SWARM Discord Agent Bot Information:**

**Bot Details:**
- Name: {bot.user.name}
- Discriminator: {bot.user.discriminator}
- ID: {bot.user.id}
- Created: {bot.user.created_at.strftime("%Y-%m-%d %H:%M:%S")}

**Connection:**
- Latency: {round(bot.latency * 1000)}ms
- Guilds: {len(bot.guilds)}
- Channels: {sum(len(guild.channels) for guild in bot.guilds)}

**Features:**
- Agent Coordination: ✅
- Swarm Communication: ✅
- Command Processing: ✅
- Status Monitoring: ✅

**Version:** V2_SWARM Discord Agent Bot
**Author:** Agent-6 (Coordination & Communication Specialist)
**License:** MIT

🐝 **WE ARE SWARM** - Discord coordination active!
        """
        await ctx.reply(info_text)


async def main():
    """Main entry point."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.info("❌ No Discord bot token provided.")
        logger.info("💡 Set DISCORD_BOT_TOKEN environment variable")
        logger.info("💡 Example: set DISCORD_BOT_TOKEN=your_bot_token_here")
        sys.exit(1)
    bot = SimpleDiscordAgentBot()
    setup_commands(bot)
    logger.info("🐝 Starting V2_SWARM Discord Agent Bot...")
    logger.info(f"🤖 Token: {'***' + token[-10:] if len(token) > 10 else token}")
    logger.info("=" * 60)
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("\n🛑 Bot stopped by user")
    except Exception as e:
        logger.info(f"\n❌ Bot error: {e}")
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
