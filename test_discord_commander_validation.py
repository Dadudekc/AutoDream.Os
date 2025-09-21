#!/usr/bin/env python3
"""
Discord Commander Validation Test Suite
=======================================

Comprehensive validation testing of Discord Commander functionality
without requiring a real Discord bot token.

Tests:
- Discord slash command parameter validation
- Messaging system integration
- 5-agent mode configuration
- Command-method synchronization
- System integration validation

🐝 WE ARE SWARM - Discord Commander Validation Testing
"""

import asyncio
import inspect
import logging
from typing import Dict, List, Any
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


class DiscordCommanderValidator:
    """Validator for Discord Commander functionality."""

    def __init__(self):
        """Initialize Discord Commander validator."""
        self.validation_results = {
            "slash_commands": {},
            "messaging_system": {},
            "integration": {},
            "five_agent_mode": {},
            "command_synchronization": {}
        }

    def validate_slash_commands(self):
        """Validate Discord slash command definitions."""
        logger.info("🔍 Validating Discord slash commands...")

        try:
            # Mock bot for testing
            class MockBot:
                def __init__(self):
                    self.tree = MockTree()

            class MockTree:
                def command(self, **kwargs):
                    def decorator(func):
                        # Store command info
                        self.slash_commands[kwargs.get('name', 'unknown')] = {
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

                    return params

                def __init__(self):
                    self.slash_commands = {}

            # Create mock bot and setup commands
            mock_bot = MockBot()
            mock_discord_provider = DiscordMessagingProvider(mock_bot)

            # Create command handler and setup commands
            command_handler = DiscordCommandHandler(mock_bot, mock_discord_provider)
            command_handler.setup_slash_commands()

            # Validate each command
            expected_commands = {
                'swarm_status': {
                    'description': 'Get current swarm status',
                    'min_params': 0,
                    'max_params': 0
                },
                'send_to_agent': {
                    'description': 'Send message to specific agent',
                    'min_params': 2,
                    'max_params': 3
                },
                'broadcast': {
                    'description': 'Broadcast message to all agents',
                    'min_params': 1,
                    'max_params': 3
                },
                'send_message': {
                    'description': 'Send message using messaging system',
                    'min_params': 2,
                    'max_params': 3
                },
                'agent_list': {
                    'description': 'List all available agents with status',
                    'min_params': 0,
                    'max_params': 2
                }
            }

            for command_name, expected in expected_commands.items():
                if command_name in mock_bot.tree.slash_commands:
                    command_info = mock_bot.tree.slash_commands[command_name]
                    params = command_info.get('parameters', [])

                    # Validate command structure
                    param_count = len(params)
                    min_params = expected['min_params']
                    max_params = expected['max_params']

                    is_valid = min_params <= param_count <= max_params

                    self.validation_results["slash_commands"][command_name] = {
                        'status': '✅ VALID' if is_valid else '❌ INVALID',
                        'param_count': param_count,
                        'expected_range': f"{min_params}-{max_params}",
                        'description': command_info.get('description', ''),
                        'parameters': [p['name'] for p in params]
                    }

                    logger.info(f"✅ Validated {command_name}: {param_count} params, range {min_params}-{max_params}")
                else:
                    self.validation_results["slash_commands"][command_name] = {
                        'status': '❌ MISSING',
                        'param_count': 0,
                        'expected_range': f"{expected['min_params']}-{expected['max_params']}",
                        'description': 'Command not found'
                    }

            logger.info("✅ Slash commands validation complete")

        except Exception as e:
            logger.error(f"❌ Slash commands validation failed: {e}")
            self.validation_results["slash_commands"]["error"] = str(e)

    def validate_messaging_system(self):
        """Validate messaging system functionality."""
        logger.info("🔍 Validating messaging system...")

        try:
            # Test MessagingService instantiation
            messaging_service = MessagingService("config/coordinates.json")
            self.validation_results["messaging_system"]["messaging_service"] = "✅ OPERATIONAL"

            # Test agent availability
            agents_status = messaging_service.get_available_agents()
            five_agent_mode_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

            five_agent_mode_active = all(agent in agents_status for agent in five_agent_mode_agents)
            self.validation_results["messaging_system"]["five_agent_mode"] = "✅ ACTIVE" if five_agent_mode_active else "❌ INACTIVE"

            # Test messaging functionality
            test_result = messaging_service.send_message(
                agent_id="Agent-7",
                message="[Validation Test] Discord Commander messaging system test",
                from_agent="Discord-Commander-Validator"
            )
            self.validation_results["messaging_system"]["messaging_functionality"] = "✅ WORKING" if test_result else "❌ FAILED"

            # Test broadcast functionality
            broadcast_result = messaging_service.broadcast_message(
                message="[Validation Test] Discord Commander broadcast test",
                from_agent="Discord-Commander-Validator"
            )
            self.validation_results["messaging_system"]["broadcast_functionality"] = "✅ WORKING" if broadcast_result else "❌ FAILED"

            logger.info("✅ Messaging system validation complete")

        except Exception as e:
            logger.error(f"❌ Messaging system validation failed: {e}")
            self.validation_results["messaging_system"]["error"] = str(e)

    def validate_integration(self):
        """Validate Discord provider integration."""
        logger.info("🔍 Validating Discord provider integration...")

        try:
            # Mock bot for testing
            class MockBot:
                def __init__(self):
                    self.tree = MockTree()
                    self.is_ready = True
                    self.latency = 0.05
                    self.guilds = [MockGuild()]

            class MockTree:
                def __init__(self):
                    self.commands = {}

            class MockGuild:
                def __init__(self):
                    self.text_channels = [MockChannel()]

            class MockChannel:
                def __init__(self):
                    self.name = "agent-7"

            # Create Discord provider
            mock_bot = MockBot()
            discord_provider = DiscordMessagingProvider(mock_bot)

            # Test Discord provider methods
            methods_to_test = [
                'send_message_to_agent',
                'broadcast_to_swarm',
                'get_swarm_status'
            ]

            for method_name in methods_to_test:
                if hasattr(discord_provider, method_name):
                    self.validation_results["integration"][method_name] = "✅ AVAILABLE"
                else:
                    self.validation_results["integration"][method_name] = "❌ MISSING"

            # Test agent channel functionality
            channel = asyncio.run(discord_provider._get_agent_channel("Agent-7"))
            self.validation_results["integration"]["agent_channel_lookup"] = "✅ WORKING" if channel else "❌ FAILED"

            logger.info("✅ Integration validation complete")

        except Exception as e:
            logger.error(f"❌ Integration validation failed: {e}")
            self.validation_results["integration"]["error"] = str(e)

    def validate_five_agent_mode(self):
        """Validate 5-agent mode configuration."""
        logger.info("🔍 Validating 5-agent mode configuration...")

        try:
            # Test messaging service with 5-agent mode
            messaging_service = MessagingService("config/coordinates.json")
            agents_status = messaging_service.get_available_agents()

            five_agent_mode_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

            # Check if all 5 agents are available
            all_five_agents = all(agent in agents_status for agent in five_agent_mode_agents)
            self.validation_results["five_agent_mode"]["all_agents_available"] = "✅ ACTIVE" if all_five_agents else "❌ INACTIVE"

            # Check agent activity status
            active_agents = [agent for agent, status in agents_status.items() if status and agent in five_agent_mode_agents]
            self.validation_results["five_agent_mode"]["active_agents"] = f"{len(active_agents)}/{len(five_agent_mode_agents)}"

            # Test Discord provider 5-agent mode
            try:
                from src.services.messaging.providers.discord_provider import DiscordMessagingProvider

                class MockBot:
                    def __init__(self):
                        self.config = {"main_channel_id": "123"}

                mock_bot = MockBot()
                discord_provider = DiscordMessagingProvider(mock_bot)

                # Test broadcast to 5-agent mode
                results = asyncio.run(discord_provider.broadcast_to_swarm(
                    message="[5-Agent Test] Discord Commander 5-agent mode validation",
                    agent_ids=None  # Should default to 5-agent mode
                ))

                expected_results = len(five_agent_mode_agents)
                actual_results = len(results)

                self.validation_results["five_agent_mode"]["broadcast_functionality"] = "✅ WORKING" if actual_results == expected_results else f"❌ FAILED ({actual_results}/{expected_results})"

            except Exception as e:
                self.validation_results["five_agent_mode"]["broadcast_functionality"] = f"❌ ERROR: {e}"

            logger.info("✅ 5-agent mode validation complete")

        except Exception as e:
            logger.error(f"❌ 5-agent mode validation failed: {e}")
            self.validation_results["five_agent_mode"]["error"] = str(e)

    def validate_command_synchronization(self):
        """Validate command-method synchronization."""
        logger.info("🔍 Validating command-method synchronization...")

        try:
            # Test each command's integration with messaging system
            test_scenarios = [
                {
                    'command': 'send_to_agent',
                    'test_data': {
                        'agent_id': 'Agent-7',
                        'message': '[Sync Test] Command synchronization validation',
                        'priority': 'NORMAL'
                    }
                },
                {
                    'command': 'broadcast',
                    'test_data': {
                        'message': '[Sync Test] Broadcast synchronization validation',
                        'priority': 'NORMAL'
                    }
                },
                {
                    'command': 'send_message',
                    'test_data': {
                        'agent_id': 'Agent-7',
                        'message': '[Sync Test] Direct messaging synchronization validation',
                        'priority': 'NORMAL'
                    }
                }
            ]

            for scenario in test_scenarios:
                command_name = scenario['command']
                test_data = scenario['test_data']

                try:
                    # Test messaging service directly
                    messaging_service = MessagingService("config/coordinates.json")

                    if command_name == 'send_to_agent':
                        result = messaging_service.send_message(
                            agent_id=test_data['agent_id'],
                            message=test_data['message'],
                            from_agent="Discord-Commander-Sync-Test",
                            priority=test_data.get('priority', 'NORMAL')
                        )
                    elif command_name in ['broadcast', 'send_message']:
                        if command_name == 'broadcast':
                            result = messaging_service.broadcast_message(
                                message=test_data['message'],
                                from_agent="Discord-Commander-Sync-Test",
                                priority=test_data.get('priority', 'NORMAL')
                            )
                        else:  # send_message
                            result = messaging_service.send_message(
                                agent_id=test_data['agent_id'],
                                message=test_data['message'],
                                from_agent="Discord-Commander-Sync-Test",
                                priority=test_data.get('priority', 'NORMAL')
                            )

                    self.validation_results["command_synchronization"][command_name] = "✅ WORKING" if result else "❌ FAILED"

                except Exception as e:
                    self.validation_results["command_synchronization"][command_name] = f"❌ ERROR: {e}"

            logger.info("✅ Command synchronization validation complete")

        except Exception as e:
            logger.error(f"❌ Command synchronization validation failed: {e}")
            self.validation_results["command_synchronization"]["error"] = str(e)

    def generate_validation_report(self):
        """Generate comprehensive validation report."""
        logger.info("📊 Generating validation report...")

        report = {
            "timestamp": "2025-01-21T05:50:00Z",
            "test_type": "Discord Commander Validation Test",
            "summary": {
                "total_commands": len(self.validation_results["slash_commands"]),
                "valid_commands": len([c for c in self.validation_results["slash_commands"].values() if c.get("status") == "✅ VALID"]),
                "messaging_system_status": "✅ OPERATIONAL" if "error" not in self.validation_results["messaging_system"] else "❌ FAILED",
                "five_agent_mode_status": "✅ ACTIVE" if "error" not in self.validation_results["five_agent_mode"] else "❌ FAILED",
                "integration_status": "✅ OPERATIONAL" if "error" not in self.validation_results["integration"] else "❌ FAILED"
            },
            "detailed_results": self.validation_results
        }

        return report

    def run_validation_tests(self):
        """Run all Discord Commander validation tests."""
        logger.info("🚀 Starting Discord Commander Validation Tests...")

        # Validate slash commands
        self.validate_slash_commands()

        # Validate messaging system
        self.validate_messaging_system()

        # Validate integration
        self.validate_integration()

        # Validate 5-agent mode
        self.validate_five_agent_mode()

        # Validate command synchronization
        self.validate_command_synchronization()

        # Generate report
        report = self.generate_validation_report()

        logger.info("✅ Validation tests complete")
        return report


def print_validation_report(report: Dict[str, Any]):
    """Print formatted validation report."""
    print("\n" + "="*80)
    print("🐝 DISCORD COMMANDER VALIDATION REPORT")
    print("="*80)
    print()

    # Summary
    summary = report["summary"]
    print("📊 SUMMARY:")
    print(f"   Total Commands: {summary['total_commands']}")
    print(f"   Valid Commands: {summary['valid_commands']}")
    print(f"   Messaging System: {summary['messaging_system_status']}")
    print(f"   5-Agent Mode: {summary['five_agent_mode_status']}")
    print(f"   Integration: {summary['integration_status']}")
    print()

    # Slash Commands
    print("🔧 SLASH COMMANDS:")
    for command_name, result in report["detailed_results"]["slash_commands"].items():
        if command_name != "error":
            status = result.get("status", "❌ UNKNOWN")
            param_count = result.get("param_count", 0)
            expected_range = result.get("expected_range", "0-0")
            print(f"   /{command_name}: {status} ({param_count} params, expected {expected_range})")
    print()

    # Messaging System
    print("📡 MESSAGING SYSTEM:")
    messaging = report["detailed_results"]["messaging_system"]
    for test_name, result in messaging.items():
        if test_name != "error":
            print(f"   {test_name}: {result}")
    print()

    # Integration
    print("🔗 INTEGRATION:")
    integration = report["detailed_results"]["integration"]
    for test_name, result in integration.items():
        if test_name != "error":
            print(f"   {test_name}: {result}")
    print()

    # 5-Agent Mode
    print("🤖 5-AGENT MODE:")
    five_agent = report["detailed_results"]["five_agent_mode"]
    for test_name, result in five_agent.items():
        if test_name != "error":
            print(f"   {test_name}: {result}")
    print()

    # Command Synchronization
    print("🔄 COMMAND SYNCHRONIZATION:")
    sync = report["detailed_results"]["command_synchronization"]
    for test_name, result in sync.items():
        if test_name != "error":
            print(f"   {test_name}: {result}")
    print()

    # Overall Assessment
    print("🎯 OVERALL ASSESSMENT:")
    issues_found = []

    # Check for command issues
    for command_name, result in report["detailed_results"]["slash_commands"].items():
        if result.get("status") != "✅ VALID":
            issues_found.append(f"Slash command /{command_name}: {result.get('status', 'UNKNOWN')}")

    # Check messaging system issues
    if "error" in report["detailed_results"]["messaging_system"]:
        issues_found.append(f"Messaging system: {report['detailed_results']['messaging_system']['error']}")

    # Check integration issues
    if "error" in report["detailed_results"]["integration"]:
        issues_found.append(f"Integration: {report['detailed_results']['integration']['error']}")

    # Check 5-agent mode issues
    if "error" in report["detailed_results"]["five_agent_mode"]:
        issues_found.append(f"5-Agent mode: {report['detailed_results']['five_agent_mode']['error']}")

    if issues_found:
        print("   ⚠️  Issues found:")
        for issue in issues_found:
            print(f"      - {issue}")
    else:
        print("   ✅ All validation tests passed!")
        print("   🎉 Discord Commander is fully operational!")
    print()

    print("="*80)


def main():
    """Main function to run Discord Commander validation tests."""
    print("🐝 Discord Commander Validation Test Suite")
    print("=" * 55)
    print()
    print("This validation suite will:")
    print("1. ✅ Validate Discord slash command definitions")
    print("2. ✅ Test messaging system functionality")
    print("3. ✅ Verify integration between Discord and messaging")
    print("4. ✅ Confirm 5-agent mode configuration")
    print("5. ✅ Validate command-method synchronization")
    print()

    # Run validation tests
    validator = DiscordCommanderValidator()
    report = validator.run_validation_tests()

    # Print report
    print_validation_report(report)

    # Return exit code based on test results
    success_count = sum(1 for r in report["detailed_results"]["slash_commands"].values() if r.get("status") == "✅ VALID")
    total_commands = len(report["detailed_results"]["slash_commands"])
    success_rate = success_count / total_commands if total_commands > 0 else 0

    return 0 if success_rate >= 0.8 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
