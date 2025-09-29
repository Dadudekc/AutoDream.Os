"""
Modal Handlers Module
=====================
Handles modal dialogs for admin actions like restart and shutdown.
"""

import logging

import discord
from src.services.discord_bot.core.security_manager import SecurityManager

logger = logging.getLogger(__name__)


class RestartModal(discord.ui.Modal, title="🔄 Confirm Bot Restart"):
    """Modal for confirming bot restart."""

    def __init__(self, security_manager: SecurityManager, bot):
        super().__init__()
        self.security_manager = security_manager
        self.bot = bot

    confirm = discord.ui.TextInput(
        label="Type 'RESTART' to confirm", placeholder="RESTART", required=True, max_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):
        if str(self.confirm).upper() == "RESTART":
            # Log successful restart
            from src.services.discord_bot.core.security_utils import security_utils

            security_utils.log_security_event(
                "RESTART_EXECUTED",
                str(interaction.user.id),
                "User successfully restarted Discord bot",
                "CRITICAL",
            )

            await interaction.response.send_message(
                content="🔄 **Restarting Discord Commander...**", ephemeral=True
            )

            # Import and use restart manager
            from src.services.discord_bot.core.restart_manager import RestartManager

            restart_manager = RestartManager()
            await restart_manager.restart_bot()
        else:
            await interaction.response.send_message(
                content="❌ Restart cancelled - confirmation text did not match.", ephemeral=True
            )


class ShutdownModal(discord.ui.Modal, title="⏹️ Confirm Bot Shutdown"):
    """Modal for confirming bot shutdown."""

    def __init__(self, security_manager: SecurityManager, bot):
        super().__init__()
        self.security_manager = security_manager
        self.bot = bot

    confirm = discord.ui.TextInput(
        label="Type 'SHUTDOWN' to confirm", placeholder="SHUTDOWN", required=True, max_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):
        if str(self.confirm).upper() == "SHUTDOWN":
            # Log successful shutdown
            from src.services.discord_bot.core.security_utils import security_utils

            security_utils.log_security_event(
                "SHUTDOWN_EXECUTED",
                str(interaction.user.id),
                "User successfully shutdown Discord bot",
                "CRITICAL",
            )

            await interaction.response.send_message(
                content="⏹️ **Shutting down Discord Commander...**", ephemeral=True
            )

            # Graceful shutdown
            await self.bot.close()
        else:
            await interaction.response.send_message(
                content="❌ Shutdown cancelled - confirmation text did not match.", ephemeral=True
            )
