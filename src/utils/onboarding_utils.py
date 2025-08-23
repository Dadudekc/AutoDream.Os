#!/usr/bin/env python3
"""
Onboarding Utilities - Agent Cellphone V2
=========================================

Coordinator module for onboarding utilities - imports focused modules.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import focused modules
from .agent_info import AgentInfoManager
from .cli_utils import CLIExecutor, CommandBuilder
from .message_builder import OnboardingMessageBuilder
from .onboarding_orchestrator import OnboardingOrchestrator


class OnboardingUtils:
    """Coordinator class for onboarding utilities"""

    def __init__(self):
        self.agent_info = AgentInfoManager()
        self.cli_executor = CLIExecutor()
        self.message_builder = OnboardingMessageBuilder()
        self.orchestrator = OnboardingOrchestrator()

    def get_agent_info(self, agent_name: str):
        """Get agent information"""
        return self.agent_info.get_agent_info(agent_name)

    def run_cli_command(self, cmd_args, description="", use_emojis=True):
        """Run CLI command"""
        return self.cli_executor.run_simple_command(cmd_args, description)

    def create_onboarding_message(self, agent_name: str, style: str = "full"):
        """Create onboarding message"""
        return self.message_builder.create_comprehensive_message(agent_name, style)

    def onboard_agent(
        self, agent_name: str, style: str = "full", use_emojis: bool = True
    ):
        """Onboard a single agent"""
        return self.orchestrator.onboard_agent(agent_name, style, use_emojis)

    def onboard_all_agents(self, style: str = "full", use_emojis: bool = True):
        """Onboard all agents"""
        return self.orchestrator.onboard_all_agents(style, use_emojis)

    def get_onboarding_status(self):
        """Get onboarding status"""
        return self.orchestrator.get_onboarding_status()


# Legacy function compatibility
def get_agent_info(agent_name: str):
    """Legacy function for backward compatibility"""
    utils = OnboardingUtils()
    return utils.get_agent_info(agent_name)


def run_cli_command(cmd_args, description="", use_emojis=True):
    """Legacy function for backward compatibility"""
    utils = OnboardingUtils()
    return utils.run_cli_command(cmd_args, description, use_emojis)


def create_comprehensive_onboarding_message(agent_name: str, style: str = "full"):
    """Legacy function for backward compatibility"""
    utils = OnboardingUtils()
    return utils.create_onboarding_message(agent_name, style)


def print_onboarding_summary(results, use_emojis=True):
    """Legacy function for backward compatibility"""
    utils = OnboardingUtils()
    utils.orchestrator.print_onboarding_summary(results, use_emojis)


def main():
    """CLI interface for testing the Onboarding Utils coordinator"""
    import argparse

    parser = argparse.ArgumentParser(description="Onboarding Utils Coordinator CLI")
    parser.add_argument("--test", "-t", action="store_true", help="Test all modules")
    parser.add_argument("--agent", "-a", help="Get agent info")
    parser.add_argument("--message", "-m", help="Create message for agent")
    parser.add_argument("--status", "-s", action="store_true", help="Show status")

    args = parser.parse_args()

    utils = OnboardingUtils()

    if args.test:
        print("🧪 Testing Onboarding Utils Coordinator...")

        # Test agent info
        try:
            info = utils.get_agent_info("Agent-1")
            print(f"✅ Agent info: {info['role']}")
        except Exception as e:
            print(f"❌ Agent info failed: {e}")

        # Test message creation
        try:
            message = utils.create_onboarding_message("Agent-2", "simple")
            print(f"✅ Message creation: {len(message)} characters")
        except Exception as e:
            print(f"❌ Message creation failed: {e}")

        # Test CLI
        try:
            success = utils.run_cli_command(["echo", "test"], "Testing CLI")
            print(f"✅ CLI test: {'Passed' if success else 'Failed'}")
        except Exception as e:
            print(f"❌ CLI test failed: {e}")

        print("🧪 Testing complete!")

    elif args.agent:
        info = utils.get_agent_info(args.agent)
        print(f"📋 {args.agent} Information:")
        print(f"  Role: {info['role']}")
        print(f"  Emoji: {info['emoji']}")

    elif args.message:
        message = utils.create_onboarding_message(args.message, "simple")
        print(f"📝 Message for {args.message}:")
        print(message[:200] + "..." if len(message) > 200 else message)

    elif args.status:
        status = utils.get_onboarding_status()
        print("📊 Onboarding Status:")
        for agent_name, agent_status in status.items():
            emoji = "✅" if agent_status["status_file_exists"] else "❌"
            print(f"  {emoji} {agent_name}: {agent_status['current_status']}")

    else:
        print("Onboarding Utils Coordinator - Use --help for options")


if __name__ == "__main__":
    main()
