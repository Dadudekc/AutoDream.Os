#!/usr/bin/env python3
"""
Unified DevLog Discord Sender - V2 Compliance Module
====================================================

Comprehensive utility to send devlog files to agent-specific Discord channels.
Combines the best features from both simple and enhanced versions.

Features:
- Explicit agent flag for reliable routing
- Direct file processing without monitoring
- Support for both webhook and channel ID methods
- Automatic category detection from content
- Robust configuration handling with fallbacks
- Comprehensive error handling
- Simulation mode for testing
- Enhanced Discord integration support

Usage:
    python scripts/send_devlog_unified.py --agent Agent-1 --file path/to/devlog.md

Arguments:
    --agent: Required agent identifier (Agent-1 through Agent-8)
    --file: Required path to the devlog markdown file
    --simulate: Optional flag to simulate sending without actual Discord API calls

Examples:
    # Basic usage
    python scripts/send_devlog_unified.py --agent Agent-1 --file devlogs/status.md

    # With simulation mode
    python scripts/send_devlog_unified.py --agent Agent-1 --file devlogs/status.md --simulate

    # Different agents
    python scripts/send_devlog_unified.py --agent Agent-4 --file captain_log.md

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import argparse
import asyncio
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests


def load_discord_config() -> Optional[dict]:
    """Load Discord channel configuration."""
    config_file = Path("config/discord_channels.json")
    if not config_file.exists():
        print("❌ Discord channels configuration not found")
        print(f"   Expected: {config_file.absolute()}")
        return None

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load Discord config: {e}")
        return None


def get_channel_config(config: dict, agent_id: str) -> Optional[dict]:
    """Get channel configuration for agent with multiple key format fallbacks."""
    if not config:
        return None

    # Try different key formats to handle various naming conventions
    key_formats = [
        agent_id,  # Agent-1
        agent_id.lower(),  # agent-1
        agent_id.lower().replace('-', '_'),  # agent_1
        f"agent-{agent_id.split('-')[1]}",  # agent-1 (from Agent-1)
        f"agent_{agent_id.split('-')[1]}",  # agent_1 (from Agent-1)
    ]

    for key in key_formats:
        if key in config:
            return config[key]

    return None


def parse_devlog_content(filepath: Path) -> Optional[dict]:
    """Parse devlog file content and extract metadata."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            print("❌ Devlog file is empty")
            return None

        # Extract title from first header
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else filepath.stem

        # Determine category from content keywords
        category = "general"
        content_lower = content.lower()

        # Category detection with priority order
        category_keywords = {
            "consolidation": ["consolidation", "merge", "unify", "consolidate"],
            "cleanup": ["cleanup", "remove", "delete", "mission", "refactor"],
            "coordination": ["coordination", "swarm", "agent", "coordinate", "sync"],
            "testing": ["testing", "test", "verify", "validation", "pytest"],
            "deployment": ["deployment", "deploy", "release", "production"],
            "documentation": ["documentation", "docs", "readme", "guide"],
            "infrastructure": ["infrastructure", "infra", "setup", "config"],
        }

        for cat, keywords in category_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                category = cat
                break

        return {
            'title': title,
            'content': content[:1500] + ("..." if len(content) > 1500 else ""),
            'category': category,
            'full_content': content,
            'word_count': len(content.split()),
            'line_count': len(content.splitlines())
        }

    except Exception as e:
        print(f"❌ Failed to parse devlog: {e}")
        return None


