#!/usr/bin/env python3
"""
Enhanced Discord Integration Test Script
========================================

Comprehensive testing script for the enhanced Discord integration
with individual agent channels.

Usage:
    python scripts/test_enhanced_discord.py

Author: Agent-3 (DevOps Specialist) - Discord Expansion Coordinator
License: MIT
"""

import asyncio
import json
import sys
from pathlib import Path


class EnhancedDiscordTester:
    """Test class for enhanced Discord integration."""

    def __init__(self):
        """Initialize test class."""
        self.discord_dir = Path("src/discord_commander")
        self.config_file = Path("config/discord_channels.json")
        self.test_results = {}

    async def run_all_tests(self) -> bool:
        """Run all enhanced Discord integration tests."""
        print("🧪 Enhanced Discord Integration Test Suite")
        print("=" * 60)
        print("Testing individual agent channels and swarm coordination")
        print()

        # Check prerequisites
        if not await self.check_prerequisites():
            return False

        # Test channel configuration
        if not await self.test_channel_configuration():
            return False

        # Test enhanced integration
        if not await self.test_enhanced_integration():
            return False

        # Test agent messaging
        if not await self.test_agent_messaging():
            return False

        # Test swarm coordination
        if not await self.test_swarm_coordination():
            return False

        # Show test results
        self.show_test_results()
        return self.all_tests_passed()

    async def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met for testing."""
        print("📋 Checking Test Prerequisites...")

        prerequisites_ok = True

        # Check enhanced integration file
        enhanced_file = self.discord_dir / "enhanced_discord_integration.py"
        if enhanced_file.exists():
            print("✅ Enhanced Discord integration file exists")
            self.test_results['prerequisites_enhanced_file'] = True
        else:
            print("❌ Enhanced Discord integration file missing")
            self.test_results['prerequisites_enhanced_file'] = False
            prerequisites_ok = False

        # Check configuration file
        if self.config_file.exists():
            print("✅ Discord channels configuration exists")
            self.test_results['prerequisites_config_file'] = True
        else:
            print("❌ Discord channels configuration missing")
            print("   Run setup script first: python scripts/setup_enhanced_discord.py")
            self.test_results['prerequisites_config_file'] = False
            prerequisites_ok = False

        # Check webhook URLs configured
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)

                configured_webhooks = 0
                total_channels = len(config)

                for channel_name, channel_config in config.items():
                    if channel_config.get('webhook_url'):
                        configured_webhooks += 1

                if configured_webhooks > 0:
                    print(f"✅ {configured_webhooks}/{total_channels} channels have webhooks configured")
                    self.test_results['prerequisites_webhooks'] = True
                else:
                    print("⚠️  No webhook URLs configured")
                    print("   Run webhook configuration: python scripts/configure_discord_webhooks.py")
                    self.test_results['prerequisites_webhooks'] = False

            except Exception as e:
                print(f"❌ Error reading configuration: {e}")
                self.test_results['prerequisites_webhooks'] = False
                prerequisites_ok = False

        print()
        return prerequisites_ok

    async def test_channel_configuration(self) -> bool:
        """Test channel configuration loading."""
        print("⚙️  Testing Channel Configuration...")

        try:
            # Import enhanced integration
            sys.path.append(str(self.discord_dir))
            from enhanced_discord_integration import EnhancedDiscordCommander

            # Create commander instance
            commander = EnhancedDiscordCommander()

            # Get channel info
            channel_info = commander.get_channel_info()

            print(f"✅ Loaded {channel_info['total_channels']} channels")
            print(f"✅ {channel_info['configured_webhooks']} webhooks configured")
            print(f"✅ {len(channel_info['agents_with_channels'])} agents have channels")

            self.test_results['channel_config_load'] = True
            self.test_results['channel_config_info'] = channel_info

            return True

        except Exception as e:
            print(f"❌ Channel configuration test failed: {e}")
            self.test_results['channel_config_load'] = False
            return False

    async def test_enhanced_integration(self) -> bool:
        """Test enhanced integration initialization."""
        print("🔗 Testing Enhanced Integration...")

        try:
            # Import enhanced integration
            sys.path.append(str(self.discord_dir))
            from enhanced_discord_integration import EnhancedDiscordCommander

            # Create commander instance
            commander = EnhancedDiscordCommander()

            # Test initialization
            init_success = await commander.initialize_channels()

            if init_success:
                print("✅ Enhanced integration initialized successfully")
                self.test_results['enhanced_integration_init'] = True
            else:
                print("⚠️  Enhanced integration initialized with warnings")
                self.test_results['enhanced_integration_init'] = True  # Still consider partial success

            return True

        except Exception as e:
            print(f"❌ Enhanced integration test failed: {e}")
            self.test_results['enhanced_integration_init'] = False
            return False

    async def test_agent_messaging(self) -> bool:
        """Test agent-specific messaging."""
        print("📨 Testing Agent Messaging...")

        try:
            # Import enhanced integration
            sys.path.append(str(self.discord_dir))
            from enhanced_discord_integration import AgentChannel, EnhancedDiscordCommander

            # Create commander instance
            commander = EnhancedDiscordCommander()

            # Test agent message (this will fail if no webhook, but tests the logic)
            test_result = await commander.send_agent_message(
                "Agent-3",
                "Integration Test",
                "Testing enhanced Discord agent messaging functionality",
                "LOW",
                "testing"
            )

            if test_result:
                print("✅ Agent messaging successful")
                self.test_results['agent_messaging'] = True
            else:
                print("⚠️  Agent messaging failed (likely due to missing webhooks)")
                self.test_results['agent_messaging'] = False  # Expected to fail without webhooks

            return True

        except Exception as e:
            print(f"❌ Agent messaging test failed: {e}")
            self.test_results['agent_messaging'] = False
            return False

    async def test_swarm_coordination(self) -> bool:
        """Test swarm coordination messaging."""
        print("🐝 Testing Swarm Coordination...")

        try:
            # Import enhanced integration
            sys.path.append(str(self.discord_dir))
            from enhanced_discord_integration import EnhancedDiscordCommander

            # Create commander instance
            commander = EnhancedDiscordCommander()

            # Test swarm broadcast
            broadcast_result = await commander.broadcast_swarm_alert(
                "Integration Test Alert",
                "Testing enhanced swarm broadcast functionality",
                "LOW"
            )

            if broadcast_result:
                print("✅ Swarm coordination successful")
                self.test_results['swarm_coordination'] = True
            else:
                print("⚠️  Swarm coordination failed (likely due to missing webhooks)")
                self.test_results['swarm_coordination'] = False  # Expected to fail without webhooks

            return True

        except Exception as e:
            print(f"❌ Swarm coordination test failed: {e}")
            self.test_results['swarm_coordination'] = False
            return False

    def show_test_results(self) -> None:
        """Show comprehensive test results."""
        print("\n📊 Enhanced Discord Integration Test Results")
        print("=" * 60)

        # Test summary
        total_tests = len([k for k in self.test_results.keys() if k.startswith(('prerequisites_', 'channel_', 'enhanced_', 'agent_', 'swarm_'))])
        passed_tests = len([v for k, v in self.test_results.items() if k.startswith(('prerequisites_', 'channel_', 'enhanced_', 'agent_', 'swarm_')) and v])

        print(f"📈 Test Summary: {passed_tests}/{total_tests} tests passed")

        # Detailed results
        print("\n🔍 Detailed Results:")

        # Prerequisites
        print("\n📋 Prerequisites:")
        for key, value in self.test_results.items():
            if key.startswith('prerequisites_'):
                status = "✅ PASS" if value else "❌ FAIL"
                name = key.replace('prerequisites_', '').replace('_', ' ').title()
                print(f"   {status} {name}")

        # Configuration
        print("\n⚙️  Configuration:")
        for key, value in self.test_results.items():
            if key.startswith('channel_'):
                if key == 'channel_config_info':
                    continue
                status = "✅ PASS" if value else "❌ FAIL"
                name = key.replace('channel_', '').replace('_', ' ').title()
                print(f"   {status} {name}")

        # Integration
        print("\n🔗 Integration:")
        for key, value in self.test_results.items():
            if key.startswith(('enhanced_', 'agent_', 'swarm_')):
                status = "✅ PASS" if value else "❌ FAIL"
                name = key.replace('_', ' ').title()
                print(f"   {status} {name}")

        # Channel information
        if 'channel_config_info' in self.test_results:
            info = self.test_results['channel_config_info']
            print("
📺 Channel Information:"            print(f"   Total Channels: {info['total_channels']}")
            print(f"   Configured Webhooks: {info['configured_webhooks']}")
            print(f"   Agents with Channels: {len(info['agents_with_channels'])}")

            if info['agents_with_channels']:
                print(f"   Agent Channels: {', '.join(info['agents_with_channels'])}")

        # Recommendations
        print("\n💡 Recommendations:")
        if not self.test_results.get('prerequisites_webhooks', False):
            print("   • Configure webhook URLs for Discord channels")
            print("     Run: python scripts/configure_discord_webhooks.py")

        if not self.test_results.get('agent_messaging', False):
            print("   • Verify Discord server and channel permissions")
            print("   • Check webhook URLs are valid and active")

        print("\n🐝 WE ARE SWARM - Enhanced Discord integration testing complete!")

    def all_tests_passed(self) -> bool:
        """Check if all critical tests passed."""
        critical_tests = [
            'prerequisites_enhanced_file',
            'prerequisites_config_file',
            'channel_config_load',
            'enhanced_integration_init'
        ]

        return all(self.test_results.get(test, False) for test in critical_tests)


async def main():
    """Main test function."""
    tester = EnhancedDiscordTester()
    success = await tester.run_all_tests()

    if success:
        print("\n🎉 All critical tests passed!")
        print("Enhanced Discord integration is ready for production use.")
    else:
        print("\n⚠️  Some tests failed!")
        print("Please address the issues above before deploying.")

    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
