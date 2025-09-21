#!/usr/bin/env python3
"""
Onboarding Discord Commands
===========================

Agent onboarding commands for Discord bot.
"""

import discord
from discord import app_commands
from typing import Optional


def setup_onboarding_commands(bot):
    """Setup agent onboarding slash commands."""

    @bot.tree.command(name="onboard-agent", description="Onboard a specific agent")
    @app_commands.describe(
        agent="Agent ID to onboard",
        dry_run="Dry run mode - don't actually send messages (default: false)"
    )
    async def onboard_agent(interaction: discord.Interaction, agent: str, dry_run: bool = False):
        """Onboard a specific agent."""
        try:
            # Validate agent ID
            if agent not in bot.agent_coordinates:
                await interaction.response.send_message(f"❌ Invalid agent ID: {agent}")
                return
            
            # Initialize onboarding service
            from src.services.messaging.service import MessagingService
            from src.services.messaging.onboarding.onboarding_service import OnboardingService
            
            messaging_service = MessagingService(dry_run=dry_run)
            onboarding_service = OnboardingService(messaging_service)
            
            # Start agent onboarding
            success = onboarding_service.hard_onboard_agent(agent)
            
            if success:
                mode_text = "DRY RUN" if dry_run else "LIVE"
                response = f"🚀 **Agent Onboarding Initiated!**\n\n"
                response += f"**Agent:** {agent}\n"
                response += f"**Mode:** {mode_text}\n"
                response += f"**Status:** ✅ Onboarding sequence started\n\n"
                response += "**Onboarding includes:**\n"
                response += "• Welcome message and system overview\n"
                response += "• Quick start guide and protocols\n"
                response += "• Current system status and features\n"
                response += "• Coordination protocols and team structure\n"
                response += "• Immediate action items and next steps\n\n"
                response += "🐝 **WE ARE SWARM** - Agent onboarding in progress!"
            else:
                response = f"❌ **Failed to onboard agent {agent}**"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error onboarding agent: {e}")

    @bot.tree.command(name="onboard-all", description="Onboard all agents")
    @app_commands.describe(
        dry_run="Dry run mode - don't actually send messages (default: false)"
    )
    async def onboard_all_agents(interaction: discord.Interaction, dry_run: bool = False):
        """Onboard all agents."""
        try:
            # Initialize onboarding service
            from src.services.messaging.service import MessagingService
            from src.services.messaging.onboarding.onboarding_service import OnboardingService
            
            messaging_service = MessagingService(dry_run=dry_run)
            onboarding_service = OnboardingService(messaging_service)
            
            # Start onboarding for all agents
            results = onboarding_service.hard_onboard_all_agents()
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            mode_text = "DRY RUN" if dry_run else "LIVE"
            response = f"🚀 **Mass Agent Onboarding Initiated!**\n\n"
            response += f"**Mode:** {mode_text}\n"
            response += f"**Agents Processed:** {successful}/{total}\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully onboarded!**\n\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to onboard**\n\n"
            
            response += "**Onboarding includes for each agent:**\n"
            response += "• Welcome message and system overview\n"
            response += "• Quick start guide and protocols\n"
            response += "• Current system status and features\n"
            response += "• Coordination protocols and team structure\n"
            response += "• Immediate action items and next steps\n\n"
            
            response += "**Agent Results:**\n"
            for agent_id, success in results.items():
                status_icon = "✅" if success else "❌"
                response += f"{status_icon} {agent_id}\n"
            
            response += "\n🐝 **WE ARE SWARM** - Mass onboarding completed!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error onboarding all agents: {e}")

    @bot.tree.command(name="onboarding-status", description="Check onboarding status for agents")
    @app_commands.describe(agent="Specific agent to check (optional - shows all if not specified)")
    async def check_onboarding_status(interaction: discord.Interaction, agent: Optional[str] = None):
        """Check onboarding status for agents."""
        try:
            # Initialize messaging service
            from src.services.messaging.service import MessagingService
            
            messaging_service = MessagingService(dry_run=False)
            
            if agent:
                # Check specific agent
                if agent not in bot.agent_coordinates:
                    await interaction.response.send_message(f"❌ Invalid agent ID: {agent}")
                    return
                
                # Check if agent has been onboarded (look for recent onboarding messages)
                messages = messaging_service.show_message_history(agent)
                onboarding_messages = [msg for msg in messages if "ONBOARDING COMPLETE" in msg.content]
                
                if onboarding_messages:
                    latest_onboarding = onboarding_messages[-1]
                    response = f"✅ **{agent} Onboarding Status:**\n\n"
                    response += f"**Status:** Onboarded\n"
                    response += f"**Last Onboarding:** {latest_onboarding.timestamp}\n"
                    response += f"**Sender:** {latest_onboarding.sender}\n"
                else:
                    response = f"❌ **{agent} Onboarding Status:**\n\n"
                    response += f"**Status:** Not onboarded\n"
                    response += f"**Action:** Use `/onboard-agent` to onboard this agent\n"
            else:
                # Check all agents
                response = "📋 **Onboarding Status for All Agents:**\n\n"
                
                for agent_id in bot.agent_coordinates.keys():
                    messages = messaging_service.show_message_history(agent_id)
                    onboarding_messages = [msg for msg in messages if "ONBOARDING COMPLETE" in msg.content]
                    
                    if onboarding_messages:
                        latest_onboarding = onboarding_messages[-1]
                        response += f"✅ **{agent_id}** - Onboarded ({latest_onboarding.timestamp})\n"
                    else:
                        response += f"❌ **{agent_id}** - Not onboarded\n"
                
                response += "\n**Legend:**\n"
                response += "✅ = Onboarded and ready\n"
                response += "❌ = Needs onboarding\n"
            
            response += "\n🐝 **WE ARE SWARM** - Onboarding status retrieved!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error checking onboarding status: {e}")

    @bot.tree.command(name="onboarding-info", description="Get information about the onboarding process")
    async def get_onboarding_info(interaction: discord.Interaction):
        """Get information about the onboarding process."""
        try:
            response = "📚 **Agent Onboarding Information:**\n\n"
            
            response += "**What is Onboarding?**\n"
            response += "Onboarding is the process of introducing new agents to the V2_SWARM system, providing them with essential information about their role, the system architecture, and how to participate effectively.\n\n"
            
            response += "**Onboarding Process:**\n"
            response += "1. **Welcome Message** - Introduction to the system\n"
            response += "2. **System Overview** - Architecture and capabilities\n"
            response += "3. **Quick Start Guide** - How to get started\n"
            response += "4. **Coordination Protocols** - Team structure and communication\n"
            response += "5. **Current Status** - System state and features\n"
            response += "6. **Action Items** - Immediate next steps\n\n"
            
            response += "**Available Commands:**\n"
            response += "• `/onboard-agent` - Onboard a specific agent\n"
            response += "• `/onboard-all` - Onboard all agents\n"
            response += "• `/onboarding-status` - Check onboarding status\n"
            response += "• `/onboarding-info` - This information\n\n"
            
            response += "**Onboarding Features:**\n"
            response += "• **Dry Run Mode** - Test onboarding without sending messages\n"
            response += "• **Status Tracking** - Monitor onboarding progress\n"
            response += "• **Comprehensive Coverage** - All essential information included\n"
            response += "• **V2 Compliance** - Follows all system standards\n\n"
            
            response += "**When to Use:**\n"
            response += "• New agents joining the system\n"
            response += "• System updates requiring re-onboarding\n"
            response += "• Agent recovery or reset scenarios\n"
            response += "• Team coordination and alignment\n\n"
            
            response += "🐝 **WE ARE SWARM** - Onboarding system ready!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error getting onboarding information: {e}")