def send_to_discord_webhook(webhook_url: str, devlog_data: dict, agent_id: str,
                           channel_config: dict, simulate: bool = False) -> bool:
    """Send devlog to Discord webhook."""
    try:
        # Get color from config or use agent-specific defaults
        agent_colors = {
            "Agent-1": 0x1ABC9C,  # Teal
            "Agent-2": 0x3498DB,  # Blue
            "Agent-3": 0x9B59B6,  # Purple
            "Agent-4": 0xE74C3C,  # Red
            "Agent-5": 0xF39C12,  # Orange
            "Agent-6": 0x27AE60,  # Green
            "Agent-7": 0x95A5A6,  # Gray
            "Agent-8": 0x8E44AD,  # Dark Purple
        }
        color = channel_config.get('color', agent_colors.get(agent_id, 0x3498DB))

        embed = {
            "title": f"📝 {devlog_data['title']}",
            "description": devlog_data['content'],
            "color": color,
            "fields": [
                {"name": "Agent", "value": agent_id, "inline": True},
                {"name": "Category", "value": devlog_data['category'].title(), "inline": True},
                {"name": "Word Count", "value": str(devlog_data['word_count']), "inline": True},
                {
                    "name": "Timestamp",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": False
                },
            ],
            "footer": {
                "text": f"V2_SWARM DevLog - {agent_id} | {devlog_data['line_count']} lines",
                "icon_url": "https://i.imgur.com/devlog_icon.png"
            }
        }

        payload = {
            "embeds": [embed],
            "username": f"V2_SWARM DevLog - {agent_id}",
        }

        if simulate:
            print("📡 Discord Webhook Simulation:")
            print(f"   Webhook URL: {webhook_url[:50]}...")
            print(f"   Username: {payload['username']}")
            print(f"   Embed Title: {embed['title']}")
            print(f"   Category: {devlog_data['category']}")
            print(f"   Color: #{color:06x}")
            print(f"   Content Preview: {devlog_data['content'][:100]}...")
            print("✅ Webhook simulation completed!")
            return True

        response = requests.post(webhook_url, json=payload, timeout=15)

        if response.status_code == 204:
            print("✅ DevLog sent to Discord successfully!")
            return True
        else:
            print(f"❌ Discord webhook error: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ Discord webhook timeout (15s)")
        return False
    except Exception as e:
        print(f"❌ Failed to send to Discord: {e}")
        return False


def send_to_discord_channel(channel_id: str, devlog_data: dict, agent_id: str,
                           channel_config: dict, simulate: bool = False) -> bool:
    """Send devlog to Discord channel via channel ID."""
    if simulate:
        # Simulation mode - just log what would happen
        agent_colors = {
            "Agent-1": 0x1ABC9C, "Agent-2": 0x3498DB, "Agent-3": 0x9B59B6,
            "Agent-4": 0xE74C3C, "Agent-5": 0xF39C12, "Agent-6": 0x27AE60,
            "Agent-7": 0x95A5A6, "Agent-8": 0x8E44AD,
        }
        color = channel_config.get('color', agent_colors.get(agent_id, 0x3498DB))

        print("📡 Discord Channel Simulation:")
        print(f"   Channel ID: {channel_id}")
        print(f"   Agent: {agent_id}")
        print(f"   Title: {devlog_data['title']}")
        print(f"   Category: {devlog_data['category']}")
        print(f"   Word Count: {devlog_data['word_count']}")
        print(f"   Line Count: {devlog_data['line_count']}")
        print(f"   Color: #{color:06x}")
        print(f"   Content Length: {len(devlog_data['content'])} characters")
        print("✅ Channel simulation completed!")
        return True

    # Implement actual Discord API integration with bot token
    import os
    import asyncio
    from typing import Optional

    # Check for Discord bot token
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    if not bot_token:
        print("❌ Discord Bot Token not found!")
        print("   Set DISCORD_BOT_TOKEN environment variable")
        print("   Example: export DISCORD_BOT_TOKEN='your_bot_token_here'")
        return False

    try:
        import discord
        from discord import Embed
    except ImportError:
        print("❌ discord.py library not installed!")
        print("   Install with: pip install discord.py")
        return False

    # Agent colors for embeds
    agent_colors = {
        "Agent-1": 0x1ABC9C, "Agent-2": 0x3498DB, "Agent-3": 0x9B59B6,
        "Agent-4": 0xE74C3C, "Agent-5": 0xF39C12, "Agent-6": 0x27AE60,
        "Agent-7": 0x95A5A6, "Agent-8": 0x8E44AD,
    }

    color = channel_config.get('color', agent_colors.get(agent_id, 0x3498DB))

    async def send_discord_message():
        """Send message to Discord channel asynchronously."""
        client = discord.Client(intents=discord.Intents.default())

        @client.event
        async def on_ready():
            try:
                channel = client.get_channel(int(channel_id))
                if not channel:
                    print(f"❌ Could not find channel with ID: {channel_id}")
                    await client.close()
                    return

                # Create embed
                embed = Embed(
                    title=devlog_data['title'],
                    description=devlog_data['content'][:2000],  # Discord limit
                    color=color
                )

                # Add fields
                embed.add_field(name="Agent", value=agent_id, inline=True)
                embed.add_field(name="Category", value=devlog_data['category'], inline=True)
                embed.add_field(name="Word Count", value=str(devlog_data['word_count']), inline=True)
                embed.add_field(name="Line Count", value=str(devlog_data['line_count']), inline=True)

                # Add timestamp
                embed.set_footer(text=f"Generated by {agent_id}")

                await channel.send(embed=embed)
                print("✅ Devlog sent to Discord successfully!")

            except Exception as e:
                print(f"❌ Failed to send to Discord: {e}")
            finally:
                await client.close()

        try:
            await client.start(bot_token)
        except Exception as e:
            print(f"❌ Discord client error: {e}")
            return False

    # Run the async Discord function
    try:
        asyncio.run(send_discord_message())
        return True
    except Exception as e:
        print(f"❌ Discord integration failed: {e}")
        return False


