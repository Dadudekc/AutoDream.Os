#!/usr/bin/env python3
"""
Discord Manager
===============
Comprehensive Discord management tool for the Agent Cellphone V2 project.
Provides complete control over Discord bot, channels, webhooks, and devlog posting.

Usage:
    python discord_manager.py --help
    python discord_manager.py status
    python discord_manager.py test-posting
    python discord_manager.py list-channels
    python discord_manager.py post-message --agent agent4 --content "Test message"
    python discord_manager.py create-webhooks
    python discord_manager.py verify-channels

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import argparse
import asyncio
import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

class DiscordManager:
    """Comprehensive Discord management tool."""
    
    def __init__(self):
        """Initialize Discord Manager."""
        self.project_root = project_root
        self.env_loaded = False
        self.discord_service = None
        self.bot = None
        
        # Load environment
        self._load_environment()
        
        # Agent configuration
        self.agents = {
            "agent1": {"name": "Integration Specialist", "enabled": False},
            "agent2": {"name": "Architecture Specialist", "enabled": False},
            "agent3": {"name": "Infrastructure Specialist", "enabled": False},
            "agent4": {"name": "Captain", "enabled": True},
            "agent5": {"name": "Coordinator", "enabled": True},
            "agent6": {"name": "Quality Specialist", "enabled": True},
            "agent7": {"name": "Implementation Specialist", "enabled": True},
            "agent8": {"name": "SSOT Manager", "enabled": True},
        }
    
    def _load_environment(self) -> bool:
        """Load environment variables from .env file."""
        try:
            env_file = self.project_root / ".env"
            if not env_file.exists():
                print("❌ .env file not found")
                return False
            
            # Load .env file manually
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        value = value.strip('"\'')
                        os.environ[key] = value
            
            self.env_loaded = True
            return True
        except Exception as e:
            print(f"❌ Failed to load .env file: {e}")
            return False
    
    def _get_discord_service(self):
        """Get Discord service instance."""
        if not self.discord_service:
            try:
                from src.services.discord_devlog_service import DiscordDevlogService
                self.discord_service = DiscordDevlogService()
            except Exception as e:
                print(f"❌ Failed to load Discord service: {e}")
                return None
        return self.discord_service
    
    def status(self) -> bool:
        """Show Discord system status."""
        print("🐝 Discord Manager - System Status")
        print("=" * 60)
        
        # Environment status
        print(f"📋 Environment: {'✅ Loaded' if self.env_loaded else '❌ Failed'}")
        
        # Discord configuration
        bot_token = os.getenv('DISCORD_BOT_TOKEN')
        main_channel = os.getenv('DISCORD_CHANNEL_ID')
        guild_id = os.getenv('DISCORD_GUILD_ID')
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        print(f"\n🔧 Discord Configuration:")
        print(f"   • Bot Token: {'✅ Available' if bot_token else '❌ Missing'}")
        if bot_token:
            print(f"     Token: {bot_token[:20]}...")
        
        print(f"   • Main Channel: {main_channel or 'Not set'}")
        print(f"   • Guild ID: {guild_id or 'Not set'}")
        print(f"   • Webhook URL: {'✅ Available' if webhook_url else '❌ Missing'}")
        if webhook_url:
            print(f"     Webhook: {webhook_url[:50]}...")
        
        # Agent channels
        print(f"\n📋 Agent Channels:")
        agent_channels = {}
        for i in range(1, 9):
            agent_key = f"DISCORD_CHANNEL_AGENT_{i}"
            channel_id = os.getenv(agent_key)
            if channel_id:
                agent_channels[f"Agent-{i}"] = channel_id
        
        for agent_id, channel_id in agent_channels.items():
            status = "🟢 ACTIVE" if int(agent_id.split('-')[1]) >= 4 else "🔴 INACTIVE"
            print(f"   • {agent_id}: {channel_id} {status}")
        
        # Discord service status
        service = self._get_discord_service()
        if service:
            print(f"\n🤖 Discord Service: ✅ Available")
            print(f"   • Agent Channels: {len(getattr(service, 'agent_channels', {}))}")
            print(f"   • Agent Webhooks: {len(getattr(service, 'agent_webhooks', {}))}")
        else:
            print(f"\n🤖 Discord Service: ❌ Failed to load")
        
        print("\n" + "=" * 60)
        return True
    
    def list_channels(self) -> bool:
        """List all configured Discord channels."""
        print("📋 Discord Channel Configuration")
        print("=" * 60)
        
        # Main channels
        print("🏠 Main Channels:")
        main_channel = os.getenv('DISCORD_CHANNEL_ID')
        guild_id = os.getenv('DISCORD_GUILD_ID')
        print(f"   • Main Channel: {main_channel or 'Not configured'}")
        print(f"   • Guild ID: {guild_id or 'Not configured'}")
        
        # Agent channels
        print(f"\n👥 Agent Channels:")
        for i in range(1, 9):
            agent_key = f"DISCORD_CHANNEL_AGENT_{i}"
            channel_id = os.getenv(agent_key)
            agent_name = self.agents.get(f"agent{i}", {}).get("name", f"Agent-{i}")
            status = "🟢 ACTIVE" if i >= 4 else "🔴 INACTIVE"
            
            if channel_id:
                print(f"   • Agent-{i} ({agent_name}): {channel_id} {status}")
            else:
                print(f"   • Agent-{i} ({agent_name}): ❌ Not configured")
        
        # Webhook channels
        print(f"\n🔗 Webhook Configuration:")
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if webhook_url:
            print(f"   • Default Webhook: ✅ Configured")
            print(f"     URL: {webhook_url[:50]}...")
        else:
            print(f"   • Default Webhook: ❌ Not configured")
        
        # Agent webhooks
        agent_webhooks = 0
        for i in range(1, 9):
            webhook_key = f"DISCORD_WEBHOOK_AGENT_{i}"
            if os.getenv(webhook_key):
                agent_webhooks += 1
        
        print(f"   • Agent Webhooks: {agent_webhooks}/8 configured")
        
        print("\n" + "=" * 60)
        return True
    
    async def test_posting(self, agent: str = None) -> bool:
        """Test Discord posting for one or all agents."""
        print("🧪 Discord Posting Test")
        print("=" * 60)
        
        service = self._get_discord_service()
        if not service:
            print("❌ Discord service not available")
            return False
        
        # Determine which agents to test
        test_agents = []
        if agent:
            if agent in self.agents:
                test_agents = [agent]
            else:
                print(f"❌ Unknown agent: {agent}")
                return False
        else:
            # Test all active agents
            test_agents = [aid for aid, config in self.agents.items() if config["enabled"]]
        
        print(f"📋 Testing {len(test_agents)} agent(s): {', '.join(test_agents)}")
        
        results = {}
        for agent_id in test_agents:
            print(f"\n🧪 Testing {agent_id} ({self.agents[agent_id]['name']})...")
            
            # Create test message
            test_content = f"""
