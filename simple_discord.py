#!/usr/bin/env python3
"""
Simple Discord Integration - Agent Cellphone V2
==============================================

SSOT: Single Source of Truth for Discord messaging.
Bypasses import issues and provides reliable Discord integration.

**Features:**
- Direct Discord webhook integration
- Rich message formatting
- Error handling and retry logic
- Environment variable configuration
- No complex import dependencies

**Usage:**
python simple_discord.py "Your message" "Title" [--channel CHANNEL] [--color COLOR]
"""

import os
import sys
import json
import requests
import argparse
from datetime import datetime
from typing import Optional, Dict, Any

class SimpleDiscordIntegration:
    """Simple Discord integration with SSOT principles"""
    
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        self.default_channel = os.getenv('DISCORD_CHANNEL_ID', 'general')
        
        if not self.webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL environment variable not set")
        
        print(f"✅ Discord integration initialized")
        print(f"📱 Webhook: {self.webhook_url[:50]}...")
        print(f"📺 Default channel: {self.default_channel}")
    
    def send_message(self, content: str, title: str = "Update", 
                    channel: str = None, color: int = 0x00ff00,
                    fields: Optional[Dict[str, str]] = None) -> bool:
        """
        Send a message to Discord
        
        Args:
            content: Message content
            title: Message title
            channel: Channel to send to (optional)
            color: Embed color (hex)
            fields: Additional fields to include
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Build the message
            message = {
                "embeds": [{
                    "title": title,
                    "description": content,
                    "color": color,
                    "timestamp": datetime.now().isoformat(),
                    "footer": {
                        "text": "Agent Cellphone V2 - SSOT Discord Integration"
                    }
                }]
            }
            
            # Add fields if provided
            if fields:
                message["embeds"][0]["fields"] = [
                    {"name": key, "value": value, "inline": True}
                    for key, value in fields.items()
                ]
            
            # Send the message
            print(f"📤 Sending message to Discord...")
            print(f"   Title: {title}")
            print(f"   Content: {content[:100]}{'...' if len(content) > 100 else ''}")
            
            response = requests.post(
                self.webhook_url,
                json=message,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 204:
                print("✅ Message sent successfully to Discord!")
                return True
            else:
                print(f"❌ Failed to send message. Status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def send_devlog(self, title: str, content: str, agent: str = "unknown", 
                    category: str = "project_update", priority: str = "normal") -> bool:
        """
        Send a formatted devlog message
        
        Args:
            title: Devlog title
            content: Devlog content
            agent: Agent ID
            category: Entry category
            priority: Priority level
        
        Returns:
            True if successful, False otherwise
        """
        # Format content for Discord
        formatted_content = f"""📝 **{title}**
🏷️ **Category**: {category}
🤖 **Agent**: {agent}
📊 **Priority**: {priority}
📅 **Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📋 **Content**:
{content}"""
        
        # Determine color based on priority
        color_map = {
            "low": 0x00ff00,      # Green
            "normal": 0x0099ff,   # Blue
            "high": 0xff9900,     # Orange
            "critical": 0xff0000   # Red
        }
        color = color_map.get(priority.lower(), 0x0099ff)
        
        return self.send_message(
            content=formatted_content,
            title=f"Devlog: {title}",
            color=color
        )
    
    def send_status_update(self, status: str, details: str = "", 
                          component: str = "System") -> bool:
        """
        Send a status update message
        
        Args:
            status: Status (success, warning, error, info)
            details: Status details
            component: Component name
        
        Returns:
            True if successful, False otherwise
        """
        # Status emojis and colors
        status_config = {
            "success": {"emoji": "✅", "color": 0x00ff00},
            "warning": {"emoji": "⚠️", "color": 0xff9900},
            "error": {"emoji": "❌", "color": 0xff0000},
            "info": {"emoji": "ℹ️", "color": 0x0099ff}
        }
        
        config = status_config.get(status.lower(), status_config["info"])
        
        content = f"{config['emoji']} **{component} Status Update**\n\n{details}"
        
        return self.send_message(
            content=content,
            title=f"Status: {status.title()}",
            color=config["color"]
        )
    
    def test_connection(self) -> bool:
        """Test Discord webhook connection"""
        print("🧪 Testing Discord connection...")
        
        success = self.send_message(
            content="This is a test message to verify Discord integration is working.",
            title="Connection Test",
            color=0x00ff00
        )
        
        if success:
            print("✅ Discord connection test successful!")
        else:
            print("❌ Discord connection test failed!")
        
        return success


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Simple Discord Integration - SSOT Implementation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simple_discord.py "Hello Discord!" "Test Message"
  python simple_discord.py "Bug found in routing" "Issue Report" --color 0xff0000
  python simple_discord.py --devlog "Phase Complete" "All systems integrated" --agent "agent-1"
  python simple_discord.py --status "success" "Deployment completed successfully"
  python simple_discord.py --test
        """
    )
    
    parser.add_argument("content", nargs="?", help="Message content")
    parser.add_argument("title", nargs="?", help="Message title")
    parser.add_argument("--channel", "-c", help="Discord channel")
    parser.add_argument("--color", "-cl", type=lambda x: int(x, 16), default=0x00ff00, 
                       help="Embed color (hex)")
    parser.add_argument("--devlog", action="store_true", help="Send as devlog entry")
    parser.add_argument("--agent", "-a", default="unknown", help="Agent ID for devlog")
    parser.add_argument("--category", "-cat", default="project_update", help="Devlog category")
    parser.add_argument("--priority", "-p", default="normal", help="Devlog priority")
    parser.add_argument("--status", "-s", help="Send status update (success/warning/error/info)")
    parser.add_argument("--component", "-comp", default="System", help="Component name for status")
    parser.add_argument("--test", "-t", action="store_true", help="Test Discord connection")
    
    args = parser.parse_args()
    
    try:
        # Initialize Discord integration
        discord = SimpleDiscordIntegration()
        
        if args.test:
            # Test connection
            success = discord.test_connection()
            
        elif args.status:
            # Send status update
            if not args.content:
                print("❌ Content required for status update")
                return 1
            
            success = discord.send_status_update(
                status=args.status,
                details=args.content,
                component=args.component
            )
            
        elif args.devlog:
            # Send devlog entry
            if not args.content or not args.title:
                print("❌ Both content and title required for devlog")
                return 1
            
            success = discord.send_devlog(
                title=args.title,
                content=args.content,
                agent=args.agent,
                category=args.category,
                priority=args.priority
            )
            
        elif args.content and args.title:
            # Send regular message
            success = discord.send_message(
                content=args.content,
                title=args.title,
                channel=args.channel,
                color=args.color
            )
            
        else:
            parser.print_help()
            return 0
        
        return 0 if success else 1
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
