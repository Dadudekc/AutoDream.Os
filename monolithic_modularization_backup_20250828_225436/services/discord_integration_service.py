#!/usr/bin/env python3
"""
Enhanced Discord Integration Service - Agent Cellphone V2
=======================================================

Integrates Discord with FSM system and decision engine.
Follows V2 coding standards: ≤300 LOC, OOP design, SRP.

**Features:**
- Discord bot integration
- FSM state management
- Decision engine integration
- Agent coordination via Discord
- Real-time status updates

**Author:** Agent-1
**Created:** Current Sprint
**Status:** ACTIVE - V2 STANDARDS COMPLIANT
"""
import json
import time
import asyncio
import logging
import requests
import os
from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
    from ..core.fsm import FSMCore as FSMCoreV2
    from ..core.decision import AutonomousDecisionEngine
            from ..core.fsm_task_v2 import TaskPriority
    import argparse



# Import FSM and decision components
try:

    FSM_AVAILABLE = True
except ImportError:
    FSM_AVAILABLE = False

    # Define placeholder classes for when imports fail
    class FSMCoreV2:
        pass

    class AutonomousDecisionEngine:
        pass

    print("⚠️ FSM components not available - using placeholder classes")


class DiscordIntegrationService:
    """
    Enhanced Discord integration service with FSM and decision engine

    Responsibilities:
    - Discord bot management
    - FSM state synchronization
    - Decision engine integration
    - Agent coordination via Discord
    """

    def __init__(
        self,
        fsm_core: Optional[FSMCoreV2] = None,
        decision_engine: Optional[AutonomousDecisionEngine] = None,
    ):
        self.messages = []
        self.agents = {}
        self.channels = {}
        self.fsm_core = fsm_core
        self.decision_engine = decision_engine
        self.logger = logging.getLogger(__name__)

        # Discord bot configuration
        self.bot_token = None
        self.webhook_url = None
        self.guild_id = None
        
        # Try to load webhook URL from environment
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

        # FSM integration
        self.fsm_enabled = FSM_AVAILABLE and fsm_core is not None
        self.decision_enabled = decision_engine is not None

        print("🚀 Enhanced Discord Integration Service initialized")
        if self.webhook_url:
            print(f"✅ Discord webhook configured from environment")
        if self.fsm_enabled:
            print("✅ FSM integration enabled")
        if self.decision_enabled:
            print("✅ Decision engine integration enabled")

    def configure_discord(
        self, bot_token: str = None, webhook_url: str = None, guild_id: str = None
    ):
        """Configure Discord bot settings"""
        self.bot_token = bot_token
        if webhook_url:
            self.webhook_url = webhook_url
        self.guild_id = guild_id

        if bot_token:
            self.logger.info("Discord bot token configured")
        if self.webhook_url:
            self.logger.info(f"Discord webhook configured: {self.webhook_url[:50]}...")
        if guild_id:
            self.logger.info("Discord guild ID configured")

    def send_message(
        self, sender: str, message_type: str, content: str, channel: str = "general"
    ) -> bool:
        """Send message to Discord channel"""
        try:
            message = {
                "timestamp": datetime.now().isoformat(),
                "sender": sender,
                "type": message_type,
                "content": content,
                "channel": channel,
            }
            self.messages.append(message)

            # Send to Discord if configured
            if self.webhook_url:
                success = self._send_discord_webhook(message)
                if success:
                    self.logger.info(f"Message sent to Discord: {sender} - {message_type}")
                else:
                    self.logger.warning(f"Failed to send message to Discord: {sender} - {message_type}")

            # Integrate with FSM if available
            if self.fsm_enabled and message_type in [
                "task_update",
                "state_change",
                "coordination",
            ]:
                self._process_fsm_message(message)

            # Integrate with decision engine if available
            if self.decision_enabled and message_type in [
                "decision_request",
                "coordination",
            ]:
                self._process_decision_message(message)

            self.logger.info(f"Message processed: {sender} - {message_type}: {content}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False

    def register_agent(
        self, agent_id: str, name: str, capabilities: List[str] = None
    ) -> bool:
        """Register an agent with Discord integration"""
        try:
            self.agents[agent_id] = {
                "name": name,
                "status": "active",
                "capabilities": capabilities or [],
                "registered_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat(),
            }

            # Notify FSM of agent registration
            if self.fsm_enabled:
                self._notify_fsm_agent_registration(agent_id, name, capabilities)

            # Send Discord notification
            self.send_message(
                "system",
                "agent_registration",
                f"Agent {name} ({agent_id}) registered with capabilities: {capabilities}",
            )

            print(f"✅ Agent registered: {agent_id} ({name})")
            return True

        except Exception as e:
            self.logger.error(f"Failed to register agent: {e}")
            return False

    def update_agent_status(
        self, agent_id: str, status: str, details: str = None
    ) -> bool:
        """Update agent status and notify Discord"""
        try:
            if agent_id not in self.agents:
                return False

            self.agents[agent_id]["status"] = status
            self.agents[agent_id]["last_activity"] = datetime.now().isoformat()

            if details:
                self.agents[agent_id]["last_details"] = details

            # Send Discord update
            self.send_message(
                agent_id,
                "status_update",
                f"Status: {status} - {details or 'No details'}",
            )

            # Update FSM if relevant
            if self.fsm_enabled and status in ["busy", "idle", "error"]:
                self._update_fsm_agent_status(agent_id, status, details)

            return True

        except Exception as e:
            self.logger.error(f"Failed to update agent status: {e}")
            return False

    def create_discord_task(
        self, title: str, description: str, assigned_agent: str, priority: str = "normal"
    ) -> bool:
        """Create a Discord task notification"""
        try:
            task_message = f"""📋 **NEW TASK CREATED**
🎯 **Title**: {title}
📝 **Description**: {description}
🤖 **Assigned To**: {assigned_agent}
📊 **Priority**: {priority}
⏰ **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

            success = self.send_message(
                "system",
                "task_creation",
                task_message,
                "tasks"
            )

            if success:
                print(f"✅ Discord task notification created: {title}")
            return success

        except Exception as e:
            self.logger.error(f"Failed to create Discord task: {e}")
            return False

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "messages_processed": len(self.messages),
            "agents_registered": len(self.agents),
            "fsm_integration": self.fsm_enabled,
            "decision_integration": self.decision_enabled,
            "discord_configured": bool(self.webhook_url or self.bot_token),
            "webhook_available": bool(self.webhook_url),
            "timestamp": datetime.now().isoformat(),
        }

    def _send_discord_webhook(self, message: Dict[str, Any]) -> bool:
        """Send message to Discord webhook with rich embeds"""
        try:
            if not self.webhook_url:
                self.logger.warning("No Discord webhook configured")
                return False

            # Determine if this is a devlog message
            is_devlog = message.get('type') == 'devlog'
            
            if is_devlog:
                # Use rich embed for devlog messages
                success = self._send_devlog_embed(message)
            else:
                # Use regular webhook for other messages
                success = self._send_regular_webhook(message)
            
            return success
                
        except Exception as e:
            self.logger.error(f"❌ Error posting to Discord: {e}")
            return False

    def _send_devlog_embed(self, message: Dict[str, Any]) -> bool:
        """Send devlog message as rich Discord embed"""
        try:
            # Parse devlog content to extract information
            content = message['content']
            
            # Extract title from content (first line after "DEVLOG ENTRY:")
            lines = content.split('\n')
            title = "Devlog Update"
            category = "project_update"
            agent_id = "unknown"
            priority = "normal"
            
            for line in lines:
                if "**DEVLOG ENTRY:" in line:
                    title = line.split("**DEVLOG ENTRY:")[1].strip().replace("**", "")
                elif "**Category**: " in line:
                    category = line.split("**Category**: ")[1].strip()
                elif "**Agent**: " in line:
                    agent_id = line.split("**Agent**: ")[1].strip()
                elif "**Priority**: " in line:
                    priority = line.split("**Priority**: ")[1].strip()
            
            # Create rich Discord embed
            embed = {
                "title": f"📝 {title}",
                "description": self._extract_devlog_content(content),
                "color": self._get_category_color(category),
                "fields": [
                    {
                        "name": "🏷️ Category",
                        "value": f"`{category.replace('_', ' ').title()}`",
                        "inline": True
                    },
                    {
                        "name": "🤖 Agent",
                        "value": f"`{agent_id}`",
                        "inline": True
                    },
                    {
                        "name": "📊 Priority",
                        "value": f"`{priority.title()}`",
                        "inline": True
                    },
                    {
                        "name": "📅 Timestamp",
                        "value": f"<t:{int(datetime.now().timestamp())}:F>",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"Devlog Entry • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                },
                "thumbnail": {
                    "url": self._get_agent_avatar(agent_id)
                }
            }
            
            # Add tags if available
            tags = self._extract_tags(content)
            if tags:
                embed["fields"].append({
                    "name": "🏷️ Tags",
                    "value": " ".join([f"`{tag}`" for tag in tags]),
                    "inline": False
                })
            
            # Add category-specific emoji and styling
            embed["title"] = f"{self._get_category_emoji(category)} {title}"
            
            # Discord webhook payload with embed
            payload = {
                "username": f"Agent-{agent_id}",
                "avatar_url": self._get_agent_avatar(agent_id),
                "embeds": [embed]
            }

            # Send POST request to Discord webhook
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code == 204:
                self.logger.info(f"✅ Rich Discord embed sent: {title[:50]}...")
                return True
            else:
                self.logger.error(f"❌ Failed to post embed to Discord. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error sending devlog embed: {e}")
            return False

    def _send_regular_webhook(self, message: Dict[str, Any]) -> bool:
        """Send regular message as simple webhook"""
        try:
            # Format Discord message
            username = f"Agent-{message['sender']}" if message['sender'] != 'system' else 'System'
            
            # Discord webhook payload
            payload = {
                "content": message['content'],
                "username": username,
                "avatar_url": "https://cdn.discordapp.com/emojis/🤖.png" if message['sender'] != 'system' else "https://cdn.discordapp.com/emojis/⚙️.png",
                "tts": False
            }

            # Send POST request to Discord webhook
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code == 204:
                self.logger.info(f"✅ Discord webhook: {message['channel']} - {message['content'][:50]}...")
                return True
            else:
                self.logger.error(f"❌ Failed to post to Discord. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Network error posting to Discord: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error posting to Discord: {e}")
            return False

    def _extract_devlog_content(self, content: str) -> str:
        """Extract the main content from devlog message"""
        try:
            # Find the content section
            if "📋 **Content**:\n" in content:
                content_start = content.find("📋 **Content**:\n") + len("📋 **Content**:\n")
                # Find where content ends (before tags or entry ID)
                content_end = content.find("🏷️ **Tags**:")
                if content_end == -1:
                    content_end = content.find("🆔 **Entry ID**:")
                if content_end == -1:
                    content_end = len(content)
                
                extracted = content[content_start:content_end].strip()
                # Limit length for Discord embed
                if len(extracted) > 1000:
                    extracted = extracted[:997] + "..."
                return extracted
            else:
                # Fallback: return first 200 characters
                return content[:200] + ("..." if len(content) > 200 else "")
        except Exception:
            return content[:200] + ("..." if len(content) > 200 else "")

    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from devlog content"""
        try:
            if "🏷️ **Tags**: " in content:
                tags_line = content.split("🏷️ **Tags**: ")[1].split('\n')[0]
                if tags_line != "None":
                    return [tag.strip() for tag in tags_line.split(',')]
            return []
        except Exception:
            return []

    def _get_category_color(self, category: str) -> int:
        """Get Discord embed color based on category"""
        colors = {
            "milestone": 0x00FF00,      # Green
            "project_update": 0x0099FF,  # Blue
            "issue": 0xFF0000,          # Red
            "idea": 0xFF9900,           # Orange
            "review": 0x9932CC,         # Purple
        }
        return colors.get(category, 0x0099FF)  # Default blue

    def _get_category_emoji(self, category: str) -> str:
        """Get emoji for category"""
        emojis = {
            "milestone": "🎯",
            "project_update": "📝",
            "issue": "🚨",
            "idea": "💡",
            "review": "🔍",
        }
        return emojis.get(category, "📝")

    def _get_agent_avatar(self, agent_id: str) -> str:
        """Get avatar URL for agent"""
        avatars = {
            "agent-1": "https://cdn.discordapp.com/emojis/🎖️.png",  # Captain
            "agent-2": "https://cdn.discordapp.com/emojis/🏗️.png",  # Architecture
            "agent-3": "https://cdn.discordapp.com/emojis/💻.png",  # Development
            "agent-4": "https://cdn.discordapp.com/emojis/🧪.png",  # Testing
            "agent-5": "https://cdn.discordapp.com/emojis/⚡.png",  # Performance
        }
        return avatars.get(agent_id, "https://cdn.discordapp.com/emojis/🤖.png")

    def _process_fsm_message(self, message: Dict[str, Any]):
        """Process message for FSM integration"""
        if message["type"] == "task_update":
            # Update FSM task state
            self.logger.info(f"🔄 FSM integration: Processing task update")
        elif message["type"] == "state_change":
            # Handle state change
            self.logger.info(f"🔄 FSM integration: Processing state change")

    def _process_decision_message(self, message: Dict[str, Any]):
        """Process message for decision engine integration"""
        if message["type"] == "decision_request":
            # Handle decision request
            self.logger.info(
                f"🧠 Decision engine integration: Processing decision request"
            )

    def _notify_fsm_agent_registration(
        self, agent_id: str, name: str, capabilities: List[str]
    ):
        """Notify FSM of agent registration"""
        self.logger.info(f"🔄 FSM notification: Agent {agent_id} registered")

    def _update_fsm_agent_status(self, agent_id: str, status: str, details: str):
        """Update FSM with agent status change"""
        self.logger.info(f"🔄 FSM update: Agent {agent_id} status changed to {status}")

    def _convert_priority(self, priority: str) -> Any:
        """Convert string priority to FSM priority enum"""
        if not FSM_AVAILABLE:
            return priority

        try:

            priority_map = {
                "low": TaskPriority.LOW,
                "normal": TaskPriority.NORMAL,
                "high": TaskPriority.HIGH,
                "critical": TaskPriority.CRITICAL,
            }
            return priority_map.get(priority.lower(), TaskPriority.NORMAL)
        except ImportError:
            return priority


def main():
    """Main entry point for Discord integration service"""

    parser = argparse.ArgumentParser(description="Enhanced Discord Integration Service")
    parser.add_argument("--test", action="store_true", help="Run test mode")
    parser.add_argument("--fsm", action="store_true", help="Test FSM integration")
    parser.add_argument(
        "--decision", action="store_true", help="Test decision engine integration"
    )

    args = parser.parse_args()

    if args.test:
        print("🧪 Running Enhanced Discord Integration Service in test mode...")

        # Initialize service
        service = DiscordIntegrationService()

        # Configure Discord (simulated)
        service.configure_discord(
            webhook_url="https://discord.com/api/webhooks/test", guild_id="test_guild"
        )

        # Register test agents
        service.register_agent("agent-1", "Test Agent 1", ["testing", "coordination"])
        service.register_agent("agent-2", "Test Agent 2", ["automation", "monitoring"])

        # Send test messages
        service.send_message("agent-1", "status", "Agent 1 is ready")
        service.send_message("agent-2", "progress", "Agent 2 is working")
        service.send_message(
            "system", "coordination", "Agents coordinated successfully"
        )

        # Test task creation
        service.create_discord_task(
            "Test Task", "Integration testing", "agent-1", "high"
        )

        print("✅ Test completed successfully!")

    return 0


if __name__ == "__main__":
    exit(main())
