#!/usr/bin/env python3
"""
DevLog Discord Poster - Manual Posting Tool
==========================================

Manually posts a devlog to Discord using webhook integration.

Usage:
    python post_devlog_to_discord.py <devlog_path>

Author: Agent-3 (Infrastructure & DevOps)
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from discord_commander.discord_webhook_integration import DiscordWebhookIntegration


def post_devlog_to_discord(devlog_path: str) -> bool:
    """Post a devlog file to Discord via webhook."""

    # Check if devlog file exists
    devlog_file = Path(devlog_path)
    if not devlog_file.exists():
        print(f"❌ DevLog file not found: {devlog_path}")
        return False

    try:
        # Read the devlog content
        with open(devlog_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse devlog metadata from filename
        filename = devlog_file.name
        metadata = parse_devlog_filename(filename)

        # Create devlog data structure
        devlog_data = {
            "title": metadata.get("title", filename),
            "description": extract_devlog_summary(content),
            "category": metadata.get("category", "infrastructure"),
            "agent": metadata.get("agent", "Agent-3"),
            "filepath": str(devlog_file),
            "timestamp": datetime.utcnow().isoformat(),
            "full_content": content  # Include full content for Discord
        }

        # Initialize Discord webhook integration
        webhook_integration = DiscordWebhookIntegration()

        # Test webhook connection first
        if not webhook_integration.test_webhook_connection():
            print("❌ Discord webhook connection failed")
            return False

        # Send the devlog notification
        success = webhook_integration.send_devlog_notification(devlog_data)

        if success:
            print(f"✅ DevLog successfully posted to Discord: {devlog_data['title']}")
            return True
        else:
            print("❌ Failed to post devlog to Discord")
            return False

    except Exception as e:
        print(f"❌ Error posting devlog to Discord: {e}")
        return False


def parse_devlog_filename(filename: str) -> dict[str, str]:
    """Parse metadata from devlog filename."""
    # Format: YYYY-MM-DD_HH-MM-SS_category_Agent-Title.md
    parts = filename.replace(".md", "").split("_")

    metadata = {
        "timestamp": "unknown",
        "category": "general",
        "agent": "Unknown",
        "title": filename,
    }

    if len(parts) >= 4:
        metadata["timestamp"] = f"{parts[0]}_{parts[1]}"
        metadata["category"] = parts[2]
        metadata["agent"] = parts[3]
        metadata["title"] = "_".join(parts[4:]) if len(parts) > 4 else "DevLog Update"

    return metadata


def extract_devlog_summary(content: str, max_length: int = 500) -> str:
    """Extract summary from devlog content."""
    lines = content.split("\n")

    # Look for summary section or first meaningful paragraph
    summary = ""
    for line in lines[:30]:  # Check first 30 lines
        line = line.strip()
        if line and not line.startswith("#") and len(line) > 10:
            summary += line + " "
            if len(summary) > max_length:
                break

    if not summary:
        summary = "Comprehensive devlog update with current project status and achievements."

    return summary[:max_length].strip()


def main():
    """Main function to post devlog."""
    if len(sys.argv) < 2:
        print("Usage: python post_devlog_to_discord.py <devlog_path>")
        print("Example: python post_devlog_to_discord.py devlogs/2025-09-09_11-03-00_infrastructure_Agent-3_SWARM_DevLog_Current_State_Report.md")
        sys.exit(1)

    devlog_path = sys.argv[1]
    print(f"🚀 Posting devlog to Discord: {devlog_path}")
    print("=" * 60)

    success = post_devlog_to_discord(devlog_path)

    if success:
        print("\n🎉 DevLog successfully posted to Discord!")
        print("🐝 WE ARE SWARM - Coordination active!")
    else:
        print("\n❌ Failed to post devlog to Discord")
        sys.exit(1)


if __name__ == "__main__":
    main()
