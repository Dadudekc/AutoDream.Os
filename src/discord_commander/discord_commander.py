#!/usr/bin/env python3
"""
Discord Commander - V2 Compliance Module
========================================

Main Discord integration for V2_SWARM DevLog monitoring and agent communication.

Author: Agent-3 (Infrastructure & DevOps) - V2 Restoration
License: MIT
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from .agent_communication_engine_refactored import AgentCommunicationEngine
    from .discord_webhook_integration import DiscordWebhookIntegration
except ImportError:
    # Fallback for direct execution
    from agent_communication_engine_refactored import AgentCommunicationEngine
    from discord_webhook_integration import DiscordWebhookIntegration


class DiscordCommander:
    """Main Discord commander for V2_SWARM DevLog integration."""

    def __init__(self, webhook_url: str | None = None):
        """Initialize Discord commander."""
        self.agent_engine = AgentCommunicationEngine()
        self.webhook_integration = DiscordWebhookIntegration(webhook_url)
        self.devlogs_path = Path("devlogs")
        self.last_check_time = datetime.utcnow()
        self.is_running = False

    async def start_devlog_monitoring(self, check_interval: int = 60):
        """Start monitoring devlogs and sending Discord notifications."""
        print("🚀 Starting Discord DevLog monitoring...")
        print(f"📁 Monitoring directory: {self.devlogs_path}")
        print(f"⏱️  Check interval: {check_interval} seconds")
        print()

        if not self.devlogs_path.exists():
            print(f"❌ DevLogs directory not found: {self.devlogs_path}")
            return

        # Test webhook connection
        if not self.webhook_integration.test_webhook_connection():
            print("⚠️  Continuing without Discord notifications...")
            print()

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
        new_files = []

        if not self.devlogs_path.exists():
            return new_files

        for file_path in self.devlogs_path.rglob("*.md"):
            if file_path.stat().st_mtime > self.last_check_time.timestamp():
                new_files.append(file_path)

        return sorted(new_files, key=lambda x: x.stat().st_mtime)

    async def _process_devlog(self, devlog_path: Path):
        """Process a single devlog file."""
        try:
            # Read devlog content
            with open(devlog_path, encoding='utf-8') as f:
                content = f.read()

            # Extract metadata from filename
            filename = devlog_path.name
            metadata = self._parse_devlog_filename(filename)

            # Create devlog data structure
            devlog_data = {
                "title": metadata.get("title", filename),
                "description": self._extract_devlog_summary(content),
                "category": metadata.get("category", "general"),
                "agent": metadata.get("agent", "Unknown"),
                "filepath": str(devlog_path),
                "timestamp": datetime.utcnow().isoformat()
            }

            print(f"📝 Processing devlog: {devlog_data['title']}")

            # Send Discord notification
            if self.webhook_integration.send_devlog_notification(devlog_data):
                print("✅ Discord notification sent")

                # Also send to relevant agents
                await self._notify_agents_of_devlog(devlog_data)

            else:
                print("❌ Failed to send Discord notification")

        except Exception as e:
            print(f"❌ Error processing devlog {devlog_path}: {e}")

    def _parse_devlog_filename(self, filename: str) -> dict[str, str]:
        """Parse metadata from devlog filename."""
        # Example: 2025-09-09_094500_general_Agent-3_Project_Status_Update.md
        parts = filename.replace('.md', '').split('_')

        metadata = {
            "timestamp": "unknown",
            "category": "general",
            "agent": "Unknown",
            "title": filename
        }

        if len(parts) >= 4:
            metadata["timestamp"] = f"{parts[0]}_{parts[1]}"
            metadata["category"] = parts[2]
            metadata["agent"] = parts[3]
            metadata["title"] = '_'.join(parts[4:]) if len(parts) > 4 else "DevLog Update"

        return metadata

    def _extract_devlog_summary(self, content: str, max_length: int = 500) -> str:
        """Extract summary from devlog content."""
        lines = content.split('\n')

        # Look for summary section or first meaningful paragraph
        summary = ""
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 20:
                summary += line + " "
                if len(summary) > max_length:
                    break

        if not summary:
            summary = "DevLog update processed by V2_SWARM monitoring system."

        return summary[:max_length].strip()

    async def _notify_agents_of_devlog(self, devlog_data: dict[str, Any]):
        """Notify relevant agents about the devlog."""
        try:
            agent = devlog_data.get("agent", "Unknown")
            category = devlog_data.get("category", "general")

            # Create agent notification message
            message = f"""🚨 DEVCORD DEVLOG ALERT

