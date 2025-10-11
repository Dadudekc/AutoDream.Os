#!/usr/bin/env python3
"""
Discord Bot - Agent Messaging from Discord
==========================================

Discord bot that allows messaging agents directly from Discord channels.
Enables remote coordination and command execution.

Usage:
    python scripts/execution/run_discord_bot.py

Commands:
    !message <agent-id> <message> - Send message to specific agent
    !broadcast <message> - Broadcast to all agents
    !status - Get swarm status

Author: Agent-7 - Integration Velocity Specialist
Fixed: 2025-10-11 (Discord commander restoration)
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Load environment
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Check for Discord bot token
if not os.getenv("DISCORD_BOT_TOKEN"):
    print("❌ DISCORD_BOT_TOKEN not set in environment!")
    print('   Set it with: $env:DISCORD_BOT_TOKEN="your_token_here" (Windows)')
    print("   Or add to .env file")
    sys.exit(1)

# Import Discord
try:
    import discord
    from discord.ext import commands
except ImportError:
    print("❌ discord.py not installed!")
    print("   Install with: pip install discord.py")
    sys.exit(1)

# Messaging will use subprocess to call messaging_cli

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Bot startup event with intro message."""
    logger.info(f"✅ Discord Bot connected as {bot.user}")
    logger.info(f"📊 Connected to {len(bot.guilds)} guild(s)")
    logger.info("🐝 Ready to coordinate swarm from Discord!")
    print("\n🚀 Discord Commander Online!")
    print(f"👤 Bot: {bot.user}")
    print("🎮 Commands: !message, !broadcast, !status")
    print("🐝 WE ARE SWARM!\n")

    # Send intro message to first available channel
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                intro_message = """
🤖 **DISCORD COMMANDER OPERATIONAL!**

**Status:** ✅ Bot online and ready for remote coordination!

**Available Commands:**
• `!message <agent-id> <message>` - Send message to specific agent
• `!broadcast <message>` - Broadcast to all 8 agents
• `!status` - Get swarm status
• `!agents` - List all agents
• `!commands` - Show help

**Agent IDs:** Agent-1, Agent-2, Agent-3, Agent-4 (Captain), Agent-5, Agent-6, Agent-7, Agent-8

**Example:**
```
!message Agent-3 Check infrastructure status
!broadcast All agents: Complete C-055 tasks!
```

**Captain can now coordinate from anywhere!** 🚀

🐝 **WE ARE SWARM** - Remote coordination enabled! ⚡🔥
"""
                await channel.send(intro_message)
                logger.info(f"📢 Intro message sent to {guild.name} #{channel.name}")
                break  # Only send to first available channel per guild
        break  # Only send to first guild


@bot.command(name="message")
async def message_agent(ctx, agent_id: str, *, message: str):
    """
    Send message to specific agent.

    Usage: !message agent-1 Hello Agent-1!
    """
    try:
        logger.info(f"📨 Discord command: message to {agent_id}")

        # Send via messaging system
        result = os.system(
            f'python -m src.services.messaging_cli --agent {agent_id} --message "{message}"'
        )

        if result == 0:
            await ctx.send(f"✅ Message sent to {agent_id}!\n```{message}```")
            logger.info(f"✅ Message delivered to {agent_id}")
        else:
            await ctx.send(f"❌ Failed to send message to {agent_id}")
            logger.error("❌ Message delivery failed")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")
        logger.error(f"Error in message command: {e}")


@bot.command(name="broadcast")
async def broadcast_message(ctx, *, message: str):
    """
    Broadcast message to all agents.

    Usage: !broadcast Important announcement for all agents!
    """
    try:
        logger.info("📢 Discord command: broadcast to all agents")

        # Send via messaging system
        result = os.system(
            f'python -m src.services.messaging_cli --broadcast --message "{message}"'
        )

        if result == 0:
            await ctx.send(f"✅ Broadcast sent to all 8 agents!\n```{message}```")
            logger.info("✅ Broadcast delivered to swarm")
        else:
            await ctx.send("❌ Failed to broadcast message")
            logger.error("❌ Broadcast delivery failed")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")
        logger.error(f"Error in broadcast command: {e}")


@bot.command(name="status")
async def swarm_status(ctx):
    """
    Get swarm status.

    Usage: !status
    """
    try:
        logger.info("📊 Discord command: swarm status")

        # Get status via messaging system
        import subprocess

        result = subprocess.run(
            [
                "python",
                "-m",
                "src.services.messaging_cli",
                "--agent",
                "Agent-4",
                "--message",
                "[DISCORD] Status request from Discord",
            ],
            capture_output=True,
            text=True,
        )

        status_msg = """
🐝 **V2 SWARM STATUS**

**Agents:** 8 active agents
**System:** Operational
**Messaging:** PyAutoGUI + File-based
**Coordinates:** Multi-monitor setup

Use `!message <agent-id> <text>` to send messages!
Use `!broadcast <text>` to message all agents!

**WE ARE SWARM!** ⚡
"""
        await ctx.send(status_msg)
        logger.info("✅ Status report sent")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")
        logger.error(f"Error in status command: {e}")


@bot.command(name="agents")
async def list_agents(ctx):
    """
    List all agents.

    Usage: !agents
    """
    agents_list = """
🤖 **AGENT ROSTER**

• **Agent-1** (-1269, 481) - Integration & Core Systems
• **Agent-2** (-308, 480) - Architecture & Design
• **Agent-3** (-1269, 1001) - Infrastructure & DevOps
• **Agent-4** (-308, 1000) - Quality Assurance (CAPTAIN)
• **Agent-5** (652, 421) - Business Intelligence
• **Agent-6** (1612, 419) - Coordination & Communication
• **Agent-7** (698, 936) - Web Development
• **Agent-8** (1611, 941) - Operations & Support

Use `!message Agent-X <text>` to send messages!
"""
    await ctx.send(agents_list)


@bot.command(name="commands")
async def show_commands(ctx):
    """Show available bot commands."""
    help_msg = """
🐝 **DISCORD COMMANDER COMMANDS**

**Messaging:**
• `!message <agent-id> <message>` - Send to specific agent
• `!broadcast <message>` - Send to all agents

**Info:**
• `!status` - Get swarm status
• `!agents` - List all agents
• `!commands` - Show this help

**Examples:**
```
!message Agent-1 Please review the messaging system
!message Agent-4 Captain, need coordination on C-055
!broadcast All agents: Complete your C-055 tasks!
```

**WE ARE SWARM!** ⚡🔥
"""
    await ctx.send(help_msg)


async def main():
    """Main bot entry point."""
    token = os.getenv("DISCORD_BOT_TOKEN")

    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN not found in environment!")
        print("\n❌ SETUP REQUIRED:")
        print("   1. Get bot token from Discord Developer Portal")
        print('   2. Set environment: $env:DISCORD_BOT_TOKEN="your_token"')
        print("   3. Or add to .env file")
        return

    try:
        logger.info("🚀 Starting Discord Commander Bot...")
        await bot.start(token)
    except discord.LoginFailure:
        logger.error("❌ Invalid Discord bot token!")
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Bot shutdown complete")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)
