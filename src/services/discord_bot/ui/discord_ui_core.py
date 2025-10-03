#!/usr/bin/env python3
"""
Discord UI Core - Core UI Operations
====================================

Core UI operations for Discord bot dashboard.
Handles main dashboard creation and basic UI functionality.

V2 Compliance: ≤400 lines, focused core UI operations module
Author: Agent-6 (Quality Assurance Specialist)
"""

import logging
from datetime import UTC, datetime

import discord

logger = logging.getLogger(__name__)


class DiscordUICore:
    """Core Discord UI operations for dashboard."""

    def __init__(self, bot):
        """Initialize Discord UI core."""
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.DiscordUICore")
        self.logger.info("Discord UI Core initialized")

    async def create_main_dashboard(self) -> discord.Embed:
        """Create the main dashboard embed."""
        try:
            # Get bot status
            bot_status = "🟢 Online" if self.bot.is_ready else "🔴 Offline"
            latency = round(self.bot.latency * 1000) if self.bot.latency else 0

            # Get social media status
            try:
                from src.services.social_media_integration import get_social_media_status

                social_status = get_social_media_status()
                social_active = "🟢 Active" if social_status.get("active", False) else "🔴 Inactive"
                social_platforms = social_status.get("platforms", 0)
            except ImportError:
                social_active = "⚠️ Service Not Available"
                social_platforms = 0

            embed = discord.Embed(
                title="🐝 Discord Commander Dashboard",
                description="**WE ARE SWARM** - Agent Coordination System",
                color=0x00FF00,
                timestamp=datetime.now(UTC),
            )

            # Bot Status Section
            embed.add_field(
                name="🤖 Bot Status",
                value=f"**Status**: {bot_status}\n**Latency**: {latency}ms",
                inline=True,
            )

            # Social Media Status Section
            embed.add_field(
                name="📱 Social Media",
                value=f"**Status**: {social_active}\n**Platforms**: {social_platforms}",
                inline=True,
            )

            # System Health Section
            embed.add_field(
                name="⚡ System Health",
                value="**Status**: 🟢 Healthy\n**Uptime**: Active",
                inline=True,
            )

            # Agent Status Section
            embed.add_field(
                name="👥 Active Agents",
                value="**Agent-4**: 🟢 Captain\n**Agent-5**: 🟢 Coordinator\n**Agent-6**: 🟢 Quality",
                inline=False,
            )

            # Footer
            embed.set_footer(
                text="WE ARE SWARM - Autonomous Agent System",
                icon_url="https://cdn.discordapp.com/emojis/1234567890123456789.png",
            )

            return embed

        except Exception as e:
            self.logger.error(f"Error creating main dashboard: {e}")
            return self._create_error_embed("Failed to create dashboard")

    def _create_error_embed(self, message: str) -> discord.Embed:
        """Create error embed."""
        embed = discord.Embed(
            title="❌ Error", description=message, color=0xFF0000, timestamp=datetime.now(UTC)
        )
        return embed

    async def get_bot_info(self) -> dict[str, str]:
        """Get bot information."""
        try:
            return {
                "status": "🟢 Online" if self.bot.is_ready else "🔴 Offline",
                "latency": f"{round(self.bot.latency * 1000)}ms" if self.bot.latency else "0ms",
                "guilds": str(len(self.bot.guilds)),
                "users": str(len(self.bot.users)),
                "uptime": "Active",
            }
        except Exception as e:
            self.logger.error(f"Error getting bot info: {e}")
            return {
                "status": "🔴 Error",
                "latency": "N/A",
                "guilds": "0",
                "users": "0",
                "uptime": "Unknown",
            }


__all__ = ["DiscordUICore"]

