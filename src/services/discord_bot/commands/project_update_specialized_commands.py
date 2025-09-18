#!/usr/bin/env python3
"""
Project Update Specialized Discord Commands
===========================================

Specialized project update slash commands for Discord bot.
"""

import discord
from discord import app_commands
from typing import Optional


def setup_project_update_specialized_commands(bot):
    """Setup specialized project update slash commands."""

    @bot.tree.command(name="v2-compliance", description="Send V2 compliance update")
    @app_commands.describe(
        status="Compliance status (Compliant, Non-Compliant, etc.)",
        files_checked="Number of files checked",
        violations="Number of violations found",
        details="Compliance details"
    )
    async def send_v2_compliance(
        interaction: discord.Interaction,
        status: str,
        files_checked: int,
        violations: int,
        details: str
    ):
        """Send V2 compliance update."""
        try:
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send V2 compliance update
            results = update_system.send_v2_compliance_update(
                compliance_status=status,
                files_checked=files_checked,
                violations_found=violations,
                details=details
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            # Compliance emoji
            compliance_emoji = "✅" if violations == 0 else "⚠️" if violations < 5 else "❌"
            
            response = f"📏 **V2 Compliance Update Sent!**\n\n"
            response += f"**Status:** {compliance_emoji} {status}\n"
            response += f"**Files Checked:** {files_checked}\n"
            response += f"**Violations:** {violations}\n"
            response += f"**Details:** {details}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive update**\n"
            
            response += "\n📋 **V2 compliance status communicated to all agents!**"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending V2 compliance update: {e}")

    @bot.tree.command(name="doc-cleanup", description="Send documentation cleanup update")
    @app_commands.describe(
        files_removed="Number of files removed",
        files_kept="Number of files kept",
        summary="Cleanup summary"
    )
    async def send_doc_cleanup(
        interaction: discord.Interaction,
        files_removed: int,
        files_kept: int,
        summary: str
    ):
        """Send documentation cleanup update."""
        try:
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send documentation cleanup update
            results = update_system.send_documentation_cleanup_update(
                files_removed=files_removed,
                files_kept=files_kept,
                cleanup_summary=summary
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"📚 **Documentation Cleanup Update Sent!**\n\n"
            response += f"**Files Removed:** {files_removed}\n"
            response += f"**Files Kept:** {files_kept}\n"
            response += f"**Summary:** {summary}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive update**\n"
            
            response += "\n🧹 **Documentation cleanup communicated to all agents!**"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending documentation cleanup update: {e}")

    @bot.tree.command(name="feature-announce", description="Send feature announcement")
    @app_commands.describe(
        name="Feature name",
        description="Feature description",
        usage="Usage instructions (optional)"
    )
    async def send_feature_announcement(
        interaction: discord.Interaction,
        name: str,
        description: str,
        usage: Optional[str] = None
    ):
        """Send feature announcement."""
        try:
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send feature announcement
            results = update_system.send_feature_announcement(
                feature_name=name,
                description=description,
                usage_instructions=usage
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"🚀 **Feature Announcement Sent!**\n\n"
            response += f"**Feature:** {name}\n"
            response += f"**Description:** {description}\n"
            if usage:
                response += f"**Usage:** {usage}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive announcement**\n"
            
            response += "\n🎉 **New feature announced to all agents!**"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending feature announcement: {e}")
