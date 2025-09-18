#!/usr/bin/env python3
"""
Project Update Core Discord Commands
====================================

Core project update slash commands for Discord bot.
"""

import discord
from discord import app_commands
from typing import Optional


def setup_project_update_core_commands(bot):
    """Setup core project update slash commands."""

    @bot.tree.command(name="project-update", description="Send project update to all agents")
    @app_commands.describe(
        update_type="Type of update (milestone, status, system_change, etc.)",
        title="Update title",
        description="Detailed description of the update",
        priority="Message priority (NORMAL, HIGH, URGENT)"
    )
    async def send_project_update(
        interaction: discord.Interaction, 
        update_type: str, 
        title: str, 
        description: str,
        priority: str = "NORMAL"
    ):
        """Send project update to all agents."""
        try:
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send project update
            results = update_system.send_project_update(
                update_type=update_type,
                title=title,
                description=description,
                priority=priority
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"📋 **Project Update Sent!**\n\n"
            response += f"**Type:** {update_type}\n"
            response += f"**Title:** {title}\n"
            response += f"**Priority:** {priority}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive update**\n"
            
            response += "\n🐝 **WE ARE SWARM** - Project update delivered!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending project update: {e}")

    @bot.tree.command(name="milestone", description="Send milestone completion notification")
    @app_commands.describe(
        name="Milestone name",
        description="Milestone description",
        completion="Completion percentage (0-100)"
    )
    async def send_milestone(
        interaction: discord.Interaction,
        name: str,
        description: str,
        completion: int
    ):
        """Send milestone completion notification."""
        try:
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send milestone notification
            results = update_system.send_milestone_notification(
                milestone=name,
                description=description,
                completion_percentage=completion
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"🎯 **Milestone Notification Sent!**\n\n"
            response += f"**Milestone:** {name}\n"
            response += f"**Completion:** {completion}%\n"
            response += f"**Description:** {description}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive notification**\n"
            
            response += "\n🏆 **Milestone achieved and communicated!**"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending milestone notification: {e}")

    @bot.tree.command(name="system-status", description="Send system status update")
    @app_commands.describe(
        system="System name",
        status="System status (Operational, Down, Maintenance, etc.)",
        details="Status details"
    )
    async def send_system_status(
        interaction: discord.Interaction,
        system: str,
        status: str,
        details: str
    ):
        """Send system status update."""
        try:
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send system status update
            results = update_system.send_system_status_update(
                system_name=system,
                status=status,
                details=details
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            # Status emoji
            status_emoji = "✅" if status.lower() in ["operational", "online", "active"] else "⚠️" if status.lower() in ["maintenance", "degraded"] else "❌"
            
            response = f"📊 **System Status Update Sent!**\n\n"
            response += f"**System:** {system}\n"
            response += f"**Status:** {status_emoji} {status}\n"
            response += f"**Details:** {details}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive update**\n"
            
            response += "\n🔧 **System status communicated to all agents!**"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending system status update: {e}")
