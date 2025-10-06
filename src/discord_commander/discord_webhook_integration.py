#!/usr/bin/env python3
"""
Discord Webhook Integration - V2 Compliance Module
==================================================

Discord webhook integration for DevLog notifications and agent communication.

Author: Agent-3 (Infrastructure & DevOps) - V2 Restoration
License: MIT
"""

import json
import os
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class DiscordWebhookIntegration:
    """Discord webhook integration for DevLog notifications."""

    def __init__(self, webhook_url: Optional[str] = None):
        """Initialize Discord webhook integration."""
        self.webhook_url = webhook_url or self._load_webhook_url()
        self.session = requests.Session()
        self.session.timeout = 10

    def _load_webhook_url(self) -> Optional[str]:
        """Load webhook URL from environment or config."""
        # Try environment variable first
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

        if not webhook_url:
            # Try to load from config file
            config_path = Path("config/discord_config.json")
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        webhook_url = config.get("webhook_url")
                except Exception:
                    pass

        return webhook_url

    def send_devlog_notification(self, devlog_data: Dict[str, Any]) -> bool:
        """Send devlog notification to Discord."""
        if not self.webhook_url:
            print("❌ No Discord webhook URL configured")
            return False

        try:
            # Create embed for devlog
            embed = self._create_devlog_embed(devlog_data)

            payload = {
                "embeds": [embed],
                "username": "V2_SWARM DevLog Monitor",
                "avatar_url": "https://i.imgur.com/XXXXXXX.png"  # Add swarm avatar URL
            }

            response = self.session.post(self.webhook_url, json=payload)

            if response.status_code == 204:
                print(f"✅ DevLog notification sent: {devlog_data.get('title', 'Unknown')}")
                return True
            else:
                print(f"❌ Failed to send devlog notification: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending devlog notification: {e}")
            return False

    def send_agent_status_notification(self, agent_status: Dict[str, Any]) -> bool:
        """Send agent status notification to Discord."""
        if not self.webhook_url:
            print("❌ No Discord webhook URL configured")
            return False

        try:
            embed = self._create_agent_status_embed(agent_status)

            payload = {
                "embeds": [embed],
                "username": "V2_SWARM Status Monitor",
                "avatar_url": "https://i.imgur.com/YYYYYYY.png"
            }

            response = self.session.post(self.webhook_url, json=payload)

            if response.status_code == 204:
                print(f"✅ Agent status notification sent for: {agent_status.get('agent_id', 'Unknown')}")
                return True
            else:
                print(f"❌ Failed to send agent status notification: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending agent status notification: {e}")
            return False

    def send_swarm_coordination_notification(self, coordination_data: Dict[str, Any]) -> bool:
        """Send swarm coordination notification to Discord."""
        if not self.webhook_url:
            print("❌ No Discord webhook URL configured")
            return False

        try:
            embed = self._create_coordination_embed(coordination_data)

            payload = {
                "embeds": [embed],
                "username": "V2_SWARM Coordinator",
                "avatar_url": "https://i.imgur.com/ZZZZZZZ.png"
            }

            response = self.session.post(self.webhook_url, json=payload)

            if response.status_code == 204:
                print(f"✅ Swarm coordination notification sent: {coordination_data.get('topic', 'Unknown')}")
                return True
            else:
                print(f"❌ Failed to send coordination notification: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending coordination notification: {e}")
            return False

    def _create_devlog_embed(self, devlog_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Discord embed for devlog notification."""
        title = devlog_data.get("title", "DevLog Update")
        description = devlog_data.get("description", "")
        category = devlog_data.get("category", "general")
        agent = devlog_data.get("agent", "Unknown")

        # Color coding based on category
        colors = {
            "general": 0x3498db,      # Blue
            "cleanup": 0xe74c3c,      # Red
            "consolidation": 0x9b59b6, # Purple
            "coordination": 0x1abc9c,  # Teal
            "testing": 0xf39c12,      # Orange
            "deployment": 0x27ae60     # Green
        }

        embed = {
            "title": f"📋 {title}",
            "description": description[:2000] if description else "DevLog update received",
            "color": colors.get(category, 0x3498db),
            "fields": [
                {
                    "name": "Category",
                    "value": category.title(),
                    "inline": True
                },
                {
                    "name": "Agent",
                    "value": agent,
                    "inline": True
                },
                {
                    "name": "Timestamp",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True
                }
            ],
            "footer": {
                "text": "V2_SWARM DevLog Monitor",
                "icon_url": "https://i.imgur.com/AAAAAAA.png"
            }
        }

        return embed

    def _create_agent_status_embed(self, agent_status: Dict[str, Any]) -> Dict[str, Any]:
        """Create Discord embed for agent status notification."""
        agent_id = agent_status.get("agent_id", "Unknown")
        status = agent_status.get("status", "unknown")
        last_activity = agent_status.get("last_activity", "Unknown")

        # Color based on status
        status_colors = {
            "active": 0x27ae60,      # Green
            "idle": 0xf39c12,        # Orange
            "error": 0xe74c3c,       # Red
            "offline": 0x95a5a6      # Gray
        }

        embed = {
            "title": f"🤖 Agent Status Update - {agent_id}",
            "color": status_colors.get(status, 0x3498db),
            "fields": [
                {
                    "name": "Status",
                    "value": status.title(),
                    "inline": True
                },
                {
                    "name": "Last Activity",
                    "value": last_activity,
                    "inline": True
                },
                {
                    "name": "Timestamp",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True
                }
            ],
            "footer": {
                "text": "V2_SWARM Status Monitor",
                "icon_url": "https://i.imgur.com/BBBBBBB.png"
            }
        }

        return embed

    def _create_coordination_embed(self, coordination_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Discord embed for swarm coordination notification."""
        topic = coordination_data.get("topic", "Swarm Coordination")
        priority = coordination_data.get("priority", "NORMAL")
        participants = coordination_data.get("participants", [])

        # Color based on priority
        priority_colors = {
            "LOW": 0x95a5a6,         # Gray
            "NORMAL": 0x3498db,      # Blue
            "HIGH": 0xf39c12,        # Orange
            "URGENT": 0xe74c3c       # Red
        }

        embed = {
            "title": f"🐝 SWARM COORDINATION - {topic}",
            "description": coordination_data.get("description", ""),
            "color": priority_colors.get(priority, 0x3498db),
            "fields": [
                {
                    "name": "Priority",
                    "value": priority,
                    "inline": True
                },
                {
                    "name": "Participants",
                    "value": ", ".join(participants) if participants else "All Agents",
                    "inline": True
                },
                {
                    "name": "Timestamp",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True
                }
            ],
            "footer": {
                "text": "V2_SWARM Coordinator",
                "icon_url": "https://i.imgur.com/CCCCCCC.png"
            }
        }

        return embed

    def test_webhook_connection(self) -> bool:
        """Test Discord webhook connection."""
        if not self.webhook_url:
            print("❌ No webhook URL configured")
            return False

        try:
            test_payload = {
                "content": "🧪 **Discord Webhook Test**\n\nV2_SWARM DevLog integration is now operational!",
                "username": "V2_SWARM Test Bot"
            }

            response = self.session.post(self.webhook_url, json=test_payload)

            if response.status_code == 204:
                print("✅ Discord webhook connection successful!")
                return True
            else:
                print(f"❌ Discord webhook test failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Discord webhook test error: {e}")
            return False
