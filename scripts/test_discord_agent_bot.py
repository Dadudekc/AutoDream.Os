#!/usr/bin/env python3
"""
Test Discord Agent Bot - V2 Compliance Module
============================================

Test script for the V2_SWARM Discord Agent Bot functionality.
Tests command parsing, agent communication, and bot operations.

Usage:
    python test_discord_agent_bot.py

Author: Agent-4 (Captain - Discord Integration Coordinator)
License: MIT
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from discord_commander.agent_communication_engine_refactored import AgentCommunicationEngine
    from discord_commander.discord_agent_bot import DiscordAgentBotManager, DiscordCommandParser
except ImportError:
    print("❌ Failed to import test modules")
    sys.exit(1)


class DiscordAgentBotTester:
    """Test suite for Discord Agent Bot functionality."""

    def __init__(self):
        """Initialize tester."""
        self.parser = DiscordCommandParser()
        self.agent_engine = AgentCommunicationEngine()
        self.manager = DiscordAgentBotManager()

    def test_command_parsing(self):
        """Test command parsing functionality."""
        print("🧪 Testing Command Parsing")
        print("=" * 40)

        test_commands = [
            (
                "!prompt @Agent-4 Please analyze the current status",
                "prompt",
                ["Agent-4", "Please analyze the current status"],
            ),
            ("!status @Agent-1", "status", ["Agent-1"]),
            (
                "!swarm Emergency test coverage mission",
                "swarm",
                ["Emergency test coverage mission"],
            ),
            ("!agents", "agents", []),
            ("!help", "help", []),
            ("!ping", "ping", []),
            ("invalid command", "unknown", []),
        ]

        passed = 0
        total = len(test_commands)

        for cmd, expected_type, expected_args in test_commands:
            cmd_type, args, _ = self.parser.parse_command(cmd)

            if cmd_type == expected_type and args == expected_args:
                print(f"✅ PASS: '{cmd}' -> {cmd_type}")
                passed += 1
            else:
                print(f"❌ FAIL: '{cmd}' -> {cmd_type} (expected {expected_type})")
                print(f"   Expected args: {expected_args}")
                print(f"   Got args: {args}")

        print(f"\n📊 Command Parsing: {passed}/{total} tests passed")
        return passed == total

    def test_agent_validation(self):
        """Test agent validation."""
        print("\n🧪 Testing Agent Validation")
        print("=" * 40)

        valid_agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]
        invalid_agents = ["Agent-9", "agent-1", "Agent-0", "Agent-10", "Bob", "Alice"]

        passed = 0
        total = len(valid_agents) + len(invalid_agents)

        for agent in valid_agents:
            if self.agent_engine.is_valid_agent(agent):
                print(f"✅ PASS: {agent} is valid")
                passed += 1
            else:
                print(f"❌ FAIL: {agent} should be valid")

        for agent in invalid_agents:
            if not self.agent_engine.is_valid_agent(agent):
                print(f"✅ PASS: {agent} is correctly invalid")
                passed += 1
            else:
                print(f"❌ FAIL: {agent} should be invalid")

        print(f"\n📊 Agent Validation: {passed}/{total} tests passed")
        return passed == total

    def test_agent_list(self):
        """Test agent listing."""
        print("\n🧪 Testing Agent Listing")
        print("=" * 40)

        agents = self.agent_engine.get_all_agent_names()
        expected_count = 8

        if len(agents) == expected_count:
            print(f"✅ PASS: Found {len(agents)} agents (expected {expected_count})")
            for agent in agents:
                print(f"  • {agent}")
            return True
        else:
            print(f"❌ FAIL: Found {len(agents)} agents (expected {expected_count})")
            return False

    def test_config_loading(self):
        """Test configuration loading."""
        print("\n🧪 Testing Configuration Loading")
        print("=" * 40)

        config = self.manager.load_config()

        if config:
            print("✅ PASS: Configuration loaded successfully")
            print(f"  • Command timeout: {config.get('command_timeout', 'N/A')}")
            print(f"  • Max concurrent commands: {config.get('max_concurrent_commands', 'N/A')}")
            print(f"  • Allowed channels: {len(config.get('allowed_channels', []))}")
            print(f"  • Admin users: {len(config.get('admin_users', []))}")
            return True
        else:
            print("❌ FAIL: Configuration loading failed")
            return False

    async def test_agent_communication_simulation(self):
        """Test agent communication simulation."""
        print("\n🧪 Testing Agent Communication (Simulation)")
        print("=" * 40)

        test_agent = "Agent-4"
        test_message = "Test message from Discord bot"
        test_sender = "Discord_Test_User"

        try:
            result = await self.agent_engine.send_to_agent_inbox(
                test_agent, test_message, test_sender
            )

            if result.success:
                print("✅ PASS: Agent communication simulation successful")
                print(f"  • Message sent to {test_agent}'s inbox")
                print(f"  • Filename: {result.data.get('filename', 'N/A')}")
                return True
            else:
                print(f"❌ FAIL: Agent communication failed: {result.message}")
                return False

        except Exception as e:
            print(f"❌ FAIL: Agent communication error: {e}")
            return False

    def run_all_tests(self):
        """Run all tests."""
        print("🐝 V2_SWARM Discord Agent Bot Test Suite")
        print("=" * 60)

        # Synchronous tests
        test1 = self.test_command_parsing()
        test2 = self.test_agent_validation()
        test3 = self.test_agent_list()
        test4 = self.test_config_loading()

        # Asynchronous tests
        async def run_async_tests():
            test5 = await self.test_agent_communication_simulation()
            return test5

        test5 = asyncio.run(run_async_tests())

        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)

        tests = [
            ("Command Parsing", test1),
            ("Agent Validation", test2),
            ("Agent Listing", test3),
            ("Config Loading", test4),
            ("Agent Communication", test5),
        ]

        passed = 0
        for test_name, result in tests:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
            if result:
                passed += 1

        print(f"\n🎯 Overall: {passed}/{len(tests)} test suites passed")

        if passed == len(tests):
            print("🎉 All tests PASSED! Discord Agent Bot is ready!")
            return True
        else:
            print("⚠️  Some tests failed. Please check the issues above.")
            return False


def main():
    """Main test function."""
    tester = DiscordAgentBotTester()
    success = tester.run_all_tests()

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
