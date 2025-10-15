#!/usr/bin/env python3
"""
Discord Webhook Management Demo
================================

Demonstrates how agents can use webhook management tools.

Author: Agent-7 (Web Development Specialist)
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def demo_list_webhooks():
    """Demo: List existing webhooks from config."""
    print("\n" + "="*60)
    print("DEMO 1: List Existing Webhooks")
    print("="*60)
    
    try:
        from tools_v2.categories.discord_webhook_tools import ListWebhooksTool
        
        tool = ListWebhooksTool()
        result = tool.execute()
        
        if result['success']:
            print(f"✅ Found {result['count']} webhook(s):")
            for webhook in result['webhooks']:
                print(f"  - {webhook['name']} ({webhook['source']})")
        else:
            print(f"❌ Error: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")


def demo_save_webhook():
    """Demo: Save a webhook URL to config."""
    print("\n" + "="*60)
    print("DEMO 2: Save Webhook to .env")
    print("="*60)
    
    # Example webhook URL (invalid, for demo only)
    webhook_url = "https://discord.com/api/webhooks/123456789/abcdefg-example"
    
    print(f"📝 Saving webhook URL: {webhook_url[:50]}...")
    
    try:
        from tools_v2.categories.discord_webhook_tools import SaveWebhookTool
        
        tool = SaveWebhookTool()
        result = tool.execute(
            webhook_url=webhook_url,
            config_key="DISCORD_DEMO_WEBHOOK",
            target="env"
        )
        
        if result['success']:
            print(f"✅ Saved to: {result['saved_to']}")
            print(f"   Config key: {result['config_key']}")
            print(f"   Action: {result['action']}")
        else:
            print(f"❌ Error: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")


def demo_test_webhook():
    """Demo: Test a webhook (will fail if not configured)."""
    print("\n" + "="*60)
    print("DEMO 3: Test Webhook")
    print("="*60)
    
    print("⚠️  This will test DISCORD_WEBHOOK_URL from your .env file")
    
    try:
        from tools_v2.categories.discord_webhook_tools import TestWebhookTool
        
        tool = TestWebhookTool()
        result = tool.execute(
            test_message="✅ Webhook management demo - test successful!"
        )
        
        if result['success']:
            print(f"✅ Webhook test successful!")
            print(f"   Status: {result['status_code']}")
            print(f"   Webhook: {result['webhook_preview']}")
        else:
            print(f"❌ Error: {result.get('error')}")
            print(f"   Tip: Set DISCORD_WEBHOOK_URL in your .env file")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")


def demo_webhook_manager():
    """Demo: Use all-in-one webhook manager."""
    print("\n" + "="*60)
    print("DEMO 4: Webhook Manager (All-in-One Tool)")
    print("="*60)
    
    try:
        from tools_v2.categories.discord_webhook_tools import WebhookManagerTool
        
        tool = WebhookManagerTool()
        
        # Demo: List action
        print("\n📋 Action: list")
        result = tool.execute(action="list")
        
        if result['success']:
            print(f"✅ Found {result['count']} webhook(s)")
        else:
            print(f"❌ Error: {result.get('error')}")
        
        # Demo: Test action (will fail if not configured)
        print("\n🧪 Action: test")
        result = tool.execute(
            action="test",
            test_message="Manager tool test"
        )
        
        if result['success']:
            print("✅ Test successful")
        else:
            print(f"⚠️  {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")


def demo_agent_workflow():
    """Demo: Complete agent workflow for webhook usage."""
    print("\n" + "="*60)
    print("DEMO 5: Complete Agent Workflow")
    print("="*60)
    
    print("\n📚 Complete Agent Workflow for Discord Webhooks:")
    print("\n1️⃣ Commander creates webhook in Discord:")
    print("   !create_webhook #devlogs Agent-7-Devlog-Webhook")
    
    print("\n2️⃣ Agent lists available webhooks:")
    print("   from tools_v2.categories.discord_webhook_tools import ListWebhooksTool")
    print("   tool = ListWebhooksTool()")
    print("   result = tool.execute()")
    
    print("\n3️⃣ Agent tests webhook:")
    print("   from tools_v2.categories.discord_webhook_tools import TestWebhookTool")
    print("   tool = TestWebhookTool()")
    print("   result = tool.execute(config_key='devlogs_webhook')")
    
    print("\n4️⃣ Agent uses webhook for posting:")
    print("   from src.services.publishers.discord_publisher import DiscordDevlogPublisher")
    print("   publisher = DiscordDevlogPublisher(webhook_url)")
    print("   publisher.publish_devlog(...)")
    
    print("\n✅ Workflow enables full Discord automation!")


def main():
    """Run all demos."""
    print("="*60)
    print("Discord Webhook Management - Demo Suite")
    print("="*60)
    print("\nThis demo shows how agents can manage Discord webhooks.")
    print("Note: Some demos may fail if webhooks aren't configured.")
    
    # Run all demos
    demo_list_webhooks()
    demo_save_webhook()
    demo_test_webhook()
    demo_webhook_manager()
    demo_agent_workflow()
    
    print("\n" + "="*60)
    print("Demo Complete!")
    print("="*60)
    print("\n📚 Next Steps:")
    print("  1. Read docs/guides/WEBHOOK_MANAGEMENT_GUIDE.md")
    print("  2. Start Discord bot: python run_unified_discord_bot.py")
    print("  3. Create webhook: !create_webhook #channel Name")
    print("  4. Use from agents: toolbelt.execute('webhook.test')")
    print("\n✅ Full Discord control achieved!")


if __name__ == "__main__":
    main()

