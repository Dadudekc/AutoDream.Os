#!/usr/bin/env python3
"""
Discord Server Manager - Core Logic
===================================

Main Discord server management logic for AI assistant control.
V2 Compliant: ≤400 lines, imports from modular components.

Features:
- Comprehensive Discord server management
- Channel management (create, delete, modify)
- Role management (create, assign, modify permissions)
- Member management (kick, ban, mute, etc.)
- Permission management
- Server settings configuration
- Message management
- Webhook management
- Server audit and monitoring

Usage:
    from src.services.discord_commander.server_manager_core import DiscordServerManager

    manager = DiscordServerManager()
    await manager.server_info()
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands

# Import our modular components
from .server_manager_commands import DiscordServerCommands
from .server_manager_utils import DiscordServerUtils


class DiscordServerManager:
    """Comprehensive Discord server management tool for AI assistant."""

    def __init__(self):
        """Initialize Discord Server Manager."""
        self.project_root = Path(__file__).parent
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

        # Initialize modular components
        self.commands = None
        self.utils = None

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
                    # Initialize modular components
                    self.commands = DiscordServerCommands(self.bot, self.guild)
                    self.utils = DiscordServerUtils(self.bot, self.guild)
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
        if not await self._connect_bot():
            return False
        return await self.utils.server_info()

    async def list_channels(self, category: str = None) -> bool:
        """List all channels in the server."""
        if not await self._connect_bot():
            return False
        return await self.commands.list_channels(category)

    async def create_channel(
        self, name: str, channel_type: str = "text", category: str = None, topic: str = None
    ) -> bool:
        """Create a new channel in the server."""
        if not await self._connect_bot():
            return False
        return await self.commands.create_channel(name, channel_type, category, topic)

    async def delete_channel(self, channel_id: int) -> bool:
        """Delete a channel by ID."""
        if not await self._connect_bot():
            return False
        return await self.commands.delete_channel(channel_id)

    async def manage_roles(
        self, action: str, role_name: str = None, permissions: str = None
    ) -> bool:
        """Manage server roles."""
        if not await self._connect_bot():
            return False
        return await self.commands.manage_roles(action, role_name, permissions)

    async def manage_members(self, action: str, member_id: int = None, reason: str = None) -> bool:
        """Manage server members."""
        if not await self._connect_bot():
            return False
        return await self.commands.manage_members(action, member_id, reason)

    async def send_message(self, channel_id: int, content: str, embed: bool = False) -> bool:
        """Send a message to a specific channel."""
        if not await self._connect_bot():
            return False
        return await self.commands.send_message(channel_id, content, embed)

    async def server_audit(self) -> bool:
        """Perform comprehensive server audit."""
        if not await self._connect_bot():
            return False
        return await self.utils.server_audit()

    def show_help(self) -> bool:
        """Show help information."""
        return self.utils.show_help() if self.utils else False


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

    # Run the command
    try:
        result = asyncio.run(run_command())
        return result
    except KeyboardInterrupt:
        print("\n⏹️ Operation cancelled by user")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
