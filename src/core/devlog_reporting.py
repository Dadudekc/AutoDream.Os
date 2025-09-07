"""Utility functions for devlog output and reporting.

These helpers are shared by :mod:`devlog_service` and keep formatting and
status display logic isolated from the core service implementation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional


def format_content_for_discord(content: str) -> str:
    """Improve readability of plain text when posted to Discord."""

    formatted = content.strip()
    replacements = {
        "✅": "✅",
        "❌": "❌",
        "⚠️": "⚠️",
        "🚀": "🚀",
        "🎯": "🎯",
        "🔧": "🔧",
        "📊": "📊",
        "💡": "💡",
    }
    for key, value in replacements.items():
        formatted = formatted.replace(key, value)

    formatted = formatted.replace(". ", ".\n").replace("! ", "!\n")
    if len(formatted) > 1000:
        formatted = formatted[:997] + "..."
    return formatted


def post_entry_to_discord(entry, discord_service, config, channel: Optional[str] = None) -> bool:
    """Send a devlog entry to Discord using ``discord_service``."""

    if not discord_service:
        print("⚠️ Discord service not available")
        return False

    channel = channel or config.get("default_channel", "devlog")
    content = (
        f"📝 **DEVLOG ENTRY: {entry.title}**\n"
        f"🏷️ **Category**: {entry.category}\n"
        f"🤖 **Agent**: {entry.agent_id}\n"
        f"📅 **Created**: {datetime.fromtimestamp(entry.created_at).strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"📊 **Priority**: {entry.metadata.get('priority', 'normal')}\n\n"
        f"📋 **Content**:\n{format_content_for_discord(entry.content)}\n\n"
        f"🏷️ **Tags**: {', '.join(entry.tags) if entry.tags else 'None'}\n"
        f"🆔 **Entry ID**: {entry.id}"
    )

    try:
        return discord_service.send_devlog(
            title=entry.title,
            content=content,
            agent=entry.agent_id,
            category=entry.category,
            priority=entry.metadata.get("priority", "normal"),
        )
    except Exception as e:
        print(f"⚠️ Discord posting failed: {e}")
        return False


def show_status(knowledge_db, discord_service, config, systems_available: bool, discord_available: bool) -> bool:
    """Display overall system status."""

    try:
        print("📊 DEVLOG SYSTEM STATUS")
        print("=" * 50)

        print("🗄️  Knowledge Database:")
        status = "✅ Available" if systems_available else "⚠️  Limited"
        print(f"   Status: {status}")
        print(f"   Path: {knowledge_db.db_path}")

        print("\n📱 Discord Integration:")
        service_status = "✅ Available" if discord_available else "⚠️  Limited"
        print(f"   Service: {service_status}")
        auto = "✅ Enabled" if config.get("auto_discord") else "❌ Disabled"
        print(f"   Auto-posting: {auto}")
        print(f"   Default Channel: {config.get('default_channel')}")

        if getattr(discord_service, "webhook_url", None):
            print(f"   Webhook: ✅ Configured ({discord_service.webhook_url[:50]}...)")
        else:
            print("   Webhook: ❌ Not configured (set DISCORD_WEBHOOK_URL environment variable)")

        print("\n🎯 SSOT Configuration:")
        ssot = "✅ Yes" if config.get("ssot_enforced") else "❌ No"
        required = "✅ Yes" if config.get("required_for_updates") else "❌ No"
        print(f"   SSOT Enforced: {ssot}")
        print(f"   Updates Required: {required}")
        print(f"   Categories: {', '.join(config.get('knowledge_categories', []))}")
        print("   CLI Version: 1.0.0")
        return True
    except Exception:
        return False

