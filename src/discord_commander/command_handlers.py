#!/usr/bin/env python3
"""
Discord Commander Command Handlers
==================================

Command handlers for the Discord commander system.
Handles all Discord slash commands and interactions.
V2 COMPLIANT: Focused command handling under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR COMMAND HANDLERS
@license MIT
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import discord
from discord.ext import commands

from .discord_commander_models import (
    SwarmStatus, CommandResult, DiscordEmbed, create_discord_embed
)


class DiscordCommandHandlers:
    """Command handlers for Discord commander"""
    
    def __init__(self, swarm_status: SwarmStatus):
        """Initialize command handlers"""
        self.logger = logging.getLogger(__name__)
        self.swarm_status = swarm_status
    
    async def handle_status_command(self, ctx) -> discord.Embed:
        """Handle status command"""
        embed = create_discord_embed(
            title="🤖 Swarm Status Report",
            description="Current swarm operational status",
            color=0x3498db
        )
        
        embed.fields = [
            {"name": "Active Agents", "value": f"{len(self.swarm_status.active_agents)}/{self.swarm_status.total_agents}", "inline": True},
            {"name": "Current Cycle", "value": f"Cycle {self.swarm_status.current_cycle}", "inline": True},
            {"name": "System Health", "value": self.swarm_status.system_health, "inline": True},
            {"name": "Efficiency Rating", "value": f"{self.swarm_status.efficiency_rating}x", "inline": True},
            {"name": "Active Missions", "value": str(len(self.swarm_status.active_missions)), "inline": True},
            {"name": "Pending Tasks", "value": str(len(self.swarm_status.pending_tasks)), "inline": True}
        ]
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    async def handle_missions_command(self, ctx) -> discord.Embed:
        """Handle missions command"""
        embed = create_discord_embed(
            title="🎯 Active Missions",
            color=0xe74c3c
        )
        
        if self.swarm_status.active_missions:
            for i, mission in enumerate(self.swarm_status.active_missions, 1):
                embed.fields.append({
                    "name": f"Mission {i}",
                    "value": mission,
                    "inline": False
                })
        else:
            embed.fields.append({
                "name": "Status",
                "value": "No active missions",
                "inline": False
            })
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    async def handle_tasks_command(self, ctx) -> discord.Embed:
        """Handle tasks command"""
        embed = create_discord_embed(
            title="📋 Pending Tasks",
            color=0xf1c40f
        )
        
        if self.swarm_status.pending_tasks:
            for i, task in enumerate(self.swarm_status.pending_tasks, 1):
                embed.fields.append({
                    "name": f"Task {i}",
                    "value": task,
                    "inline": False
                })
        else:
            embed.fields.append({
                "name": "Status",
                "value": "No pending tasks",
                "inline": False
            })
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    async def handle_execute_command(self, ctx, agent: str, command: str) -> Dict[str, Any]:
        """Handle execute command"""
        if not self._is_valid_agent(agent):
            return {
                "success": False,
                "message": f"❌ Invalid agent: {agent}",
                "embed": None
            }
        
        # Create execution embed
        embed = create_discord_embed(
            title="⚡ Command Execution Started",
            color=0x27ae60
        )
        
        embed.fields = [
            {"name": "Target Agent", "value": agent, "inline": True},
            {"name": "Command", "value": command, "inline": True},
            {"name": "Status", "value": "🟡 Executing...", "inline": True}
        ]
        
        return {
            "success": True,
            "message": None,
            "embed": embed
        }
    
    async def handle_execute_result(self, agent: str, command: str, result: CommandResult) -> discord.Embed:
        """Handle execute command result"""
        embed = create_discord_embed(
            title="⚡ Command Execution Result",
            color=0x27ae60 if result.success else 0xe74c3c
        )
        
        embed.fields = [
            {"name": "Target Agent", "value": agent, "inline": True},
            {"name": "Command", "value": command, "inline": True},
            {"name": "Status", "value": "✅ Completed" if result.success else "❌ Failed", "inline": True}
        ]
        
        if result.message:
            embed.fields.append({
                "name": "Result",
                "value": result.message[:1024],
                "inline": False
            })
        
        if result.execution_time:
            embed.fields.append({
                "name": "Execution Time",
                "value": f"{result.execution_time:.2f}s",
                "inline": True
            })
        
        return embed
    
    async def handle_broadcast_command(self, ctx, message: str) -> discord.Embed:
        """Handle broadcast command"""
        embed = create_discord_embed(
            title="📢 Swarm Broadcast",
            description=message,
            color=0x9b59b6
        )
        
        embed.fields = [
            {"name": "Broadcaster", "value": ctx.author.display_name, "inline": True},
            {"name": "Target", "value": "All Agents", "inline": True},
            {"name": "Status", "value": "🟡 Broadcasting...", "inline": True}
        ]
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    async def handle_broadcast_result(self, success: bool, message: str) -> discord.Embed:
        """Handle broadcast command result"""
        embed = create_discord_embed(
            title="📢 Broadcast Result",
            color=0x27ae60 if success else 0xe74c3c
        )
        
        embed.fields = [
            {"name": "Status", "value": "✅ Broadcast Sent" if success else "❌ Broadcast Failed", "inline": True},
            {"name": "Target", "value": "All Agents", "inline": True}
        ]
        
        if not success:
            embed.fields.append({
                "name": "Error",
                "value": message[:1024],
                "inline": False
            })
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    async def handle_human_prompt_command(self, ctx, prompt: str) -> Dict[str, Any]:
        """Handle human prompt command"""
        embed = create_discord_embed(
            title="👤 Human Prompt to Captain",
            description=prompt[:500] + "..." if len(prompt) > 500 else prompt,
            color=0x3498db
        )
        
        embed.fields = [
            {"name": "Target Agent", "value": "Agent-4 (Captain)", "inline": True},
            {"name": "Sender", "value": ctx.author.display_name, "inline": True},
            {"name": "Status", "value": "🟡 Sending...", "inline": True}
        ]
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        
        return {
            "success": True,
            "message": None,
            "embed": embed
        }
    
    async def handle_human_prompt_result(self, success: bool, message: str, prompt: str) -> discord.Embed:
        """Handle human prompt command result"""
        embed = create_discord_embed(
            title="👤 Human Prompt Result",
            color=0x27ae60 if success else 0xe74c3c
        )
        
        embed.fields = [
            {"name": "Target Agent", "value": "Agent-4 (Captain)", "inline": True},
            {"name": "Status", "value": "✅ Delivered" if success else "❌ Failed", "inline": True}
        ]
        
        if success:
            embed.fields.append({
                "name": "Prompt Preview",
                "value": prompt[:500] + "..." if len(prompt) > 500 else prompt,
                "inline": False
            })
        else:
            embed.fields.append({
                "name": "Error",
                "value": message[:1024],
                "inline": False
            })
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    async def handle_captain_status_command(self, ctx, status_data: Dict[str, Any]) -> discord.Embed:
        """Handle captain status command"""
        embed = create_discord_embed(
            title="🎯 Captain Agent-4 Status Report",
            color=0x3498db
        )
        
        embed.fields = [
            {"name": "Agent ID", "value": status_data.get("agent_id", "Unknown"), "inline": True},
            {"name": "Mission Priority", "value": status_data.get("mission_priority", "Unknown"), "inline": True},
            {"name": "Last Updated", "value": status_data.get("last_updated", "Unknown"), "inline": True}
        ]
        
        # Add current mission
        current_mission = status_data.get("current_mission", "Unknown")
        embed.fields.append({
            "name": "Current Mission",
            "value": current_mission[:500],
            "inline": False
        })
        
        # Add current tasks if available
        current_tasks = status_data.get("current_tasks", [])
        if current_tasks:
            tasks_text = "\n".join([f"• {task[:100]}" for task in current_tasks[:3]])
            embed.fields.append({
                "name": "Current Tasks",
                "value": tasks_text,
                "inline": False
            })
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    def _is_valid_agent(self, agent: str) -> bool:
        """Check if agent name is valid"""
        return agent in [f"Agent-{i}" for i in range(1, 9)]


# Factory function for dependency injection
def create_discord_command_handlers(swarm_status: SwarmStatus) -> DiscordCommandHandlers:
    """Factory function to create Discord command handlers"""
    return DiscordCommandHandlers(swarm_status)


# Export for DI
__all__ = ['DiscordCommandHandlers', 'create_discord_command_handlers']
