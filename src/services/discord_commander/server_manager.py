#!/usr/bin/env python3
"""
Discord Server Manager
======================
Comprehensive Discord server management tool for AI assistant control.
Allows AI to manage Discord server, channels, permissions, members, roles, etc.

Features:
- Channel management (create, delete, modify)
- Role management (create, assign, modify permissions)
- Member management (kick, ban, mute, etc.)
- Permission management
- Server settings configuration
- Message management
- Webhook management
- Server audit and monitoring

Usage:
    python discord_server_manager.py --help
    python discord_server_manager.py server-info
    python discord_server_manager.py list-channels
    python discord_server_manager.py create-channel --name "new-channel" --type text
    python discord_server_manager.py manage-roles --action list

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import argparse
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

import discord
from discord.ext import commands

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))


class DiscordServerManager:
    """Comprehensive Discord server management tool for AI assistant."""

    def __init__(self):
        """Initialize Discord Server Manager."""
        self.project_root = project_root
        self.bot = None
        self.guild = None
        self.env_loaded = False

        # Load environment
        self._load_environment()

        # Discord configuration
        self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
        self.guild_id = (
            int(os.getenv("DISCORD_GUILD_ID", 0)) if os.getenv("DISCORD_GUILD_ID") else None
        )

        if not self.bot_token or not self.guild_id:
            print("❌ Missing Discord bot token or guild ID")
            sys.exit(1)

    def _load_environment(self) -> bool:
        """Load environment variables from .env file."""
        try:
            env_file = self.project_root / ".env"
            if not env_file.exists():
                print("❌ .env file not found")
                return False

            # Load .env file manually
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        value = value.strip("\"'")
                        os.environ[key] = value

            self.env_loaded = True
            return True
        except Exception as e:
            print(f"❌ Failed to load .env file: {e}")
            return False

    async def _connect_bot(self) -> bool:
        """Connect Discord bot."""
        try:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.guilds = True
            intents.members = True
            intents.guild_messages = True
            intents.guild_reactions = True

            self.bot = commands.Bot(command_prefix="!", intents=intents)

            @self.bot.event
            async def on_ready():
                print(f"🤖 Discord bot ready: {self.bot.user}")
                self.guild = self.bot.get_guild(self.guild_id)
                if self.guild:
                    print(f"🏰 Connected to server: {self.guild.name}")
                else:
                    print(f"❌ Server {self.guild_id} not found")

            # Start bot and wait for ready
            bot_task = asyncio.create_task(self.bot.start(self.bot_token))

            # Wait for bot to be ready with timeout
            try:
                await asyncio.wait_for(asyncio.sleep(5), timeout=10)
            except TimeoutError:
                print("❌ Bot connection timeout")
                return False

            return self.guild is not None

        except Exception as e:
            print(f"❌ Failed to connect bot: {e}")
            return False

    async def server_info(self) -> bool:
        """Get comprehensive server information."""
        print("🏰 Discord Server Information")
        print("=" * 60)

        if not await self._connect_bot():
            return False

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

    async def list_channels(self, category: str = None) -> bool:
        """List all channels in the server."""
        print("📺 Discord Server Channels")
        print("=" * 60)

        if not await self._connect_bot():
            return False

        if not self.guild:
            print("❌ Server not accessible")
            return False

        # List categories
        if not category:
            print("📁 Categories:")
            for cat in self.guild.categories:
                print(f"   • {cat.name} (ID: {cat.id})")
                for channel in cat.channels:
                    channel_type = (
                        "🔤 Text" if isinstance(channel, discord.TextChannel) else "🔊 Voice"
                    )
                    print(f"     - {channel.name} {channel_type} (ID: {channel.id})")

            # List uncategorized channels
            uncategorized = [c for c in self.guild.channels if c.category is None]
            if uncategorized:
                print("\n📋 Uncategorized Channels:")
                for channel in uncategorized:
                    channel_type = (
                        "🔤 Text" if isinstance(channel, discord.TextChannel) else "🔊 Voice"
                    )
                    print(f"   • {channel.name} {channel_type} (ID: {channel.id})")

        else:
            # List specific category
            cat = discord.utils.get(self.guild.categories, name=category)
            if cat:
                print(f"📁 Category: {cat.name}")
                for channel in cat.channels:
                    channel_type = (
                        "🔤 Text" if isinstance(channel, discord.TextChannel) else "🔊 Voice"
                    )
                    print(f"   • {channel.name} {channel_type} (ID: {channel.id})")
            else:
                print(f"❌ Category '{category}' not found")
                return False

        print("\n" + "=" * 60)
        return True

    async def create_channel(
        self, name: str, channel_type: str = "text", category: str = None, topic: str = None
    ) -> bool:
        """Create a new channel in the server."""
        print(f"➕ Creating {channel_type} Channel: {name}")
        print("=" * 60)

        if not await self._connect_bot():
            return False

        if not self.guild:
            print("❌ Server not accessible")
            return False

        try:
            # Get category if specified
            category_obj = None
            if category:
                category_obj = discord.utils.get(self.guild.categories, name=category)
                if not category_obj:
                    print(f"❌ Category '{category}' not found")
                    return False

            # Create channel based on type
            if channel_type.lower() in ["text", "txt"]:
                overwrites = {
                    self.guild.default_role: discord.PermissionOverwrite(
                        read_messages=True, send_messages=True
                    )
                }

                channel = await self.guild.create_text_channel(
                    name=name, category=category_obj, topic=topic, overwrites=overwrites
                )
                print(f"✅ Text channel '{name}' created successfully")
                print(f"   • ID: {channel.id}")
                print(f"   • Category: {category_obj.name if category_obj else 'None'}")

            elif channel_type.lower() in ["voice", "vc"]:
                channel = await self.guild.create_voice_channel(name=name, category=category_obj)
                print(f"✅ Voice channel '{name}' created successfully")
                print(f"   • ID: {channel.id}")
                print(f"   • Category: {category_obj.name if category_obj else 'None'}")

            elif channel_type.lower() in ["category", "cat"]:
                channel = await self.guild.create_category(name=name)
                print(f"✅ Category '{name}' created successfully")
                print(f"   • ID: {channel.id}")

            else:
                print(f"❌ Unknown channel type: {channel_type}")
                return False

            print(f"💡 Channel URL: https://discord.com/channels/{self.guild.id}/{channel.id}")
            print("\n" + "=" * 60)
            return True

        except discord.Forbidden:
            print("❌ Insufficient permissions to create channel")
            return False
        except discord.HTTPException as e:
            print(f"❌ Discord API error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error creating channel: {e}")
            return False

    async def delete_channel(self, channel_id: int) -> bool:
        """Delete a channel by ID."""
        print(f"🗑️ Deleting Channel: {channel_id}")
        print("=" * 60)

        if not await self._connect_bot():
            return False

        if not self.guild:
            print("❌ Server not accessible")
            return False

        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                print(f"❌ Channel with ID {channel_id} not found")
                return False

            channel_name = channel.name
            await channel.delete()
            print(f"✅ Channel '{channel_name}' deleted successfully")

            print("\n" + "=" * 60)
            return True

        except discord.Forbidden:
            print("❌ Insufficient permissions to delete channel")
            return False
        except discord.HTTPException as e:
            print(f"❌ Discord API error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error deleting channel: {e}")
            return False

    async def manage_roles(
        self, action: str, role_name: str = None, permissions: str = None
    ) -> bool:
        """Manage server roles."""
        print(f"🎭 Managing Roles - Action: {action}")
        print("=" * 60)

        if not await self._connect_bot():
            return False

        if not self.guild:
            print("❌ Server not accessible")
            return False

        try:
            if action == "list":
                print("📋 Server Roles:")
                for role in sorted(self.guild.roles, key=lambda r: r.position, reverse=True):
                    member_count = len([m for m in self.guild.members if role in m.roles])
                    print(f"   • {role.name} (ID: {role.id}) - {member_count} members")

            elif action == "create":
                if not role_name:
                    print("❌ Role name required for creation")
                    return False

                # Parse permissions
                perm_value = discord.Permissions.none()
                if permissions:
                    perm_value = discord.Permissions(
                        **{p.strip(): True for p in permissions.split(",")}
                    )

                role = await self.guild.create_role(
                    name=role_name, permissions=perm_value, color=discord.Color.random()
                )
                print(f"✅ Role '{role_name}' created successfully")
                print(f"   • ID: {role.id}")
                print(f"   • Permissions: {permissions or 'Default'}")

            elif action == "delete":
                if not role_name:
                    print("❌ Role name required for deletion")
                    return False

                role = discord.utils.get(self.guild.roles, name=role_name)
                if not role:
                    print(f"❌ Role '{role_name}' not found")
                    return False

                await role.delete()
                print(f"✅ Role '{role_name}' deleted successfully")

            else:
                print(f"❌ Unknown action: {action}")
                return False

            print("\n" + "=" * 60)
            return True

        except discord.Forbidden:
            print("❌ Insufficient permissions to manage roles")
            return False
        except discord.HTTPException as e:
            print(f"❌ Discord API error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error managing roles: {e}")
            return False

    async def manage_members(self, action: str, member_id: int = None, reason: str = None) -> bool:
        """Manage server members."""
        print(f"👥 Managing Members - Action: {action}")
        print("=" * 60)

        if not await self._connect_bot():
            return False

        if not self.guild:
            print("❌ Server not accessible")
            return False

        try:
            if action == "list":
                print("📋 Server Members (showing first 20):")
                for i, member in enumerate(self.guild.members[:20]):
                    status_icon = {
                        discord.Status.online: "🟢",
                        discord.Status.idle: "🟡",
                        discord.Status.dnd: "🔴",
                        discord.Status.offline: "⚫",
                    }.get(member.status, "❓")

                    print(f"   • {member.display_name} ({member.name}) {status_icon}")
                    print(
                        f"     ID: {member.id}, Joined: {member.joined_at.strftime('%Y-%m-%d') if member.joined_at else 'Unknown'}"
                    )

                if len(self.guild.members) > 20:
                    print(f"   ... and {len(self.guild.members) - 20} more members")

            elif action == "kick":
                if not member_id:
                    print("❌ Member ID required for kick action")
                    return False

                member = self.guild.get_member(member_id)
                if not member:
                    print(f"❌ Member with ID {member_id} not found")
                    return False

                await member.kick(reason=reason or "Kicked by Discord Server Manager")
                print(f"✅ Member '{member.display_name}' kicked successfully")

            elif action == "ban":
                if not member_id:
                    print("❌ Member ID required for ban action")
                    return False

                member = self.guild.get_member(member_id)
                if not member:
                    print(f"❌ Member with ID {member_id} not found")
                    return False

                await member.ban(reason=reason or "Banned by Discord Server Manager")
                print(f"✅ Member '{member.display_name}' banned successfully")

            else:
                print(f"❌ Unknown action: {action}")
                return False

            print("\n" + "=" * 60)
            return True

        except discord.Forbidden:
            print("❌ Insufficient permissions to manage members")
            return False
        except discord.HTTPException as e:
            print(f"❌ Discord API error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error managing members: {e}")
            return False

    async def send_message(self, channel_id: int, content: str, embed: bool = False) -> bool:
        """Send a message to a specific channel."""
        print(f"📤 Sending Message to Channel: {channel_id}")
        print("=" * 60)

        if not await self._connect_bot():
            return False

        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                print(f"❌ Channel with ID {channel_id} not found")
                return False

            if embed:
                # Create embed message
                embed_obj = discord.Embed(
                    title="🤖 Discord Server Manager",
                    description=content,
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow(),
                )
                embed_obj.set_footer(text="Sent by Discord Server Manager")

                message = await channel.send(embed=embed_obj)
            else:
                # Send regular message
                message = await channel.send(content)

            print("✅ Message sent successfully")
            print(f"   • Channel: {channel.name}")
            print(f"   • Message ID: {message.id}")
            print(f"   • Content: {content[:100]}{'...' if len(content) > 100 else ''}")

            print("\n" + "=" * 60)
            return True

        except discord.Forbidden:
            print("❌ Insufficient permissions to send message")
            return False
        except discord.HTTPException as e:
            print(f"❌ Discord API error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False

    async def server_audit(self) -> bool:
        """Perform comprehensive server audit."""
        print("🔍 Discord Server Audit")
        print("=" * 60)

        if not await self._connect_bot():
            return False

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


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Discord Server Manager - Complete Discord server control"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Server info command
    subparsers.add_parser("server-info", help="Get comprehensive server information")

    # List channels command
    list_parser = subparsers.add_parser("list-channels", help="List all channels")
    list_parser.add_argument("--category", help="Filter by category name")

    # Create channel command
    create_parser = subparsers.add_parser("create-channel", help="Create a new channel")
    create_parser.add_argument("--name", required=True, help="Channel name")
    create_parser.add_argument(
        "--type",
        choices=["text", "txt", "voice", "vc", "category", "cat"],
        default="text",
        help="Channel type",
    )
    create_parser.add_argument("--category", help="Category name")
    create_parser.add_argument("--topic", help="Channel topic (text channels only)")

    # Delete channel command
    delete_parser = subparsers.add_parser("delete-channel", help="Delete a channel")
    delete_parser.add_argument("--id", type=int, required=True, help="Channel ID")

    # Manage roles command
    roles_parser = subparsers.add_parser("manage-roles", help="Manage server roles")
    roles_parser.add_argument(
        "--action", choices=["list", "create", "delete"], required=True, help="Action to perform"
    )
    roles_parser.add_argument("--name", help="Role name")
    roles_parser.add_argument("--permissions", help="Comma-separated permissions")

    # Manage members command
    members_parser = subparsers.add_parser("manage-members", help="Manage server members")
    members_parser.add_argument(
        "--action", choices=["list", "kick", "ban"], required=True, help="Action to perform"
    )
    members_parser.add_argument("--member-id", type=int, help="Member ID")
    members_parser.add_argument("--reason", help="Reason for action")

    # Send message command
    message_parser = subparsers.add_parser("send-message", help="Send message to channel")
    message_parser.add_argument("--channel-id", type=int, required=True, help="Channel ID")
    message_parser.add_argument("--content", required=True, help="Message content")
    message_parser.add_argument("--embed", action="store_true", help="Send as embed")

    # Server audit command
    subparsers.add_parser("server-audit", help="Perform comprehensive server audit")

    # Help command
    subparsers.add_parser("help", help="Show help information")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return False

    # Create manager instance
    manager = DiscordServerManager()

    if not manager.env_loaded:
        print("❌ Cannot proceed without .env file")
        return False

    # Execute command
    async def run_command():
        if args.command == "server-info":
            return await manager.server_info()
        elif args.command == "list-channels":
            return await manager.list_channels(args.category)
        elif args.command == "create-channel":
            return await manager.create_channel(args.name, args.type, args.category, args.topic)
        elif args.command == "delete-channel":
            return await manager.delete_channel(args.id)
        elif args.command == "manage-roles":
            return await manager.manage_roles(args.action, args.name, args.permissions)
        elif args.command == "manage-members":
            return await manager.manage_members(args.action, args.member_id, args.reason)
        elif args.command == "send-message":
            return await manager.send_message(args.channel_id, args.content, args.embed)
        elif args.command == "server-audit":
            return await manager.server_audit()
        elif args.command == "help":
            return manager.show_help()
        else:
            print(f"❌ Unknown command: {args.command}")
            return False

    try:
        success = asyncio.run(run_command())
        return success
    except KeyboardInterrupt:
        print("\n👋 Discord Server Manager interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Discord Server Manager error: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        # Clean up bot connection
        if manager.bot:
            asyncio.run(manager.bot.close())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
