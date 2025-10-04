#!/usr/bin/env python3
"""
Discord Webhook CLI Tool
========================

Command-line interface for Discord webhook management.
Provides easy access to webhook creation and agent provisioning.

Usage:
    python tools/discord_webhook_cli.py provision-agent Agent-7
    python tools/discord_webhook_cli.py provision-all
    python tools/discord_webhook_cli.py create-webhook <channel_id>
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.discord_commander.webhook_manager import WebhookManager
from src.services.discord_commander.bot_main import create_discord_bot


async def provision_agent_webhook(agent_id: str):
    """Provision webhook for specific agent."""
    print(f"🔄 Provisioning webhook for {agent_id}...")
    
    try:
        # Create Discord bot (minimal setup)
        bot_config = create_discord_bot()
        
        if not bot_config:
            print("❌ Failed to create Discord bot configuration")
            return False
            
        # Note: For CLI, we'll need the bot token to connect
        # For now, we'll create a simple webhook manager
        manager = WebhookManager(None)  # No bot instance needed for CLI
        
        # Get agent channel ID
        import os
        agent_num = agent_id.split('-')[1] if '-' in agent_id else agent_id.replace('Agent', '')
        channel_key = f"DISCORD_CHANNEL_AGENT_{agent_num}"
        channel_id = os.getenv(channel_key)
        
        if not channel_id:
            print(f"❌ Channel ID not found for {agent_id} (missing {channel_key})")
            return False
            
        print(f"📍 Agent {agent_id} channel: {channel_id}")
        print(f"📝 Add this to your Discord channel manually:")
        print(f"   1. Go to Discord → Channel Settings → Integrations → Webhooks")
        print(f"   2. Create webhook named '{agent_id} Devlog Webhook'")
        print(f"   3. Copy webhook URL")
        print(f"NEXT STEP: Add webhook URL to .env file:")
        print(f"   DISCORD_WEBHOOK_AGENT_{agent_num}=<webhook_url_here>")
        
        return True
        
    except Exception as e:
        print(f"❌ Error provisioning webhook: {e}")
        return False


async def provision_all_agents():
    """Provision webhooks for all configured agents."""
    print("🔄 Provisioning webhooks for all agents...")
    
    agent_channels = []
    for i in range(1, 9):
        agent_id = f"Agent-{i}"
        channel_key = f"DISCORD_CHANNEL_AGENT_{i}"
        
        import os
        channel_id = os.getenv(channel_key)
        
        if channel_id:
            agent_channels.append((agent_id, channel_id))
            print(f"✅ {agent_id}: Channel {channel_id}")
        else:
            print(f"❌ {agent_id}: No channel configured")
    
    if not agent_channels:
        print("❌ No agent channels configured. Check your .env file.")
        return False
        
    print(f"\n📝 MANUAL WEBHOOK CREATION REQUIRED:")
    print(f"Create webhooks in Discord for each agent channel:")
    
    for agent_id, channel_id in agent_channels:
        agent_num = agent_id.split('-')[1]
        print(f"\n🔗 {agent_id}:")
        print(f"   Channel ID: {channel_id}")
        print(f"   Webhook name: '{agent_id} Devlog Webhook'")
        print(f"   Add to .env: DISCORD_WEBHOOK_AGENT_{agent_num}=<webhook_url>")
    
    return True


async def create_webhook_for_channel(channel_id: int, webhook_name: str = None):
    """Create webhook for specific channel."""
    print(f"🔄 Creating webhook for channel {channel_id}...")
    
    # For a full implementation, we'd need to connect to Discord
    # For CLI, we'll provide manual instructions:
    
    print(f"📝 MANUAL WEBHOOK CREATION:")
    print(f"1. Go to Discord → Channel Settings → Integrations → Webhooks")
    print(f"2. Click 'Create Webhook'")
    print(f"3. Name: {webhook_name or 'Agent Webhook'}")
    print(f"4. Copy the webhook URL")
    print(f"5. Use webhook URL for posting messages")
    
    return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Discord Webhook Management CLI",
        epilog="🐝 WE ARE SWARM - Discord Webhook Management"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Provision agent webhook command
    prov_agent_parser = subparsers.add_parser("provision-agent", help="Provision webhook for specific agent")
    prov_agent_parser.add_argument("agent_id", help="Agent ID (e.g., Agent-7)")
    
    # Provision all webhooks command
    subparsers.add_parser("provision-all", help="Provision webhooks for all agents")
    
    # Create webhook command
    create_parser = subparsers.add_parser("create-webhook", help="Create webhook for channel")
    create_parser.add_argument("channel_id", type=int, help="Discord channel ID")
    create_parser.add_argument("--name", help="Webhook name")
    
    # List webhooks command
    list_parser = subparsers.add_parser("list-webhooks", help="List configured webhooks")
    list_parser.add_argument("channel_id", type=int, help="Discord channel ID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    async def run_command():
        if args.command == "provision-agent":
            success = await provision_agent_webhook(args.agent_id)
        elif args.command == "provision-all":
            success = await provision_all_agents()
        elif args.command == "create-webhook":
            success = await create_webhook_for_channel(args.channel_id, args.name)
        elif args.command == "list-webhooks":
            print(f"📋 List webhooks for channel {args.channel_id}")
            print("⚠️  Feature not fully implemented - use Discord interface")
            success = True
        else:
            print(f"❌ Unknown command: {args.command}")
            success = False
            
        return success
    
    try:
        success = asyncio.run(run_command())
        if success:
            print("\n✅ Command completed successfully")
        else:
            print("\n❌ Command failed")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Command cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