def validate_environment() -> bool:
    """Validate that the environment is properly set up."""
    issues = []

    # Check if config file exists
    config_file = Path("config/discord_channels.json")
    if not config_file.exists():
        issues.append("Discord channels configuration file not found")

    # Check if we're in the right directory (has config folder)
    if not Path("config").exists():
        issues.append("Config directory not found - run from project root")

    if issues:
        print("❌ Environment validation failed:")
        for issue in issues:
            print(f"   - {issue}")
        return False

    return True


def main():
    """Main entry point for unified devlog sender."""
    if not validate_environment():
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Send devlog files to agent-specific Discord channels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python scripts/send_devlog_unified.py --agent Agent-1 --file devlogs/status.md

  # With simulation mode (safe for testing)
  python scripts/send_devlog_unified.py --agent Agent-1 --file devlogs/status.md --simulate

  # Different agents and files
  python scripts/send_devlog_unified.py --agent Agent-4 --file captain_log.md
  python scripts/send_devlog_unified.py --agent Agent-8 --file coordination_update.md

Valid agents: Agent-1, Agent-2, Agent-3, Agent-4, Agent-5, Agent-6, Agent-7, Agent-8

Configuration:
- Discord channels configured in: config/discord_channels.json
- Supports both webhook URLs and channel IDs
- Use --simulate flag for testing without actual Discord API calls
        """
    )

    parser.add_argument(
        "--agent",
        required=True,
        choices=[f"Agent-{i}" for i in range(1, 9)],
        help="Agent identifier (required)"
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Path to the devlog markdown file (required)"
    )

    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Simulate sending without actual Discord API calls"
    )

    args = parser.parse_args()

    print("🐝 V2_SWARM Unified DevLog Discord Sender")
    print("=" * 55)
    print(f"📝 Agent: {args.agent}")
    print(f"📄 File: {args.file}")
    print(f"🎭 Mode: {'Simulation' if args.simulate else 'Production'}")
    print("=" * 55)

    # Validate file exists and is readable
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"❌ File not found: {args.file}")
        sys.exit(1)

    if not filepath.is_file():
        print(f"❌ Path is not a file: {args.file}")
        sys.exit(1)

    if filepath.suffix.lower() != '.md':
        print(f"⚠️  File doesn't have .md extension: {args.file}")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)

    # Load Discord configuration
    config = load_discord_config()
    if not config:
        sys.exit(1)

    # Get channel configuration
    channel_config = get_channel_config(config, args.agent)
    if not channel_config:
        print(f"❌ No Discord channel configured for {args.agent}")
        print("   Please check config/discord_channels.json")
        sys.exit(1)

    # Parse devlog content
    devlog_data = parse_devlog_content(filepath)
    if not devlog_data:
        sys.exit(1)

    # Show devlog summary
    print(f"📊 DevLog Summary:")
    print(f"   Title: {devlog_data['title']}")
    print(f"   Category: {devlog_data['category']}")
    print(f"   Words: {devlog_data['word_count']}")
    print(f"   Lines: {devlog_data['line_count']}")
    print()

    # Send to Discord
    success = False

    # Try webhook first, then channel ID
    webhook_url = channel_config.get('webhook_url')
    channel_id = channel_config.get('channel_id')

    if webhook_url:
        print("📡 Sending via Discord webhook...")
        success = send_to_discord_webhook(webhook_url, devlog_data, args.agent,
                                        channel_config, args.simulate)
    elif channel_id:
        print("📡 Sending via Discord channel...")
        success = send_to_discord_channel(channel_id, devlog_data, args.agent,
                                        channel_config, args.simulate)
    else:
        print("❌ No webhook URL or channel ID configured for this agent")
        print("   Please configure webhook_url or channel_id in config/discord_channels.json")
        sys.exit(1)

    if success:
        mode_text = "simulated" if args.simulate else "sent"
        print(f"\n✅ DevLog successfully {mode_text} to {args.agent}'s dedicated channel!")
        print("🎯 Routing completed successfully")
        if args.simulate:
            print("💡 Remove --simulate flag to send to actual Discord")
    else:
        print("\n❌ Failed to send devlog to Discord")
        print("   Check your Discord configuration and try again")
        sys.exit(1)


if __name__ == "__main__":
    main()
