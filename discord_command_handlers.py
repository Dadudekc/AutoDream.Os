#!/usr/bin/env python3
"""
Discord Commander - Command Handlers
Extracted command functions for Lean Excellence compliance.

Author: Agent-7 (Web Development)
Date: 2025-10-14
Purpose: Reduce run_discord_commander.py from 462→400 lines
"""

import asyncio
import logging
import os
import re
from pathlib import Path

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class DiscordCommandHandlers:
    """All Discord bot command handlers."""

    def __init__(self, bot, messaging_controller, status_reader):
        """Initialize handlers."""
        self.bot = bot
        self.messaging_controller = messaging_controller
        self.status_reader = status_reader

    async def message_agent(self, ctx, agent_id: str, message: str):
        """Send message to specific agent."""
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

    async def broadcast_message(self, ctx, message: str):
        """Broadcast to all agents."""
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

    async def quick_status(self, ctx):
        """Detailed swarm status from status.json."""
        try:
            logger.info("📊 Discord command: detailed status")

            statuses = self.status_reader.read_all_statuses()

            if not statuses:
                await ctx.send("❌ Could not read agent status files")
                return

            # Calculate totals
            total_points = sum(
                s.get("sprint_info", {}).get("points_completed", 0) for s in statuses.values()
            )
            total_agents = len(statuses)
            active = sum(
                1 for s in statuses.values() if "ACTIVE" in str(s.get("status", "")).upper()
            )

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

    async def list_agents(self, ctx):
        """List all agents."""
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

    async def agent_interact(self, ctx):
        """Interactive agent messaging with dropdown."""
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

            view = self.messaging_controller.create_agent_messaging_view()
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            logger.error(f"Error in agent_interact: {e}")
            await ctx.send(f"❌ Error creating interactive interface: {e}")

    async def interactive_status(self, ctx):
        """Interactive swarm status with detailed info + refresh button."""
        try:
            # Use the messaging controller's view for refresh button functionality
            view = self.messaging_controller.create_swarm_status_view()
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

    async def live_status_monitor(self, ctx):
        """🔥 LIVE status.json monitoring with auto-updates!"""
        try:
            logger.info("🔥 Starting LIVE status monitor")

            # Create initial embed
            statuses = self.status_reader.read_all_statuses()

            embed = self._create_live_embed(statuses, 0)

            # Send initial message
            message = await ctx.send(embed=embed)
            logger.info("✅ LIVE status monitor started")

            # Auto-update loop (10 times = 100 seconds)
            for i in range(10):
                await asyncio.sleep(10)

                # Re-read statuses
                statuses = self.status_reader.read_all_statuses()

                # Recreate embed with updated data
                embed = self._create_live_embed(statuses, i + 1)

                await message.edit(embed=embed)

            # Final update
            embed.set_footer(
                text="✅ Live monitoring complete (100 seconds) | Use !live_status to restart"
            )
            await message.edit(embed=embed)
            logger.info("✅ LIVE status monitor completed")

        except Exception as e:
            await ctx.send(f"❌ Error: {e}")
            logger.error(f"Error in live_status command: {e}")

    def _create_live_embed(self, statuses, update_num):
        """Create live status embed with current data."""
        title = (
            "🔥 LIVE SWARM STATUS - AUTO-UPDATING"
            if update_num == 0
            else f"🔥 LIVE SWARM STATUS - Update #{update_num}/10"
        )

        embed = discord.Embed(
            title=title,
            description="Real-time status.json monitoring with WOW factor! 🚀",
            color=discord.Color.gold(),
        )

        # Calculate totals
        total_points = sum(
            s.get("sprint_info", {}).get("points_completed", 0) for s in statuses.values()
        )
        active = sum(1 for s in statuses.values() if "ACTIVE" in str(s.get("status", "")).upper())
        legendary = sum(
            1 for s in statuses.values() if "LEGENDARY" in str(s.get("status", "")).upper()
        )

        embed.add_field(
            name="🎯 SWARM METRICS",
            value=f"**Agents:** 8/8 | **Active:** {active} | **Legendary:** {legendary} | **Points:** {total_points:,}",
            inline=False,
        )

        # Individual agents with WOW factor
        for agent_id in sorted(statuses.keys()):
            data = statuses[agent_id]
            status = data.get("status", "UNKNOWN")

            # Enhanced status emoji
            if "LEGENDARY" in status.upper():
                emoji = "🏆"
            elif "COMPLETE" in status.upper():
                emoji = "✅"
            elif "ACTIVE" in status.upper():
                emoji = "🟢"
            elif "EXECUTING" in status.upper():
                emoji = "⚡"
            else:
                emoji = "🟡"

            mission = data.get("current_mission", "No mission")[:60]
            points = data.get("sprint_info", {}).get("points_completed", 0)
            session_points = data.get("sprint_info", {}).get("session_2025_10_14", "")

            # Extract session points if available
            session_info = ""
            if "LEGENDARY" in str(session_points):
                match = re.search(r"(\d+,?\d*)\s*points", session_points)
                if match:
                    session_info = f" | 🔥 Session: {match.group(1)} pts!"

            value_text = (
                f"**Status:** {status[:30]}\n**Mission:** {mission}\n**Points:** {points:,}{session_info}"
            )

            embed.add_field(
                name=f"{emoji} {agent_id}",
                value=value_text,
                inline=False,
            )

        if update_num == 0:
            embed.set_footer(text="🔄 Auto-refreshes every 10 seconds! | 🐝 WE ARE SWARM")
        else:
            embed.set_footer(text=f"🔄 Auto-update {update_num}/10 | Next in 10s | 🐝 WE ARE SWARM")

        return embed

    async def show_help(self, ctx):
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
                "• `!live_status` 🔥 - LIVE auto-updating status (WOW FACTOR!)\n"
                "\n**Better UX:**\n"
                "- No typing errors (dropdowns)\n"
                "- Guided forms (modals)\n"
                "- Real-time updates (refresh buttons)\n"
                "- 🔥 Live monitoring (auto-updates every 10s!)"
            ),
            inline=False,
        )

        embed.add_field(
            name="ℹ️ Info Commands",
            value=("• `!agents` - List all 8 agents with coordinates\n" "• `!help` - Show this help message"),
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


def register_commands(bot, handlers):
    """Register all command handlers with the bot."""

    @bot.command(name="message")
    async def message_command(ctx, agent_id: str, *, message: str):
        """Send message to specific agent."""
        await handlers.message_agent(ctx, agent_id, message)

    @bot.command(name="broadcast")
    async def broadcast_command(ctx, *, message: str):
        """Broadcast to all agents."""
        await handlers.broadcast_message(ctx, message)

    @bot.command(name="status")
    async def status_command(ctx):
        """Detailed swarm status."""
        await handlers.quick_status(ctx)

    @bot.command(name="agents")
    async def agents_command(ctx):
        """List all agents."""
        await handlers.list_agents(ctx)

    @bot.command(name="agent_interact")
    async def interact_command(ctx):
        """Interactive agent messaging."""
        await handlers.agent_interact(ctx)

    @bot.command(name="swarm_status")
    async def swarm_command(ctx):
        """Interactive swarm status."""
        await handlers.interactive_status(ctx)

    @bot.command(name="live_status")
    async def live_command(ctx):
        """Live status monitoring."""
        await handlers.live_status_monitor(ctx)

    @bot.command(name="help")
    async def help_command(ctx):
        """Show help."""
        await handlers.show_help(ctx)

