#!/usr/bin/env python3
"""
Discord Service - V2 Compliance Module
=======================================

Unified Discord integration for V2_SWARM DevLog monitoring and agent communication.
Consolidates: discord_commander.py + discord_webhook_integration.py

Author: Agent-3 (Infrastructure & DevOps) - V2 Consolidation
License: MIT
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

try:
    from .discord_agent_communication import AgentCommunicationEngine
    from .discord_embeds import (
        create_agent_status_embed,
        create_coordination_embed,
        create_devlog_embed,
    )
except ImportError:
    from discord_agent_communication import AgentCommunicationEngine
    from discord_embeds import (
        create_agent_status_embed,
        create_coordination_embed,
        create_devlog_embed,
    )


class DiscordService:
    """Unified Discord service for DevLog monitoring, webhooks, and agent communication."""

    def __init__(self, webhook_url: str | None = None):
        """Initialize Discord service."""
        self.webhook_url = webhook_url or self._load_webhook_url()
        self.agent_engine = AgentCommunicationEngine()
        self.devlogs_path = Path("devlogs")
        self.last_check_time = datetime.utcnow()
        self.is_running = False
        self.session = requests.Session()
        self.session.timeout = 10

    def _load_webhook_url(self) -> str | None:
        """Load webhook URL from environment or config."""
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

        if not webhook_url:
            config_path = Path("config/discord_config.json")
            if config_path.exists():
                try:
                    with open(config_path) as f:
                        config = json.load(f)
                        webhook_url = config.get("webhook_url")
                except Exception:
                    pass

        return webhook_url

    async def start_devlog_monitoring(self, check_interval: int = 60):
        """Start monitoring devlogs and sending Discord notifications."""
        print("🚀 Starting Discord DevLog monitoring...")
        print(f"📁 Monitoring directory: {self.devlogs_path}")
        print(f"⏱️  Check interval: {check_interval} seconds\n")

        if not self.devlogs_path.exists():
            print(f"❌ DevLogs directory not found: {self.devlogs_path}")
            return

        if not self.test_webhook_connection():
            print("⚠️  Continuing without Discord notifications...\n")

        self.is_running = True

        try:
            while self.is_running:
                await self._check_for_new_devlogs()
                await asyncio.sleep(check_interval)
        except KeyboardInterrupt:
            print("\n🛑 DevLog monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ DevLog monitoring error: {e}")
        finally:
            self.is_running = False

    async def _check_for_new_devlogs(self):
        """Check for new devlog files and process them."""
        try:
            new_devlogs = self._find_new_devlogs()
            for devlog_path in new_devlogs:
                await self._process_devlog(devlog_path)
        except Exception as e:
            print(f"❌ Error checking devlogs: {e}")

    def _find_new_devlogs(self) -> list[Path]:
        """Find devlog files newer than last check."""
        if not self.devlogs_path.exists():
            return []

        new_files = [
            file_path
            for file_path in self.devlogs_path.rglob("*.md")
            if file_path.stat().st_mtime > self.last_check_time.timestamp()
        ]
        return sorted(new_files, key=lambda x: x.stat().st_mtime)

    async def _process_devlog(self, devlog_path: Path):
        """Process a single devlog file."""
        try:
            with open(devlog_path, encoding="utf-8") as f:
                content = f.read()

            metadata = self._parse_devlog_filename(devlog_path.name)
            devlog_data = {
                "title": metadata.get("title", devlog_path.name),
                "description": self._extract_devlog_summary(content),
                "category": metadata.get("category", "general"),
                "agent": metadata.get("agent", "Unknown"),
                "filepath": str(devlog_path),
                "timestamp": datetime.utcnow().isoformat(),
            }

            print(f"📝 Processing devlog: {devlog_data['title']}")

            if self.send_devlog_notification(devlog_data):
                print("✅ Discord notification sent")
                await self._notify_agents_of_devlog(devlog_data)
            else:
                print("❌ Failed to send Discord notification")

        except Exception as e:
            print(f"❌ Error processing devlog {devlog_path}: {e}")

    def _parse_devlog_filename(self, filename: str) -> dict[str, str]:
        """Parse metadata from devlog filename."""
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

    def _extract_devlog_summary(self, content: str, max_length: int = 500) -> str:
        """Extract summary from devlog content."""
        lines = content.split("\n")
        summary = ""

        for line in lines[:20]:
            line = line.strip()
            if line and not line.startswith("#") and len(line) > 20:
                summary += line + " "
                if len(summary) > max_length:
                    break

        return (
            summary[:max_length].strip()
            if summary
            else "DevLog update processed by V2_SWARM monitoring system."
        )

    async def _notify_agents_of_devlog(self, devlog_data: dict[str, Any]):
        """Notify relevant agents about the devlog."""
        try:
            message = f"""🚨 DISCORD DEVLOG ALERT

**New DevLog Activity Detected:**
• **Title:** {devlog_data['title']}
• **Category:** {devlog_data['category'].title()}
• **Agent:** {devlog_data['agent']}
• **Summary:** {devlog_data['description'][:200]}...

**DevLog monitoring is active and Discord notifications are enabled.**
**WE ARE SWARM - Stay coordinated!**

