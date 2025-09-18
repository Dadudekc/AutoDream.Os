#!/usr/bin/env python3
"""
Project Update Management Discord Commands
==========================================

Management and monitoring slash commands for project updates.
"""

import discord
from discord import app_commands


def setup_project_update_management_commands(bot):
    """Setup project update management slash commands."""

    @bot.tree.command(name="update-history", description="View project update history")
    @app_commands.describe(limit="Number of updates to show (default: 10)")
    async def view_update_history(interaction: discord.Interaction, limit: int = 10):
        """View project update history."""
        try:
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Get update history
            history = update_system.get_update_history(limit=limit)
            
            if not history:
                await interaction.response.send_message("📋 **No update history found.**")
                return
            
            response = f"📋 **Project Update History (Last {len(history)} Updates):**\n\n"
            
            for i, record in enumerate(history, 1):
                timestamp = record.get("timestamp", "Unknown")
                update_type = record.get("update_type", "Unknown")
                title = record.get("title", "Unknown")
                success_count = record.get("success_count", 0)
                total_count = record.get("total_count", 0)
                
                # Format timestamp
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    formatted_time = timestamp
                
                response += f"**{i}.** {title}\n"
                response += f"   📅 {formatted_time} | 📝 {update_type} | 📊 {success_count}/{total_count} agents\n\n"
            
            response += "🐝 **WE ARE SWARM** - Update history retrieved!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error retrieving update history: {e}")

    @bot.tree.command(name="update-stats", description="View project update statistics")
    async def view_update_stats(interaction: discord.Interaction):
        """View project update statistics."""
        try:
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Get update statistics
            stats = update_system.get_update_statistics()
            
            if "error" in stats:
                await interaction.response.send_message(f"❌ Error: {stats['error']}")
                return
            
            response = "📊 **Project Update Statistics:**\n\n"
            response += f"**Total Updates:** {stats.get('total_updates', 0)}\n"
            response += f"**Total Deliveries:** {stats.get('total_deliveries', 0)}\n"
            response += f"**Successful Deliveries:** {stats.get('successful_deliveries', 0)}\n"
            response += f"**Success Rate:** {stats.get('success_rate', 0)}%\n\n"
            
            update_types = stats.get('update_types', {})
            if update_types:
                response += "**Update Types:**\n"
                for update_type, count in update_types.items():
                    response += f"  • {update_type}: {count}\n"
            
            response += "\n🐝 **WE ARE SWARM** - Statistics retrieved!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error retrieving update statistics: {e}")
