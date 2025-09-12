#!/usr/bin/env python3
"""
Discord Webhook Integration - Enhanced Swarm Coordination
========================================================

Enhanced Discord webhook integration for DevLog notifications, agent communication,
and swarm coordination with proper swarm avatar URLs and advanced capabilities.

Features:
- Proper swarm avatar URLs for all webhook types
- Enhanced agent coordination messaging
- Real-time status synchronization
- Mission progress tracking
- Contract assignment notifications
- Error and recovery notifications

Author: Agent-6 (Web Interface & Communication Specialist) - Enhanced Implementation
Original Author: Agent-3 (Infrastructure & DevOps) - V2 Restoration
License: MIT
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


class DiscordWebhookIntegration:
    """
    Enhanced Discord webhook integration for swarm coordination.

    Features:
    - Multiple webhook types with proper swarm avatars
    - Enhanced agent coordination messaging
    - Real-time status and mission progress tracking
    - Contract assignment and completion notifications
    - Error handling and recovery notifications
    """

    # Swarm Avatar URLs for different webhook types
    SWARM_AVATARS = {
        "devlog": "https://i.imgur.com/dKoWQ7W.png",  # Swarm DevLog Monitor avatar
        "status": "https://i.imgur.com/8wJzQ2N.png",  # Swarm Status Monitor avatar
        "coordinator": "https://i.imgur.com/Rt5Qz8K.png",  # Swarm Coordinator avatar
        "contract": "https://i.imgur.com/MvLkW9P.png",  # Swarm Contract Manager avatar
        "error": "https://i.imgur.com/Hq8Tx4L.png",  # Swarm Error Handler avatar
        "recovery": "https://i.imgur.com/Yp4Nx8R.png",  # Swarm Recovery Specialist avatar
        "agent": "https://i.imgur.com/6w8Qx9M.png",  # Generic Agent avatar
    }

    def __init__(self, webhook_url: str | None = None):
        """Initialize enhanced Discord webhook integration."""
        self.webhook_url = webhook_url or self._load_webhook_url()
        self.session = requests.Session()
        self.session.timeout = 10

        # Enhanced coordination tracking
        self.active_missions = {}
        self.agent_status_cache = {}
        self.contract_assignments = {}
        self.coordination_events = []

        # Initialize coordination monitoring
        self._initialize_coordination_tracking()

    def _load_webhook_url(self) -> str | None:
        """Load webhook URL from environment or config."""
        # Try environment variable first
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

        if not webhook_url:
            # Try to load from config file
            config_path = Path("config/discord_config.json")
            if config_path.exists():
                try:
                    with open(config_path) as f:
                        config = json.load(f)
                        webhook_url = config.get("webhook_url")
                except Exception:
                    pass

        return webhook_url

    def send_devlog_notification(self, devlog_data: dict[str, Any]) -> bool:
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
                "avatar_url": self.SWARM_AVATARS["devlog"],
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

    def send_agent_status_notification(self, agent_status: dict[str, Any]) -> bool:
        """Send agent status notification to Discord."""
        if not self.webhook_url:
            print("❌ No Discord webhook URL configured")
            return False

        try:
            embed = self._create_agent_status_embed(agent_status)

            payload = {
                "embeds": [embed],
                "username": "V2_SWARM Status Monitor",
                "avatar_url": self.SWARM_AVATARS["status"],
            }

            response = self.session.post(self.webhook_url, json=payload)

            if response.status_code == 204:
                print(
                    f"✅ Agent status notification sent for: {agent_status.get('agent_id', 'Unknown')}"
                )
                return True
            else:
                print(f"❌ Failed to send agent status notification: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending agent status notification: {e}")
            return False

    def send_swarm_coordination_notification(self, coordination_data: dict[str, Any]) -> bool:
        """Send swarm coordination notification to Discord."""
        if not self.webhook_url:
            print("❌ No Discord webhook URL configured")
            return False

        try:
            embed = self._create_coordination_embed(coordination_data)

            payload = {
                "embeds": [embed],
                "username": "V2_SWARM Coordinator",
                "avatar_url": self.SWARM_AVATARS["coordinator"],
            }

            response = self.session.post(self.webhook_url, json=payload)

            if response.status_code == 204:
                print(
                    f"✅ Swarm coordination notification sent: {coordination_data.get('topic', 'Unknown')}"
                )
                return True
            else:
                print(f"❌ Failed to send coordination notification: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending coordination notification: {e}")
            return False

    def _create_devlog_embed(self, devlog_data: dict[str, Any]) -> dict[str, Any]:
        """Create Discord embed for devlog notification."""
        title = devlog_data.get("title", "DevLog Update")
        description = devlog_data.get("description", "")
        category = devlog_data.get("category", "general")
        agent = devlog_data.get("agent", "Unknown")

        # Color coding based on category
        colors = {
            "general": 0x3498DB,  # Blue
            "cleanup": 0xE74C3C,  # Red
            "consolidation": 0x9B59B6,  # Purple
            "coordination": 0x1ABC9C,  # Teal
            "testing": 0xF39C12,  # Orange
            "deployment": 0x27AE60,  # Green
        }

        embed = {
            "title": f"📋 {title}",
            "description": description[:2000] if description else "DevLog update received",
            "color": colors.get(category, 0x3498DB),
            "fields": [
                {"name": "Category", "value": category.title(), "inline": True},
                {"name": "Agent", "value": agent, "inline": True},
                {
                    "name": "Timestamp",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True,
                },
            ],
            "footer": {
                "text": "V2_SWARM DevLog Monitor",
                "icon_url": self.SWARM_AVATARS["devlog"],
            },
        }

        return embed

    def _create_agent_status_embed(self, agent_status: dict[str, Any]) -> dict[str, Any]:
        """Create Discord embed for agent status notification."""
        agent_id = agent_status.get("agent_id", "Unknown")
        status = agent_status.get("status", "unknown")
        last_activity = agent_status.get("last_activity", "Unknown")

        # Color based on status
        status_colors = {
            "active": 0x27AE60,  # Green
            "idle": 0xF39C12,  # Orange
            "error": 0xE74C3C,  # Red
            "offline": 0x95A5A6,  # Gray
        }

        embed = {
            "title": f"🤖 Agent Status Update - {agent_id}",
            "color": status_colors.get(status, 0x3498DB),
            "fields": [
                {"name": "Status", "value": status.title(), "inline": True},
                {"name": "Last Activity", "value": last_activity, "inline": True},
                {
                    "name": "Timestamp",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True,
                },
            ],
            "footer": {
                "text": "V2_SWARM Status Monitor",
                "icon_url": self.SWARM_AVATARS["status"],
            },
        }

        return embed

    def _create_coordination_embed(self, coordination_data: dict[str, Any]) -> dict[str, Any]:
        """Create Discord embed for swarm coordination notification."""
        topic = coordination_data.get("topic", "Swarm Coordination")
        priority = coordination_data.get("priority", "NORMAL")
        participants = coordination_data.get("participants", [])

        # Color based on priority
        priority_colors = {
            "LOW": 0x95A5A6,  # Gray
            "NORMAL": 0x3498DB,  # Blue
            "HIGH": 0xF39C12,  # Orange
            "URGENT": 0xE74C3C,  # Red
        }

        embed = {
            "title": f"🐝 SWARM COORDINATION - {topic}",
            "description": coordination_data.get("description", ""),
            "color": priority_colors.get(priority, 0x3498DB),
            "fields": [
                {"name": "Priority", "value": priority, "inline": True},
                {
                    "name": "Participants",
                    "value": ", ".join(participants) if participants else "All Agents",
                    "inline": True,
                },
                {
                    "name": "Timestamp",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True,
                },
            ],
            "footer": {
                "text": "V2_SWARM Coordinator",
                "icon_url": self.SWARM_AVATARS["coordinator"],
            },
        }

        return embed

    def _initialize_coordination_tracking(self) -> None:
        """Initialize coordination tracking systems."""
        print("🔧 Initializing enhanced coordination tracking...")

        # Load existing coordination data if available
        self._load_coordination_data()

        print("✅ Coordination tracking initialized")

    def _load_coordination_data(self) -> None:
        """Load existing coordination data from storage."""
        try:
            data_file = Path("data/webhook_coordination.json")
            if data_file.exists():
                with open(data_file) as f:
                    data = json.load(f)
                    self.active_missions = data.get("active_missions", {})
                    self.agent_status_cache = data.get("agent_status_cache", {})
                    self.contract_assignments = data.get("contract_assignments", {})
                    self.coordination_events = data.get("coordination_events", [])
        except Exception as e:
            print(f"⚠️ Could not load coordination data: {e}")

    def _save_coordination_data(self) -> None:
        """Save coordination data to storage."""
        try:
            data_file = Path("data/webhook_coordination.json")
            data_file.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "active_missions": self.active_missions,
                "agent_status_cache": self.agent_status_cache,
                "contract_assignments": self.contract_assignments,
                "coordination_events": self.coordination_events[-100:],  # Keep last 100 events
                "last_updated": datetime.utcnow().isoformat(),
            }

            with open(data_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save coordination data: {e}")

    # ===========================================
    # ENHANCED COORDINATION METHODS
    # ===========================================

    def send_contract_assignment_notification(self, contract_data: dict[str, Any]) -> bool:
        """Send contract assignment notification to Discord."""
        if not self.webhook_url:
            print("❌ No Discord webhook URL configured")
            return False

        try:
            embed = self._create_contract_assignment_embed(contract_data)

            payload = {
                "embeds": [embed],
                "username": "V2_SWARM Contract Manager",
                "avatar_url": self.SWARM_AVATARS["contract"],
            }

            response = self.session.post(self.webhook_url, json=payload)

            if response.status_code == 204:
                contract_id = contract_data.get("contract_id", "Unknown")
                print(f"✅ Contract assignment notification sent: {contract_id}")

                # Track contract assignment
                self.contract_assignments[contract_id] = {
                    "assigned_to": contract_data.get("agent_id", "Unknown"),
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "assigned",
                }
                self._save_coordination_data()

                return True
            else:
                print(f"❌ Failed to send contract notification: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending contract notification: {e}")
            return False

    def send_mission_progress_notification(self, mission_data: dict[str, Any]) -> bool:
        """Send mission progress notification to Discord."""
        if not self.webhook_url:
            print("❌ No Discord webhook URL configured")
            return False

        try:
            embed = self._create_mission_progress_embed(mission_data)

            payload = {
                "embeds": [embed],
                "username": "V2_SWARM Mission Tracker",
                "avatar_url": self.SWARM_AVATARS["coordinator"],
            }

            response = self.session.post(self.webhook_url, json=payload)

            if response.status_code == 204:
                mission_id = mission_data.get("mission_id", "Unknown")
                progress = mission_data.get("progress", 0)
                print(f"✅ Mission progress notification sent: {mission_id} ({progress}%)")

                # Track mission progress
                self.active_missions[mission_id] = {
                    "progress": progress,
                    "last_update": datetime.utcnow().isoformat(),
                    "agent": mission_data.get("agent_id", "Unknown"),
                }
                self._save_coordination_data()

                return True
            else:
                print(f"❌ Failed to send mission progress notification: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending mission progress notification: {e}")
            return False

    def send_error_recovery_notification(self, error_data: dict[str, Any]) -> bool:
        """Send error recovery notification to Discord."""
        if not self.webhook_url:
            print("❌ No Discord webhook URL configured")
            return False

        try:
            embed = self._create_error_recovery_embed(error_data)

            payload = {
                "embeds": [embed],
                "username": "V2_SWARM Recovery Specialist",
                "avatar_url": self.SWARM_AVATARS["recovery"],
            }

            response = self.session.post(self.webhook_url, json=payload)

            if response.status_code == 204:
                error_type = error_data.get("error_type", "Unknown")
                recovery_status = error_data.get("recovery_status", "Unknown")
                print(f"✅ Error recovery notification sent: {error_type} - {recovery_status}")
                return True
            else:
                print(f"❌ Failed to send error recovery notification: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending error recovery notification: {e}")
            return False

    def send_coordination_event_notification(self, event_data: dict[str, Any]) -> bool:
        """Send coordination event notification to Discord."""
        if not self.webhook_url:
            print("❌ No Discord webhook URL configured")
            return False

        try:
            embed = self._create_coordination_event_embed(event_data)

            payload = {
                "embeds": [embed],
                "username": "V2_SWARM Event Coordinator",
                "avatar_url": self.SWARM_AVATARS["coordinator"],
            }

            response = self.session.post(self.webhook_url, json=payload)

            if response.status_code == 204:
                event_type = event_data.get("event_type", "Unknown")
                print(f"✅ Coordination event notification sent: {event_type}")

                # Track coordination event
                self.coordination_events.append(
                    {
                        "event_type": event_type,
                        "timestamp": datetime.utcnow().isoformat(),
                        "participants": event_data.get("participants", []),
                        "details": event_data.get("details", ""),
                    }
                )
                self._save_coordination_data()

                return True
            else:
                print(f"❌ Failed to send coordination event notification: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending coordination event notification: {e}")
            return False

    # ===========================================
    # ENHANCED EMBED CREATION METHODS
    # ===========================================

    def _create_contract_assignment_embed(self, contract_data: dict[str, Any]) -> dict[str, Any]:
        """Create Discord embed for contract assignment notification."""
        contract_id = contract_data.get("contract_id", "Unknown")
        title = contract_data.get("contract_title", "Contract Assignment")
        agent_id = contract_data.get("agent_id", "Unknown")
        priority = contract_data.get("priority", "NORMAL")
        deadline = contract_data.get("deadline", "No deadline")

        # Color based on priority
        priority_colors = {
            "LOW": 0x95A5A6,  # Gray
            "NORMAL": 0x3498DB,  # Blue
            "HIGH": 0xF39C12,  # Orange
            "CRITICAL": 0xE74C3C,  # Red
        }

        embed = {
            "title": f"📋 CONTRACT ASSIGNED - {contract_id}",
            "description": contract_data.get("description", ""),
            "color": priority_colors.get(priority, 0x3498DB),
            "fields": [
                {"name": "Agent", "value": agent_id, "inline": True},
                {"name": "Priority", "value": priority, "inline": True},
                {"name": "Deadline", "value": deadline, "inline": True},
                {
                    "name": "XP Reward",
                    "value": str(contract_data.get("experience_points", 0)),
                    "inline": True,
                },
            ],
            "footer": {
                "text": "V2_SWARM Contract Manager",
                "icon_url": self.SWARM_AVATARS["contract"],
            },
        }

        return embed

    def _create_mission_progress_embed(self, mission_data: dict[str, Any]) -> dict[str, Any]:
        """Create Discord embed for mission progress notification."""
        mission_id = mission_data.get("mission_id", "Unknown")
        title = mission_data.get("title", "Mission Progress")
        progress = mission_data.get("progress", 0)
        agent_id = mission_data.get("agent_id", "Unknown")
        status = mission_data.get("status", "unknown")

        # Color based on progress
        if progress >= 90:
            color = 0x27AE60  # Green - Near completion
        elif progress >= 50:
            color = 0xF39C12  # Orange - Good progress
        elif progress >= 25:
            color = 0x3498DB  # Blue - Started
        else:
            color = 0x95A5A6  # Gray - Just started

        embed = {
            "title": f"📊 MISSION PROGRESS - {mission_id}",
            "description": mission_data.get("description", ""),
            "color": color,
            "fields": [
                {"name": "Agent", "value": agent_id, "inline": True},
                {"name": "Progress", "value": f"{progress}%", "inline": True},
                {"name": "Status", "value": status.title(), "inline": True},
                {
                    "name": "Last Update",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True,
                },
            ],
            "footer": {
                "text": "V2_SWARM Mission Tracker",
                "icon_url": self.SWARM_AVATARS["coordinator"],
            },
        }

        return embed

    def _create_error_recovery_embed(self, error_data: dict[str, Any]) -> dict[str, Any]:
        """Create Discord embed for error recovery notification."""
        error_type = error_data.get("error_type", "Unknown Error")
        recovery_status = error_data.get("recovery_status", "Unknown")
        agent_id = error_data.get("agent_id", "Unknown")

        # Color based on recovery status
        if recovery_status.lower() in ["success", "completed", "resolved"]:
            color = 0x27AE60  # Green - Successful recovery
        elif recovery_status.lower() in ["in_progress", "attempting"]:
            color = 0xF39C12  # Orange - Recovery in progress
        else:
            color = 0xE74C3C  # Red - Recovery failed

        embed = {
            "title": f"🛡️ ERROR RECOVERY - {error_type}",
            "description": error_data.get("description", ""),
            "color": color,
            "fields": [
                {"name": "Agent", "value": agent_id, "inline": True},
                {"name": "Recovery Status", "value": recovery_status.title(), "inline": True},
                {
                    "name": "Timestamp",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True,
                },
            ],
            "footer": {
                "text": "V2_SWARM Recovery Specialist",
                "icon_url": self.SWARM_AVATARS["recovery"],
            },
        }

        return embed

    def _create_coordination_event_embed(self, event_data: dict[str, Any]) -> dict[str, Any]:
        """Create Discord embed for coordination event notification."""
        event_type = event_data.get("event_type", "Coordination Event")
        participants = event_data.get("participants", [])
        priority = event_data.get("priority", "NORMAL")

        # Color based on priority
        priority_colors = {
            "LOW": 0x95A5A6,  # Gray
            "NORMAL": 0x3498DB,  # Blue
            "HIGH": 0xF39C12,  # Orange
            "URGENT": 0xE74C3C,  # Red
        }

        embed = {
            "title": f"🤝 COORDINATION EVENT - {event_type}",
            "description": event_data.get("description", ""),
            "color": priority_colors.get(priority, 0x3498DB),
            "fields": [
                {"name": "Priority", "value": priority, "inline": True},
                {
                    "name": "Participants",
                    "value": ", ".join(participants) if participants else "All Agents",
                    "inline": True,
                },
                {
                    "name": "Timestamp",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True,
                },
            ],
            "footer": {
                "text": "V2_SWARM Event Coordinator",
                "icon_url": self.SWARM_AVATARS["coordinator"],
            },
        }

        return embed

    # ===========================================
    # COORDINATION STATUS METHODS
    # ===========================================

    def get_coordination_status(self) -> dict[str, Any]:
        """Get comprehensive coordination status."""
        return {
            "active_missions": self.active_missions,
            "agent_status_cache": self.agent_status_cache,
            "contract_assignments": self.contract_assignments,
            "coordination_events_count": len(self.coordination_events),
            "webhook_configured": bool(self.webhook_url),
            "swarm_avatars": self.SWARM_AVATARS,
            "last_updated": datetime.utcnow().isoformat(),
        }

    def update_agent_status_cache(self, agent_id: str, status_data: dict[str, Any]) -> None:
        """Update agent status cache."""
        self.agent_status_cache[agent_id] = {
            **status_data,
            "last_updated": datetime.utcnow().isoformat(),
        }
        self._save_coordination_data()

    def clear_coordination_cache(self) -> None:
        """Clear coordination cache and reset tracking."""
        self.active_missions = {}
        self.agent_status_cache = {}
        self.contract_assignments = {}
        self.coordination_events = []
        self._save_coordination_data()
        print("🧹 Coordination cache cleared")

    def test_webhook_connection(self) -> bool:
        """Test Discord webhook connection."""
        if not self.webhook_url:
            print("❌ No webhook URL configured")
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
                print(f"Response: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Discord webhook test error: {e}")
            return False
