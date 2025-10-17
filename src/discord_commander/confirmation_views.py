"""Confirmation Views - Extracted from unified_discord_bot.py for V2 compliance."""

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None


class ConfirmShutdownView(discord.ui.View if DISCORD_AVAILABLE else object):
    """Confirmation view for shutdown command."""

    def __init__(self):
        super().__init__(timeout=30)
        self.confirmed = False

    @discord.ui.button(label="✅ Confirm Shutdown", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction, button):
        """Confirm shutdown button."""
        self.confirmed = True
        await interaction.response.send_message("✅ Shutdown confirmed", ephemeral=True)
        self.stop()

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction, button):
        """Cancel shutdown button."""
        self.confirmed = False
        await interaction.response.send_message("❌ Cancelled", ephemeral=True)
        self.stop()


class ConfirmRestartView(discord.ui.View if DISCORD_AVAILABLE else object):
    """Confirmation view for restart command."""

    def __init__(self):
        super().__init__(timeout=30)
        self.confirmed = False

    @discord.ui.button(label="✅ Confirm Restart", style=discord.ButtonStyle.primary)
    async def confirm(self, interaction, button):
        """Confirm restart button."""
        self.confirmed = True
        await interaction.response.send_message("✅ Restart confirmed", ephemeral=True)
        self.stop()

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction, button):
        """Cancel restart button."""
        self.confirmed = False
        await interaction.response.send_message("❌ Cancelled", ephemeral=True)
        self.stop()

