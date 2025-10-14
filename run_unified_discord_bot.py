#!/usr/bin/env python3
"""
Discord Commander Bot - Remote Swarm Control Center
Text commands + Interactive UI + Detailed agent status
Author: Agent-8 | Enhanced: 2025-10-13
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Load environment
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Discord imports
try:
    import discord
    from discord.ext import commands
except ImportError:
    print("❌ discord.py not installed!")
    print("   Install with: pip install discord.py")
    sys.exit(1)

# Import our messaging system
from src.discord_commander.messaging_controller import DiscordMessagingController
from src.discord_commander.status_reader import StatusReader
from src.services.messaging_service import ConsolidatedMessagingService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("discord_unified_bot.log")],
)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Initialize messaging systems
messaging_service = ConsolidatedMessagingService()
messaging_controller = DiscordMessagingController(messaging_service)
status_reader = StatusReader()


@bot.event
async def on_ready():
    """Bot startup event."""
    logger.info(f"✅ Discord Commander connected as {bot.user}")
    print("\n🚀 DISCORD COMMANDER ONLINE! Remote swarm control ready!\n")

    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="the swarm 🤖")
    )

    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="🤖 DISCORD COMMANDER",
                    description="Remote Swarm Control Center",
                    color=discord.Color.green(),
                )
                embed.add_field(
                    name="📝 Quick Commands",
                    value="`!message <agent> <text>`\n`!broadcast <text>`\n`!status`",
                    inline=True,
                )
                embed.add_field(
                    name="🎮 Interactive UI",
                    value="`!agent_interact`\n`!swarm_status`\n`!agents`",
                    inline=True,
                )
                embed.add_field(name="ℹ️ Info", value="`!help`", inline=True)
                embed.set_footer(text="🐝 Remote Coordination Enabled!")
                await channel.send(embed=embed)
                logger.info(f"📢 Commander online in {guild.name}")
                break
        break


@bot.command(name="message")
async def message_agent(ctx, agent_id: str, *, message: str):
    """Send message to specific agent. Usage: !message Agent-8 <text>"""
    try:
        logger.info(f"📨 Discord command: message to {agent_id}")

        # Send via messaging CLI
        result = os.system(
            f'python -m src.services.messaging_cli --agent {agent_id} --message "{message}"'
        )

        if result == 0:
            embed = discord.Embed(
                title="✅ Message Sent",
                description=f"Message delivered to **{agent_id}**",
                color=discord.Color.green(),
            )
            embed.add_field(name="Message", value=message[:500], inline=False)
            embed.add_field(name="From", value=ctx.author.display_name, inline=True)

            await ctx.send(embed=embed)
            logger.info(f"✅ Message delivered to {agent_id}")
        else:
            await ctx.send(f"❌ Failed to send message to {agent_id}")
            logger.error("❌ Message delivery failed")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")
        logger.error(f"Error in message command: {e}")


@bot.command(name="broadcast")
async def broadcast_message(ctx, *, message: str):
    """Broadcast to all agents. Usage: !broadcast <text>"""
    try:
        logger.info("📢 Discord command: broadcast to all agents")

        # Send via messaging CLI
        result = os.system(
            f'python -m src.services.messaging_cli --broadcast --message "{message}"'
        )

        if result == 0:
            embed = discord.Embed(
                title="✅ Broadcast Sent",
                description="Message delivered to all 8 agents",
                color=discord.Color.green(),
            )
            embed.add_field(name="Message", value=message[:500], inline=False)
            embed.add_field(name="From", value=ctx.author.display_name, inline=True)

            await ctx.send(embed=embed)
            logger.info("✅ Broadcast delivered to swarm")
        else:
            await ctx.send("❌ Failed to broadcast message")
            logger.error("❌ Broadcast delivery failed")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")
        logger.error(f"Error in broadcast command: {e}")


@bot.command(name="status")
async def quick_status(ctx):
    """Detailed swarm status from status.json. Usage: !status"""
    try:
        logger.info("📊 Discord command: detailed status")

        statuses = status_reader.read_all_statuses()

        if not statuses:
            await ctx.send("❌ Could not read agent status files")
            return

        # Calculate totals
        total_points = sum(
            s.get("sprint_info", {}).get("points_completed", 0) for s in statuses.values()
        )
        total_agents = len(statuses)
        active = sum(1 for s in statuses.values() if "ACTIVE" in str(s.get("status", "")).upper())

        embed = discord.Embed(
            title="🤖 SWARM STATUS - DETAILED",
            description=f"Real-time from status.json • {total_points:,} points earned",
            color=discord.Color.green(),
        )

        # Summary with points
        embed.add_field(
            name="📊 Swarm Summary",
            value=f"**Agents:** {total_agents}/8 | **Active:** {active} | **Points:** {total_points:,}",
            inline=False,
        )

        # Individual agent status with details
        for agent_id in sorted(statuses.keys()):
            data = statuses[agent_id]
            status = data.get("status", "UNKNOWN")

            # Status emoji
            emoji = (
                "🟢"
                if "ACTIVE" in status.upper()
                else "✅" if "COMPLETE" in status.upper() else "🟡"
            )

            # Get details
            mission = data.get("current_mission", "No mission")
            if len(mission) > 50:
                mission = mission[:47] + "..."

            points = data.get("sprint_info", {}).get("points_completed", 0)
            pct = data.get("sprint_info", {}).get("completion_percentage", "0%")
            current_tasks = data.get("current_tasks", [])
            task_preview = (
                current_tasks[0][:40] + "..."
                if current_tasks and len(current_tasks[0]) > 40
                else (current_tasks[0] if current_tasks else "None")
            )

            embed.add_field(
                name=f"{emoji} {agent_id}",
                value=(
                    f"**Mission:** {mission}\n"
                    f"**Points:** {points} ({pct})\n"
                    f"**Task:** {task_preview}"
                ),
                inline=False,
            )

        embed.set_footer(
            text="🔄 Use !swarm_status for refresh button • Updated: "
            + statuses.get("Agent-1", {}).get("last_updated", "Unknown")
        )

        await ctx.send(embed=embed)
        logger.info("✅ Detailed status sent")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")
        logger.error(f"Error in status command: {e}")


@bot.command(name="agents")
async def list_agents(ctx):
    """List all agents. Usage: !agents"""
    embed = discord.Embed(
        title="🤖 AGENT ROSTER",
        description="All swarm agents and their coordinates",
        color=discord.Color.blue(),
    )

    agents = [
        ("Agent-1", "(-1269, 481)", "Integration & Core Systems"),
        ("Agent-2", "(-308, 480)", "Architecture & Design"),
        ("Agent-3", "(-1269, 1001)", "Infrastructure & DevOps"),
        ("Agent-4", "(-308, 1000)", "Quality Assurance (CAPTAIN)"),
        ("Agent-5", "(652, 421)", "Business Intelligence"),
        ("Agent-6", "(1612, 419)", "Coordination & Communication"),
        ("Agent-7", "(698, 936)", "Web Development"),
        ("Agent-8", "(1611, 941)", "Operations & Support"),
    ]

    for agent_id, coords, role in agents:
        embed.add_field(name=f"{agent_id}", value=f"**{role}**\n📍 {coords}", inline=True)

    embed.set_footer(text="Use !message <agent> <text> to send messages")

    await ctx.send(embed=embed)


@bot.command(name="agent_interact")
async def agent_interact(ctx):
    """Interactive agent messaging with dropdown. Usage: !agent_interact"""
    try:
        embed = discord.Embed(
            title="🤖 Interactive Agent Messaging",
            description="Select an agent from the dropdown below to send a message",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="How to use",
            value=(
                "1. Select an agent from the dropdown menu\n"
                "2. Type your message in the modal form\n"
                "3. Submit to send via PyAutoGUI!"
            ),
            inline=False,
        )

        view = messaging_controller.create_agent_messaging_view()
        await ctx.send(embed=embed, view=view)

    except Exception as e:
        logger.error(f"Error in agent_interact: {e}")
        await ctx.send(f"❌ Error creating interactive interface: {e}")


@bot.command(name="swarm_status")
async def interactive_status(ctx):
    """Interactive swarm status with detailed info + refresh button. Usage: !swarm_status"""
    try:
        # Use the messaging controller's view for refresh button functionality
        view = messaging_controller.create_swarm_status_view()
        embed = await view._create_status_embed()

        await ctx.send(embed=embed, view=view)
        logger.info("✅ Interactive swarm status with refresh button sent")

    except Exception as e:
        logger.error(f"Error in swarm_status: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description=f"Error getting swarm status: {e}",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


@bot.command(name="help")
async def show_help(ctx):
    """Show all commands."""
    embed = discord.Embed(
        title="🐝 DISCORD COMMANDER - REMOTE SWARM CONTROL",
        description="Control your swarm remotely from anywhere!",
        color=discord.Color.gold(),
    )

    embed.add_field(
        name="📝 Simple Text Commands",
        value=(
            "**Quick & Fast:**\n"
            "• `!message <agent> <text>` - Send to specific agent\n"
            "• `!broadcast <text>` - Broadcast to all agents\n"
            "• `!status` - Quick swarm status\n"
            "• `!agents` - List all agents\n"
            "\n**Examples:**\n"
            "`!message Agent-8 Check your inbox`\n"
            "`!broadcast All agents: complete tasks!`"
        ),
        inline=False,
    )

    embed.add_field(
        name="🎮 Interactive UI Commands",
        value=(
            "**Easy & Intuitive:**\n"
            "• `!agent_interact` - Dropdown agent selection + modal form\n"
            "• `!swarm_status` - Status with refresh button\n"
            "\n**Better UX:**\n"
            "- No typing errors (dropdowns)\n"
            "- Guided forms (modals)\n"
            "- Real-time updates (refresh buttons)"
        ),
        inline=False,
    )

    embed.add_field(
        name="ℹ️ Info Commands",
        value=(
            "• `!agents` - List all 8 agents with coordinates\n"
            "• `!help` - Show this help message"
        ),
        inline=False,
    )

    embed.add_field(
        name="🎯 Which to use?",
        value=(
            "**Text commands:** Fast for power users\n"
            "**Interactive UI:** Easy for everyone, mobile-friendly\n"
            "\n**Both work perfectly!** Use whatever you prefer."
        ),
        inline=False,
    )

    embed.set_footer(text="🐝 WE ARE SWARM - Remote coordination from anywhere!")

    await ctx.send(embed=embed)


async def main():
    """Main entry point."""
    token = os.getenv("DISCORD_BOT_TOKEN")

    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN not found!")
        print("\n❌ SETUP: Set DISCORD_BOT_TOKEN in .env file")
        return

    try:
        logger.info("🚀 Starting Discord Commander - Remote Swarm Control...")
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
