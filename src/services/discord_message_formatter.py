#!/usr/bin/env python3
"""
Discord Devlog Service - Message Formatter
==========================================

Handles message formatting and spam prevention for Discord devlogs.
V2 Compliant: ≤400 lines, focused message formatting.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import logging
import re
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class DiscordMessageFormatter:
    """Handles message formatting and spam prevention."""

    def __init__(self):
        """Initialize message formatter."""
        self.spam_patterns = [
            r"🎯 QUALITY GATES REMINDER",
            r"📝 DISCORD DEVLOG REMINDER",
            r"============================================================",
            r"\[A2A\] MESSAGE",
            r"📤 FROM:",
            r"📥 TO:",
            r"Priority:",
            r"Tags:",
        ]
        self.last_messages = {}  # Track last messages per agent
        self.spam_threshold = 3  # Max identical messages

    def format_message(self, content: str, agent_id: Optional[str] = None) -> Optional[str]:
        """Format message for Discord with spam prevention."""
        try:
            # Check for spam patterns
            if self._is_spam(content, agent_id):
                logger.info(f"Spam detected for {agent_id}, suppressing message")
                return None

            # Format the message
            formatted = self._format_content(content, agent_id)
            
            # Track message for spam prevention
            if agent_id:
                self._track_message(agent_id, content)

            return formatted

        except Exception as e:
            logger.error(f"Failed to format message: {e}")
            return None

    def _is_spam(self, content: str, agent_id: Optional[str] = None) -> bool:
        """Check if content contains spam patterns."""
        try:
            # Check for spam patterns
            for pattern in self.spam_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    logger.info(f"Spam pattern detected: {pattern}")
                    return True

            # Check for duplicate messages
            if agent_id and agent_id in self.last_messages:
                last_content = self.last_messages[agent_id].get("content", "")
                if content.strip() == last_content.strip():
                    count = self.last_messages[agent_id].get("count", 0)
                    if count >= self.spam_threshold:
                        logger.info(f"Duplicate message spam detected for {agent_id}")
                        return True

            return False

        except Exception as e:
            logger.error(f"Error checking spam: {e}")
            return False

    def _format_content(self, content: str, agent_id: Optional[str] = None) -> str:
        """Format content for Discord."""
        try:
            # Clean up excessive formatting
            formatted = content
            
            # Remove excessive separator lines
            formatted = re.sub(r'={50,}', '=' * 20, formatted)
            formatted = re.sub(r'-{50,}', '-' * 20, formatted)
            
            # Clean up excessive emojis
            formatted = re.sub(r'🎯.*?REMINDER.*?🎯', '🎯 REMINDER', formatted)
            formatted = re.sub(r'📝.*?REMINDER.*?📝', '📝 REMINDER', formatted)
            
            # Add agent identifier if provided
            if agent_id:
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted = f"**{agent_id}** [{timestamp}]\n{formatted}"
            
            # Ensure message is not too long for Discord
            if len(formatted) > 2000:
                formatted = formatted[:1900] + "\n... (truncated)"
            
            return formatted

        except Exception as e:
            logger.error(f"Error formatting content: {e}")
            return content

    def _track_message(self, agent_id: str, content: str) -> None:
        """Track message for spam prevention."""
        try:
            if agent_id not in self.last_messages:
                self.last_messages[agent_id] = {"content": content, "count": 1}
            else:
                if self.last_messages[agent_id]["content"] == content:
                    self.last_messages[agent_id]["count"] += 1
                else:
                    self.last_messages[agent_id] = {"content": content, "count": 1}

        except Exception as e:
            logger.error(f"Error tracking message: {e}")

    def create_embed_message(self, title: str, description: str, agent_id: Optional[str] = None) -> dict:
        """Create Discord embed message."""
        try:
            embed = {
                "title": title,
                "description": description,
                "color": 0x00ff00,  # Green color
                "timestamp": datetime.now().isoformat(),
                "footer": {
                    "text": f"Agent Cellphone V2 - {agent_id or 'System'}"
                }
            }

            if agent_id:
                embed["author"] = {
                    "name": agent_id,
                    "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png"
                }

            return embed

        except Exception as e:
            logger.error(f"Error creating embed: {e}")
            return {"title": title, "description": description}

    def create_status_message(self, status: str, details: str, agent_id: Optional[str] = None) -> str:
        """Create status message."""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            emoji = "✅" if status.lower() == "success" else "❌" if status.lower() == "error" else "ℹ️"
            
            message = f"{emoji} **{status.upper()}** [{timestamp}]"
            if agent_id:
                message = f"**{agent_id}** {message}"
            
            message += f"\n{details}"
            
            return message

        except Exception as e:
            logger.error(f"Error creating status message: {e}")
            return f"{status}: {details}"

    def create_progress_message(self, task: str, progress: int, total: int, agent_id: Optional[str] = None) -> str:
        """Create progress message."""
        try:
            percentage = (progress / total) * 100 if total > 0 else 0
            bar_length = 20
            filled_length = int(bar_length * progress // total) if total > 0 else 0
            
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            
            message = f"📊 **{task}**\n"
            message += f"Progress: {progress}/{total} ({percentage:.1f}%)\n"
            message += f"`{bar}`"
            
            if agent_id:
                message = f"**{agent_id}** {message}"
            
            return message

        except Exception as e:
            logger.error(f"Error creating progress message: {e}")
            return f"{task}: {progress}/{total}"


def create_message_formatter() -> DiscordMessageFormatter:
    """Create message formatter."""
    return DiscordMessageFormatter()

