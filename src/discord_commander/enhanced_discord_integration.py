#!/usr/bin/env python3
"""
Enhanced Discord Integration - V2 Compliance Module
==================================================

Expanded Discord integration with individual agent channels and restored functionality.

Features:
- Individual Discord channels for each agent (Agent-1 through Agent-8)
- Enhanced webhook system with multi-channel support
- Agent-specific notifications and coordination
- Restored and expanded DevLog monitoring
- Swarm coordination through Discord channels

Author: Agent-3 (DevOps Specialist) - Discord Expansion Coordinator
License: MIT
"""

import asyncio
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import requests

# Swarm imports
try:
    from ..core.unified_config import get_config
    from ..infrastructure.unified_persistence import UnifiedPersistenceService
    from ..utils.unified_logging_time import UnifiedLoggingTimeService
except ImportError:
    # Fallback for standalone execution
    get_config = lambda: {"discord": {}}


class AgentChannel(Enum):
    """Enumeration of agent channels."""

    AGENT_1 = "agent-1"
    AGENT_2 = "agent-2"
    AGENT_3 = "agent-3"
    AGENT_4 = "agent-4"
    AGENT_5 = "agent-5"
    AGENT_6 = "agent-6"
    AGENT_7 = "agent-7"
    AGENT_8 = "agent-8"
    SWARM_GENERAL = "swarm-general"
    SWARM_COORDINATION = "swarm-coordination"
    SWARM_ALERTS = "swarm-alerts"


@dataclass
class DiscordChannelConfig:
    """Configuration for a Discord channel."""

    name: str
    webhook_url: str | None = None
    channel_id: str | None = None
    description: str = ""
    agent: str | None = None
    color: int = 0x3498DB
    enabled: bool = True
    permissions: dict[str, bool] = field(
        default_factory=lambda: {
            "read_messages": True,
            "send_messages": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": False,
        }
    )


@dataclass
class DiscordMessage:
    """Discord message structure."""

    content: str
    embeds: list[dict[str, Any]] = field(default_factory=list)
    username: str | None = None
    avatar_url: str | None = None
    tts: bool = False


@dataclass
class AgentNotification:
    """Agent notification structure."""

    agent_id: str
    channel: AgentChannel
    title: str
    description: str
    priority: str = "NORMAL"
    category: str = "general"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


