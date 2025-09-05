#!/usr/bin/env python3
"""
Discord Commander Orchestrator
==============================

Main orchestrator for the Discord commander system.
Coordinates all components and provides unified interface.
V2 COMPLIANT: Focused orchestration under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR ORCHESTRATOR
@license MIT
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import discord
from discord.ext import commands

from .discord_commander_models import SwarmStatus, create_swarm_status
from .configuration_manager import DiscordConfigurationManager, create_discord_configuration_manager
from .command_handlers import DiscordCommandHandlers, create_discord_command_handlers
from .agent_communication_engine import AgentCommunicationEngine, create_agent_communication_engine
from .discord_integration_engine import DiscordIntegrationEngine, create_discord_integration_engine


class DiscordCommanderOrchestrator(commands.Bot):
    """Main Discord Commander orchestrator for swarm coordination"""
    
    def __init__(self, command_prefix: str = "!", intents: discord.Intents = None):
        """Initialize Discord Commander orchestrator"""
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True

        super().__init__(command_prefix=command_prefix, intents=intents)
        
        # Initialize components
        self.config_manager = create_discord_configuration_manager()
        self.config = self.config_manager.load_config()
        self.swarm_status = create_swarm_status()
        self.command_handlers = create_discord_command_handlers(self.swarm_status)
        self.agent_comm = create_agent_communication_engine()
        self.discord_integration = create_discord_integration_engine(self.config, self.swarm_status)
        
        # Command tracking
        self.command_history: List[Dict] = []
        self.active_commands: Dict[str, asyncio.Task] = {}
        
        # Captain agent
        self.captain_agent = "Agent-4"
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Discord Commander Orchestrator initialized")
    
    async def on_ready(self):
        """Called when the bot is ready and connected"""
        self.logger.info(f"Discord Commander connected as {self.user}")
        
        # Initialize channels
        for guild in self.guilds:
            if str(guild.id) == self.config.guild_id:
                success = await self.discord_integration.initialize_channels(guild)
                if success:
                    await self.discord_integration.send_startup_message()
                break
    
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.MissingRole):
            await ctx.send("❌ You don't have permission to use this command.")
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument: {error.param}")
            return
        
        self.logger.error(f"Command error: {error}")
        await ctx.send(f"❌ An error occurred: {str(error)}")
    
    # ================================
    # STATUS COMMANDS
    # ================================
    
    @commands.command(name="status")
    async def status_command(self, ctx):
        """Get swarm status"""
        embed = await self.command_handlers.handle_status_command(ctx)
        await ctx.send(embed=embed)
    
    @commands.command(name="missions")
    async def missions_command(self, ctx):
        """List all active missions"""
        embed = await self.command_handlers.handle_missions_command(ctx)
        await ctx.send(embed=embed)
    
    @commands.command(name="tasks")
    async def tasks_command(self, ctx):
        """List pending tasks"""
        embed = await self.command_handlers.handle_tasks_command(ctx)
        await ctx.send(embed=embed)
    
    # ================================
    # EXECUTION COMMANDS
    # ================================
    
    @commands.command(name="execute")
    @commands.has_role("Captain")
    async def execute_command(self, ctx, agent: str, *, command: str):
        """Execute a command on a specific agent"""
        result = await self.command_handlers.handle_execute_command(ctx, agent, command)
        
        if not result["success"]:
            await ctx.send(result["message"])
            return
        
        message = await ctx.send(embed=result["embed"])
        
        try:
            # Execute command
            command_result = await self.agent_comm.execute_agent_command(agent, command)
            
            # Update embed with results
            updated_embed = await self.command_handlers.handle_execute_result(agent, command, command_result)
            await message.edit(embed=updated_embed)
            
        except Exception as e:
            self.logger.error(f"Command execution error: {e}")
            error_embed = self.discord_integration.create_error_embed("Command Execution Error", str(e))
            await message.edit(embed=error_embed)
    
    @commands.command(name="broadcast")
    @commands.has_role("Captain")
    async def broadcast_command(self, ctx, *, message: str):
        """Broadcast message to all agents"""
        embed = await self.command_handlers.handle_broadcast_command(ctx, message)
        msg = await ctx.send(embed=embed)
        
        try:
            result = await self.agent_comm.broadcast_to_all_agents(message, ctx.author.display_name)
            updated_embed = await self.command_handlers.handle_broadcast_result(result.success, result.message)
            await msg.edit(embed=updated_embed)
            
        except Exception as e:
            self.logger.error(f"Broadcast error: {e}")
            error_embed = self.discord_integration.create_error_embed("Broadcast Error", str(e))
            await msg.edit(embed=error_embed)
    
    # ================================
    # HUMAN INTERACTION COMMANDS
    # ================================
    
    @commands.command(name="prompt")
    async def human_prompt_command(self, ctx, *, prompt: str):
        """Send human prompt to Captain Agent-4"""
        result = await self.command_handlers.handle_human_prompt_command(ctx, prompt)
        
        if not result["success"]:
            await ctx.send(result["message"])
            return
        
        message = await ctx.send(embed=result["embed"])
        
        try:
            command_result = await self.agent_comm.send_human_prompt_to_captain(prompt, ctx.author.display_name)
            updated_embed = await self.command_handlers.handle_human_prompt_result(
                command_result.success, command_result.message, prompt
            )
            await message.edit(embed=updated_embed)
            
        except Exception as e:
            self.logger.error(f"Human prompt error: {e}")
            error_embed = self.discord_integration.create_error_embed("Human Prompt Error", str(e))
            await message.edit(embed=error_embed)
    
    @commands.command(name="captain_status")
    async def captain_status_command(self, ctx):
        """Get Captain Agent-4's current status"""
        try:
            status_data = await self.agent_comm.read_agent_status("Agent-4")
            
            if status_data:
                embed = await self.command_handlers.handle_captain_status_command(ctx, status_data)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Captain Agent-4 status file not found")
                
        except Exception as e:
            self.logger.error(f"Captain status error: {e}")
            await ctx.send(f"❌ Error reading Captain status: {str(e)}")
    
    # ================================
    # LIFECYCLE METHODS
    # ================================
    
    async def close(self):
        """Clean shutdown of the Discord commander"""
        self.logger.info("Shutting down Discord Commander...")
        
        # Cancel all active commands
        for task in self.active_commands.values():
            if not task.done():
                task.cancel()
        
        # Send shutdown message
        await self.discord_integration.send_shutdown_message()
        
        await super().close()
        self.logger.info("Discord Commander shutdown complete")
    
    # ================================
    # UTILITY METHODS
    # ================================
    
    def is_valid_agent(self, agent: str) -> bool:
        """Check if agent name is valid"""
        return self.agent_comm.is_valid_agent(agent)
    
    async def cleanup_completed_commands(self):
        """Clean up completed command tasks"""
        completed = []
        for command_id, task in self.active_commands.items():
            if task.done():
                completed.append(command_id)
        
        for command_id in completed:
            del self.active_commands[command_id]


# Factory function for dependency injection
def create_discord_commander_orchestrator() -> DiscordCommanderOrchestrator:
    """Factory function to create Discord commander orchestrator"""
    return DiscordCommanderOrchestrator()


# Export for DI
__all__ = ['DiscordCommanderOrchestrator', 'create_discord_commander_orchestrator']
