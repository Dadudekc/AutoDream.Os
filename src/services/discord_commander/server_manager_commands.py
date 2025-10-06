#!/usr/bin/env python3
"""
Discord Server Manager - Commands
=================================

Channel, role, member, and message management commands for Discord server.
Extracted from main server manager for V2 compliance.

Features:
- Channel management (create, delete, modify)
- Role management (create, assign, modify permissions)
- Member management (kick, ban, mute, etc.)
- Message management
- Permission management

Usage:
    from src.services.discord_commander.server_manager_commands import DiscordServerCommands

    commands = DiscordServerCommands(bot, guild)
    await commands.create_channel("new-channel", "text")
"""

import discord
from discord.ext import commands


class DiscordServerCommands:
    """Discord server management commands for AI assistant."""

    def __init__(self, bot: commands.Bot, guild: discord.Guild):
        """
        Initialize Discord server commands.

        Args:
            bot: Discord bot instance
            guild: Discord guild (server) instance
        """
        self.bot = bot
        self.guild = guild

    async def list_channels(self, category: str = None) -> bool:
        """List all channels in the server."""
        print("📺 Discord Server Channels")
        print("=" * 60)

        if not self.guild:
            print("❌ Server not accessible")
            return False

        try:
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

        except Exception as e:
            print(f"❌ Error listing channels: {e}")
            return False

    async def create_channel(
        self, name: str, channel_type: str = "text", category: str = None, topic: str = None
    ) -> bool:
        """Create a new channel in the server."""
        print(f"➕ Creating {channel_type} Channel: {name}")
        print("=" * 60)

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

        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                print(f"❌ Channel with ID {channel_id} not found")
                return False

            if embed:
                # Create embed message
                from datetime import datetime

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
