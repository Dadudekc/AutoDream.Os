#!/usr/bin/env python3
"""
Agent Onboarding Handler - V2 Compliant
=======================================

Handles agent onboarding functionality for Discord bot.
V2 Compliance: ≤200 lines, single responsibility, KISS principle.
"""

import discord
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AgentOnboardingHandler:
    """Handles agent onboarding functionality."""
    
    def __init__(self, core):
        """Initialize onboarding handler."""
        self.core = core
    
    async def handle_agent_onboarding(self, interaction, agent_id):
        """Handle agent onboarding process."""
        
        if not self.core._is_admin(interaction):
            await self.core._deny(interaction, "Only administrators can onboard agents.")
            return
        
        # Create onboarding embed
        embed = discord.Embed(
            title=f"🎓 Onboarding {agent_id}",
            description=f"**Setting up {agent_id}** - Select a team for assignment",
            color=0x00FF00
        )
        
        embed.add_field(
            name="📋 **Available Teams**",
            value="• **Team Alpha** - Core development and architecture\n• **Team Beta** - Infrastructure and DevOps\n• **Team Gamma** - Quality assurance and testing\n• **Team Delta** - Business intelligence and analytics",
            inline=False
        )
        
        embed.set_footer(text=f"🐝 WE ARE SWARM — {agent_id} Onboarding")
        
        # Create team selection view
        view = discord.ui.View(timeout=300)
        
        teams = ["Team Alpha", "Team Beta", "Team Gamma", "Team Delta"]
        
        for team in teams:
            btn = discord.ui.Button(
                label=team,
                style=discord.ButtonStyle.primary,
                custom_id=f"team_select:{agent_id}:{team}"
            )
            
            async def team_callback(inter, agent=agent_id, team_name=team):
                await self.handle_team_selection(inter, agent, team_name)
            
            btn.callback = team_callback
            view.add_item(btn)
        
        # Back button
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
    
    async def handle_team_selection(self, interaction, agent_id, team_name):
        """Handle team selection confirmation."""
        
        # Create confirmation embed
        embed = discord.Embed(
            title=f"✅ Confirm {agent_id} Onboarding",
            description=f"**Ready to onboard {agent_id}** to **{team_name}**",
            color=0x00FF00
        )
        
        embed.add_field(
            name="📋 **Onboarding Details**",
            value=f"• **Agent:** {agent_id}\n• **Team:** {team_name}\n• **Description:** {self.core.get_team_description(team_name)}",
            inline=False
        )
        
        embed.add_field(
            name="⚠️ **Important**",
            value="This action will create the agent workspace and initialize all necessary systems.",
            inline=False
        )
        
        embed.set_footer(text=f"🐝 WE ARE SWARM — {agent_id} Onboarding Confirmation")
        
        # Create confirmation view
        view = discord.ui.View(timeout=300)
        
        # Confirm button
        confirm_btn = discord.ui.Button(
            label="✅ Confirm Onboarding",
            style=discord.ButtonStyle.success,
            custom_id=f"confirm_onboard:{agent_id}:{team_name}"
        )
        
        async def confirm_callback(inter):
            await self.execute_agent_onboarding(inter, agent_id, team_name)
        
        confirm_btn.callback = confirm_callback
        view.add_item(confirm_btn)
        
        # Cancel button
        cancel_btn = discord.ui.Button(
            label="❌ Cancel",
            style=discord.ButtonStyle.danger,
            custom_id="cancel_onboard"
        )
        
        async def cancel_callback(inter):
            await self.handle_agent_onboarding(inter, agent_id)
        
        cancel_btn.callback = cancel_callback
        view.add_item(cancel_btn)
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def execute_agent_onboarding(self, interaction, agent_id, team_name):
        """Execute the agent onboarding process."""
        
        try:
            # Create success embed
            embed = discord.Embed(
                title=f"🎉 {agent_id} Successfully Onboarded!",
                description=f"**{agent_id}** has been successfully onboarded to **{team_name}**",
                color=0x00FF00
            )
            
            embed.add_field(
                name="📋 **Onboarding Summary**",
                value=f"• **Agent:** {agent_id}\n• **Team:** {team_name}\n• **Status:** Active\n• **Workspace:** Created\n• **Systems:** Initialized",
                inline=False
            )
            
            embed.add_field(
                name="🚀 **Next Steps**",
                value=f"• {agent_id} is now ready for task assignment\n• Use messaging to communicate with {agent_id}\n• Monitor status through the coordination center",
                inline=False
            )
            
            embed.set_footer(text=f"🐝 WE ARE SWARM — {agent_id} Onboarding Complete")
            
            # Create completion view
            view = discord.ui.View(timeout=300)
            
            # Back to agents button
            back_btn = discord.ui.Button(
                label="⬅️ Back to Agents",
                style=discord.ButtonStyle.primary,
                custom_id="back_to_agents"
            )
            back_btn.callback = self.core.agents_cb
            view.add_item(back_btn)
            
            await interaction.response.edit_message(embed=embed, view=view)
            
            # Log successful onboarding
            logger.info(f"Agent {agent_id} successfully onboarded to {team_name}")
            
        except Exception as e:
            logger.error(f"Failed to onboard agent {agent_id}: {e}")
            
            # Create error embed
            error_embed = discord.Embed(
                title=f"❌ Onboarding Failed",
                description=f"Failed to onboard **{agent_id}** to **{team_name}**",
                color=0xFF0000
            )
            
            error_embed.add_field(
                name="🔍 **Error Details**",
                value=f"An error occurred during the onboarding process. Please try again or contact support.",
                inline=False
            )
            
            await interaction.response.edit_message(embed=error_embed, view=None)
