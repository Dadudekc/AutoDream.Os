#!/usr/bin/env python3
"""
Agent Devlog System Test
========================

Test script to verify the agent devlog posting functionality.
Tests the standalone Python script approach for agents to post devlogs.

Usage:
    python test_agent_devlog_system.py --test-config
    python test_agent_devlog_system.py --test-posting
    python test_agent_devlog_system.py --test-all
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from argparse import ArgumentParser

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentDevlogTester:
    """Test the agent devlog posting system."""

    def __init__(self):
        """Initialize test system."""
        self.test_agent = "Agent-4"
        self.test_action = "Test devlog posting"
        self.test_status = "completed"
        self.test_details = "Testing the new agent devlog posting system"

    def test_configuration(self):
        """Test configuration loading."""
        print("🔧 Testing Configuration Loading...")
        print("=" * 40)

        try:
            # Test Discord configuration
            bot_token = os.getenv("DISCORD_BOT_TOKEN")
            main_channel_id = os.getenv("DISCORD_CHANNEL_ID")

            if bot_token:
                print("✅ Discord bot token configured")
            else:
                print("⚠️ Discord bot token not configured")

            if main_channel_id:
                print("✅ Main Discord channel configured")
            else:
                print("⚠️ Main Discord channel not configured")

            # Test agent channels
            agent_channels = {}
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                env_var = f"DISCORD_CHANNEL_{agent_id.replace('-', '_')}"
                channel_id = os.getenv(env_var)

                if channel_id:
                    agent_channels[agent_id] = channel_id
                    print(f"✅ {agent_id} channel configured: {channel_id}")
                else:
                    print(f"⚠️ {agent_id} channel not configured")

            print(f"\n📊 Configuration Summary: {len(agent_channels)}/8 agent channels configured")
            return True

        except Exception as e:
            print(f"❌ Configuration test failed: {e}")
            return False

    async def test_devlog_posting(self):
        """Test devlog posting functionality."""
        print("📝 Testing Devlog Posting...")
        print("=" * 40)

        try:
            # Import the agent devlog posting service
            from services.agent_devlog_posting import AgentDevlogPoster

            # Initialize poster
            poster = AgentDevlogPoster()

            print(f"📡 Agent channels loaded: {len(poster.agent_channels)}")

            # Test agent flag validation
            print(f"🔍 Testing agent flag validation for {self.test_agent}...")
            is_valid = poster.validate_agent_flag(self.test_agent)
            print(f"✅ Agent flag validation: {'PASSED' if is_valid else 'FAILED'}")

            if not is_valid:
                return False

            # Test channel routing
            print(f"🔍 Testing channel routing for {self.test_agent}...")
            channel_id = poster.get_agent_channel(self.test_agent)
            if channel_id:
                print(f"✅ Channel routing: {self.test_agent} -> {channel_id}")
            else:
                print(f"⚠️ No channel configured for {self.test_agent}")

            # Test file saving (without Discord posting)
            print("📄 Testing file saving functionality...")
            filepath = poster.save_devlog_file(
                self.test_agent,
                self.test_action,
                self.test_status,
                self.test_details
            )

            if filepath:
                print(f"✅ File saved: {filepath}")
                print("📄 Devlog content preview:")
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    for line in lines[:10]:
                        print(f"   {line}")
                    if len(lines) > 10:
                        print(f"   ... ({len(lines) - 10} more lines)")
            else:
                print("❌ File saving failed")
                return False

            # Test Discord posting (if configured)
            print("📡 Testing Discord posting...")
            discord_success = await poster.post_to_discord(
                self.test_agent,
                self.test_action,
                self.test_status,
                self.test_details
            )

            if discord_success:
                print("✅ Discord posting successful")
            else:
                print("⚠️ Discord posting failed (check configuration)")

            return True

        except Exception as e:
            print(f"❌ Devlog posting test failed: {e}")
            return False

    async def run_all_tests(self):
        """Run all tests."""
        print("🚀 Running Agent Devlog System Tests")
        print("=" * 50)

        # Test configuration
        config_success = self.test_configuration()
        print()

        # Test devlog posting
        posting_success = await self.test_devlog_posting()
        print()

        # Summary
        print("📊 Test Results:")
        print(f"   Configuration: {'✅ PASS' if config_success else '❌ FAIL'}")
        print(f"   Devlog Posting: {'✅ PASS' if posting_success else '❌ FAIL'}")

        overall_success = config_success and posting_success

        if overall_success:
            print("\n🎉 All tests passed! Agent devlog system is ready!")
            print("\n📝 Usage Examples:")
            print(f"   python src/services/agent_devlog_posting.py --agent {self.test_agent} --action \"Task completed\"")
            print("   python src/services/agent_devlog_posting.py --agent Agent-3 --action \"Code review\" --status in_progress --details \"Reviewing pull request\"")
            print("   python src/services/agent_devlog_posting.py --help")
        else:
            print("\n❌ Some tests failed. Check configuration and Discord setup.")

        return overall_success


async def main():
    """Main test function."""
    parser = ArgumentParser(description="Test Agent Devlog System")
    parser.add_argument("--test-config", action="store_true", help="Test configuration only")
    parser.add_argument("--test-posting", action="store_true", help="Test devlog posting only")
    parser.add_argument("--test-all", action="store_true", help="Run all tests")

    args = parser.parse_args()

    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '--help']:
        print(__doc__)
        return 0

    tester = AgentDevlogTester()

    if args.test_config:
        success = tester.test_configuration()
        return 0 if success else 1

    elif args.test_posting:
        success = await tester.test_devlog_posting()
        return 0 if success else 1

    elif args.test_all:
        success = await tester.run_all_tests()
        return 0 if success else 1

    else:
        # Run all tests by default
        success = await tester.run_all_tests()
        return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
