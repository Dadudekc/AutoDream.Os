"""
Discord Devlog Publisher
Extracted from Auto_Blogger repository and adapted for agent devlog posting

Pattern Source: Auto_Blogger/autoblogger/services/publishing/discord_publisher.py
Extraction Date: 2025-10-15
Extracted By: Agent-8
Value: 500 points (automates manual Discord posting)
"""

import logging
import requests
from typing import Dict, Any, Optional
from datetime import datetime
from .base import DevlogPublisher


class DiscordDevlogPublisher(DevlogPublisher):
    """
    Discord webhook publisher for agent devlogs.
    
    Automates devlog posting to Discord channels via webhooks.
    Replaces manual copy-paste workflow with programmatic posting.
    """

    def __init__(self, webhook_url: str):
        """
        Initialize Discord devlog publisher.
        
        Args:
            webhook_url: Discord webhook URL for the devlog channel
        """
        self.webhook_url = webhook_url
        self._last_message_id = None
        self.logger = logging.getLogger(__name__)

    def publish_devlog(
        self, 
        agent_id: str,
        title: str,
        content: str,
        cycle: str = None,
        tags: list[str] = None,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """
        Publish agent devlog to Discord.
        
        Args:
            agent_id: Agent ID (e.g., "Agent-8")
            title: Devlog title
            content: Main devlog content
            cycle: Cycle identifier (e.g., "C-047")
            tags: List of hashtags
            metadata: Additional metadata (points, discoveries, etc.)
            
        Returns:
            bool: True if published successfully, False otherwise
        """
        try:
            # Format devlog for Discord
            formatted_content = self._format_devlog(
                agent_id=agent_id,
                title=title,
                content=content,
                cycle=cycle,
                tags=tags,
                metadata=metadata
            )
            
            # Build Discord webhook payload
            message = {
                "content": formatted_content,
                "username": f"{agent_id} Devlog",
                "embeds": []
            }
            
            # Add metadata as embed if provided
            if metadata:
                embed = self._create_metadata_embed(metadata)
                if embed:
                    message["embeds"].append(embed)
            
            # Post to Discord
            response = requests.post(self.webhook_url, json=message, timeout=10)
            
            if response.status_code == 204:  # Discord success
                self._last_message_id = response.headers.get("X-Webhook-Id")
                self.logger.info(f"✅ Devlog posted to Discord: {title}")
                return True
            
            self.logger.error(f"❌ Discord webhook failed: {response.status_code} - {response.text}")
            return False
            
        except requests.RequestException as e:
            self.logger.error(f"❌ Network error posting to Discord: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Failed to publish devlog: {e}")
            return False

    def _format_devlog(
        self,
        agent_id: str,
        title: str,
        content: str,
        cycle: str = None,
        tags: list[str] = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Format devlog content for Discord display."""
        parts = []
        
        # Header
        header = f"# 🚀 {title}"
        if cycle:
            header += f" | {cycle}"
        parts.append(header)
        
        # Agent attribution
        parts.append(f"**Agent:** {agent_id}")
        
        # Timestamp
        parts.append(f"**Posted:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Separator
        parts.append("---")
        
        # Main content
        parts.append(content)
        
        # Tags (if provided)
        if tags:
            parts.append("\n---")
            parts.append(" ".join([f"#{tag}" for tag in tags]))
        
        return "\n\n".join(parts)

    def _create_metadata_embed(self, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create Discord embed from metadata."""
        try:
            embed = {
                "title": "📊 Analysis Metrics",
                "color": 0x00FF00,  # Green
                "fields": []
            }
            
            # Add metadata fields
            if "value" in metadata:
                embed["fields"].append({
                    "name": "💎 Value Found",
                    "value": str(metadata["value"]),
                    "inline": True
                })
            
            if "jackpots" in metadata:
                embed["fields"].append({
                    "name": "🏆 JACKPOTS",
                    "value": str(metadata["jackpots"]),
                    "inline": True
                })
            
            if "roi_improvement" in metadata:
                embed["fields"].append({
                    "name": "📈 ROI Improvement",
                    "value": str(metadata["roi_improvement"]),
                    "inline": True
                })
            
            return embed if embed["fields"] else None
            
        except Exception as e:
            self.logger.warning(f"Failed to create metadata embed: {e}")
            return None

    def validate_webhook(self) -> bool:
        """
        Validate Discord webhook by sending test message.
        
        Returns:
            bool: True if webhook is valid, False otherwise
        """
        try:
            test_message = {
                "content": "✅ Discord webhook validation - connection OK!",
                "username": "Webhook Validator"
            }
            response = requests.post(self.webhook_url, json=test_message, timeout=10)
            return response.status_code == 204
            
        except Exception as e:
            self.logger.error(f"Discord webhook validation failed: {e}")
            return False

    def get_last_message_id(self) -> Optional[str]:
        """Get the ID of the last posted message."""
        return self._last_message_id


# Quick test function
def test_discord_publisher(webhook_url: str) -> bool:
    """
    Test Discord publisher with sample devlog.
    
    Args:
        webhook_url: Discord webhook URL to test
        
    Returns:
        bool: True if test successful
    """
    publisher = DiscordDevlogPublisher(webhook_url)
    
    # Validate webhook
    if not publisher.validate_webhook():
        print("❌ Webhook validation failed!")
        return False
    
    print("✅ Webhook validated!")
    
    # Test publish
    success = publisher.publish_devlog(
        agent_id="Agent-8",
        title="Test Devlog - Discord Publisher Extraction",
        content="Testing automated Discord posting from extracted Auto_Blogger pattern!",
        cycle="C-048",
        tags=["test", "extraction", "discord-publisher"],
        metadata={
            "value": "500 pts",
            "extraction_source": "Auto_Blogger",
            "status": "Testing"
        }
    )
    
    if success:
        print("✅ Test devlog posted successfully!")
    else:
        print("❌ Test devlog posting failed!")
    
    return success

