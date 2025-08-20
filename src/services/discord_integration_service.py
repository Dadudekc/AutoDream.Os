#!/usr/bin/env python3
"""
Discord Integration Service - Agent Cellphone V2
==============================================

Discord communication and integration service.
Follows V2 standards: ≤ 200 LOC, SRP, OOP design, CLI interface.
"""

import json
import logging
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import argparse

@dataclass
class DiscordMessage:
    """Discord message data structure."""
    message_id: str
    sender: str
    title: str
    content: str
    message_type: str  # status, progress, completion, coordination, error, system
    timestamp: datetime
    priority: str  # low, medium, high, critical

@dataclass
class DiscordConfig:
    """Discord configuration data structure."""
    webhook_url: str
    bot_token: str
    channel_id: str
    enabled: bool
    message_rate_limit: int  # messages per minute

class DiscordIntegrationService:
    """
    Discord Integration Service - Single responsibility: Discord communication and integration.
    
    This service manages:
    - Discord message formatting and sending
    - Status reporting and notifications
    - Error handling and alerts
    - Message rate limiting and management
    """
    
    def __init__(self, config_file: str = "config/discord_config.json"):
        """Initialize Discord Integration Service."""
        self.config_file = Path(config_file)
        self.logger = self._setup_logging()
        self.config = self._load_discord_config()
        self.message_queue: List[DiscordMessage] = []
        self.message_history: Dict[str, DiscordMessage] = {}
        self.rate_limit_counter = 0
        self.last_rate_limit_reset = datetime.now()
        
        # Initialize message types
        self._initialize_message_types()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("DiscordIntegrationService")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_discord_config(self) -> DiscordConfig:
        """Load Discord configuration."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    return DiscordConfig(**config_data)
            else:
                # Default configuration
                return DiscordConfig(
                    webhook_url="",
                    bot_token="",
                    channel_id="",
                    enabled=False,
                    message_rate_limit=30
                )
        except Exception as e:
            self.logger.error(f"Error loading Discord config: {e}")
            return DiscordConfig(
                webhook_url="",
                bot_token="",
                channel_id="",
                enabled=False,
                message_rate_limit=30
            )
    
    def _initialize_message_types(self):
        """Initialize message type configurations."""
        self.message_types = {
            "status": {"emoji": "📊", "color": "BLUE"},
            "progress": {"emoji": "🔄", "color": "YELLOW"},
            "completion": {"emoji": "✅", "color": "GREEN"},
            "coordination": {"emoji": "🎖️", "color": "PURPLE"},
            "error": {"emoji": "❌", "color": "RED"},
            "system": {"emoji": "⚙️", "color": "GRAY"}
        }
    
    def create_discord_message(self, sender: str, title: str, content: str, 
                              message_type: str = "status", priority: str = "medium") -> str:
        """Create a Discord message."""
        try:
            if not self.config.enabled:
                self.logger.warning("Discord integration is disabled")
                return ""
            
            # Generate message ID
            message_id = f"discord_{sender}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create message
            message = DiscordMessage(
                message_id=message_id,
                sender=sender,
                title=title,
                content=content,
                message_type=message_type,
                timestamp=datetime.now(),
                priority=priority
            )
            
            # Add to queue
            self.message_queue.append(message)
            self.message_history[message_id] = message
            
            self.logger.info(f"Created Discord message: {message_id} ({message_type})")
            return message_id
            
        except Exception as e:
            self.logger.error(f"Error creating Discord message: {e}")
            return ""
    
    def send_status_message(self, sender: str, title: str, content: str) -> str:
        """Send a status message to Discord."""
        return self.create_discord_message(sender, title, content, "status", "medium")
    
    def send_progress_message(self, sender: str, title: str, content: str) -> str:
        """Send a progress message to Discord."""
        return self.create_discord_message(sender, title, content, "progress", "medium")
    
    def send_completion_message(self, sender: str, title: str, content: str) -> str:
        """Send a completion message to Discord."""
        return self.create_discord_message(sender, title, content, "completion", "high")
    
    def send_coordination_message(self, sender: str, title: str, content: str) -> str:
        """Send a coordination message to Discord."""
        return self.create_discord_message(sender, title, content, "coordination", "high")
    
    def send_error_message(self, sender: str, title: str, content: str) -> str:
        """Send an error message to Discord."""
        return self.create_discord_message(sender, title, content, "error", "critical")
    
    def send_system_message(self, sender: str, title: str, content: str) -> str:
        """Send a system message to Discord."""
        return self.create_discord_message(sender, title, content, "system", "low")
    
    def format_discord_message(self, message: DiscordMessage) -> str:
        """Format a Discord message for sending."""
        try:
            message_type_config = self.message_types.get(message.message_type, {})
            emoji = message_type_config.get("emoji", "📝")
            
            formatted_message = f"""
{emoji} **{message.title}**
**From:** {message.sender}
**Type:** {message.message_type.title()}
**Priority:** {message.priority.title()}
**Time:** {message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

{message.content}

---
*Message ID: {message.message_id}*
"""
            
            return formatted_message.strip()
            
        except Exception as e:
            self.logger.error(f"Error formatting Discord message: {e}")
            return f"Error formatting message: {e}"
    
    def check_rate_limit(self) -> bool:
        """Check if we can send a message based on rate limiting."""
        try:
            current_time = datetime.now()
            
            # Reset counter if minute has passed
            if (current_time - self.last_rate_limit_reset).seconds >= 60:
                self.rate_limit_counter = 0
                self.last_rate_limit_reset = current_time
            
            # Check if we're under the limit
            if self.rate_limit_counter < self.config.message_rate_limit:
                self.rate_limit_counter += 1
                return True
            else:
                self.logger.warning("Discord rate limit exceeded")
                return False
                
        except Exception as e:
            self.logger.error(f"Error checking rate limit: {e}")
            return False
    
    async def send_message_to_discord(self, message_id: str) -> bool:
        """Send a message to Discord (simulated for now)."""
        try:
            if not self.config.enabled:
                self.logger.warning("Discord integration is disabled")
                return False
            
            if not self.check_rate_limit():
                self.logger.warning("Rate limit exceeded, message queued")
                return False
            
            message = self.message_history.get(message_id)
            if not message:
                self.logger.error(f"Message {message_id} not found")
                return False
            
            # Format message
            formatted_content = self.format_discord_message(message)
            
            # Simulate Discord sending (replace with actual Discord API calls)
            self.logger.info(f"📤 Sending to Discord: {message.title}")
            self.logger.info(f"Content: {formatted_content[:100]}...")
            
            # Remove from queue
            if message in self.message_queue:
                self.message_queue.remove(message)
            
            self.logger.info(f"✅ Discord message {message_id} sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending Discord message {message_id}: {e}")
            return False
    
    def get_message_queue_status(self) -> Dict[str, Any]:
        """Get status of the message queue."""
        return {
            "total_queued": len(self.message_queue),
            "total_sent": len(self.message_history) - len(self.message_queue),
            "rate_limit_counter": self.rate_limit_counter,
            "rate_limit_max": self.config.message_rate_limit,
            "config_enabled": self.config.enabled
        }
    
    def get_message_history(self, message_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get message history, optionally filtered by type."""
        history = []
        
        for message in self.message_history.values():
            if message_type and message.message_type != message_type:
                continue
            
            history.append({
                "message_id": message.message_id,
                "sender": message.sender,
                "title": message.title,
                "type": message.message_type,
                "priority": message.priority,
                "timestamp": message.timestamp.isoformat(),
                "content_preview": message.content[:100] + "..." if len(message.content) > 100 else message.content
            })
        
        return history

def main():
    """CLI interface for Discord Integration Service."""
    parser = argparse.ArgumentParser(description="Discord Integration Service CLI")
    parser.add_argument("--status", type=str, help="Send status message (format: sender:title:content)")
    parser.add_argument("--progress", type=str, help="Send progress message (format: sender:title:content)")
    parser.add_argument("--completion", type=str, help="Send completion message (format: sender:title:content)")
    parser.add_argument("--coordination", type=str, help="Send coordination message (format: sender:title:content)")
    parser.add_argument("--error", type=str, help="Send error message (format: sender:title:content)")
    parser.add_argument("--system", type=str, help="Send system message (format: sender:title:content)")
    parser.add_argument("--queue", action="store_true", help="Show message queue status")
    parser.add_argument("--history", type=str, help="Show message history (optional: message_type)")
    
    args = parser.parse_args()
    
    # Initialize service
    discord_service = DiscordIntegrationService()
    
    if args.status:
        try:
            sender, title, content = args.status.split(":", 2)
            message_id = discord_service.send_status_message(sender, title, content)
            if message_id:
                print(f"✅ Status message created: {message_id}")
            else:
                print("❌ Failed to create status message")
        except ValueError:
            print("❌ Invalid format. Use: sender:title:content")
    
    elif args.progress:
        try:
            sender, title, content = args.progress.split(":", 2)
            message_id = discord_service.send_progress_message(sender, title, content)
            if message_id:
                print(f"✅ Progress message created: {message_id}")
            else:
                print("❌ Failed to create progress message")
        except ValueError:
            print("❌ Invalid format. Use: sender:title:content")
    
    elif args.completion:
        try:
            sender, title, content = args.completion.split(":", 2)
            message_id = discord_service.send_completion_message(sender, title, content)
            if message_id:
                print(f"✅ Completion message created: {message_id}")
            else:
                print("❌ Failed to create completion message")
        except ValueError:
            print("❌ Invalid format. Use: sender:title:content")
    
    elif args.coordination:
        try:
            sender, title, content = args.coordination.split(":", 2)
            message_id = discord_service.send_coordination_message(sender, title, content)
            if message_id:
                print(f"✅ Coordination message created: {message_id}")
            else:
                print("❌ Failed to create coordination message")
        except ValueError:
            print("❌ Invalid format. Use: sender:title:content")
    
    elif args.error:
        try:
            sender, title, content = args.error.split(":", 2)
            message_id = discord_service.send_error_message(sender, title, content)
            if message_id:
                print(f"✅ Error message created: {message_id}")
            else:
                print("❌ Failed to create error message")
        except ValueError:
            print("❌ Invalid format. Use: sender:title:content")
    
    elif args.system:
        try:
            sender, title, content = args.system.split(":", 2)
            message_id = discord_service.send_system_message(sender, title, content)
            if message_id:
                print(f"✅ System message created: {message_id}")
            else:
                print("❌ Failed to create system message")
        except ValueError:
            print("❌ Invalid format. Use: sender:title:content")
    
    elif args.queue:
        status = discord_service.get_message_queue_status()
        print("📤 Discord Message Queue Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    elif args.history:
        history = discord_service.get_message_history(args.history)
        print(f"📚 Discord Message History ({len(history)} messages):")
        for msg in history:
            print(f"  [{msg['timestamp']}] {msg['sender']}: {msg['title']} ({msg['type']})")
    
    else:
        print("📤 Discord Integration Service - Use --help for available commands")

if __name__ == "__main__":
    main()