---
*Automated DevLog Monitor*
"""
            result = await self.agent_engine.broadcast_to_all_agents(
                message, sender="Discord_DevLog_Monitor"
            )

            if result.success:
                print(f"✅ Notified {result.data.get('successful_deliveries', 0)} agents")
            else:
                print("❌ Failed to notify agents about devlog")

        except Exception as e:
            print(f"❌ Error notifying agents: {e}")

    def send_devlog_notification(self, devlog_data: dict[str, Any]) -> bool:
        """Send devlog notification to Discord."""
        if not self.webhook_url:
            return False

        try:
            embed = self._create_devlog_embed(devlog_data)
            payload = {
                "embeds": [embed],
                "username": "V2_SWARM DevLog Monitor",
                "avatar_url": os.getenv("DISCORD_AVATAR_URL", None),
            }

            response = self.session.post(self.webhook_url, json=payload)
            return response.status_code == 204

        except Exception as e:
            print(f"❌ Error sending devlog notification: {e}")
            return False

    def send_agent_status_notification(self, agent_status: dict[str, Any]) -> bool:
        """Send agent status notification to Discord."""
        if not self.webhook_url:
            return False

        try:
            embed = self._create_agent_status_embed(agent_status)
            payload = {
                "embeds": [embed],
                "username": "V2_SWARM Status Monitor",
                "avatar_url": os.getenv("DISCORD_AVATAR_URL", None),
            }

            response = self.session.post(self.webhook_url, json=payload)
            return response.status_code == 204

        except Exception as e:
            print(f"❌ Error sending agent status notification: {e}")
            return False

    def send_swarm_coordination_notification(self, coordination_data: dict[str, Any]) -> bool:
        """Send swarm coordination notification to Discord."""
        if not self.webhook_url:
            return False

        try:
            embed = self._create_coordination_embed(coordination_data)
            payload = {
                "embeds": [embed],
                "username": "V2_SWARM Coordinator",
                "avatar_url": os.getenv("DISCORD_AVATAR_URL", None),
            }

            response = self.session.post(self.webhook_url, json=payload)
            return response.status_code == 204

        except Exception as e:
            print(f"❌ Error sending coordination notification: {e}")
            return False

    def _create_devlog_embed(self, devlog_data: dict[str, Any]) -> dict[str, Any]:
        """Create Discord embed for devlog notification."""
        return create_devlog_embed(devlog_data)

    def _create_agent_status_embed(self, agent_status: dict[str, Any]) -> dict[str, Any]:
        """Create Discord embed for agent status notification."""
        return create_agent_status_embed(agent_status)

    def _create_coordination_embed(self, coordination_data: dict[str, Any]) -> dict[str, Any]:
        """Create Discord embed for swarm coordination notification."""
        return create_coordination_embed(coordination_data)

    def test_webhook_connection(self) -> bool:
        """Test Discord webhook connection."""
        if not self.webhook_url:
            return False

        try:
            test_payload = {
                "content": "🧪 **Discord Webhook Test**\n\nV2_SWARM DevLog integration is now operational!",
                "username": "V2_SWARM Test Bot",
            }

            response = self.session.post(self.webhook_url, json=test_payload)

            if response.status_code == 204:
                print("✅ Discord webhook connection successful!")
                return True
            else:
                print(f"❌ Discord webhook test failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Discord webhook test error: {e}")
            return False

    async def test_integration(self) -> bool:
        """Test all Discord integration components."""
        print("🧪 Testing Discord Service Integration")
        print("=" * 50)

        # Test webhook
        webhook_test = self.test_webhook_connection()
        print(f"Webhook Connection: {'✅ PASS' if webhook_test else '❌ FAIL'}")

        # Test agent communication
        test_message = (
            "🧪 **Discord Service Integration Test**\n\nTesting agent communication system..."
        )
        broadcast_result = await self.agent_engine.broadcast_to_all_agents(
            test_message, sender="Discord_Service_Test"
        )
        agent_test = broadcast_result.success
        print(f"Agent Communication: {'✅ PASS' if agent_test else '❌ FAIL'}")

        # Test devlog processing
        devlog_test_data = {
            "title": "Integration Test DevLog",
            "description": "Testing Discord DevLog integration functionality",
            "category": "testing",
            "agent": "Discord_Service",
            "filepath": "test/integration_test.md",
            "timestamp": datetime.utcnow().isoformat(),
        }

        devlog_test = self.send_devlog_notification(devlog_test_data)
        print(f"DevLog Processing: {'✅ PASS' if devlog_test else '❌ FAIL'}")

        all_tests_pass = webhook_test and agent_test and devlog_test
        print(
            f"\n📊 Integration Test Result: {'✅ ALL TESTS PASSED' if all_tests_pass else '❌ SOME TESTS FAILED'}"
        )

        return all_tests_pass

    def stop_monitoring(self):
        """Stop devlog monitoring."""
        self.is_running = False
        print("🛑 DevLog monitoring stopping...")


# Global instance for singleton pattern
_discord_service_instance = None


def get_discord_service(webhook_url: str | None = None) -> DiscordService:
    """Get Discord service instance (singleton pattern)."""
    global _discord_service_instance
    if _discord_service_instance is None:
        _discord_service_instance = DiscordService(webhook_url)
    return _discord_service_instance


async def start_discord_devlog_monitoring(webhook_url: str | None = None, check_interval: int = 60):
    """Start Discord DevLog monitoring (convenience function)."""
    service = get_discord_service(webhook_url)
    await service.start_devlog_monitoring(check_interval)


if __name__ == "__main__":

    async def main():
        service = DiscordService()
        await service.test_integration()

    asyncio.run(main())
