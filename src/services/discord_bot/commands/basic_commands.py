#!/usr/bin/env python3
"""
🎉 Vibe-Coder Friendly Discord Commands
- Button-first control center (/vibe)
- Consolidated, simple slash commands: /ping, /vibe, /help
- Admin-guarded risky actions (restart/shutdown)
"""

from __future__ import annotations

import logging
import asyncio
import os
from typing import Callable, Awaitable

import discord
from discord import app_commands
from discord.ui import Button, View
from discord.errors import HTTPException, RateLimited
from src.services.discord_bot.core.command_logger import command_logger_decorator, command_logger
from src.services.onboarding.entry import kickoff_onboarding, is_onboarding_running
from src.services.discord_bot.core.restart_manager import restart_manager
from src.services.discord_bot.core.security_utils import security_utils

logger = logging.getLogger(__name__)

# --- Help Registry (single source of truth) ----------------------------------

HELP_SECTIONS: dict[str, list[str]] = {
    "Basic Commands": [
        "`/ping` - Test bot responsiveness",
        "`/vibe` - Launch main vibe-coder interface with all controls",
        "`/help` - Get vibe-coder friendly help and guidance",
        "`/status` - Show system status",
    ],
    "Agent Commands": [
        "`/agents` - List all agents and their status",
        "`/agent-status` - Get detailed agent status",
        "`/agent-channels` - List agent-specific Discord channels",
        "`/swarm` - Send message to all agents",
        "`/send` - Send message to specific agent",
        "`/broadcast` - Broadcast message to multiple agents",
    ],
    "Messaging Commands": [
        "`/send-advanced` - Send advanced message with options",
        "`/broadcast-advanced` - Advanced broadcast with priority",
        "`/message-history` - Get message history for agent",
        "`/messaging-status` - Get comprehensive messaging system status",
        "`/msg-status` - Alias for messaging status",
        "`/list-agents` - List all available agents and their status",
    ],
    "Devlog Commands": [
        "`/devlog` - Create devlog entry",
        "`/agent-devlog` - Create devlog for specific agent",
        "`/test-devlog` - Test devlog functionality",
        "`/devlog-list` - List recent devlog entries",
        "`/devlog-search` - Search devlog entries",
    ],
    "Project Update Commands": [
        "`/project-update` - Create project update",
        "`/milestone` - Record milestone achievement",
        "`/v2-compliance` - Report V2 compliance status",
        "`/update-history` - View update history",
        "`/update-stats` - Get update statistics",
        "`/doc-cleanup` - Documentation cleanup update",
        "`/feature-announce` - Feature announcement",
        "`/system-status` - Send system status update",
        "`/info` - Show bot information",
    ],
    "Onboarding Commands": [
        "`/onboard-agent` - Onboard new agent",
        "`/onboard-all` - Onboard all agents",
        "`/onboarding-status` - Check onboarding status",
        "`/onboarding-info` - About the onboarding process",
        "`/agent-setup` - Setup agent configuration",
        "`/welcome` - Welcome new team member",
    ],
    "Admin Commands": [
        "`/command-stats` - View command execution statistics",
        "`/command-history` - View recent command execution history",
        "`/bot-health` - Check bot health and system status",
        "`/clear-logs` - Clear command logs (admin only)",
    ],
    "Usage Examples": [
        "`/swarm message:All agents report status`",
        "`/devlog action:Tools cleanup completed`",
        "`/agent-devlog agent:Agent-4 action:Mission completed`",
        "`/send agent:Agent-1 message:Hello from Discord`",
        "`/send-advanced agent:Agent-1 message:Urgent update priority:URGENT message_type:system`",
        "`/broadcast-advanced message:System maintenance in 1 hour priority:HIGH`",
        "`/message-history agent:Agent-1 limit:5`",
        "`/list-agents`",
        "`/onboard-agent agent:Agent-1 dry_run:false`",
        "`/onboard-all dry_run:true`",
        "`/onboarding-status agent:Agent-1`",
        "`/project-update update_type:milestone title:V2 Compliance Complete description:All agents now V2 compliant`",
        "`/milestone name:Documentation Cleanup completion:100 description:Removed 13 redundant files`",
        "`/system-status system:Messaging Service status:Operational details:All systems green`",
        "`/v2-compliance status:Compliant files_checked:150 violations:0 details:All files under 400 lines`",
        "`/agent-channels`",
    ],
}
HELP_TITLE = "V2_SWARM Enhanced Discord Agent Bot Commands"
HELP_FOOTER = "🐝 WE ARE SWARM — All agents coordinated through Discord!"

