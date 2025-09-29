"""
Ping Command Module
===================
Simple ping command for testing bot responsiveness (hardened).
"""

import discord
import logging
from src.services.discord_bot.core.command_logger import command_logger_decorator, command_logger
from .safe_response_utils import safe_send, safe_log_info

logger = logging.getLogger(__name__)


def setup_ping_command(bot, security_manager):
    """Setup the ping command once."""
    # Prevent duplicate registration if this module is imported twice
    if getattr(bot, "_ping_cmd_registered", False):
        logger.debug("ping command already registered; skipping")
        return
    bot._ping_cmd_registered = True
    
    @bot.tree.command(name="ping", description="Test bot responsiveness")
    @command_logger_decorator(command_logger)
    async def ping_cmd(interaction: discord.Interaction):
        # Check rate limits (early exit)
        user_id = str(interaction.user.id)
        channel_id = str(getattr(interaction.channel, "id", "dm"))
        if not await security_manager.check_rate_limit(user_id, "ping", channel_id, interaction):
            return
        
        # Safe send (avoids 40060 if decorators or error paths already responded)
        await safe_send(interaction, content="🏓 Pong! Bot is responsive.", ephemeral=True)
        
        # Safe logging (ASCII-only to avoid cp1252 console explosions)
        safe_log_info("Ping command used", user_id=user_id, channel_id=channel_id)