**🧪 DISCORD POSTING TEST**

**Agent:** {agent_id} ({self.agents[agent_id]['name']})
**Test Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Purpose:** Verify Discord posting functionality

**Expected Channel:** {os.getenv(f'DISCORD_CHANNEL_AGENT_{agent_id[-1]}', 'Not configured')}

**Status:** Testing channel connectivity and message delivery.

**If you see this message:** Discord integration is working correctly! ✅

---
*Automated test message - please confirm receipt*
            """.strip()
            
            try:
                # Test posting
                result = await service.post_devlog_to_discord(test_content, f"Agent-{agent_id[-1]}")
                results[agent_id] = result
                
                if result:
                    channel_id = os.getenv(f'DISCORD_CHANNEL_AGENT_{agent_id[-1]}', 'Unknown')
                    print(f"   ✅ Posted successfully to channel {channel_id}")
                else:
                    print(f"   ❌ Posting failed")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results[agent_id] = False
        
        # Summary
        print(f"\n📊 Test Results:")
        success_count = sum(1 for result in results.values() if result)
        total_count = len(results)
        
        for agent_id, result in results.items():
            status = "✅ Success" if result else "❌ Failed"
            print(f"   • {agent_id}: {status}")
        
        print(f"\n📈 Overall: {success_count}/{total_count} agents posted successfully")
        
        if success_count == total_count:
            print("🎉 All tests passed! Discord integration is working perfectly.")
        elif success_count > 0:
            print("⚠️ Partial success. Some agents are working, others need attention.")
        else:
            print("❌ All tests failed. Check Discord configuration and permissions.")
        
        print("\n" + "=" * 60)
        return success_count == total_count
    
    async def post_message(self, agent: str, content: str) -> bool:
        """Post a custom message to a specific agent's channel."""
        print(f"📤 Posting Message to {agent}")
        print("=" * 60)
        
        if agent not in self.agents:
            print(f"❌ Unknown agent: {agent}")
            return False
        
        service = self._get_discord_service()
        if not service:
            print("❌ Discord service not available")
            return False
        
        agent_info = self.agents[agent]
        agent_number = agent[-1]
        
        print(f"📋 Agent: {agent} ({agent_info['name']})")
        print(f"📝 Content: {content[:100]}{'...' if len(content) > 100 else ''}")
        print(f"🎯 Target Channel: {os.getenv(f'DISCORD_CHANNEL_AGENT_{agent_number}', 'Not configured')}")
        
        try:
            # Format message with timestamp
            formatted_content = f"""
**📢 MANUAL MESSAGE**

**Agent:** {agent} ({agent_info['name']})
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source:** Discord Manager Tool

---

{content}

---
*Message sent via Discord Manager*
            """.strip()
            
            # Post message
            result = await service.post_devlog_to_discord(formatted_content, f"Agent-{agent_number}")
            
            if result:
                print("✅ Message posted successfully!")
                print(f"💡 Check {agent}'s channel for the message")
            else:
                print("❌ Failed to post message")
            
            return result
            
        except Exception as e:
            print(f"❌ Error posting message: {e}")
            return False
    
    async def verify_channels(self) -> bool:
        """Verify that all configured channels are accessible."""
        print("🔍 Discord Channel Verification")
        print("=" * 60)
        
        service = self._get_discord_service()
        if not service:
            print("❌ Discord service not available")
            return False
        
        # Test bot connection
        print("🤖 Testing bot connection...")
        try:
            if not await service._connect_bot():
                print("❌ Failed to connect bot")
                return False
            print("✅ Bot connected successfully")
        except Exception as e:
            print(f"❌ Bot connection error: {e}")
            return False
        
        # Verify each agent channel
        print(f"\n📋 Verifying agent channels...")
        verification_results = {}
        
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            channel_id = os.getenv(f'DISCORD_CHANNEL_AGENT_{i}')
            
            if not channel_id:
                print(f"   • {agent_id}: ❌ No channel configured")
                verification_results[agent_id] = False
                continue
            
            try:
                # Test channel access
                channel = await service._get_channel(agent_id)
                if channel:
                    print(f"   • {agent_id}: ✅ Channel accessible (ID: {channel_id})")
                    verification_results[agent_id] = True
                else:
                    print(f"   • {agent_id}: ❌ Channel not accessible (ID: {channel_id})")
                    verification_results[agent_id] = False
                    
            except Exception as e:
                print(f"   • {agent_id}: ❌ Error accessing channel: {e}")
                verification_results[agent_id] = False
        
        # Summary
        accessible_count = sum(1 for result in verification_results.values() if result)
        total_count = len(verification_results)
        
        print(f"\n📊 Verification Results: {accessible_count}/{total_count} channels accessible")
        
        if accessible_count == total_count:
            print("🎉 All channels are accessible!")
        elif accessible_count > 0:
            print("⚠️ Some channels are accessible, others need attention.")
        else:
            print("❌ No channels are accessible. Check bot permissions.")
        
        print("\n" + "=" * 60)
        return accessible_count == total_count
    
    def show_help(self) -> bool:
        """Show help information."""
        print("🐝 Discord Manager - Help")
        print("=" * 60)
        
        print("📋 Available Commands:")
        print("   status              - Show Discord system status")
        print("   list-channels       - List all configured Discord channels")
        print("   test-posting        - Test Discord posting for all active agents")
        print("   test-posting --agent AGENT - Test posting for specific agent")
        print("   post-message --agent AGENT --content MESSAGE - Post custom message")
        print("   verify-channels     - Verify all channels are accessible")
        print("   help                - Show this help message")
        
        print(f"\n👥 Available Agents:")
        for agent_id, config in self.agents.items():
            status = "🟢 ACTIVE" if config["enabled"] else "🔴 INACTIVE"
            print(f"   • {agent_id}: {config['name']} {status}")
        
        print(f"\n💡 Examples:")
        print("   python discord_manager.py status")
        print("   python discord_manager.py test-posting")
        print("   python discord_manager.py test-posting --agent agent4")
        print("   python discord_manager.py post-message --agent agent5 --content 'Hello from Discord Manager!'")
        print("   python discord_manager.py verify-channels")
        
        print("\n" + "=" * 60)
        return True

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Discord Manager - Complete Discord management tool")
    parser.add_argument('command', choices=[
        'status', 'list-channels', 'test-posting', 'post-message', 
        'verify-channels', 'help'
    ], help='Command to execute')
    
    parser.add_argument('--agent', help='Agent ID (e.g., agent4)')
    parser.add_argument('--content', help='Message content for post-message command')
    
    args = parser.parse_args()
    
    # Create manager instance
    manager = DiscordManager()
    
    if not manager.env_loaded:
        print("❌ Cannot proceed without .env file")
        return False
    
    # Execute command
    if args.command == 'status':
        return manager.status()
    
    elif args.command == 'list-channels':
        return manager.list_channels()
    
    elif args.command == 'test-posting':
        return asyncio.run(manager.test_posting(args.agent))
    
    elif args.command == 'post-message':
        if not args.agent or not args.content:
            print("❌ Both --agent and --content are required for post-message")
            return False
        return asyncio.run(manager.post_message(args.agent, args.content))
    
    elif args.command == 'verify-channels':
        return asyncio.run(manager.verify_channels())
    
    elif args.command == 'help':
        return manager.show_help()
    
    else:
        print(f"❌ Unknown command: {args.command}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Discord Manager interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Discord Manager error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
