#!/usr/bin/env python3
"""
Agent Status Handler - V2 Compliant
===================================

Handles agent status checking functionality for Discord bot.
V2 Compliance: ≤200 lines, single responsibility, KISS principle.
"""

import discord
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AgentStatusHandler:
    """Handles agent status checking functionality."""
    
    def __init__(self, core):
        """Initialize status handler."""
        self.core = core
    
    async def handle_agent_status_check(self, interaction, agent_id):
        """Handle agent status check."""
        
        try:
            # Get agent status (mock implementation)
            status = self.get_agent_status(agent_id)
            
            # Create status embed
            embed = discord.Embed(
                title=f"📊 {agent_id} Status Report",
                description=f"**Current status of {agent_id}**",
                color=self.get_status_color(status["status"])
            )
            
            embed.add_field(
                name="📋 **Status Information**",
                value=f"• **Status:** {status['status']}\n• **Last Active:** {status['last_active']}\n• **Current Task:** {status['current_task']}\n• **Team:** {status['team']}",
                inline=False
            )
            
            embed.add_field(
                name="📈 **Performance Metrics**",
                value=f"• **Tasks Completed:** {status['tasks_completed']}\n• **Success Rate:** {status['success_rate']}\n• **Uptime:** {status['uptime']}",
                inline=False
            )
            
            embed.set_footer(text=f"🐝 WE ARE SWARM — {agent_id} Status Report")
            
            # Create status view
            view = discord.ui.View(timeout=300)
            
            # Refresh button
            refresh_btn = discord.ui.Button(
                label="🔄 Refresh Status",
                style=discord.ButtonStyle.primary,
                custom_id=f"refresh_status:{agent_id}"
            )
            refresh_btn.callback = lambda inter: self.handle_agent_status_check(inter, agent_id)
            view.add_item(refresh_btn)
            
            # Back to agent button
            back_btn = discord.ui.Button(
                label="⬅️ Back to Agent",
                style=discord.ButtonStyle.secondary,
                custom_id="back_to_agent"
            )
            
            async def back_callback(inter):
                await self.core.handle_agent_selection(inter, agent_id)
            
            back_btn.callback = back_callback
            view.add_item(back_btn)
            
            await interaction.response.edit_message(embed=embed, view=view)
            
        except Exception as e:
            logger.error(f"Failed to get status for agent {agent_id}: {e}")
            
            # Create error embed
            error_embed = discord.Embed(
                title=f"❌ Status Check Failed",
                description=f"Failed to retrieve status for **{agent_id}**",
                color=0xFF0000
            )
            
            error_embed.add_field(
                name="🔍 **Error Details**",
                value="An error occurred while checking agent status. Please try again.",
                inline=False
            )
            
            await interaction.response.edit_message(embed=error_embed, view=None)
    
    def get_agent_status(self, agent_id):
        """Get agent status information."""
        # Mock status data - in real implementation, this would query actual agent status
        status_data = {
            "Agent-1": {
                "status": "Active",
                "last_active": "2 minutes ago",
                "current_task": "API Integration Hub Development",
                "team": "Team Alpha",
                "tasks_completed": 15,
                "success_rate": "98%",
                "uptime": "99.5%"
            },
            "Agent-2": {
                "status": "Active",
                "last_active": "5 minutes ago",
                "current_task": "Architecture Design Review",
                "team": "Team Alpha",
                "tasks_completed": 12,
                "success_rate": "96%",
                "uptime": "99.2%"
            },
            "Agent-3": {
                "status": "Active",
                "last_active": "1 minute ago",
                "current_task": "Database Optimization",
                "team": "Team Beta",
                "tasks_completed": 18,
                "success_rate": "99%",
                "uptime": "99.8%"
            },
            "Agent-4": {
                "status": "Active",
                "last_active": "Just now",
                "current_task": "Technical Debt Elimination",
                "team": "Team Gamma",
                "tasks_completed": 20,
                "success_rate": "100%",
                "uptime": "100%"
            }
        }
        
        # Return status for specific agent or default status
        return status_data.get(agent_id, {
            "status": "Unknown",
            "last_active": "Unknown",
            "current_task": "No active task",
            "team": "Unassigned",
            "tasks_completed": 0,
            "success_rate": "0%",
            "uptime": "0%"
        })
    
    def get_status_color(self, status):
        """Get color for status."""
        status_colors = {
            "Active": 0x00FF00,
            "Idle": 0xFFFF00,
            "Busy": 0xFF9900,
            "Error": 0xFF0000,
            "Unknown": 0x808080
        }
        return status_colors.get(status, 0x808080)