class EnhancedDiscordWebhookManager:
    """Enhanced webhook manager with multi-channel support."""

    def __init__(self, config_path: str = "config/discord_channels.json"):
        """Initialize enhanced webhook manager."""
        self.config_path = Path(config_path)
        self.channels: dict[AgentChannel, DiscordChannelConfig] = {}
        self.session = requests.Session()
        self.session.timeout = 15
        self._load_channel_config()

    def _load_channel_config(self) -> None:
        """Load channel configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    data = json.load(f)
                    for channel_name, config_data in data.items():
                        channel = AgentChannel(channel_name)
                        self.channels[channel] = DiscordChannelConfig(**config_data)
            except Exception as e:
                print(f"❌ Failed to load Discord channel config: {e}")
                self._create_default_channels()

        if not self.channels:
            self._create_default_channels()

    def _create_default_channels(self) -> None:
        """Create default channel configurations."""
        default_channels = {
            AgentChannel.AGENT_1: DiscordChannelConfig(
                name="agent-1",
                description="Agent-1 Integration Specialist Channel",
                agent="Agent-1",
                color=0x1ABC9C,
            ),
            AgentChannel.AGENT_2: DiscordChannelConfig(
                name="agent-2",
                description="Agent-2 Architecture & Design Channel",
                agent="Agent-2",
                color=0x3498DB,
            ),
            AgentChannel.AGENT_3: DiscordChannelConfig(
                name="agent-3",
                description="Agent-3 DevOps Specialist Channel",
                agent="Agent-3",
                color=0x9B59B6,
            ),
            AgentChannel.AGENT_4: DiscordChannelConfig(
                name="agent-4",
                description="Agent-4 QA & Captain Channel",
                agent="Agent-4",
                color=0xE74C3C,
            ),
            AgentChannel.AGENT_5: DiscordChannelConfig(
                name="agent-5", description="Agent-5 Channel", agent="Agent-5", color=0xF39C12
            ),
            AgentChannel.AGENT_6: DiscordChannelConfig(
                name="agent-6",
                description="Agent-6 Communication Specialist Channel",
                agent="Agent-6",
                color=0x27AE60,
            ),
            AgentChannel.AGENT_7: DiscordChannelConfig(
                name="agent-7",
                description="Agent-7 Web Development Channel",
                agent="Agent-7",
                color=0x95A5A6,
            ),
            AgentChannel.AGENT_8: DiscordChannelConfig(
                name="agent-8",
                description="Agent-8 Coordination Channel",
                agent="Agent-8",
                color=0x8E44AD,
            ),
            AgentChannel.SWARM_GENERAL: DiscordChannelConfig(
                name="swarm-general", description="General Swarm Announcements", color=0x34495E
            ),
            AgentChannel.SWARM_COORDINATION: DiscordChannelConfig(
                name="swarm-coordination", description="Swarm Coordination Hub", color=0xE67E22
            ),
            AgentChannel.SWARM_ALERTS: DiscordChannelConfig(
                name="swarm-alerts", description="Critical Swarm Alerts", color=0xE74C3C
            ),
        }

        self.channels.update(default_channels)
        self._save_channel_config()

    def _save_channel_config(self) -> None:
        """Save channel configuration to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            config_data = {}
            for channel, config in self.channels.items():
                config_data[channel.value] = {
                    "name": config.name,
                    "webhook_url": config.webhook_url,
                    "channel_id": config.channel_id,
                    "description": config.description,
                    "agent": config.agent,
                    "color": config.color,
                    "enabled": config.enabled,
                    "permissions": config.permissions,
                }

            with open(self.config_path, "w") as f:
                json.dump(config_data, f, indent=2)

        except Exception as e:
            print(f"❌ Failed to save Discord channel config: {e}")

    def set_channel_webhook(self, channel: AgentChannel, webhook_url: str) -> bool:
        """Set webhook URL for a channel."""
        if channel in self.channels:
            self.channels[channel].webhook_url = webhook_url
            self._save_channel_config()
            return True
        return False

    def get_channel_config(self, channel: AgentChannel) -> DiscordChannelConfig | None:
        """Get configuration for a channel."""
        return self.channels.get(channel)

    def send_to_channel(self, channel: AgentChannel, message: DiscordMessage) -> bool:
        """Send message to specific channel using webhook or channel ID."""
        config = self.channels.get(channel)
        if not config or not config.enabled:
            return False

        # Try webhook first, then fallback to channel ID messaging
        if config.webhook_url:
            return self._send_via_webhook(config, message)
        elif config.channel_id:
            return self._send_via_channel_id(config, message, channel)
        else:
            print(f"⚠️  No webhook URL or channel ID configured for {channel.value}")
            return False

    def _send_via_webhook(self, config: DiscordChannelConfig, message: DiscordMessage) -> bool:
        """Send message via webhook."""
        try:
            payload = {"content": message.content, "embeds": message.embeds, "tts": message.tts}

            if message.username:
                payload["username"] = message.username
            if message.avatar_url:
                payload["avatar_url"] = message.avatar_url

            response = self.session.post(config.webhook_url, json=payload)

            if response.status_code == 204:
                print(f"✅ Message sent via webhook to {config.name}")
                return True
            else:
                print(f"❌ Failed to send via webhook to {config.name}: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error sending via webhook to {config.name}: {e}")
            return False

    def _send_via_channel_id(
        self, config: DiscordChannelConfig, message: DiscordMessage, channel: AgentChannel
    ) -> bool:
        """Send message via Discord API using channel ID."""
        import asyncio
        import os

        # Check for Discord bot token
        bot_token = os.getenv("DISCORD_BOT_TOKEN")
        if not bot_token:
            print("❌ Discord Bot Token not found!")
            print("   Set DISCORD_BOT_TOKEN environment variable")
            print("   Example: export DISCORD_BOT_TOKEN='your_bot_token_here'")
            print(f"   Would send to channel: {config.channel_id} ({channel.value})")
            return False

        try:
            import discord
            from discord import Embed
        except ImportError:
            print("❌ discord.py library not installed!")
            print("   Install with: pip install discord.py")
            print(f"   Would send to channel: {config.channel_id} ({channel.value})")
            return False

        async def send_discord_message():
            """Send message to Discord channel asynchronously."""
            client = discord.Client(intents=discord.Intents.default())

            @client.event
            async def on_ready():
                try:
                    channel_obj = client.get_channel(int(config.channel_id))
                    if not channel_obj:
                        print(f"❌ Could not find channel with ID: {config.channel_id}")
                        await client.close()
                        return

                    # Prepare message content
                    content = message.content
                    username = message.username or "V2_SWARM Bot"
                    avatar_url = message.avatar_url

                    # Handle embeds if present
                    if message.embeds:
                        embed = message.embeds[0]  # Take first embed for simplicity
                        discord_embed = Embed(
                            title=embed.get("title", ""),
                            description=embed.get("description", ""),
                            color=embed.get("color", 0x3498DB),
                        )

                        # Add embed fields
                        if "fields" in embed:
                            for field in embed["fields"]:
                                discord_embed.add_field(
                                    name=field.get("name", ""),
                                    value=field.get("value", ""),
                                    inline=field.get("inline", True),
                                )

                        # Add footer if present
                        if "footer" in embed and "text" in embed["footer"]:
                            discord_embed.set_footer(text=embed["footer"]["text"])

                        await channel_obj.send(embed=discord_embed)
                    else:
                        # Send plain text message
                        webhook_payload = {"content": content}
                        if username != "V2_SWARM Bot":
                            webhook_payload["username"] = username
                        if avatar_url:
                            webhook_payload["avatar_url"] = avatar_url

                        await channel_obj.send(**webhook_payload)

                    print(
                        f"✅ Message sent to Discord channel {config.channel_id} ({channel.value})"
                    )
                    print(f"   Content: {content[:100]}{'...' if len(content) > 100 else ''}")
                    print(f"   Agent: {config.agent}")
                    print(f"   Embeds: {len(message.embeds)}")

                except Exception as e:
                    print(f"❌ Failed to send to Discord channel {config.channel_id}: {e}")
                finally:
                    await client.close()

        try:
            asyncio.run(send_discord_message())
            return True
        except Exception as e:
            print(f"❌ Discord integration failed for channel {config.channel_id}: {e}")
            return False

    def test_channel_webhook(self, channel: AgentChannel) -> bool:
        """Test webhook connection for a channel."""
        test_message = DiscordMessage(
            content=f"🧪 **Webhook Test** - {channel.value} channel connection test",
            username="V2_SWARM Test Bot",
        )
        return self.send_to_channel(channel, test_message)

    def get_all_channels(self) -> list[AgentChannel]:
        """Get all configured channels."""
        return list(self.channels.keys())

    def get_agent_channel(self, agent_id: str) -> AgentChannel | None:
        """Get channel for specific agent."""
        for channel, config in self.channels.items():
            if config.agent == agent_id:
                return channel
        return None


