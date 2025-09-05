#!/usr/bin/env python3
"""
Discord Devlog CLI - Agent Cellphone V2
======================================

Command-line interface for the Discord devlog system.
SSOT (Single Source of Truth) for team communication.

Usage:
    python -m src.core.devlog_cli status
    python -m src.core.devlog_cli create "Title" "Content" [category]

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
import os
import argparse
from ..core.unified_utility_system import get_unified_utility

# Add scripts directory to path for devlog import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))

try:
    from devlog import DevlogSystem
except ImportError:
    print("❌ ERROR: devlog.py script not found in scripts directory")
    print("Please ensure scripts/devlog.py exists")
    sys.exit(1)


class DevlogCLI:
    """Command-line interface for devlog system."""

    def __init__(self):
        """Initialize CLI."""
        self.devlog = DevlogSystem()

    def status(self):
        """Show devlog system status."""
        print("🎯 DISCORD DEVLOG SYSTEM STATUS")
        print("=" * 50)

        status = self.devlog.get_status()

        print(f"📊 System Status: {status['system_status'].upper()}")
        print(f"🤖 Agent: {status['agent_name']}")
        print(f"📁 Devlog Directory: {status['devlog_directory']}")
        print(f"📝 Total Entries: {status['entries_count']}")
        print(
            f"💾 File Logging: {'✅ Enabled' if status['file_logging'] else '❌ Disabled'}"
        )
        print(
            f"📡 Discord Integration: {'✅ Enabled' if status['discord_enabled'] else '❌ Disabled'}"
        )
        print(
            f"⚙️  Config File: {'✅ Found' if status['config_file_exists'] else '❌ Not Found'}"
        )

        print("\n📋 AVAILABLE COMMANDS:")
        print("  status                    Show system status")
        print('  create "Title" "Content"   Create devlog entry')
        print('  create "Title" "Content" category   Create categorized entry')
        print("\n📂 Categories: general, progress, issue, success, warning, info")

        if not status["discord_enabled"]:
            print("\n⚠️  WARNING: Discord integration is disabled")
            print("   To enable: Set DISCORD_WEBHOOK_URL environment variable")
            print("   Or configure config/devlog_config.json")

    def create(self, title: str, content: str, category: str = "general"):
        """Create a devlog entry."""
        print(f"📝 Creating devlog entry: {title}")
        print(f"🏷️  Category: {category}")

        success = self.devlog.create_entry(title, content, category)

        if success:
            print("✅ Devlog entry created successfully!")
            if self.devlog.config["log_to_file"]:
                print(f"💾 Saved to: {self.devlog.devlog_dir}")
            if self.devlog.config["enable_discord"]:
                print("📡 Posted to Discord")
        else:
            print("❌ Failed to create devlog entry")
            return False

        return True

    def list_entries(self, limit: int = 10):
        """List recent devlog entries."""
        print("📜 RECENT DEVLOG ENTRIES")
        print("=" * 50)

        try:
            entries = []
            for file_path in sorted(
                self.devlog.devlog_dir.glob("*.json"), reverse=True
            ):
                with open(file_path, "r") as f:
                    file_entries = get_unified_utility().read_json(f)
                    entries.extend(file_entries)

            # Sort by timestamp and limit
            entries.sort(key=lambda x: x["timestamp"], reverse=True)
            entries = entries[:limit]

            if not get_unified_utility().validate_required(entries):
                print("No devlog entries found.")
                return

            for i, entry in enumerate(entries, 1):
                timestamp = entry["timestamp"][:19]  # YYYY-MM-DDTHH:MM:SS
                print(f"{i}. [{timestamp}] {entry['agent']}: {entry['title']}")
                print(
                    f"   📂 {entry['category']} | 💬 {entry['content'][:100]}{'...' if len(entry['content']) > 100 else ''}"
                )
                print()

        except Exception as e:
            print(f"❌ Error listing entries: {e}")


def create_parser():
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Discord Devlog CLI - V2 SWARM Communication System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.core.devlog_cli status
  python -m src.core.devlog_cli create "V2 Compliance Update" "System at 98% compliance"
  python -m src.core.devlog_cli create "Phase 3 Complete" "All contracts fulfilled" success

Categories:
  general  - General updates and information
  progress - Progress reports and milestones
  issue    - Problems, bugs, or concerns
  success  - Achievements and completed tasks
  warning  - Important notices or cautions
  info     - Informational updates
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    subparsers.add_parser("status", help="Show devlog system status")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create devlog entry")
    create_parser.add_argument("title", help="Devlog entry title")
    create_parser.add_argument("content", help="Devlog entry content")
    create_parser.add_argument(
        "category",
        nargs="?",
        default="general",
        choices=["general", "progress", "issue", "success", "warning", "info"],
        help="Entry category (default: general)",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List recent devlog entries")
    list_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of entries to show (default: 10)",
    )

    return parser



def main():
    """Main entry point for devlog CLI."""
    cli = DevlogCLI()
    
    if len(sys.argv) < 2:
        cli.help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        cli.status()
    elif command == "create":
        if len(sys.argv) < 4:
            print("Usage: python -m src.core.devlog_cli create \"Title\" \"Content\" [category]")
            return
        title = sys.argv[2]
        content = sys.argv[3]
        category = sys.argv[4] if len(sys.argv) > 4 else "general"
        cli.create(title, content, category)
    elif command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        cli.list_entries(limit)
    elif command == "help":
        cli.help()
    else:
        print(f"Unknown command: {command}")
        cli.help()

if __name__ == "__main__":
    main()
