#!/usr/bin/env python3
"""
Discord Devlog System - Agent Cellphone V2
==========================================

SSOT (Single Source of Truth) for team communication.
Posts updates to Discord automatically.

Usage:
    python scripts/devlog.py "Title" "Content"

Author: V2 SWARM CAPTAIN
License: MIT
"""

import os
import sys
import json
import requests
import argparse
from datetime import datetime
from pathlib import Path


class DevlogSystem:
    """Discord devlog system for team communication."""

    def __init__(self, agent_name=None):
        """Initialize devlog system."""
        self.config_file = Path("config/devlog_config.json")
        self.devlog_dir = Path("devlogs")
        self.devlog_dir.mkdir(exist_ok=True)

        # Load configuration
        self.config = self._load_config()
        
        # Override agent name if specified
        if agent_name:
            self.config["agent_name"] = agent_name

    def _load_config(self):
        """Load devlog configuration."""
        default_config = {
            "discord_webhook_url": os.getenv("DISCORD_WEBHOOK_URL", ""),
            "agent_name": "Agent-1",
            "default_channel": "devlog",
            "enable_discord": True,
            "log_to_file": True
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Failed to load devlog config: {e}")

        # Handle special case where config says to use environment variable
        if default_config.get("discord_webhook_url") in ["USE_ENV_VAR", ""]:
            default_config["discord_webhook_url"] = os.getenv("DISCORD_WEBHOOK_URL", "")

        return default_config

    def create_entry(self, title: str, content: str, category: str = "general") -> bool:
        """Create a devlog entry and post to Discord.

        Args:
            title: Entry title
            content: Entry content
            category: Entry category (general, progress, issue, success, warning, info)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create file entry if enabled
            if self.config.get("log_to_file", True):
                self._save_to_file(title, content, category)

            # Post to Discord if enabled and webhook URL is available
            if (self.config.get("enable_discord", False) and 
                self.config.get("discord_webhook_url")):
                return self._post_to_discord(title, content, category)
            else:
                print(f"Discord posting disabled or webhook URL not configured")
                print(f"Enable discord: {self.config.get('enable_discord')}")
                print(f"Webhook URL available: {bool(self.config.get('discord_webhook_url'))}")
                return True

        except Exception as e:
            print(f"Error creating devlog entry: {e}")
            return False

    def _save_to_file(self, title: str, content: str, category: str):
        """Save devlog entry to file."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Replace problematic characters for Windows filenames
        safe_title = title.replace(' ', '_').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
        filename = f"{timestamp}_{category}_{safe_title}.md"
        filepath = self.devlog_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"**Date**: {datetime.now().isoformat()}\n")
            f.write(f"**Agent**: {self.config['agent_name']}\n")
            f.write(f"**Category**: {category}\n\n")
            f.write(f"---\n\n{content}\n")

        print(f"Devlog saved to: {filepath}")

    def _post_to_discord(self, title: str, content: str, category: str) -> bool:
        """Post devlog entry to Discord."""
        webhook_url = self.config["discord_webhook_url"]
        
        # Category emoji mapping
        category_emojis = {
            "general": "📝",
            "progress": "🚀", 
            "issue": "⚠️",
            "success": "✅",
            "warning": "🔶",
            "info": "ℹ️"
        }

        emoji = category_emojis.get(category, "📝")
        agent_name = self.config.get("agent_name", "Unknown Agent")
        
        # Create Discord embed
        embed = {
            "title": f"{emoji} {title}",
            "description": content,
            "color": self._get_category_color(category),
            "fields": [
                {
                    "name": "Agent",
                    "value": agent_name,
                    "inline": True
                },
                {
                    "name": "Category", 
                    "value": category.title(),
                    "inline": True
                },
                {
                    "name": "Timestamp",
                    "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "inline": True
                }
            ],
            "footer": {
                "text": "Agent Cellphone V2 - Devlog System"
            }
        }

        payload = {
            "embeds": [embed],
            "username": f"Agent Cellphone V2 - {agent_name}"
        }

        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            print(f"✅ Successfully posted to Discord: {title}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to post to Discord: {e}")
            return False

    def _get_category_color(self, category: str) -> int:
        """Get Discord embed color for category."""
        colors = {
            "general": 0x7289DA,    # Discord blurple
            "progress": 0x00FF00,   # Green
            "issue": 0xFF0000,      # Red
            "success": 0x00FF00,    # Green
            "warning": 0xFFFF00,    # Yellow
            "info": 0x00FFFF        # Cyan
        }
        return colors.get(category, 0x7289DA)


def main():
    """Main entry point for devlog script."""
    parser = argparse.ArgumentParser(
        description="Create and post devlog entries to Discord",
        epilog="""
Examples:
  python scripts/devlog.py "Daily Progress" "Completed task X and Y"
  python scripts/devlog.py "Issue Found" "Bug in module Z" --category issue
  python scripts/devlog.py "Success!" "All tests passing" --category success --agent Agent-7

Categories: general, progress, issue, success, warning, info
        """
    )
    
    parser.add_argument("title", help="Devlog entry title")
    parser.add_argument("content", help="Devlog entry content")
    parser.add_argument("--category", "-c", default="general", 
                       choices=["general", "progress", "issue", "success", "warning", "info"],
                       help="Entry category (default: general)")
    parser.add_argument("--agent", "-a", help="Agent name (overrides config)")
    
    args = parser.parse_args()

    # Initialize devlog system with optional agent override
    devlog = DevlogSystem(agent_name=args.agent)

    # Create devlog entry
    success = devlog.create_entry(args.title, args.content, args.category)

    if success:
        print(f"✅ Devlog entry created: {args.title}")
        if args.agent:
            print(f"📝 Agent: {args.agent}")
        print(f"📂 Category: {args.category}")
    else:
        print(f"❌ Failed to create devlog entry: {args.title}")
        sys.exit(1)


if __name__ == "__main__":
    main()
