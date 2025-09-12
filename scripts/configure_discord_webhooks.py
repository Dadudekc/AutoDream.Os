#!/usr/bin/env python3
"""
Discord Webhook Configuration Helper
====================================

Helper script to configure Discord webhooks for agent channels.

Usage:
    python scripts/configure_discord_webhooks.py
"""

import json
from pathlib import Path


def configure_webhooks():
    """Configure webhooks for all channels."""
    config_file = Path("config/discord_channels.json")

    if not config_file.exists():
        print("❌ Configuration file not found")
        return False

    print("🔧 Discord Webhook Configuration")
    print("=" * 40)

    # Load current config
    with open(config_file) as f:
        config = json.load(f)

    # Configure each channel
    for channel_name, channel_config in config.items():
        print(f"\n📺 Configuring {channel_name}...")
        print(f"   Description: {channel_config.get('description', 'N/A')}")

        current_webhook = channel_config.get("webhook_url")
        if current_webhook:
            print(f"   Current webhook: {current_webhook[:50]}...")
            change = input("   Change webhook? (y/N): ").lower().strip()
            if change != "y":
                continue

        # Get new webhook URL
        webhook_url = input(f"   Enter webhook URL for {channel_name}: ").strip()
        if webhook_url:
            config[channel_name]["webhook_url"] = webhook_url
            print("   ✅ Webhook configured")
        else:
            print("   ⚠️  Skipped webhook configuration")

    # Save updated config
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    print("\n✅ Webhook configuration complete!")
    return True


if __name__ == "__main__":
    configure_webhooks()
