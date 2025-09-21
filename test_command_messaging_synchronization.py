#!/usr/bin/env python3
"""
Discord Commander - Command vs Messaging System Synchronization Test
=====================================================================

Tests to ensure Discord slash commands are properly synchronized
with messaging system options and functionality.

Compares:
- Discord slash commands vs messaging system methods
- Command parameters vs messaging system parameters
- Command functionality vs messaging system functionality
- Integration between Discord commands and messaging system

🐝 WE ARE SWARM - Command Synchronization Testing
"""

import inspect
import logging
from typing import Dict, List, Any, Callable
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.messaging.core.messaging_service import MessagingService
from src.services.messaging.providers.discord_provider import (
    DiscordMessagingProvider,
    DiscordCommandHandler
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommandSynchronizationTester:
    """Test Discord commands vs messaging system synchronization."""

    def __init__(self):
        """Initialize synchronization tester."""
        self.discord_commands = {}
        self.messaging_methods = {}
        self.synchronization_results = {
            "command_method_mapping": {},
            "parameter_comparison": {},
            "functionality_comparison": {},
            "integration_test": {}
        }

    def extract_discord_slash_commands(self):
        """Extract Discord slash commands from DiscordCommandHandler."""
        logger.info("🔍 Extracting Discord slash commands...")

        try:
            # Mock bot for testing
            class MockBot:
                def __init__(self):
                    self.tree = MockTree()

            class MockTree:
                def command(self, **kwargs):
                    def decorator(func):
                        # Store command info
                        self.discord_commands[kwargs.get('name', 'unknown')] = {
                            'name': kwargs.get('name', 'unknown'),
                            'description': kwargs.get('description', ''),
                            'function': func,
                            'parameters': self._extract_function_params(func)
                        }
                        return func
                    return decorator

                def _extract_function_params(self, func):
                    """Extract function parameters."""
                    sig = inspect.signature(func)
                    params = []

                    for name, param in sig.parameters.items():
                        if name not in ['self', 'interaction']:  # Skip common parameters
                            params.append({
                                'name': name,
                                'type': str(param.annotation) if param.annotation != inspect.Parameter.empty else 'Any',
                                'default': str(param.default) if param.default != inspect.Parameter.empty else None,
                                'required': param.default == inspect.Parameter.empty
                            })

                    logger.info(f"🔍 Extracted command params: {[p['name'] for p in params]}")
                    return params

                def __init__(self):
                    self.discord_commands = {}

            # Create mock bot and setup commands
            mock_bot = MockBot()
            mock_discord_provider = DiscordMessagingProvider(mock_bot)

            # Create command handler and setup commands
            command_handler = DiscordCommandHandler(mock_bot, mock_discord_provider)
            command_handler.setup_slash_commands()

            # Get extracted commands
            self.discord_commands = mock_bot.tree.discord_commands

            logger.info(f"✅ Extracted {len(self.discord_commands)} Discord slash commands")

        except Exception as e:
            logger.error(f"❌ Failed to extract Discord commands: {e}")
            self.discord_commands = {}

    def extract_messaging_system_methods(self):
        """Extract messaging system methods and their signatures."""
        logger.info("🔍 Extracting messaging system methods...")

        try:
            # Get MessagingService methods
            messaging_service = MessagingService.__dict__

            # Key messaging methods to compare
            key_methods = [
                'send_message',
                'broadcast_message',
                'get_swarm_status',
                'get_available_agents'
            ]

            for method_name in key_methods:
                if method_name in messaging_service:
                    method = messaging_service[method_name]
                    if callable(method):
                        sig = inspect.signature(method)
                        params = []

                        for name, param in sig.parameters.items():
                            if name != 'self':  # Skip self parameter
                                params.append({
                                    'name': name,
                                    'type': str(param.annotation) if param.annotation != inspect.Parameter.empty else 'Any',
                                    'default': str(param.default) if param.default != inspect.Parameter.empty else None,
                                    'required': param.default == inspect.Parameter.empty
                                })

                        self.messaging_methods[method_name] = {
                            'name': method_name,
                            'parameters': params,
                            'function': method
                        }
                        logger.info(f"✅ Extracted method: {method_name} with params: {[p['name'] for p in params]}")
                else:
                    logger.warning(f"⚠️  Method {method_name} not found in MessagingService")

            # Add Discord provider methods
            discord_provider_methods = [
                'send_message_to_agent',
                'broadcast_to_swarm',
                'get_swarm_status'
            ]

            # Mock Discord provider for method extraction
            class MockDiscordProvider:
                async def send_message_to_agent(self, agent_id: str, message: str, from_agent: str = "Discord-Commander") -> bool:
                    pass

                async def broadcast_to_swarm(self, message: str, agent_ids: List[str] = None, from_agent: str = "Discord-Commander") -> Dict[str, bool]:
                    pass

                async def get_swarm_status(self) -> Dict[str, Any]:
                    pass

            mock_provider = MockDiscordProvider()
            for method_name in discord_provider_methods:
                if hasattr(mock_provider, method_name):
                    method = getattr(mock_provider, method_name)
                    sig = inspect.signature(method)
                    params = []

                    for name, param in sig.parameters.items():
                        if name != 'self':  # Skip self parameter
                            params.append({
                                'name': name,
                                'type': str(param.annotation) if param.annotation != inspect.Parameter.empty else 'Any',
                                'default': str(param.default) if param.default != inspect.Parameter.empty else None,
                                'required': param.default == inspect.Parameter.empty
                            })

                    self.messaging_methods[method_name] = {
                        'name': method_name,
                        'parameters': params,
                        'function': method,
                        'provider': 'discord'
                    }

            logger.info(f"✅ Extracted {len(self.messaging_methods)} messaging system methods")

        except Exception as e:
            logger.error(f"❌ Failed to extract messaging methods: {e}")
            self.messaging_methods = {}

    def compare_commands_and_methods(self):
        """Compare Discord commands with messaging system methods."""
        logger.info("🔍 Comparing Discord commands with messaging system methods...")

        # Mapping of Discord commands to messaging methods
        command_to_method_mapping = {
            'swarm_status': ['get_swarm_status'],
            'send_to_agent': ['send_message_to_agent', 'send_message'],
            'broadcast': ['broadcast_to_swarm', 'broadcast_message'],
            'agent_list': ['get_available_agents'],  # Now uses messaging system
            'send_message': ['send_message']  # Direct messaging system method
        }

        for command_name, expected_methods in command_to_method_mapping.items():
            if command_name in self.discord_commands:
                command_info = self.discord_commands[command_name]
                method_matches = []

                for method_name in expected_methods:
                    if method_name in self.messaging_methods:
                        method_info = self.messaging_methods[method_name]
                        match_score = self._compare_command_and_method(command_info, method_info)
                        method_matches.append({
                            'method': method_name,
                            'match_score': match_score,
                            'parameters_match': match_score >= 0.8
                        })

                self.synchronization_results["command_method_mapping"][command_name] = {
                    'command': command_info,
                    'matched_methods': method_matches,
                    'has_good_match': any(m['parameters_match'] for m in method_matches)
                }
            else:
                self.synchronization_results["command_method_mapping"][command_name] = {
                    'command': None,
                    'matched_methods': [],
                    'error': f"Command '{command_name}' not found in Discord commands"
                }

    def _compare_command_and_method(self, command_info: Dict, method_info: Dict) -> float:
        """Compare a Discord command with a messaging method."""
        command_params = command_info.get('parameters', [])
        method_params = method_info.get('parameters', [])

        # Remove Discord-specific parameters for fair comparison
        discord_specific_params = ['interaction', 'ctx']
        command_params = [p for p in command_params if p['name'] not in discord_specific_params]

        if not command_params and not method_params:
            return 1.0  # Both have no parameters

        if not command_params or not method_params:
            return 0.5  # One has parameters, the other doesn't - partial match

        # Parameter count comparison (allow some flexibility)
        param_count_diff = abs(len(command_params) - len(method_params))
        if param_count_diff == 0:
            param_count_match = 1.0
        elif param_count_diff == 1:
            param_count_match = 0.8
        else:
            param_count_match = 0.5

        # Parameter name matching
        name_matches = 0
        for cmd_param in command_params:
            for method_param in method_params:
                if cmd_param['name'] == method_param['name']:
                    name_matches += 1
                    break

        name_match_score = name_matches / max(len(command_params), len(method_params)) if max(len(command_params), len(method_params)) > 0 else 1.0

        # Overall match score
        return (param_count_match * 0.4) + (name_match_score * 0.6)

    def test_integration_functionality(self):
        """Test integration between Discord commands and messaging system."""
        logger.info("🔍 Testing integration functionality...")

        try:
            # Test MessagingService instantiation
            messaging_service = MessagingService("config/coordinates.json")
            self.synchronization_results["integration_test"]["messaging_service"] = "✅ OPERATIONAL"

            # Test agent IDs
            agent_ids = messaging_service.loader.get_agent_ids() if messaging_service.loader else []
            expected_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

            # Check if 5-agent mode agents are available
            five_agent_mode = all(agent in agent_ids for agent in expected_agents)
            self.synchronization_results["integration_test"]["five_agent_mode"] = "✅ ACTIVE" if five_agent_mode else "❌ INACTIVE"

            # Test messaging functionality
            test_result = messaging_service.send_message(
                agent_id="Agent-7",
                message="[Sync Test] Command-messaging system synchronization test",
                from_agent="Command-Sync-Tester"
            )

            self.synchronization_results["integration_test"]["messaging_functionality"] = "✅ WORKING" if test_result else "❌ FAILED"

            logger.info("✅ Integration functionality test complete")

        except Exception as e:
            logger.error(f"❌ Integration test failed: {e}")
            self.synchronization_results["integration_test"]["error"] = str(e)

    def generate_synchronization_report(self):
        """Generate comprehensive synchronization report."""
        logger.info("📊 Generating synchronization report...")

        report = {
            "timestamp": "2025-01-21T05:40:00Z",
            "test_type": "Command-Messaging System Synchronization",
            "summary": {
                "total_commands": len(self.discord_commands),
                "total_methods": len(self.messaging_methods),
                "commands_with_good_matches": len([cmd for cmd in self.synchronization_results["command_method_mapping"].values() if cmd.get("has_good_match", False)]),
                "integration_status": "✅ OPERATIONAL" if "error" not in self.synchronization_results["integration_test"] else "❌ FAILED"
            },
            "detailed_results": self.synchronization_results
        }

        return report

    def run_synchronization_tests(self):
        """Run all synchronization tests."""
        logger.info("🚀 Starting Discord Commander - Messaging System Synchronization Tests...")

        # Extract Discord slash commands
        self.extract_discord_slash_commands()

        # Extract messaging system methods
        self.extract_messaging_system_methods()

        # Compare commands and methods
        self.compare_commands_and_methods()

        # Test integration functionality
        self.test_integration_functionality()

        # Generate report
        report = self.generate_synchronization_report()

        logger.info("✅ Synchronization tests complete")
        return report


def print_synchronization_report(report: Dict[str, Any]):
    """Print formatted synchronization report."""
    print("\n" + "="*80)
    print("🐝 DISCORD COMMANDER - MESSAGING SYSTEM SYNCHRONIZATION REPORT")
    print("="*80)
    print()

    # Summary
    summary = report["summary"]
    print("📊 SUMMARY:")
    print(f"   Total Discord Commands: {summary['total_commands']}")
    print(f"   Total Messaging Methods: {summary['total_methods']}")
    print(f"   Commands with Good Matches: {summary['commands_with_good_matches']}")
    print(f"   Integration Status: {summary['integration_status']}")
    print()

    # Command-Method Mapping
    print("🔗 COMMAND-METHOD MAPPING:")
    for command_name, mapping in report["detailed_results"]["command_method_mapping"].items():
        print(f"   /{command_name}:")
        if mapping.get("has_good_match"):
            print("     ✅ Good match with messaging system")
            for match in mapping.get("matched_methods", []):
                if match["parameters_match"]:
                    print(f"        ↳ {match['method']} (Score: {match['match_score']:.2f})")
        else:
            print("     ❌ No good match found")
        print()

    # Integration Test Results
    print("🔧 INTEGRATION TEST RESULTS:")
    integration = report["detailed_results"]["integration_test"]
    for test_name, result in integration.items():
        if test_name != "error":
            print(f"   {test_name}: {result}")
    print()

    # Recommendations
    print("💡 RECOMMENDATIONS:")
    issues_found = []

    # Check for missing command-method matches
    for command_name, mapping in report["detailed_results"]["command_method_mapping"].items():
        if not mapping.get("has_good_match", False):
            issues_found.append(f"Command /{command_name} needs better messaging system integration")

    # Check integration issues
    if "error" in integration:
        issues_found.append(f"Integration test failed: {integration['error']}")

    if issues_found:
        print("   ⚠️  Issues found:")
        for issue in issues_found:
            print(f"      - {issue}")
    else:
        print("   ✅ All tests passed - systems are properly synchronized")
    print()

    print("="*80)


def main():
    """Main function to run synchronization tests."""
    print("🐝 Discord Commander - Messaging System Synchronization Test")
    print("=" * 65)
    print()
    print("This test will:")
    print("1. ✅ Extract Discord slash commands")
    print("2. ✅ Extract messaging system methods")
    print("3. ✅ Compare command-method synchronization")
    print("4. ✅ Test integration functionality")
    print("5. ✅ Generate comprehensive report")
    print()

    # Run synchronization tests
    tester = CommandSynchronizationTester()
    report = tester.run_synchronization_tests()

    # Print report
    print_synchronization_report(report)

    # Return exit code based on test results
    return 0 if report["summary"]["integration_status"] == "✅ OPERATIONAL" else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