# --- Utilities ----------------------------------------------------------------

DISCORD_MESSAGE_LIMIT = 2000

async def send_text_or_embed(
    interaction: discord.Interaction,
    title: str,
    sections: dict[str, list[str]],
    ephemeral: bool = True,
) -> None:
    """Send as pretty embed; fall back to chunked text if limits exceeded."""
    try:
        embed = discord.Embed(title=title, color=0x00FF00)
        for section, lines in sections.items():
            value = "\n".join(lines)
            if len(value) <= 1000:
                embed.add_field(name=f"**{section}**", value=value, inline=False)
            else:
                for i, chunk in enumerate(_chunk(value, 1000), start=1):
                    embed.add_field(name=f"**{section} ({i})**", value=chunk, inline=False)
        embed.set_footer(text=HELP_FOOTER)
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
    except Exception as e:
        logger.warning(f"Embed failed ({e}); falling back to text.")
        text = _plain_help_text(title, sections)
        for part in _chunk(text, DISCORD_MESSAGE_LIMIT - 50):
            if interaction.response.is_done():
                await interaction.followup.send(part, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(part, ephemeral=ephemeral)

def _chunk(s: str, n: int):
    return [s[i : i + n] for i in range(0, len(s), n)]

def _plain_help_text(title: str, sections: dict[str, list[str]]) -> str:
    lines = [f"**{title}**", ""]
    for section, items in sections.items():
        lines.append(f"**{section}:**")
        lines.extend(f"- {item}" for item in items)
        lines.append("")
    lines.append(HELP_FOOTER)
    return "\n".join(lines)

def _is_admin(interaction) -> bool:
    """Enhanced admin verification with security validation."""
    try:
        if isinstance(interaction.channel, discord.abc.GuildChannel):
            perms = interaction.user.guild_permissions  # type: ignore[attr-defined]
            
            # Validate permissions object
            if not security_utils.validate_discord_permissions(perms):
                logger.warning(f"[SECURITY] Invalid permissions object for user {interaction.user.id}")
                return False
            
            is_admin = bool(perms and perms.administrator)
            
            # Log admin access attempts
            if is_admin:
                security_utils.log_security_event(
                    "ADMIN_ACCESS", 
                    str(interaction.user.id), 
                    f"Admin access granted for command in channel {interaction.channel.id}",
                    "INFO"
                )
            
            return is_admin
    except Exception as e:
        logger.error(f"[SECURITY] Admin verification failed: {e}")
        security_utils.log_security_event(
            "ADMIN_VERIFICATION_FAILED", 
            str(interaction.user.id), 
            f"Admin verification exception: {e}",
            "MEDIUM"
        )
    return False

async def send_discord_response(interaction: discord.Interaction, **kwargs) -> bool:
    """
    Safely send a Discord response with rate limit handling and retry logic.
    Returns True if successful, False if failed after retries.
    """
    max_retries = 3
    base_delay = 1.0

    for attempt in range(max_retries):
        try:
            if interaction.response.is_done():
                await interaction.followup.send(**kwargs)
            else:
                await interaction.response.send_message(**kwargs)
            return True

        except RateLimited as e:
            retry_after = getattr(e, 'retry_after', base_delay * (2 ** attempt))
            logger.warning(f"Rate limited. Retrying in {retry_after}s (attempt {attempt + 1}/{max_retries})")
            await asyncio.sleep(retry_after)

        except HTTPException as e:
            if e.code == 40060:  # Interaction has already been acknowledged
                logger.warning(f"Interaction already acknowledged, trying followup: {e}")
                try:
                    await interaction.followup.send(**kwargs)
                    return True
                except Exception as followup_error:
                    logger.error(f"Followup also failed: {followup_error}")
                    return False
            else:
                logger.error(f"HTTP error (code {e.code}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(base_delay * (2 ** attempt))
                    continue
                return False

        except Exception as e:
            logger.error(f"Unexpected error sending Discord response: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(base_delay * (2 ** attempt))
                continue
            return False

    return False

def safe_command(fn):
    """Wrap command with logging, error handling, and compose with command_logger."""
    @command_logger_decorator(command_logger)
    async def wrapped(interaction):
        # The command_logger_decorator already handles interaction validation and logging
        # Just execute the function - no double wrapping
        return await fn(interaction)
    return wrapped

# --- Command Setup -------------------------------------------------------------

def setup_basic_commands(bot):
    """Setup basic bot slash commands with unified help & safe wrapper."""

    @bot.tree.command(name="ping", description="Test bot responsiveness")
    @safe_command
    async def ping(interaction):
        latency_ms = round(bot.latency * 1000)
        await send_discord_response(interaction, content=f"🏓 Pong! Latency: {latency_ms}ms", ephemeral=True)

    # Main interface function (moved from vibe command)
    async def launch_main_interface(interaction):
        """Main control center with button UI."""
        embed = discord.Embed(
            title="🎉 Vibe-Coder Control Center",
            description="**V2_SWARM Main Interface** — All controls in one place!",
            color=0xFF6B35
        )
        embed.add_field(
            name="🎯 **Available Controls:**",
            value=(
                "• **👥 Agent Coordination** — Send messages to agents\n"
                "• **📝 Devlog & Updates** — Record your work\n"
                "• **📊 System Status** — Check bot health\n"
                "• **🎓 Onboard Agent** — Launch agent onboarding (admin)\n"
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
        agent_button = Button(label="👥 Agent Coordination", style=discord.ButtonStyle.primary, custom_id="main:agents")
        devlog_button = Button(label="📝 Devlog & Updates", style=discord.ButtonStyle.secondary, custom_id="main:devlog")
        status_button = Button(label="📊 System Status", style=discord.ButtonStyle.success, custom_id="main:status")
        restart_button = Button(label="🔄 Restart Bot", style=discord.ButtonStyle.danger, custom_id="main:restart")
        shutdown_button = Button(label="⏹️ Shutdown Bot", style=discord.ButtonStyle.danger, custom_id="main:shutdown")

        # --- Callbacks --------------------------------------------------------
        async def agent_cb(cb_inter):
            agent_embed = discord.Embed(
                title="👥 Agent Coordination",
                description="Choose how you want to coordinate with the swarm:",
                color=0x00FF00
            )
            agent_info = {
                "Agent-1": "Integration & Core Systems Specialist",
                "Agent-2": "Architecture & Design Specialist",
                "Agent-3": "Infrastructure & DevOps Specialist",
                "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
                "Agent-5": "Business Intelligence Specialist",
                "Agent-6": "Coordination & Communication Specialist",
                "Agent-7": "Web Development Specialist",
                "Agent-8": "Operations & Support Specialist"
            }
            for agent_id, role in agent_info.items():
                agent_embed.add_field(name=f"**{agent_id}**", value=f"• {role}", inline=True)
            agent_embed.set_footer(text="🐝 WE ARE SWARM — Click to send messages!")
            if cb_inter.response.is_done():
                await cb_inter.followup.send(embed=agent_embed, ephemeral=True)
            else:
                await cb_inter.response.edit_message(embed=agent_embed, view=None)

        async def devlog_cb(cb_inter):
            devlog_embed = discord.Embed(
                title="📝 Devlog & Project Updates",
                description="Record your work and create updates:",
                color=0x0099FF
            )
            devlog_embed.add_field(
                name="📝 **Available Actions:**",
                value="• Create devlog entries\n• Record milestones\n• Update project status\n• Track V2 compliance",
                inline=False
            )
            devlog_embed.set_footer(text="📝 Click to start logging your work!")
            if cb_inter.response.is_done():
                await cb_inter.followup.send(embed=devlog_embed, ephemeral=True)
            else:
                await cb_inter.response.edit_message(embed=devlog_embed, view=None)

        async def status_cb(cb_inter):
            bot_name = bot.user.name if bot.user else "Discord Commander"
            status_embed = discord.Embed(title="📊 System Status", description="Current status of all systems:", color=0x00FF00)
            status_embed.add_field(
                name="✅ **Messaging System**",
                value="• PyAutoGUI automation active\n• Agent coordinates loaded\n• Message delivery operational",
                inline=False
            )
            status_embed.add_field(
                name="🚀 **Discord Bot**",
                value=f"• Bot: {bot_name}\n• Status: Online and ready\n• Commands: 2 active",
                inline=False
            )
            if cb_inter.response.is_done():
                await cb_inter.followup.send(embed=status_embed, ephemeral=True)
            else:
                await cb_inter.response.edit_message(embed=status_embed, view=None)

        async def restart_cb(cb_inter):
            if not _is_admin(cb_inter):
                return await _deny(cb_inter, "You need **Administrator** to restart the bot.")
            
            # Log critical action attempt
            security_utils.log_security_event(
                "CRITICAL_ACTION_ATTEMPT", 
                str(cb_inter.user.id), 
                f"Restart command initiated by admin in channel {cb_inter.channel.id}",
                "HIGH"
            )
            
            confirm_view = discord.ui.View(timeout=60)
            yes_btn = Button(label="✅ Yes, Restart", style=discord.ButtonStyle.danger, custom_id="confirm:restart:yes")
            no_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, custom_id="confirm:restart:no")

            async def yes_restart(inner):
                # Log critical action execution
                security_utils.log_security_event(
                    "CRITICAL_ACTION_EXECUTED", 
                    str(inner.user.id), 
                    f"Restart command executed by admin in channel {inner.channel.id}",
                    "CRITICAL"
                )
                
                if inner.response.is_done():
                    await inner.followup.send("🔄 Restart initiated! Bot will restart shortly.", ephemeral=True)
                else:
                    await inner.response.edit_message(content="🔄 **Restarting Discord Commander...**", embed=None, view=None)
                    await inner.followup.send("✅ Restart initiated! Bot will restart shortly.", ephemeral=True)
                
                # Actually restart the bot
                restart_success = await restart_manager.restart_bot("Admin requested restart via Discord interface")
                if not restart_success:
                    await inner.followup.send("❌ Restart failed. Please restart manually.", ephemeral=True)

            async def no_restart(inner):
                if inner.response.is_done():
                    await inner.followup.send("❌ Restart cancelled.", ephemeral=True)
                else:
                    await inner.response.edit_message(content="❌ **Restart cancelled**", embed=None, view=None)

            yes_btn.callback = yes_restart
            no_btn.callback = no_restart
            confirm_view.add_item(yes_btn)
            confirm_view.add_item(no_btn)

            embed = discord.Embed(
                title="🔄 Bot Restart",
                description="Are you sure you want to restart the Discord Commander?",
                color=0xFF9900
            ).add_field(
                name="⚠️ **Warning:**",
                value="• This will disconnect the bot\n• Active sessions will be lost\n• Bot should restart automatically",
                inline=False
            )
            if cb_inter.response.is_done():
                await cb_inter.followup.send(embed=embed, view=confirm_view, ephemeral=True)
            else:
                await cb_inter.response.edit_message(embed=embed, view=confirm_view)

        async def shutdown_cb(cb_inter):
            if not _is_admin(cb_inter):
                return await _deny(cb_inter, "You need **Administrator** to shutdown the bot.")
            
            # Log critical action attempt
            security_utils.log_security_event(
                "CRITICAL_ACTION_ATTEMPT", 
                str(cb_inter.user.id), 
                f"Shutdown command initiated by admin in channel {cb_inter.channel.id}",
                "HIGH"
            )
            
            confirm_view = discord.ui.View(timeout=60)
            yes_btn = Button(label="⏹️ Yes, Shutdown", style=discord.ButtonStyle.danger, custom_id="confirm:shutdown:yes")
            no_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, custom_id="confirm:shutdown:no")

            async def yes_shutdown(inner):
                # Log critical action execution
                security_utils.log_security_event(
                    "CRITICAL_ACTION_EXECUTED", 
                    str(inner.user.id), 
                    f"Shutdown command executed by admin in channel {inner.channel.id}",
                    "CRITICAL"
                )
                
                if inner.response.is_done():
                    await inner.followup.send("⏹️ Shutdown initiated! Bot is shutting down.", ephemeral=True)
                else:
                    await inner.response.edit_message(content="⏹️ **Shutting down Discord Commander...**", embed=None, view=None)
                    await inner.followup.send("⏹️ Shutdown initiated! Bot is shutting down.", ephemeral=True)
                
                # Actually shutdown the bot
                logger.info("[SHUTDOWN] Admin requested shutdown via Discord interface")
                await asyncio.sleep(1)  # Give time for the message to be sent
                os._exit(0)  # Graceful shutdown

            async def no_shutdown(inner):
                if inner.response.is_done():
                    await inner.followup.send("❌ Shutdown cancelled.", ephemeral=True)
                else:
                    await inner.response.edit_message(content="❌ **Shutdown cancelled**", embed=None, view=None)

            yes_btn.callback = yes_shutdown
            no_btn.callback = no_shutdown
            confirm_view.add_item(yes_btn)
            confirm_view.add_item(no_btn)

            embed = discord.Embed(
                title="⏹️ Bot Shutdown",
                description="Are you sure you want to shutdown the Discord Commander?",
                color=0xFF0000
            ).add_field(
                name="⚠️ **Warning:**",
                value="• This will disconnect the bot\n• Bot will NOT restart automatically\n• Active sessions will be lost",
                inline=False
            )
            if cb_inter.response.is_done():
                await cb_inter.followup.send(embed=embed, view=confirm_view, ephemeral=True)
            else:
                await cb_inter.response.edit_message(embed=embed, view=confirm_view)

        # Bind callbacks
        agent_button.callback = agent_cb
        devlog_button.callback = devlog_cb
        status_button.callback = status_cb
        restart_button.callback = restart_cb
        shutdown_button.callback = shutdown_cb

        # Onboard Agent button
        onboard_button = Button(
            label="🎓 Onboard Agent",
            style=discord.ButtonStyle.primary,
            custom_id="main:onboard"
        )

        async def onboard_callback(cb_inter: discord.Interaction):
            if not _is_admin(cb_inter):
                return await _deny(cb_inter, "Administrator required to onboard.")
            
            class OnboardModal(discord.ui.Modal, title="🎓 Onboard Agent"):
                agent = discord.ui.TextInput(
                    label="Agent (e.g., Agent-8)", placeholder="Agent-8", required=True, max_length=32
                )
                mode = discord.ui.TextInput(
                    label="Mode (manual|semi|full)", placeholder="manual", required=True, max_length=10, default="manual"
                )
                role = discord.ui.TextInput(
                    label="Role (optional)", placeholder="SSOT & System Integration Specialist", required=False, max_length=80
                )
                dry = discord.ui.TextInput(
                    label="Dry run? true/false", placeholder="false", required=False, max_length=5
                )

                async def on_submit(self, inter: discord.Interaction):
                    agent_val = str(self.agent).strip()
                    mode_val  = str(self.mode).strip().lower()
                    role_val  = str(self.role).strip() or None
                    dry_val   = (str(self.dry).strip().lower() == "true")

                    if mode_val not in {"manual","semi","full"}:
                        return await _reply(inter, content="⚠ Invalid mode. Use manual|semi|full.", ephemeral=True)

                    if is_onboarding_running(agent_val):
                        return await _reply(inter, content=f"⏳ Onboarding already running for **{agent_val}**.", ephemeral=True)

                    await _reply(inter, content=f"🎓 Starting onboarding for **{agent_val}** in **{mode_val}**…", ephemeral=True)
                    await kickoff_onboarding(agent=agent_val, mode=mode_val, role=role_val, dry_run=dry_val)
                    await _reply(inter, content=f"✅ Onboarding launched for **{agent_val}** (mode={mode_val}).", ephemeral=True)

            await cb_inter.response.send_modal(OnboardModal())

        onboard_button.callback = onboard_callback

        # Add buttons
        view.add_item(agent_button)
        view.add_item(devlog_button)
        view.add_item(status_button)
        view.add_item(onboard_button)
        view.add_item(restart_button)
        view.add_item(shutdown_button)

        # Use safe response function to handle rate limits and double acknowledgment
        await send_discord_response(interaction, embed=embed, view=view, ephemeral=True)
        logger.info(f"Main interface sent to {interaction.user}")

    @bot.tree.command(name="help", description="💡 Get help and learn how to use V2_SWARM")
    @safe_command
    async def help_cmd(interaction):
        """Vibe-coder help + quick action buttons."""
        embed = discord.Embed(
            title="💡 Vibe-Coder Help Guide",
            description="**V2_SWARM is designed for vibe coding!**",
            color=0x00FF00
        )
        embed.add_field(
            name="🎯 **Getting Started:**",
            value="1) Click **Launch Main Interface**  2) Click buttons  3) Follow prompts  4) Get instant feedback",
            inline=False
        )
        embed.add_field(
            name="🚀 **Controls:**",
            value="👥 Agents • 📝 Devlog • 📊 Status • 🎓 Onboard (admin) • 🔄 Restart (admin) • ⏹️ Shutdown (admin)",
            inline=False
        )
        embed.set_footer(text="🎉 Vibe coding made simple — just click and create!")

        view = discord.ui.View(timeout=300)
        launch_btn = Button(label="🎯 Launch Main Interface", style=discord.ButtonStyle.primary, custom_id="help:launch")
        agents_btn = Button(label="👥 See Agent List", style=discord.ButtonStyle.secondary, custom_id="help:agents")
        status_btn = Button(label="📊 Check Status", style=discord.ButtonStyle.success, custom_id="help:status")

        async def launch_cb(cb_inter):
            # Launch the main interface directly
            await launch_main_interface(cb_inter)

        async def agents_cb(cb_inter):
            agents_embed = discord.Embed(
                title="👥 V2_SWARM Agents",
                description="Eight specialized agents ready to coordinate:",
                color=0xFF6B35
            )
            for k, v in {
                "Agent-1": "Integration & Core Systems",
                "Agent-2": "Architecture & Design",
                "Agent-3": "Infrastructure & DevOps",
                "Agent-4": "Quality Assurance (CAPTAIN)",
                "Agent-5": "Business Intelligence",
                "Agent-6": "Coordination & Communication",
                "Agent-7": "Web Development",
                "Agent-8": "Operations & Support",
            }.items():
                agents_embed.add_field(name=f"**{k}**", value=f"• {v}", inline=True)
            agents_embed.set_footer(text="🐝 WE ARE SWARM — All agents coordinated!")
            if cb_inter.response.is_done():
                await cb_inter.followup.send(embed=agents_embed, ephemeral=True)
            else:
                await cb_inter.response.edit_message(embed=agents_embed, view=None)

        async def status_cb(cb_inter):
            bot_name = bot.user.name if bot.user else "Discord Commander"
            status_embed = discord.Embed(title="📊 System Status", description="Current status of all systems:", color=0x00FF00)
            status_embed.add_field(
                name="✅ **Messaging System**",
                value="• PyAutoGUI automation active\n• Agent coordinates loaded\n• Message delivery operational",
                inline=False
            )
            status_embed.add_field(
                name="🚀 **Discord Bot**",
                value=f"• Bot: {bot_name}\n• Status: Online and ready\n• Commands: 3 active",
                inline=False
            )
            if cb_inter.response.is_done():
                await cb_inter.followup.send(embed=status_embed, ephemeral=True)
            else:
                await cb_inter.response.edit_message(embed=status_embed, view=None)

        launch_btn.callback = launch_cb
        agents_btn.callback = agents_cb
        status_btn.callback = status_cb

        view.add_item(launch_btn)
        view.add_item(agents_btn)
        view.add_item(status_btn)

        # Use safe response function to handle rate limits and double acknowledgment
        await send_discord_response(interaction, embed=embed, view=view, ephemeral=True)

    logger.info("=== DISCORD COMMANDS REGISTERED ===")
    logger.info("Available commands:")
    logger.info("  /ping - Test bot responsiveness")
    logger.info("  /help - Vibe-coder friendly help guide with main interface")
    logger.info("  /agents - List all agents and status")
    logger.info("  /swarm - Send message to all agents")
    logger.info("  /send - Send message to specific agent")
    logger.info("  /devlog - Create devlog entry")
    logger.info("  /status - Show system status")
    logger.info("  /command-stats - View command statistics")
    logger.info("  /command-history - View command history")
    logger.info("  /bot-health - Check bot health")
    logger.info("  /clear-logs - Clear logs (admin only)")
    logger.info("==================================")
    logger.info("Bot is ready! Use /help and click 'Launch Main Interface' to get started.")


async def _reply(inter: discord.Interaction, *, content: str | None = None,
                 embed: discord.Embed | None = None, view: discord.ui.View | None = None,
                 ephemeral: bool = True):
    """Reply safely across guild/DM, response/followup, with ephemeral fallback."""
    # Filter out None values to avoid Discord.py issues
    kwargs = {}
    if content is not None:
        kwargs["content"] = content
    if embed is not None:
        kwargs["embed"] = embed
    if view is not None:
        kwargs["view"] = view
    
    try:
        if hasattr(inter, "response") and not inter.response.is_done():
            await inter.response.send_message(**kwargs, ephemeral=ephemeral)
        else:
            await inter.followup.send(**kwargs, ephemeral=ephemeral)
    except discord.HTTPException:
        # Ephemeral not allowed (e.g., DM) → retry non-ephemeral
        if hasattr(inter, "response") and not inter.response.is_done():
            await inter.response.send_message(**kwargs, ephemeral=False)
        else:
            await inter.followup.send(**kwargs, ephemeral=False)

async def _deny(inter, reason):
    """Ephemeral permission denial helper."""
    msg = f"⛔ **Action denied** — {reason}"
    try:
        await send_discord_response(inter, content=msg, ephemeral=True)
    except Exception:
        pass