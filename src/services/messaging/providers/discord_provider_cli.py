#!/usr/bin/env python3
"""
Discord Provider CLI - Command Line Interface
=============================================

Command-line interface for Discord messaging provider.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: discord_provider.py (432 lines) - CLI module
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import discord
from discord.ext import commands

from src.services.messaging.providers.discord_provider_core import DiscordMessagingProvider


def create_argument_parser():
    """Create argument parser for CLI commands"""
    parser = argparse.ArgumentParser(
        description="Discord Provider CLI - Discord messaging system interface"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Send message command
    send_parser = subparsers.add_parser("send", help="Send message to agent")
    send_parser.add_argument("--agent-id", required=True, help="Target agent ID")
    send_parser.add_argument("--message", required=True, help="Message content")
    send_parser.add_argument("--from-agent", help="Sender agent ID")
    
    # Broadcast command
    broadcast_parser = subparsers.add_parser("broadcast", help="Send broadcast message")
    broadcast_parser.add_argument("--message", required=True, help="Message content")
    broadcast_parser.add_argument("--from-agent", help="Sender agent ID")
    broadcast_parser.add_argument("--exclude", nargs="*", help="Agents to exclude")
    
    # Channel command
    channel_parser = subparsers.add_parser("channel", help="Send message to channel")
    channel_parser.add_argument("--channel-id", type=int, required=True, help="Discord channel ID")
    channel_parser.add_argument("--message", required=True, help="Message content")
    channel_parser.add_argument("--from-agent", help="Sender agent ID")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Get provider status")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test Discord provider")
    
    return parser


async def handle_send_command(args, provider):
    """Handle send message command"""
    success = await provider.manage_messaging(
        "send_to_agent",
        agent_id=args.agent_id,
        message=args.message,
        from_agent=args.from_agent
    )
    
    if success:
        print(f"✅ Message sent to agent {args.agent_id}")
        return 0
    else:
        print(f"❌ Failed to send message to agent {args.agent_id}")
        return 1


async def handle_broadcast_command(args, provider):
    """Handle broadcast command"""
    sent_count = await provider.manage_messaging(
        "send_broadcast",
        message=args.message,
        from_agent=args.from_agent,
        exclude_agents=args.exclude or []
    )
    
    print(f"✅ Broadcast sent to {sent_count} agents")
    return 0


async def handle_channel_command(args, provider):
    """Handle channel message command"""
    success = await provider.manage_messaging(
        "send_to_channel",
        channel_id=args.channel_id,
        message=args.message,
        from_agent=args.from_agent
    )
    
    if success:
        print(f"✅ Message sent to channel {args.channel_id}")
        return 0
    else:
        print(f"❌ Failed to send message to channel {args.channel_id}")
        return 1


async def handle_status_command(args, provider):
    """Handle status command"""
    status = provider.get_provider_status()
    
    print("Discord Provider Status:")
    print(f"  Provider Type: {status['provider_type']}")
    print(f"  Bot Connected: {status['bot_connected']}")
    print(f"  Registered Agents: {status['registered_agents']}")
    print(f"  Agent Channels: {', '.join(status['agent_channels'])}")
    print(f"  Messaging Service Connected: {status['messaging_service_connected']}")
    
    return 0


async def handle_test_command(args, provider):
    """Handle test command"""
    print("Testing Discord Provider...")
    
    # Test status
    status = provider.get_provider_status()
    print(f"✅ Provider status retrieved: {status['provider_type']}")
    
    # Test agent channel registration
    test_channel = None  # Would need actual Discord channel for real test
    if test_channel:
        provider.manage_messaging("register_channel", agent_id="test-agent", channel=test_channel)
        print("✅ Agent channel registration tested")
    
    print("🎉 Discord provider test completed!")
    return 0


async def handle_command(args, provider):
    """Handle command execution"""
    try:
        if args.command == "send":
            return await handle_send_command(args, provider)
        elif args.command == "broadcast":
            return await handle_broadcast_command(args, provider)
        elif args.command == "channel":
            return await handle_channel_command(args, provider)
        elif args.command == "status":
            return await handle_status_command(args, provider)
        elif args.command == "test":
            return await handle_test_command(args, provider)
        else:
            print(f"Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


async def main():
    """Main CLI entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Create Discord bot and provider
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    provider = DiscordMessagingProvider(bot)
    
    # Run the command
    return await handle_command(args, provider)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