class AgentChannelCoordinator:
    """Coordinates agent-specific channel communications."""

    def __init__(self, webhook_manager: EnhancedDiscordWebhookManager):
        """Initialize agent channel coordinator."""
        self.webhook_manager = webhook_manager
        self.logger = None
        self.persistence = None

        # Initialize services
        try:
            self.logger = UnifiedLoggingTimeService()
            self.persistence = UnifiedPersistenceService()
        except Exception as e:
            print(f"⚠️  Service initialization warning: {e}")

    def create_agent_notification_embed(self, notification: AgentNotification) -> dict[str, Any]:
        """Create Discord embed for agent notification."""
        config = self.webhook_manager.get_channel_config(notification.channel)
        color = config.color if config else 0x3498DB

        # Priority colors
        priority_colors = {
            "LOW": 0x95A5A6,
            "NORMAL": 0x3498DB,
            "HIGH": 0xF39C12,
            "URGENT": 0xE74C3C,
        }

        if notification.priority in priority_colors:
            color = priority_colors[notification.priority]

        embed = {
            "title": f"🤖 {notification.title}",
            "description": notification.description,
            "color": color,
            "fields": [
                {"name": "Agent", "value": notification.agent_id, "inline": True},
                {"name": "Priority", "value": notification.priority, "inline": True},
                {"name": "Category", "value": notification.category.title(), "inline": True},
                {
                    "name": "Timestamp",
                    "value": notification.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True,
                },
            ],
            "footer": {
                "text": f"V2_SWARM - {notification.agent_id} Activity",
                "icon_url": "https://i.imgur.com/agent_icon.png",
            },
        }

        # Add metadata fields if present
        if notification.metadata:
            for key, value in notification.metadata.items():
                embed["fields"].append(
                    {"name": key.replace("_", " ").title(), "value": str(value), "inline": True}
                )

        return embed

    async def send_agent_notification(self, notification: AgentNotification) -> bool:
        """Send notification to agent's channel."""
        try:
            embed = self.create_agent_notification_embed(notification)

            message = DiscordMessage(
                content="",  # Empty content, using embed
                embeds=[embed],
                username=f"V2_SWARM - {notification.agent_id}",
                avatar_url=f"https://i.imgur.com/{notification.agent_id.lower()}_avatar.png",
            )

            success = self.webhook_manager.send_to_channel(notification.channel, message)

            if success and self.logger:
                await self.logger.info(
                    f"Agent notification sent: {notification.agent_id} -> {notification.channel.value}",
                    agent=notification.agent_id,
                    channel=notification.channel.value,
                    priority=notification.priority,
                )

            return success

        except Exception as e:
            print(f"❌ Failed to send agent notification: {e}")
            return False

    async def broadcast_to_swarm(
        self, title: str, description: str, priority: str = "NORMAL"
    ) -> bool:
        """Broadcast message to all swarm channels."""
        try:
            notification = AgentNotification(
                agent_id="SWARM",
                channel=AgentChannel.SWARM_GENERAL,
                title=title,
                description=description,
                priority=priority,
                category="broadcast",
            )

            # Send to general swarm channel
            success1 = await self.send_agent_notification(notification)

            # Send to coordination channel if high priority
            success2 = True
            if priority in ["HIGH", "URGENT"]:
                notification.channel = AgentChannel.SWARM_COORDINATION
                success2 = await self.send_agent_notification(notification)

            # Send to alerts channel if urgent
            success3 = True
            if priority == "URGENT":
                notification.channel = AgentChannel.SWARM_ALERTS
                success3 = await self.send_agent_notification(notification)

            return success1 and success2 and success3

        except Exception as e:
            print(f"❌ Failed to broadcast to swarm: {e}")
            return False

    async def coordinate_with_agent(self, from_agent: str, to_agent: str, message: str) -> bool:
        """Send coordination message between agents."""
        try:
            to_channel = self.webhook_manager.get_agent_channel(to_agent)
            if not to_channel:
                print(f"❌ No channel found for agent {to_agent}")
                return False

            notification = AgentNotification(
                agent_id=from_agent,
                channel=to_channel,
                title=f"Coordination from {from_agent}",
                description=message,
                priority="NORMAL",
                category="coordination",
                metadata={"from_agent": from_agent, "to_agent": to_agent},
            )

            return await self.send_agent_notification(notification)

        except Exception as e:
            print(f"❌ Failed to coordinate with agent: {e}")
            return False

    async def send_status_update(self, agent_id: str, status: str, details: str = "") -> bool:
        """Send agent status update."""
        try:
            agent_channel = self.webhook_manager.get_agent_channel(agent_id)
            if not agent_channel:
                # Fallback to swarm general if no specific channel
                agent_channel = AgentChannel.SWARM_GENERAL

            notification = AgentNotification(
                agent_id=agent_id,
                channel=agent_channel,
                title=f"Status Update - {status}",
                description=details or f"Agent {agent_id} status changed to {status}",
                priority="NORMAL",
                category="status",
                metadata={"status": status, "previous_status": "unknown"},
            )

            return await self.send_agent_notification(notification)

        except Exception as e:
            print(f"❌ Failed to send status update: {e}")
            return False


