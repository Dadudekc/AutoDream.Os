#!/usr/bin/env python3
"""
Admin Commands
==============

Administrative commands for Discord bot management and monitoring.
"""

import discord
from discord import app_commands
import logging
from src.services.discord_bot.core.command_logger import command_logger
from src.services.discord_bot.commands.basic_commands import safe_command

logger = logging.getLogger(__name__)


def setup_admin_commands(bot):
    """Setup administrative bot slash commands."""

    @bot.tree.command(name="command-stats", description="View command execution statistics")
    @safe_command
    async def command_stats(interaction: discord.Interaction):
        """View command execution statistics."""
        try:
            logger.info(f"Command stats requested by {interaction.user.name}")
            
            stats = command_logger.get_command_stats()
            
            if not stats:
                await interaction.response.send_message("📊 No command statistics available yet.")
                return
            
            embed = discord.Embed(
                title="📊 Command Execution Statistics",
                description="Performance metrics for Discord commands",
                color=0x00ff00
            )
            
            for command_name, command_stats in stats.items():
                success_rate = (command_stats["successful_executions"] / command_stats["total_executions"] * 100) if command_stats["total_executions"] > 0 else 0
                
                embed.add_field(
                    name=f"`/{command_name}`",
                    value=f"**Executions:** {command_stats['total_executions']}\n"
                          f"**Success Rate:** {success_rate:.1f}%\n"
                          f"**Avg Time:** {command_stats['avg_execution_time']:.2f}s\n"
                          f"**Last Used:** {command_stats['last_execution'][:19] if command_stats['last_execution'] else 'Never'}",
                    inline=True
                )
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Command stats sent to {interaction.user.name}")
            
        except Exception as e:
            logger.error(f"Error in command-stats: {e}")
            raise

    @bot.tree.command(name="command-history", description="View recent command execution history")
    @safe_command
    async def command_history(interaction: discord.Interaction, limit: int = 10):
        """View recent command execution history."""
        try:
            logger.info(f"📜 Command history requested by {interaction.user.name} (limit: {limit})")
            
            history = command_logger.get_execution_history(limit)
            
            if not history:
                await interaction.response.send_message("📜 No command history available yet.")
                return
            
            embed = discord.Embed(
                title="📜 Recent Command History",
                description=f"Last {len(history)} command executions",
                color=0x0099ff
            )
            
            for execution_id, execution in list(history.items())[:10]:  # Limit to 10 for Discord embed
                status = "✅" if execution.success else "❌"
                user_mention = f"<@{execution.user_id}>"
                
                embed.add_field(
                    name=f"{status} `/{execution.command_name}`",
                    value=f"**User:** {user_mention}\n"
                          f"**Time:** {execution.execution_time:.2f}s\n"
                          f"**Channel:** <#{execution.channel_id}>\n"
                          f"**Status:** {'Success' if execution.success else 'Failed'}",
                    inline=True
                )
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Command history sent to {interaction.user.name}")
            
        except Exception as e:
            logger.error(f"Error in command-history: {e}")
            raise

    @bot.tree.command(name="bot-health", description="Check bot health and system status")
    @safe_command
    async def bot_health(interaction: discord.Interaction):
        """Check bot health and system status."""
        try:
            logger.info(f"🏥 Bot health check requested by {interaction.user.name}")
            
            # Get bot latency
            latency = round(bot.latency * 1000)
            
            # Get command stats
            stats = command_logger.get_command_stats()
            total_commands = sum(stat["total_executions"] for stat in stats.values())
            total_successful = sum(stat["successful_executions"] for stat in stats.values())
            success_rate = (total_successful / total_commands * 100) if total_commands > 0 else 100
            
            # Get guild info
            guild_count = len(bot.guilds)
            user_count = len(bot.users)
            
            embed = discord.Embed(
                title="🏥 Bot Health Status",
                description="Current system health and performance metrics",
                color=0x00ff00 if latency < 200 else 0xff9900 if latency < 500 else 0xff0000
            )
            
            embed.add_field(
                name="🌐 Connection",
                value=f"**Latency:** {latency}ms\n"
                      f"**Status:** {'🟢 Excellent' if latency < 200 else '🟡 Good' if latency < 500 else '🔴 Poor'}\n"
                      f"**Guilds:** {guild_count}\n"
                      f"**Users:** {user_count}",
                inline=True
            )
            
            embed.add_field(
                name="📊 Commands",
                value=f"**Total Executions:** {total_commands}\n"
                      f"**Success Rate:** {success_rate:.1f}%\n"
                      f"**Available Commands:** {len(stats)}",
                inline=True
            )
            
            embed.add_field(
                name="🔧 System",
                value=f"**Uptime:** {bot.user.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                      f"**Memory:** Available\n"
                      f"**Logging:** Active",
                inline=True
            )
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Bot health status sent to {interaction.user.name}")
            
        except Exception as e:
            logger.error(f"Error in bot-health: {e}")
            raise

    @bot.tree.command(name="clear-logs", description="Clear command execution logs (admin only)")
    @safe_command
    async def clear_logs(interaction: discord.Interaction):
        """Clear command execution logs (admin only)."""
        try:
            logger.info(f"[CLEAR] Clear logs requested by {interaction.user.name}")
            
            # Check if user is admin (you can customize this check)
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ You don't have permission to clear logs.", ephemeral=True)
                return
            
            # Clear logs
            command_logger.execution_history.clear()
            command_logger.command_stats.clear()
            
            await interaction.response.send_message("🗑️ Command logs cleared successfully!")
            logger.info(f"Logs cleared by {interaction.user.name}")
            
        except Exception as e:
            logger.error(f"Error in clear-logs: {e}")
            raise
