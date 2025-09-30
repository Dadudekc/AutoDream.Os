"""
Discord Commander Bot Commands
Command implementations for Discord bot functionality
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

from .bot_core import BotCore, CommandContext, EmbedBuilder


class CommandManager:
    """Command management system"""
    
    def __init__(self, bot_core: BotCore):
        self.bot_core = bot_core
        self.commands_registered: List[str] = []
        self.command_history: List[Dict[str, Any]] = []
    
    def register_commands(self, bot: commands.Bot) -> None:
        """Register all bot commands"""
        if not DISCORD_AVAILABLE:
            return
        
        @bot.command(name="ping")
        async def ping_command(ctx: commands.Context):
            """Ping command to test bot responsiveness"""
            await self._handle_ping_command(ctx)
        
        @bot.command(name="status")
        async def status_command(ctx: commands.Context):
            """Get bot status information"""
            await self._handle_status_command(ctx)
        
        @bot.command(name="help")
        async def help_command(ctx: commands.Context):
            """Show help information"""
            await self._handle_help_command(ctx)
        
        @bot.command(name="agents")
        async def agents_command(ctx: commands.Context):
            """Show agent information"""
            await self._handle_agents_command(ctx)
        
        @bot.command(name="swarm")
        async def swarm_command(ctx: commands.Context):
            """Show swarm coordination information"""
            await self._handle_swarm_command(ctx)
        
        self.commands_registered = ["ping", "status", "help", "agents", "swarm"]
    
    async def _handle_ping_command(self, ctx: commands.Context) -> None:
        """Handle ping command"""
        try:
            context = CommandContext(ctx)
            latency = round(self.bot_core.bot.latency * 1000) if self.bot_core.bot else 0
            
            embed = EmbedBuilder.create_success_embed(
                "Pong!",
                f"Latency: {latency}ms\nBot is responsive!"
            )
            
            await ctx.send(embed=embed)
            self._log_command_execution("ping", context.user.name, True)
            
        except Exception as e:
            await self._handle_command_error(ctx, "ping", str(e))
    
    async def _handle_status_command(self, ctx: commands.Context) -> None:
        """Handle status command"""
        try:
            context = CommandContext(ctx)
            status_info = self.bot_core.get_status_info()
            
            embed = EmbedBuilder.create_info_embed(
                "Bot Status",
                f"**Online:** {'Yes' if status_info['is_online'] else 'No'}\n"
                f"**Uptime:** {status_info['uptime']}\n"
                f"**Commands Executed:** {status_info['commands_executed']}\n"
                f"**Errors:** {status_info['errors_count']}\n"
                f"**Last Error:** {status_info['last_error'] or 'None'}"
            )
            
            await ctx.send(embed=embed)
            self._log_command_execution("status", context.user.name, True)
            
        except Exception as e:
            await self._handle_command_error(ctx, "status", str(e))
    
    async def _handle_help_command(self, ctx: commands.Context) -> None:
        """Handle help command"""
        try:
            context = CommandContext(ctx)
            
            embed = EmbedBuilder.create_info_embed(
                "Help - Available Commands",
                "**!ping** - Test bot responsiveness\n"
                "**!status** - Get bot status information\n"
                "**!help** - Show this help message\n"
                "**!agents** - Show agent information\n"
                "**!swarm** - Show swarm coordination info\n\n"
                "Use `!help <command>` for detailed information about a specific command."
            )
            
            await ctx.send(embed=embed)
            self._log_command_execution("help", context.user.name, True)
            
        except Exception as e:
            await self._handle_command_error(ctx, "help", str(e))
    
    async def _handle_agents_command(self, ctx: commands.Context) -> None:
        """Handle agents command"""
        try:
            context = CommandContext(ctx)
            
            embed = EmbedBuilder.create_info_embed(
                "Agent Information",
                "**Active Agents:**\n"
                "• Agent-4 (Captain) - Strategic oversight\n"
                "• Agent-5 (Coordinator) - Inter-agent coordination\n"
                "• Agent-6 (Quality) - Quality assurance\n"
                "• Agent-7 (Implementation) - Web development\n"
                "• Agent-8 (Integration) - System integration\n\n"
                "**Status:** All agents are active and coordinating via PyAutoGUI messaging."
            )
            
            await ctx.send(embed=embed)
            self._log_command_execution("agents", context.user.name, True)
            
        except Exception as e:
            await self._handle_command_error(ctx, "agents", str(e))
    
    async def _handle_swarm_command(self, ctx: commands.Context) -> None:
        """Handle swarm command"""
        try:
            context = CommandContext(ctx)
            
            embed = EmbedBuilder.create_info_embed(
                "Swarm Coordination",
                "**Current Mode:** 5-Agent Quality Focus Team\n"
                "**Coordination:** PyAutoGUI messaging system\n"
                "**Status:** Active swarm intelligence\n"
                "**Capabilities:**\n"
                "• Real-time agent coordination\n"
                "• Dynamic role assignment\n"
                "• Quality gates enforcement\n"
                "• Vector database intelligence\n\n"
                "🐝 **WE ARE SWARM** - Autonomous agent coordination system"
            )
            
            await ctx.send(embed=embed)
            self._log_command_execution("swarm", context.user.name, True)
            
        except Exception as e:
            await self._handle_command_error(ctx, "swarm", str(e))
    
    async def _handle_command_error(self, ctx: commands.Context, command: str, error: str) -> None:
        """Handle command execution error"""
        embed = EmbedBuilder.create_error_embed(
            f"Command Error: {command}",
            f"An error occurred while executing the command:\n```{error}```"
        )
        
        await ctx.send(embed=embed)
        self.bot_core.status.errors_count += 1
        self.bot_core.status.last_error = error
        self._log_command_execution(command, ctx.author.name, False, error)
    
    def _log_command_execution(self, command: str, user: str, success: bool, error: Optional[str] = None) -> None:
        """Log command execution"""
        execution_log = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "user": user,
            "success": success,
            "error": error
        }
        
        self.command_history.append(execution_log)
        self.bot_core.status.commands_executed += 1
        
        if success:
            self.bot_core.logger.info(f"Command '{command}' executed successfully by {user}")
        else:
            self.bot_core.logger.error(f"Command '{command}' failed for {user}: {error}")
    
    def get_command_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent command history"""
        return self.command_history[-limit:] if self.command_history else []
    
    def get_command_stats(self) -> Dict[str, Any]:
        """Get command statistics"""
        if not self.command_history:
            return {"total": 0, "successful": 0, "failed": 0, "success_rate": 0.0}
        
        total = len(self.command_history)
        successful = sum(1 for log in self.command_history if log["success"])
        failed = total - successful
        success_rate = (successful / total) * 100 if total > 0 else 0.0
        
        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": success_rate
        }