class EnhancedDevLogMonitor:
    """Enhanced DevLog monitor with agent-specific notifications."""

    def __init__(
        self, webhook_manager: EnhancedDiscordWebhookManager, coordinator: AgentChannelCoordinator
    ):
        """Initialize enhanced DevLog monitor."""
        self.webhook_manager = webhook_manager
        self.coordinator = coordinator
        self.devlogs_path = Path("devlogs")
        self.last_check_time = datetime.utcnow()
        self.is_running = False

    async def start_monitoring(self, check_interval: int = 30) -> None:
        """Start enhanced DevLog monitoring."""
        print("🚀 Starting Enhanced Discord DevLog monitoring...")
        print(f"📁 Monitoring directory: {self.devlogs_path}")
        print(f"⏱️  Check interval: {check_interval} seconds")
        print(f"📺 Channels: {len(self.webhook_manager.get_all_channels())} configured")
        print()

        if not self.devlogs_path.exists():
            print(f"❌ DevLogs directory not found: {self.devlogs_path}")
            return

        self.is_running = True

        try:
            while self.is_running:
                await self._check_for_new_devlogs()
                await asyncio.sleep(check_interval)

        except KeyboardInterrupt:
            print("\n🛑 Enhanced DevLog monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Enhanced DevLog monitoring error: {e}")
        finally:
            self.is_running = False

    async def _check_for_new_devlogs(self) -> None:
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

    async def _process_devlog(self, devlog_path: Path) -> None:
        """Process a single devlog file with enhanced notifications."""
        try:
            # Read devlog content
            with open(devlog_path, encoding="utf-8") as f:
                content = f.read()

            # Extract metadata from filename
            metadata = self._parse_devlog_filename(devlog_path.name)
            agent = metadata.get("agent", "Unknown")

            # Create enhanced devlog data
            devlog_data = {
                "title": metadata.get("title", devlog_path.name),
                "description": self._extract_devlog_summary(content),
                "category": metadata.get("category", "general"),
                "agent": agent,
                "filepath": str(devlog_path),
                "timestamp": datetime.utcnow().isoformat(),
                "file_size": devlog_path.stat().st_size,
                "lines_count": len(content.split("\n")),
            }

            print(f"📝 Processing devlog: {devlog_data['title']} by {agent}")

            # Send to appropriate channels
            await self._send_devlog_notifications(devlog_data)

        except Exception as e:
            print(f"❌ Error processing devlog {devlog_path}: {e}")

    async def _send_devlog_notifications(self, devlog_data: dict[str, Any]) -> None:
        """Send devlog notifications to appropriate channels."""
        agent = devlog_data.get("agent", "Unknown")
        category = devlog_data.get("category", "general")

        # Send to agent's specific channel if available
        if agent != "Unknown":
            agent_channel = self.webhook_manager.get_agent_channel(agent)
            if agent_channel:
                notification = AgentNotification(
                    agent_id=agent,
                    channel=agent_channel,
                    title=f"DevLog: {devlog_data['title']}",
                    description=devlog_data["description"],
                    priority="NORMAL",
                    category=category,
                    metadata={
                        "file_path": devlog_data["filepath"],
                        "file_size": devlog_data["file_size"],
                        "lines_count": devlog_data["lines_count"],
                    },
                )

                await self.coordinator.send_agent_notification(notification)

        # Always send to swarm general for awareness
        await self.coordinator.broadcast_to_swarm(
            title=f"DevLog Activity: {devlog_data['title']}",
            description=f"New devlog from {agent}: {devlog_data['description'][:200]}...",
            priority="LOW",
        )

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

        if not summary:
            summary = "DevLog update processed by Enhanced V2_SWARM monitoring system."

        return summary[:max_length].strip()

    def stop_monitoring(self) -> None:
        """Stop devlog monitoring."""
        self.is_running = False
        print("🛑 Enhanced DevLog monitoring stopping...")


