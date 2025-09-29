#!/usr/bin/env python3
"""
Webhook Provisioner CLI
=======================
Command-line tool to provision Discord webhooks for agents.
"""

import asyncio
import discord
import os
import sys
from pathlib import Path
from typing import Dict, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.secret_store import SecretStore
from src.services.discord_bot.tools.webhook_provisioner import DiscordWebhookProvisioner


class WebhookProvisionerCLI:
    """CLI tool for provisioning Discord webhooks."""
    
    def __init__(self):
        self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
        self.bot = None
        self.provisioner = None
        
        # Agent channel mapping
        self.agent_channels = {
            "Agent-1": 1387514611351421079,
            "Agent-2": 1387514933041696900,
            "Agent-3": 1387515009621430392,
            "Agent-4": 1387514978348826664,
            "Agent-5": 1415916580910665758,
            "Agent-6": 1415916621847072828,
            "Agent-7": 1415916665283022980,
            "Agent-8": 1415916707704213565
        }
    
    async def initialize_bot(self) -> bool:
        """Initialize Discord bot connection."""
        if not self.bot_token:
            print("❌ DISCORD_BOT_TOKEN environment variable not set")
            return False
        
        try:
            intents = discord.Intents.default()
            intents.guilds = True
            intents.guild_messages = True
            
            self.bot = discord.Client(intents=intents)
            
            @self.bot.event
            async def on_ready():
                print(f"✅ Bot connected: {self.bot.user}")
                self.provisioner = DiscordWebhookProvisioner(self.bot)
            
            # Start bot
            await self.bot.start(self.bot_token)
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize bot: {e}")
            return False
    
    async def provision_webhook(self, agent_id: str) -> bool:
        """Provision webhook for a specific agent."""
        if not self.provisioner:
            print("❌ Bot not initialized")
            return False
        
        channel_id = self.agent_channels.get(agent_id)
        if not channel_id:
            print(f"❌ No channel mapping found for {agent_id}")
            return False
        
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                print(f"❌ Channel not found: {channel_id}")
                return False
            
            print(f"🔧 Provisioning webhook for {agent_id} in #{channel.name}...")
            
            webhook_url = await self.provisioner.create(agent_id, channel)
            if webhook_url:
                masked_token = webhook_url.split("/")[-1][:6] + "..."
                print(f"✅ Webhook created for {agent_id}")
                print(f"🔐 Token: {masked_token}")
                print(f"📺 Channel: #{channel.name}")
                return True
            else:
                print(f"❌ Failed to create webhook for {agent_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error provisioning webhook for {agent_id}: {e}")
            return False
    
    async def provision_all_webhooks(self) -> Dict[str, bool]:
        """Provision webhooks for all agents."""
        print("🚀 Provisioning webhooks for all agents...")
        print("=" * 50)
        
        results = {}
        for agent_id in self.agent_channels.keys():
            results[agent_id] = await self.provision_webhook(agent_id)
            print()  # Add spacing between agents
        
        return results
    
    async def test_webhook(self, agent_id: str) -> bool:
        """Test webhook for a specific agent."""
        if not self.provisioner:
            print("❌ Bot not initialized")
            return False
        
        print(f"🧪 Testing webhook for {agent_id}...")
        
        success = await self.provisioner.test(agent_id)
        if success:
            print(f"✅ Test message sent successfully to {agent_id}")
        else:
            print(f"❌ Test failed for {agent_id}")
        
        return success
    
    async def list_webhooks(self):
        """List all configured webhooks."""
        print("📋 Configured Webhooks:")
        print("=" * 25)
        
        webhooks = SecretStore.list_webhooks()
        
        if not webhooks:
            print("❌ No webhooks configured")
            return
        
        for agent_id, webhook_data in webhooks.items():
            channel_id = webhook_data.get("channel_id")
            webhook_id = webhook_data.get("webhook_id")
            
            try:
                channel = self.bot.get_channel(channel_id) if self.bot else None
                channel_name = channel.name if channel else f"Channel {channel_id}"
                print(f"✅ {agent_id}: #{channel_name} (ID: {webhook_id})")
            except Exception:
                print(f"✅ {agent_id}: Channel {channel_id} (ID: {webhook_id})")
    
    async def rotate_webhook(self, agent_id: str) -> bool:
        """Rotate webhook for a specific agent."""
        if not self.provisioner:
            print("❌ Bot not initialized")
            return False
        
        print(f"🔄 Rotating webhook for {agent_id}...")
        
        webhook_url = await self.provisioner.rotate(agent_id)
        if webhook_url:
            masked_token = webhook_url.split("/")[-1][:6] + "..."
            print(f"✅ Webhook rotated for {agent_id}")
            print(f"🔐 New token: {masked_token}")
            return True
        else:
            print(f"❌ Failed to rotate webhook for {agent_id}")
            return False
    
    async def revoke_webhook(self, agent_id: str) -> bool:
        """Revoke webhook for a specific agent."""
        if not self.provisioner:
            print("❌ Bot not initialized")
            return False
        
        print(f"🧨 Revoking webhook for {agent_id}...")
        
        success = await self.provisioner.revoke(agent_id)
        if success:
            print(f"✅ Webhook revoked for {agent_id}")
        else:
            print(f"❌ Failed to revoke webhook for {agent_id}")
        
        return success


async def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Discord Webhook Provisioner CLI")
    parser.add_argument("--action", required=True, 
                       choices=["provision-all", "provision", "test", "list", "rotate", "revoke"],
                       help="Action to perform")
    parser.add_argument("--agent", help="Agent ID (required for provision, test, rotate, revoke)")
    
    args = parser.parse_args()
    
    # Validate agent argument for single-agent operations
    if args.action in ["provision", "test", "rotate", "revoke"] and not args.agent:
        print(f"❌ --agent required for action: {args.action}")
        sys.exit(1)
    
    # Validate agent ID format
    if args.agent and not args.agent.startswith("Agent-"):
        print("❌ Agent ID must start with 'Agent-' (e.g., Agent-1)")
        sys.exit(1)
    
    cli = WebhookProvisionerCLI()
    
    try:
        # Initialize bot connection
        print("🔗 Connecting to Discord...")
        bot_task = asyncio.create_task(cli.initialize_bot())
        
        # Wait for bot to be ready
        await asyncio.sleep(5)
        
        if not cli.provisioner:
            print("❌ Bot initialization failed")
            sys.exit(1)
        
        # Execute requested action
        if args.action == "provision-all":
            results = await cli.provision_all_webhooks()
            success_count = sum(1 for success in results.values() if success)
            print(f"\n📊 Results: {success_count}/{len(results)} webhooks created successfully")
            
        elif args.action == "provision":
            success = await cli.provision_webhook(args.agent)
            sys.exit(0 if success else 1)
            
        elif args.action == "test":
            success = await cli.test_webhook(args.agent)
            sys.exit(0 if success else 1)
            
        elif args.action == "list":
            await cli.list_webhooks()
            
        elif args.action == "rotate":
            success = await cli.rotate_webhook(args.agent)
            sys.exit(0 if success else 1)
            
        elif args.action == "revoke":
            success = await cli.revoke_webhook(args.agent)
            sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        if cli.bot:
            await cli.bot.close()


if __name__ == "__main__":
    asyncio.run(main())
