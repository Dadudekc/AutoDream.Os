from ..core.unified_entry_point_system import main
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
from ..core.unified_utility_system import get_unified_utility

# Add scripts directory to path for devlog import
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))

try:
    from devlog import DevlogSystem
except ImportError:
    get_logger(__name__).info("❌ ERROR: devlog.py script not found in scripts directory")
    get_logger(__name__).info("Please ensure scripts/devlog.py exists")
    sys.exit(1)


class DevlogCLI:
    """Command-line interface for devlog system."""

    def __init__(self):
        """Initialize CLI."""
        self.devlog = DevlogSystem()

    def status(self):
        """Show devlog system status."""
        get_logger(__name__).info("🎯 DISCORD DEVLOG SYSTEM STATUS")
        get_logger(__name__).info("=" * 50)

        status = self.devlog.get_status()

        get_logger(__name__).info(f"📊 System Status: {status['system_status'].upper()}")
        get_logger(__name__).info(f"🤖 Agent: {status['agent_name']}")
        get_logger(__name__).info(f"📁 Devlog Directory: {status['devlog_directory']}")
        get_logger(__name__).info(f"📝 Total Entries: {status['entries_count']}")
        get_logger(__name__).info(
            f"💾 File Logging: {'✅ Enabled' if status['file_logging'] else '❌ Disabled'}"
        )
        get_logger(__name__).info(
            f"📡 Discord Integration: {'✅ Enabled' if status['discord_enabled'] else '❌ Disabled'}"
        )
        get_logger(__name__).info(
            f"⚙️  Config File: {'✅ Found' if status['config_file_exists'] else '❌ Not Found'}"
        )

        get_logger(__name__).info("\n📋 AVAILABLE COMMANDS:")
        get_logger(__name__).info("  status                    Show system status")
        get_logger(__name__).info('  create "Title" "Content"   Create devlog entry')
        get_logger(__name__).info('  create "Title" "Content" category   Create categorized entry')
        get_logger(__name__).info("\n📂 Categories: general, progress, issue, success, warning, info")

        if not status["discord_enabled"]:
            get_logger(__name__).info("\n⚠️  WARNING: Discord integration is disabled")
            get_logger(__name__).info("   To enable: Set DISCORD_WEBHOOK_URL environment variable")
            get_logger(__name__).info("   Or configure config/devlog_config.json")

    def create(self, title: str, content: str, category: str = "general"):
        """Create a devlog entry."""
        get_logger(__name__).info(f"📝 Creating devlog entry: {title}")
        get_logger(__name__).info(f"🏷️  Category: {category}")

        success = self.devlog.create_entry(title, content, category)

        if success:
            get_logger(__name__).info("✅ Devlog entry created successfully!")
            if self.devlog.config["log_to_file"]:
                get_logger(__name__).info(f"💾 Saved to: {self.devlog.devlog_dir}")
            if self.devlog.config["enable_discord"]:
                get_logger(__name__).info("📡 Posted to Discord")
        else:
            get_logger(__name__).info("❌ Failed to create devlog entry")
            return False

        return True

    def list_entries(self, limit: int = 10):
        """List recent devlog entries."""
        get_logger(__name__).info("📜 RECENT DEVLOG ENTRIES")
        get_logger(__name__).info("=" * 50)

        try:
            entries = []
            for file_path in sorted(
                self.devlog.devlog_dir.glob("*.json"), reverse=True
            ):
                with open(file_path, "r") as f:
                    file_entries = read_json(f)
                    entries.extend(file_entries)

            # Sort by timestamp and limit
            entries.sort(key=lambda x: x["timestamp"], reverse=True)
            entries = entries[:limit]

            if not get_unified_validator().validate_required(entries):
                get_logger(__name__).info("No devlog entries found.")
                return

            for i, entry in enumerate(entries, 1):
                timestamp = entry["timestamp"][:19]  # YYYY-MM-DDTHH:MM:SS
                get_logger(__name__).info(f"{i}. [{timestamp}] {entry['agent']}: {entry['title']}")
                get_logger(__name__).info(
                    f"   📂 {entry['category']} | 💬 {entry['content'][:100]}{'...' if len(entry['content']) > 100 else ''}"
                )
                get_logger(__name__).info()

        except Exception as e:
            get_logger(__name__).info(f"❌ Error listing entries: {e}")


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



if __name__ == "__main__":
    main()
