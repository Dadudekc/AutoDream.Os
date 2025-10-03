#!/usr/bin/env python3
"""
Discord UI Controller - Unified Interface
=========================================

Unified interface for Discord bot dashboard UI.
Provides backward compatibility and easy access to all UI components.

V2 Compliance: ≤400 lines, unified interface module
Author: Agent-6 (Quality Assurance Specialist)
"""

from .discord_ui_core import DiscordUICore
from .discord_ui_modals import BroadcastModal, MessageAgentModal, SocialMediaPostModal
from .discord_ui_views import AgentControlView, SocialMediaView, SystemControlView


class DiscordUI:
    """Unified Discord UI controller for interactive dashboard."""

    def __init__(self, bot):
        """Initialize Discord UI controller."""
        self.bot = bot
        self.core = DiscordUICore(bot)
        self.logger = self.core.logger

    async def create_main_dashboard(self) -> tuple[discord.Embed, list[discord.ui.View]]:
        """Create the main dashboard with embed and views."""
        try:
            # Create main dashboard embed
            embed = await self.core.create_main_dashboard()

            # Create views
            views = [
                AgentControlView(self.bot),
                SystemControlView(self.bot),
                SocialMediaView(self.bot),
            ]

            return embed, views

        except Exception as e:
            self.logger.error(f"Error creating main dashboard: {e}")
            embed = self.core._create_error_embed("Failed to create dashboard")
            return embed, []

    async def get_bot_info(self) -> dict[str, str]:
        """Get bot information."""
        return await self.core.get_bot_info()

    def create_message_agent_modal(self) -> MessageAgentModal:
        """Create message agent modal."""
        return MessageAgentModal(self.bot)

    def create_broadcast_modal(self) -> BroadcastModal:
        """Create broadcast modal."""
        return BroadcastModal(self.bot)

    def create_social_media_post_modal(self) -> SocialMediaPostModal:
        """Create social media post modal."""
        return SocialMediaPostModal(self.bot)


# Re-export all components for backward compatibility
__all__ = [
    "DiscordUI",
    "DiscordUICore",
    "AgentControlView",
    "SystemControlView",
    "SocialMediaView",
    "MessageAgentModal",
    "BroadcastModal",
    "SocialMediaPostModal",
]