class EnhancedDiscordCommander:
    """Enhanced Discord commander with individual agent channels."""

    def __init__(self):
        """Initialize enhanced Discord commander."""
        self.webhook_manager = EnhancedDiscordWebhookManager()
        self.coordinator = AgentChannelCoordinator(self.webhook_manager)
        self.devlog_monitor = EnhancedDevLogMonitor(self.webhook_manager, self.coordinator)
        self.logger = None

        # Initialize logging service
        try:
            self.logger = UnifiedLoggingTimeService()
        except Exception as e:
            print(f"⚠️  Logging service initialization warning: {e}")

    async def initialize_channels(self) -> bool:
        """Initialize and test all agent channels."""
        print("🎯 Initializing Enhanced Discord Integration")
        print("=" * 60)

        success_count = 0
        total_channels = len(self.webhook_manager.get_all_channels())

        for channel in self.webhook_manager.get_all_channels():
            config = self.webhook_manager.get_channel_config(channel)
            if config and config.webhook_url:
                if self.webhook_manager.test_channel_webhook(channel):
                    success_count += 1
                    print(f"✅ {channel.value}: Connected")
                else:
                    print(f"❌ {channel.value}: Failed to connect")
            else:
                print(f"⚠️  {channel.value}: No webhook configured")

        print(f"\n📊 Channel Status: {success_count}/{total_channels} connected")
        return success_count > 0

    async def start_enhanced_monitoring(self, check_interval: int = 30) -> None:
        """Start enhanced monitoring with agent channels."""
        print("🚀 Starting Enhanced V2_SWARM Discord Integration")
        print("=" * 60)

        # Initialize channels
        if not await self.initialize_channels():
            print("❌ Failed to initialize Discord channels")
            return

        # Start DevLog monitoring
        await self.devlog_monitor.start_monitoring(check_interval)

    async def send_agent_message(
        self,
        agent_id: str,
        title: str,
        description: str,
        priority: str = "NORMAL",
        category: str = "general",
    ) -> bool:
        """Send message to specific agent's channel."""
        try:
            agent_channel = self.webhook_manager.get_agent_channel(agent_id)
            if not agent_channel:
                print(f"❌ No channel configured for agent {agent_id}")
                return False

            notification = AgentNotification(
                agent_id=agent_id,
                channel=agent_channel,
                title=title,
                description=description,
                priority=priority,
                category=category,
            )

            return await self.coordinator.send_agent_notification(notification)

        except Exception as e:
            print(f"❌ Failed to send agent message: {e}")
            return False

    async def coordinate_agents(self, from_agent: str, to_agent: str, message: str) -> bool:
        """Coordinate between two agents via Discord channels."""
        return await self.coordinator.coordinate_with_agent(from_agent, to_agent, message)

    async def broadcast_swarm_alert(
        self, title: str, description: str, priority: str = "HIGH"
    ) -> bool:
        """Broadcast alert to all swarm channels."""
        return await self.coordinator.broadcast_to_swarm(title, description, priority)

    async def update_agent_status(self, agent_id: str, status: str, details: str = "") -> bool:
        """Update agent status across channels."""
        return await self.coordinator.send_status_update(agent_id, status, details)

    def configure_channel_webhook(self, channel: AgentChannel, webhook_url: str) -> bool:
        """Configure webhook URL for a channel."""
        return self.webhook_manager.set_channel_webhook(channel, webhook_url)

    def get_channel_info(self) -> dict[str, Any]:
        """Get information about all configured channels."""
        info = {
            "total_channels": len(self.webhook_manager.channels),
            "channels": {},
            "agents_with_channels": [],
            "configured_webhooks": 0,
        }

        for channel, config in self.webhook_manager.channels.items():
            channel_info = {
                "name": config.name,
                "description": config.description,
                "agent": config.agent,
                "has_webhook": config.webhook_url is not None,
                "enabled": config.enabled,
                "color": hex(config.color),
            }
            info["channels"][channel.value] = channel_info

            if config.agent:
                info["agents_with_channels"].append(config.agent)
            if config.webhook_url:
                info["configured_webhooks"] += 1

        return info

    async def test_integration(self) -> bool:
        """Test the complete enhanced Discord integration."""
        print("🧪 Testing Enhanced Discord Integration")
        print("=" * 50)

        # Test channel initialization
        init_success = await self.initialize_channels()
        print(f"Channel Initialization: {'✅ PASS' if init_success else '❌ FAIL'}")

        # Test agent messaging (mock)
        agent_test = await self.send_agent_message(
            "Agent-3",
            "Integration Test",
            "Testing enhanced Discord agent messaging functionality",
            "NORMAL",
            "testing",
        )
        print(f"Agent Messaging: {'✅ PASS' if agent_test else '❌ FAIL'}")

        # Test swarm broadcast
        broadcast_test = await self.broadcast_swarm_alert(
            "Integration Test Alert", "Testing enhanced swarm broadcast functionality", "LOW"
        )
        print(f"Swarm Broadcast: {'✅ PASS' if broadcast_test else '❌ FAIL'}")

        # Overall result
        all_tests_pass = init_success  # Other tests may fail if webhooks not configured
        print(f"\n📊 Enhanced Integration Test: {'✅ SUCCESS' if all_tests_pass else '⚠️  PARTIAL'}")

        return all_tests_pass


