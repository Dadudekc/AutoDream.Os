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

import sys
import os
import json
import requests
import argparse
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.logger import get_logger
from utils.config_core import get_config

class DevlogSystem:
    """Discord devlog system for team communication."""

    def __init__(self, agent_name=None):
        """Initialize devlog system."""
        self.logger = get_logger("devlog")
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
            "enable_discord": False,
            "log_to_file": True
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                self.logger.error(f"Failed to load devlog config: {e}")

        return default_config

    def create_entry(self, title: str, content: str, category: str = "general") -> bool:
        """Create a devlog entry and post to Discord.

        Args:
            title: Devlog entry title
            content: Devlog entry content
            category: Entry category (general, progress, issue, success)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create devlog entry
            timestamp = datetime.now()
            entry_id = f"{timestamp.strftime('%Y%m%d_%H%M%S')}"

            devlog_entry = {
                "id": entry_id,
                "timestamp": timestamp.isoformat(),
                "agent": self.config["agent_name"],
                "category": category,
                "title": title,
                "content": content,
                "channel": self.config["default_channel"]
            }

            # Log to file
            if self.config["log_to_file"]:
                self._save_to_file(devlog_entry)

            # Post to Discord
            if self.config["enable_discord"] and self.config["discord_webhook_url"]:
                self._post_to_discord(devlog_entry)

            self.logger.info(f"Devlog entry created: {title}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create devlog entry: {e}")
            return False

    def _save_to_file(self, entry: dict):
        """Save devlog entry to file."""
        try:
            date_str = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d")
            filename = self.devlog_dir / f"devlog_{date_str}.json"

            # Load existing entries or create new list
            if filename.exists():
                with open(filename, 'r') as f:
                    entries = json.load(f)
            else:
                entries = []

            # Add new entry
            entries.append(entry)

            # Save back to file
            with open(filename, 'w') as f:
                json.dump(entries, f, indent=2)

        except Exception as e:
            self.logger.error(f"Failed to save devlog to file: {e}")

    def _post_to_discord(self, entry: dict):
        """Post devlog entry to Discord."""
        try:
            webhook_url = self.config["discord_webhook_url"]
            if not webhook_url:
                return

            # Format Discord message
            discord_message = {
                "embeds": [{
                    "title": f"📝 {entry['title']}",
                    "description": entry["content"],
                    "color": self._get_category_color(entry["category"]),
                    "fields": [
                        {
                            "name": "Agent",
                            "value": entry["agent"],
                            "inline": True
                        },
                        {
                            "name": "Category",
                            "value": entry["category"],
                            "inline": True
                        },
                        {
                            "name": "Timestamp",
                            "value": entry["timestamp"],
                            "inline": True
                        }
                    ],
                    "footer": {
                        "text": "V2 SWARM - Agent Cellphone Devlog"
                    }
                }]
            }

            # Send to Discord
            response = requests.post(webhook_url, json=discord_message)

            if response.status_code == 204:
                self.logger.info("Devlog posted to Discord successfully")
            else:
                self.logger.error(f"Failed to post to Discord: {response.status_code}")

        except Exception as e:
            self.logger.error(f"Failed to post to Discord: {e}")

    def _get_category_color(self, category: str) -> int:
        """Get Discord embed color for category."""
        colors = {
            "general": 0x3498db,    # Blue
            "progress": 0x2ecc71,  # Green
            "issue": 0xe74c3c,     # Red
            "success": 0x27ae60,   # Dark Green
            "warning": 0xf39c12,   # Orange
            "info": 0x9b59b6       # Purple
        }
        return colors.get(category.lower(), 0x3498db)

    def get_status(self) -> dict:
        """Get devlog system status."""
        return {
            "system_status": "operational" if self.config["discord_webhook_url"] else "limited",
            "discord_enabled": self.config["enable_discord"],
            "file_logging": self.config["log_to_file"],
            "agent_name": self.config["agent_name"],
            "config_file_exists": self.config_file.exists(),
            "devlog_directory": str(self.devlog_dir),
            "entries_count": self._count_entries()
        }

    def _count_entries(self) -> int:
        """Count total devlog entries."""
        try:
            count = get_config('count', 0)
            for file_path in self.devlog_dir.glob("*.json"):
                with open(file_path, 'r') as f:
                    entries = json.load(f)
                    count += len(entries)
            return count
        except Exception:
            return 0


def main():
    """Main CLI entry point for devlog system."""
    parser = argparse.ArgumentParser(
        description="Discord Devlog System - V2 SWARM Communication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/devlog.py "Title" "Content"
  python scripts/devlog.py "Title" "Content" --category success
  python scripts/devlog.py "Title" "Content" --agent Agent-7
  python scripts/devlog.py "Title" "Content" --category progress --agent Agent-5

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
