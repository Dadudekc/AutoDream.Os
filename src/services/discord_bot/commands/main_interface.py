"""
Main Interface Module
Handles the main Discord interface and basic commands.
"""

import discord
import logging
from src.services.discord_bot.core.security_utils import security_utils

logger = logging.getLogger(__name__)


class MainInterface:
    """Handles main interface functionality for Discord bot."""
    
    def __init__(self, bot):
        self.bot = bot
        self.agent_coordination = None  # Will be set by dependency injection
    
    def set_agent_coordination(self, agent_coordination):
        """Set the agent coordination instance."""
        self.agent_coordination = agent_coordination
    
    async def launch_main_interface(self, interaction):
        """Launch the main interface with all controls."""
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

        view = discord.ui.View(timeout=600)  # 10 min

        # --- Buttons ----------------------------------------------------------
        agent_button = discord.ui.Button(label="🎯 Agent Coordination", style=discord.ButtonStyle.primary, custom_id="main:agents")
        devlog_button = discord.ui.Button(label="📝 Devlog & Updates", style=discord.ButtonStyle.secondary, custom_id="main:devlog")
        status_button = discord.ui.Button(label="📊 System Status", style=discord.ButtonStyle.success, custom_id="main:status")
        restart_button = discord.ui.Button(label="🔄 Restart Bot", style=discord.ButtonStyle.danger, custom_id="main:restart")
        shutdown_button = discord.ui.Button(label="⏹️ Shutdown Bot", style=discord.ButtonStyle.danger, custom_id="main:shutdown")

        # --- Callbacks --------------------------------------------------------
        async def agent_cb(cb_inter):
            """Call the enhanced agent coordination interface."""
            if self.agent_coordination:
                await self.agent_coordination.agents_cb(cb_inter)
            else:
                await self._reply(cb_inter, content="❌ Agent coordination not available", ephemeral=True)

        async def devlog_cb(cb_inter):
            devlog_embed = discord.Embed(
                title="📝 Devlog & Project Updates",
                description="Record your work and create updates:",
                color=0x0099FF
            )
            devlog_embed.add_field(
                name="📋 **Available Actions:**",
                value=(
                    "• **Create Devlog** — Record your work progress\n"
                    "• **Project Updates** — Share project status\n"
                    "• **Feature Announcements** — Announce new features\n"
                    "• **Bug Reports** — Report issues found"
                ),
                inline=False
            )
            devlog_embed.set_footer(text="📝 Keep your team informed with regular updates!")
            if cb_inter.response.is_done():
                await cb_inter.followup.send(embed=devlog_embed, ephemeral=True)
            else:
                await cb_inter.response.edit_message(embed=devlog_embed, view=None)

        async def status_cb(cb_inter):
            bot_name = self.bot.user.name if self.bot.user else "Discord Commander"
            status_embed = discord.Embed(title="📊 System Status", description="Current status of all systems:", color=0x00FF00)
            status_embed.add_field(
                name="✅ **Messaging System**",
                value="• PyAutoGUI automation active\n• Agent coordinates loaded\n• Message delivery operational",
                inline=False
            )
            status_embed.add_field(
                name="🤖 **Discord Bot**",
                value=f"• **{bot_name}** is online\n• Commands registered\n• Security policies active",
                inline=False
            )
            status_embed.add_field(
                name="🔧 **System Health**",
                value="• All services operational\n• No critical errors\n• Performance optimal",
                inline=False
            )
            status_embed.set_footer(text="🐝 WE ARE SWARM — All systems green!")
            if cb_inter.response.is_done():
                await cb_inter.followup.send(embed=status_embed, ephemeral=True)
            else:
                await cb_inter.response.edit_message(embed=status_embed, view=None)

        async def restart_cb(cb_inter):
            if not self._is_admin(cb_inter):
                return await self._deny(cb_inter, "Administrator required to restart bot.")
            
            # Log restart attempt
            security_utils.log_security_event(
                "RESTART_ATTEMPTED",
                str(cb_inter.user.id),
                "User attempted to restart Discord bot",
                "HIGH"
            )
            
            # Create confirmation modal
            class RestartModal(discord.ui.Modal, title="🔄 Confirm Bot Restart"):
                confirm = discord.ui.TextInput(
                    label="Type 'RESTART' to confirm",
                    placeholder="RESTART",
                    required=True,
                    max_length=10
                )

                async def on_submit(self, inter: discord.Interaction):
                    if str(self.confirm).upper() == "RESTART":
                        # Log successful restart
                        security_utils.log_security_event(
                            "RESTART_EXECUTED",
                            str(inter.user.id),
                            "User successfully restarted Discord bot",
                            "CRITICAL"
                        )
                        
                        await self._reply(inter, content="🔄 **Restarting Discord Commander...**", ephemeral=True)
                        
                        # Import and use restart manager
                        from src.services.discord_bot.core.restart_manager import RestartManager
                        restart_manager = RestartManager()
                        await restart_manager.restart_bot()
                    else:
                        await self._reply(inter, content="❌ Restart cancelled - confirmation text did not match.", ephemeral=True)

            await cb_inter.response.send_modal(RestartModal())

        async def shutdown_cb(cb_inter):
            if not self._is_admin(cb_inter):
                return await self._deny(cb_inter, "Administrator required to shutdown bot.")
            
            # Log shutdown attempt
            security_utils.log_security_event(
                "SHUTDOWN_ATTEMPTED",
                str(cb_inter.user.id),
                "User attempted to shutdown Discord bot",
                "CRITICAL"
            )
            
            # Create confirmation modal
            class ShutdownModal(discord.ui.Modal, title="⏹️ Confirm Bot Shutdown"):
                confirm = discord.ui.TextInput(
                    label="Type 'SHUTDOWN' to confirm",
                    placeholder="SHUTDOWN",
                    required=True,
                    max_length=10
                )

                async def on_submit(self, inter: discord.Interaction):
                    if str(self.confirm).upper() == "SHUTDOWN":
                        # Log successful shutdown
                        security_utils.log_security_event(
                            "SHUTDOWN_EXECUTED",
                            str(inter.user.id),
                            "User successfully shutdown Discord bot",
                            "CRITICAL"
                        )
                        
                        await self._reply(inter, content="⏹️ **Shutting down Discord Commander...**", ephemeral=True)
                        
                        # Graceful shutdown
                        await self.bot.close()
                    else:
                        await self._reply(inter, content="❌ Shutdown cancelled - confirmation text did not match.", ephemeral=True)

            await cb_inter.response.send_modal(ShutdownModal())

        # Assign callbacks
        agent_button.callback = agent_cb
        devlog_button.callback = devlog_cb
        status_button.callback = status_cb
        restart_button.callback = restart_cb
        shutdown_button.callback = shutdown_cb

        # Add buttons
        view.add_item(agent_button)
        view.add_item(devlog_button)
        view.add_item(status_button)
        view.add_item(restart_button)
        view.add_item(shutdown_button)

        # Use safe response function to handle rate limits and double acknowledgment
        await self._send_discord_response(interaction, embed=embed, view=view, ephemeral=True)
        logger.info(f"Main interface sent to {interaction.user}")

    async def _send_discord_response(self, interaction, **kwargs):
        """Safely send Discord response, handling rate limits and double acknowledgment."""
        try:
            # Filter out None values to prevent Discord errors
            filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
            
            if interaction.response.is_done():
                await interaction.followup.send(**filtered_kwargs)
            else:
                await interaction.response.send_message(**filtered_kwargs)
        except discord.HTTPException as e:
            logger.warning(f"Discord HTTP error: {e}")
            if interaction.response.is_done():
                await interaction.followup.send("⚠️ Response error occurred", ephemeral=True)

    async def _reply(self, interaction, **kwargs):
        """Helper function to send replies safely."""
        await self._send_discord_response(interaction, **kwargs)

    def _is_admin(self, interaction):
        """Check if user is administrator."""
        return interaction.user.guild_permissions.administrator

    async def _deny(self, interaction, message):
        """Send denial message."""
        embed = discord.Embed(title="❌ Access Denied", description=message, color=0xFF0000)
        await self._reply(interaction, embed=embed, ephemeral=True)