**New DevLog Activity Detected:**
• **Title:** {devlog_data['title']}
• **Category:** {category.title()}
• **Agent:** {agent}
• **Summary:** {devlog_data['description'][:200]}...

**DevLog monitoring is active and Discord notifications are enabled.**
**WE ARE SWARM - Stay coordinated!**

---
*Automated DevLog Monitor*
"""

            # Send to all agents for awareness
            result = await self.agent_engine.broadcast_to_all_agents(
                message,
                sender="Discord_DevLog_Monitor"
            )

            if result.success:
                print(f"✅ Notified {result.data.get('successful_deliveries', 0)} agents")
            else:
                print("❌ Failed to notify agents about devlog")

        except Exception as e:
            print(f"❌ Error notifying agents: {e}")

    async def send_agent_status_update(self, agent_id: str, status: str, details: str = ""):
        """Send agent status update via Discord."""
        status_data = {
            "agent_id": agent_id,
            "status": status,
            "last_activity": details or f"Status update at {datetime.utcnow().isoformat()}",
            "timestamp": datetime.utcnow().isoformat()
        }

        if self.webhook_integration.send_agent_status_notification(status_data):
            print(f"✅ Agent {agent_id} status sent to Discord")
        else:
            print(f"❌ Failed to send agent {agent_id} status to Discord")

    async def send_coordination_notification(self, topic: str, description: str, priority: str = "NORMAL"):
        """Send swarm coordination notification via Discord."""
        coordination_data = {
            "topic": topic,
            "description": description,
            "priority": priority,
            "participants": ["All Agents"],
            "timestamp": datetime.utcnow().isoformat()
        }

        if self.webhook_integration.send_swarm_coordination_notification(coordination_data):
            print(f"✅ Coordination notification sent: {topic}")
        else:
            print("❌ Failed to send coordination notification")

    def stop_monitoring(self):
        """Stop devlog monitoring."""
        self.is_running = False
        print("🛑 DevLog monitoring stopping...")

    async def test_integration(self):
        """Test all Discord integration components."""
        print("🧪 Testing Discord Commander Integration")
        print("=" * 50)

        # Test webhook connection
        webhook_test = self.webhook_integration.test_webhook_connection()
        print(f"Webhook Connection: {'✅ PASS' if webhook_test else '❌ FAIL'}")

        # Test agent communication
        test_message = "🧪 **Discord Commander Integration Test**\n\nTesting agent communication system..."
        broadcast_result = await self.agent_engine.broadcast_to_all_agents(
            test_message,
            sender="Discord_Commander_Test"
        )
        agent_test = broadcast_result.success
        print(f"Agent Communication: {'✅ PASS' if agent_test else '❌ FAIL'}")

        # Test devlog processing
        devlog_test_data = {
            "title": "Integration Test DevLog",
            "description": "Testing Discord DevLog integration functionality",
            "category": "testing",
            "agent": "Discord_Commander",
            "filepath": "test/integration_test.md",
            "timestamp": datetime.utcnow().isoformat()
        }

        devlog_test = self.webhook_integration.send_devlog_notification(devlog_test_data)
        print(f"DevLog Processing: {'✅ PASS' if devlog_test else '❌ FAIL'}")

        # Summary
        all_tests_pass = webhook_test and agent_test and devlog_test
        print(f"\n📊 Integration Test Result: {'✅ ALL TESTS PASSED' if all_tests_pass else '❌ SOME TESTS FAILED'}")

        return all_tests_pass


# Global instance for easy access
_discord_commander_instance = None


def get_discord_commander(webhook_url: str | None = None) -> DiscordCommander:
    """Get Discord commander instance (singleton pattern)."""
    global _discord_commander_instance
    if _discord_commander_instance is None:
        _discord_commander_instance = DiscordCommander(webhook_url)
    return _discord_commander_instance


async def start_discord_devlog_monitoring(webhook_url: str | None = None, check_interval: int = 60):
    """Start Discord DevLog monitoring (convenience function)."""
    commander = get_discord_commander(webhook_url)
    await commander.start_devlog_monitoring(check_interval)


if __name__ == "__main__":
    # Test the integration when run directly
    async def main():
        commander = DiscordCommander()
        await commander.test_integration()

    asyncio.run(main())
