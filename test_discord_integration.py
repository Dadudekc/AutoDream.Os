#!/usr/bin/env python3
"""
Test Discord Integration
========================

Simple test script to verify Discord Commander functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_discord_imports():
    """Test that Discord Commander can be imported."""
    try:
        from discord_commander.discord_commander import DiscordCommander
        from discord_commander.discord_webhook_integration import DiscordWebhookIntegration
        from discord_commander.agent_communication_engine_refactored import AgentCommunicationEngine

        print("✅ All Discord Commander imports successful!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_discord_commander_creation():
    """Test creating Discord Commander instance."""
    try:
        from discord_commander.discord_commander import DiscordCommander

        commander = DiscordCommander()
        print("✅ Discord Commander instance created successfully!")
        return True

    except Exception as e:
        print(f"❌ Error creating Discord Commander: {e}")
        return False

def test_webhook_integration():
    """Test Discord webhook integration."""
    try:
        from discord_commander.discord_webhook_integration import DiscordWebhookIntegration

        webhook = DiscordWebhookIntegration()
        print("✅ Discord Webhook Integration created successfully!")
        print(f"📡 Webhook URL configured: {webhook.webhook_url is not None}")
        return True

    except Exception as e:
        print(f"❌ Error creating webhook integration: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Discord Integration")
    print("=" * 50)

    tests = [
        ("Import Test", test_discord_imports),
        ("Commander Creation Test", test_discord_commander_creation),
        ("Webhook Integration Test", test_webhook_integration),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")

    print("
📊 Test Results:"    print(f"   ✅ Passed: {passed}/{total}")
    print(f"   ❌ Failed: {total - passed}/{total}")

    if passed == total:
        print("
🎉 ALL TESTS PASSED! Discord integration is working!"        print("🐝 Ready for DevLog monitoring and agent coordination!")
    else:
        print("
⚠️  Some tests failed. Discord integration needs debugging."        print("🔧 Check import paths and dependencies.")

if __name__ == "__main__":
    main()