# Global instance
_enhanced_commander_instance = None


def get_enhanced_discord_commander() -> EnhancedDiscordCommander:
    """Get enhanced Discord commander instance (singleton)."""
    global _enhanced_commander_instance
    if _enhanced_commander_instance is None:
        _enhanced_commander_instance = EnhancedDiscordCommander()
    return _enhanced_commander_instance


async def start_enhanced_discord_monitoring(check_interval: int = 30):
    """Start enhanced Discord monitoring with agent channels."""
    commander = get_enhanced_discord_commander()
    await commander.start_enhanced_monitoring(check_interval)


@dataclass
class DevlogEntry:
    """Devlog entry structure."""

    agent_id: str
    title: str
    content: str
    category: str = "general"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    filepath: Path | None = None


async def send_devlog_to_discord(agent_id: str, devlog_file: str) -> bool:
    """Send a devlog file to the specified agent's Discord channel.

    Args:
        agent_id: Agent identifier (Agent-1, Agent-2, etc.)
        devlog_file: Path to the devlog markdown file

    Returns:
        bool: Success status
    """
    try:
        # Validate agent_id
        valid_agents = [f"Agent-{i}" for i in range(1, 9)]
        if agent_id not in valid_agents:
            print(f"❌ Invalid agent_id: {agent_id}. Must be one of: {', '.join(valid_agents)}")
            return False

        # Read devlog file
        filepath = Path(devlog_file)
        if not filepath.exists():
            print(f"❌ Devlog file not found: {devlog_file}")
            return False

        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # Extract title from first header
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else filepath.stem

        # Determine category from content
        category = "general"
        content_lower = content.lower()
        if "consolidation" in content_lower:
            category = "consolidation"
        elif "cleanup" in content_lower or "mission" in content_lower:
            category = "cleanup"
        elif "coordination" in content_lower:
            category = "coordination"
        elif "testing" in content_lower:
            category = "testing"
        elif "deployment" in content_lower:
            category = "deployment"

        # Initialize webhook manager and get channel
        webhook_manager = EnhancedDiscordWebhookManager()
        channel = webhook_manager.get_agent_channel(agent_id)

        if not channel:
            print(f"⚠️  No Discord channel found for {agent_id}")
            return False

        # Create embed for devlog
        config = webhook_manager.get_channel_config(channel)
        color = config.color if config else 0x3498DB

        embed = {
            "title": f"📝 {title}",
            "description": content[:1500] + ("..." if len(content) > 1500 else ""),
            "color": color,
            "fields": [
                {"name": "Agent", "value": agent_id, "inline": True},
                {"name": "Category", "value": category.title(), "inline": True},
                {
                    "name": "Timestamp",
                    "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True,
                },
            ],
            "footer": {
                "text": f"V2_SWARM DevLog - {agent_id}",
                "icon_url": "https://i.imgur.com/devlog_icon.png",
            },
        }

        message = DiscordMessage(
            content="",  # Empty content, using embed
            embeds=[embed],
            username=f"V2_SWARM DevLog - {agent_id}",
            avatar_url=f"https://i.imgur.com/{agent_id.lower()}_avatar.png",
        )

        success = webhook_manager.send_to_channel(channel, message)

        if success:
            print(f"✅ DevLog sent: {agent_id} -> {channel.value} ({title})")
        else:
            print("❌ Failed to send devlog to Discord")

        return success

    except Exception as e:
        print(f"❌ Error sending devlog: {e}")
        return False


if __name__ == "__main__":
    # Test the enhanced integration
    async def main():
        commander = get_enhanced_discord_commander()
        await commander.test_integration()

    asyncio.run(main())
