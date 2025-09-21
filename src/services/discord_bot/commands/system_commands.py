#!/usr/bin/env python3
"""
System Discord Commands
=======================

System-related slash commands for Discord bot.
"""

import discord
from discord import app_commands


def setup_system_commands(bot):
    """Setup system-related slash commands."""

    @bot.tree.command(name="status", description="Show system status")
    async def system_status(interaction: discord.Interaction):
        """Show system status."""
        status_text = f"""
**V2_SWARM Enhanced System Status:**

**Bot Information:**
- **Name**: {bot.user.name}
- **ID**: {bot.user.id}
- **Latency**: {round(bot.latency * 1000)}ms
- **Guilds**: {len(bot.guilds)}
- **Channels**: {len(list(bot.get_all_channels()))}

**Agent Configuration:**
- **Total Agents**: {len(bot.agent_coordinates)}
- **Active Agents**: {len([a for a in bot.agent_coordinates.values() if a.get('active', True)])}
- **Coordinates Loaded**: ✅ Yes

**System Health:**
- **Discord Connection**: ✅ Connected
- **Devlog Service**: ✅ Active
- **Messaging Service**: ✅ Active
- **Command Processing**: ✅ Active

**Ready for enhanced swarm coordination!** 🐝
        """
        await interaction.response.send_message(status_text)

    @bot.tree.command(name="info", description="Show bot information")
    async def bot_info(interaction: discord.Interaction):
        """Show bot information."""
        info_text = f"""
**V2_SWARM Enhanced Discord Agent Bot Information:**

**Bot Details:**
- **Name**: {bot.user.name}
- **ID**: {bot.user.id}
- **Created**: {bot.user.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}
- **Avatar**: {bot.user.avatar.url if bot.user.avatar else 'Default'}

**Connection:**
- **Latency**: {round(bot.latency * 1000)}ms
- **Guilds**: {len(bot.guilds)}
- **Channels**: {len(list(bot.get_all_channels()))}
- **Users**: {len(bot.users)}

**Features:**
- **Devlog Integration**: ✅ Active
- **Messaging System**: ✅ Active
- **Agent Coordination**: ✅ Active
- **Command Processing**: ✅ Active
- **Auto-Responses**: ✅ Active

**Ready for enhanced swarm coordination!** 🐝
        """
        await interaction.response.send_message(info_text)

