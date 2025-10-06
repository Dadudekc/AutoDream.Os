#!/usr/bin/env python3
"""
Discord Server Manager - Utilities
==================================

Server information, audit, and utility functions for Discord server management.
Extracted from main server manager for V2 compliance.

Features:
- Server information and statistics
- Comprehensive server audit
- Security analysis
- Help and documentation
- Utility functions

Usage:
    from src.services.discord_commander.server_manager_utils import DiscordServerUtils

    utils = DiscordServerUtils(bot, guild)
    await utils.server_info()
"""

from datetime import datetime

import discord


class DiscordServerUtils:
    """Discord server utility functions for AI assistant."""

    def __init__(self, bot, guild: discord.Guild):
        """
        Initialize Discord server utilities.

        Args:
            bot: Discord bot instance
            guild: Discord guild (server) instance
        """
        self.bot = bot
        self.guild = guild

    async def server_info(self) -> bool:
        """Get comprehensive server information."""
        print("🏰 Discord Server Information")
        print("=" * 60)

        if not self.guild:
            print("❌ Server not accessible")
            return False

        # Basic server info
        print("📋 Server Details:")
        print(f"   • Name: {self.guild.name}")
        print(f"   • ID: {self.guild.id}")
        print(f"   • Owner: {self.guild.owner}")
        print(f"   • Created: {self.guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   • Verification Level: {self.guild.verification_level}")
        print(f"   • Boost Level: {self.guild.premium_tier}")

        # Member statistics
        member_count = self.guild.member_count
        online_count = len([m for m in self.guild.members if m.status != discord.Status.offline])
        bot_count = len([m for m in self.guild.members if m.bot])

        print("\n👥 Member Statistics:")
        print(f"   • Total Members: {member_count}")
        print(f"   • Online Members: {online_count}")
        print(f"   • Bots: {bot_count}")
        print(f"   • Humans: {member_count - bot_count}")

        # Channel statistics
        text_channels = len(self.guild.text_channels)
        voice_channels = len(self.guild.voice_channels)
        categories = len(self.guild.categories)

        print("\n📺 Channel Statistics:")
        print(f"   • Text Channels: {text_channels}")
        print(f"   • Voice Channels: {voice_channels}")
        print(f"   • Categories: {categories}")
        print(f"   • Total Channels: {text_channels + voice_channels}")

        # Role statistics
        role_count = len(self.guild.roles)
        print("\n🎭 Role Statistics:")
        print(f"   • Total Roles: {role_count}")

        # Emoji and sticker statistics
        emoji_count = len(self.guild.emojis)
        sticker_count = len(self.guild.stickers)

        print("\n😀 Content Statistics:")
        print(f"   • Custom Emojis: {emoji_count}")
        print(f"   • Stickers: {sticker_count}")

        print("\n" + "=" * 60)
        return True

    async def server_audit(self) -> bool:
        """Perform comprehensive server audit."""
        print("🔍 Discord Server Audit")
        print("=" * 60)

        if not self.guild:
            print("❌ Server not accessible")
            return False

        # Security audit
        print("🔒 Security Audit:")

        # Check bot permissions
        bot_member = self.guild.get_member(self.bot.user.id)
        if bot_member:
            perms = bot_member.guild_permissions
            print(f"   • Administrator: {'✅' if perms.administrator else '❌'}")
            print(f"   • Manage Channels: {'✅' if perms.manage_channels else '❌'}")
            print(f"   • Manage Roles: {'✅' if perms.manage_roles else '❌'}")
            print(f"   • Manage Members: {'✅' if perms.kick_members else '❌'}")
            print(f"   • Send Messages: {'✅' if perms.send_messages else '❌'}")

        # Check for dangerous permissions
        dangerous_roles = []
        for role in self.guild.roles:
            if role.permissions.administrator and role.name != self.guild.owner.name:
                dangerous_roles.append(role.name)

        if dangerous_roles:
            print(f"   ⚠️ Roles with Administrator permission: {', '.join(dangerous_roles)}")
        else:
            print("   ✅ No dangerous administrator roles found")

        # Channel audit
        print("\n📺 Channel Audit:")
        orphaned_channels = [
            c
            for c in self.guild.channels
            if c.category is None and not isinstance(c, discord.CategoryChannel)
        ]
        if orphaned_channels:
            print(f"   ⚠️ Orphaned channels: {len(orphaned_channels)}")
            for channel in orphaned_channels:
                print(f"     - {channel.name} ({channel.id})")
        else:
            print("   ✅ All channels are properly categorized")

        # Member audit
        print("\n👥 Member Audit:")
        recent_joins = [
            m
            for m in self.guild.members
            if m.joined_at and (datetime.now(m.joined_at.tzinfo) - m.joined_at).days < 7
        ]
        print(f"   • Recent joins (7 days): {len(recent_joins)}")

        inactive_members = [m for m in self.guild.members if m.status == discord.Status.offline]
        print(f"   • Inactive members: {len(inactive_members)}")

        # Role audit
        print("\n🎭 Role Audit:")
        unused_roles = []
        for role in self.guild.roles:
            if (
                role.name != "@everyone"
                and len([m for m in self.guild.members if role in m.roles]) == 0
            ):
                unused_roles.append(role.name)

        if unused_roles:
            print(f"   ⚠️ Unused roles: {len(unused_roles)}")
            for role in unused_roles[:5]:  # Show first 5
                print(f"     - {role}")
        else:
            print("   ✅ No unused roles found")

        print("\n" + "=" * 60)
        return True

    def show_help(self) -> bool:
        """Show help information."""
        print("🤖 Discord Server Manager - Help")
        print("=" * 60)

        print("📋 Available Commands:")
        print("   server-info                    - Get comprehensive server information")
        print("   list-channels [--category CAT] - List all channels (optionally by category)")
        print("   create-channel --name NAME --type TYPE [--category CAT] [--topic TOPIC]")
        print("   delete-channel --id CHANNEL_ID - Delete a channel by ID")
        print("   manage-roles --action ACTION [--name NAME] [--permissions PERMS]")
        print("   manage-members --action ACTION [--member-id ID] [--reason REASON]")
        print("   send-message --channel-id ID --content CONTENT [--embed]")
        print("   server-audit                   - Perform comprehensive server audit")
        print("   help                           - Show this help message")

        print("\n🎭 Role Actions:")
        print("   list                           - List all roles")
        print("   create                         - Create new role")
        print("   delete                         - Delete role")

        print("\n👥 Member Actions:")
        print("   list                           - List all members")
        print("   kick                           - Kick member")
        print("   ban                            - Ban member")

        print("\n📺 Channel Types:")
        print("   text, txt                      - Text channel")
        print("   voice, vc                      - Voice channel")
        print("   category, cat                  - Category")

        print("\n💡 Examples:")
        print("   python discord_server_manager.py server-info")
        print("   python discord_server_manager.py list-channels")
        print("   python discord_server_manager.py create-channel --name 'general' --type text")
        print("   python discord_server_manager.py manage-roles --action list")
        print(
            "   python discord_server_manager.py send-message --channel-id 123456789 --content 'Hello!'"
        )

        print("\n" + "=" * 60)
        return True
