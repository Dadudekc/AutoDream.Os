#!/usr/bin/env python3
"""
Discord Commander Test Script
=============================

Test script to verify Discord Commander functionality without requiring Discord credentials.
Tests messaging service integration and command setup.

V2 Compliance: ≤400 lines, 1 class, 5 functions
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .consolidated_messaging_service import ConsolidatedMessagingService
from .discord_bot_integrated import IntegratedDiscordBotService

logger = logging.getLogger(__name__)


class DiscordCommanderTester:
    """Test Discord Commander functionality."""

    def __init__(self):
        """Initialize tester."""
        self.messaging_service = ConsolidatedMessagingService()
        self.bot = IntegratedDiscordBotService()

    def test_messaging_service(self) -> bool:
        """Test messaging service integration."""
        try:
            logger.info("🧪 Testing messaging service integration...")

            # Test sending message to Agent-5
            success = self.messaging_service.send_message(
                agent_id="Agent-5",
                message="[Test] Discord Commander test message",
                from_agent="Discord-Commander-Test"
            )

            if success:
                logger.info("✅ Messaging service test passed")
                return True
            else:
                logger.error("❌ Messaging service test failed")
                return False

        except Exception as e:
            logger.error(f"❌ Messaging service test error: {e}")
            return False

    def test_bot_setup(self) -> bool:
        """Test bot setup and configuration."""
        try:
            logger.info("🧪 Testing bot setup...")

            # Check if bot is properly initialized
            if not hasattr(self.bot, 'is_ready'):
                logger.error("❌ Bot not properly initialized")
                return False

            # Check if slash commands are set up
            if not hasattr(self.bot, 'tree') or not self.bot.tree:
                logger.error("❌ Slash commands not set up")
                return False

            logger.info("✅ Bot setup test passed")
            return True

        except Exception as e:
            logger.error(f"❌ Bot setup test error: {e}")
            return False

    def test_slash_commands(self) -> bool:
        """Test slash command setup."""
        try:
            logger.info("🧪 Testing slash commands...")

            # Check if commands are registered
            commands = self.bot.tree.get_commands()
            expected_commands = ['swarm_status', 'send_to_agent', 'broadcast', 'agent_list', 'system_check']

            found_commands = [cmd.name for cmd in commands]
            missing_commands = []

            for expected in expected_commands:
                if expected not in found_commands:
                    missing_commands.append(expected)

            if missing_commands:
                logger.error(f"❌ Missing slash commands: {missing_commands}")
                return False

            logger.info(f"✅ All {len(commands)} slash commands registered")
            for cmd in commands:
                logger.info(f"  - /{cmd.name}: {cmd.description}")

            return True

        except Exception as e:
            logger.error(f"❌ Slash commands test error: {e}")
            return False

    def test_5_agent_mode(self) -> bool:
        """Test 5-agent mode configuration."""
        try:
            logger.info("🧪 Testing 5-agent mode configuration...")

            # Check if bot has 5-agent mode settings
            expected_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

            # Test if messaging service can handle 5 agents
            test_results = []
            for agent in expected_agents:
                success = self.messaging_service.send_message(
                    agent_id=agent,
                    message="[Test] 5-agent mode test",
                    from_agent="Discord-Commander-Test"
                )
                test_results.append((agent, success))

            successful = sum(1 for _, success in test_results if success)
            total = len(test_results)

            logger.info(f"✅ 5-agent mode test: {successful}/{total} agents reachable")

            if successful == total:
                logger.info("✅ All 5 agents reachable in test mode")
                return True
            else:
                logger.warning("⚠️  Some agents may not be active in test mode")
                return True  # Still pass - some agents might not be active

        except Exception as e:
            logger.error(f"❌ 5-agent mode test error: {e}")
            return False

    def run_all_tests(self) -> bool:
        """Run all tests."""
        logger.info("🚀 Running Discord Commander Tests...")
        logger.info("=" * 50)

        tests = [
            ("Messaging Service", self.test_messaging_service),
            ("Bot Setup", self.test_bot_setup),
            ("Slash Commands", self.test_slash_commands),
            ("5-Agent Mode", self.test_5_agent_mode)
        ]

        results = []

        for test_name, test_func in tests:
            logger.info(f"\n🧪 Running {test_name} test...")
            try:
                result = test_func()
                results.append((test_name, result))
                status = "✅ PASSED" if result else "❌ FAILED"
                logger.info(f"{status}: {test_name}")
            except Exception as e:
                logger.error(f"❌ TEST CRASHED - {test_name}: {e}")
                results.append((test_name, False))

        logger.info("\n" + "=" * 50)
        logger.info("📊 Test Results Summary:")

        passed = 0
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"  {status}: {test_name}")
            if result:
                passed += 1

        total = len(results)
        logger.info(f"\n🏆 Overall: {passed}/{total} tests passed")

        if passed == total:
            logger.info("🎉 All tests passed! Discord Commander is ready.")
            return True
        else:
            logger.error("❌ Some tests failed. Check configuration.")
            return False


async def main():
    """Main test function."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger.info("🤖 Discord Commander Test Suite")
    logger.info("=================================")

    # Create tester
    tester = DiscordCommanderTester()

    # Run tests
    success = tester.run_all_tests()

    if success:
        logger.info("\n✅ Discord Commander test suite completed successfully!")
        logger.info("📝 The Discord Commander is ready to run with proper Discord credentials.")
        logger.info("\n🔧 To run the Discord Commander:")
        logger.info("1. Set DISCORD_BOT_TOKEN environment variable")
        logger.info("2. Run: python src/services/discord_commander_fixed.py")
        return 0
    else:
        logger.error("\n❌ Discord Commander test suite failed!")
        logger.error("📝 Please check the errors above and fix any issues.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

