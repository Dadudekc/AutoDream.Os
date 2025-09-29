"""
Help Command Module
==================
Simple, focused help command implementation (hardened).
"""

import discord
import logging
from src.services.discord_bot.core.command_logger import command_logger_decorator, command_logger
from .safe_response_utils import safe_send, safe_log_info

logger = logging.getLogger(__name__)


def setup_help_command(bot, security_manager):
    """Setup the help command once."""
    # Prevent duplicate registration if this module is imported twice
    if getattr(bot, "_help_cmd_registered", False):
        logger.debug("help command already registered; skipping")
        return
    bot._help_cmd_registered = True

    @bot.tree.command(name="help", description="Vibe-coder friendly help guide with main interface")
    @command_logger_decorator(command_logger)
    async def help_cmd(interaction: discord.Interaction):
        # Check rate limits (early exit)
        user_id = str(interaction.user.id)
        channel_id = str(getattr(interaction.channel, "id", "dm"))
        if not await security_manager.check_rate_limit(user_id, "help", channel_id, interaction):
            return

        # Build embed (emojis are fine here)
        embed = discord.Embed(
            title="🎉 Vibe-Coder Control Center",
            description="**V2_SWARM Main Interface** — All controls in one place!",
            color=0xFF6B35
        )
        embed.add_field(
            name="🎯 **Available Controls:**",
            value=(
                "• **🎯 Agent Coordination** — Onboard, message, and manage agents\n"
                "• **📝 Devlog & Updates** — Record your work\n"
                "• **📊 System Status** — Check bot health\n"
                "• **🔄 Restart Bot** — Restart the Discord Commander (admin)\n"
                "• **⏹️ Shutdown Bot** — Gracefully shutdown the bot (admin)"
            ),
            inline=False
        )
        embed.add_field(
            name="💫 **How to Use:**",
            value="Click a button. No complex commands. Real-time visual feedback.",
            inline=False
        )
        embed.set_footer(text="🎉 Vibe coding made simple — just click and control!")

        # Import here to avoid circulars if your UI module imports commands
        from .button_handlers import create_main_interface_view
        view = create_main_interface_view(bot, security_manager)

        # Safe send (avoids 40060 if decorators or error paths already responded)
        await safe_send(interaction, embed=embed, view=view, ephemeral=True)

        # Safe logging (ASCII-only to avoid cp1252 console explosions)
        safe_log_info("Main interface sent", user_id=user_id, channel_id=channel_id)
