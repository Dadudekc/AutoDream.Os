"""
Onboarding Coordinator Module - Unified Interface

This module coordinates the onboarding system by importing from focused modules.
Follows Single Responsibility Principle - only coordinates other modules.

Architecture: Single Responsibility Principle - coordination only
LOC: 100 lines (under 200 limit)
"""

from typing import Dict, Optional
from .agent_info import AgentInfoManager
from .message_builder import MessageBuilder
from .cli_utils import CLIExecutor


class OnboardingCoordinator:
    """
    Coordinates the onboarding system components.

    Responsibilities:
    - Coordinate agent information and message building
    - Provide unified onboarding interface
    - Manage onboarding workflow
    """

    def __init__(self):
        self.agent_info = AgentInfoManager()
        self.message_builder = MessageBuilder()
        self.cli_executor = CLIExecutor()

    def get_agent_onboarding_info(self, agent_name: str) -> Dict:
        """Get complete onboarding information for an agent"""
        agent_info = self.agent_info.get_agent_info(agent_name)
        return {
            "name": agent_name,
            "role": agent_info.role,
            "emoji": agent_info.emoji,
            "leadership": agent_info.leadership,
            "responsibilities": agent_info.key_responsibilities,
            "onboarding_path": agent_info.onboarding_path,
            "priority_docs": agent_info.priority_docs,
        }

    def create_onboarding_message(self, agent_name: str, style: str = "full") -> str:
        """Create onboarding message for an agent"""
        return self.message_builder.create_onboarding_message(agent_name, style)

    def run_onboarding_command(self, cmd_args: list, description: str = "") -> Dict:
        """Run an onboarding-related command"""
        return self.cli_executor.run_command(cmd_args, description)

    def get_all_agents_summary(self) -> Dict[str, str]:
        """Get summary of all agents"""
        agents = self.agent_info.get_all_agents()
        return {name: f"{info.emoji} {info.role}" for name, info in agents.items()}

    def validate_agent_name(self, agent_name: str) -> bool:
        """Check if agent name is valid"""
        try:
            self.agent_info.get_agent_info(agent_name)
            return True
        except:
            return False


def run_smoke_test():
    """Run basic functionality test for OnboardingCoordinator"""
    print("🧪 Running OnboardingCoordinator Smoke Test...")

    try:
        coordinator = OnboardingCoordinator()

        # Test agent info retrieval
        info = coordinator.get_agent_onboarding_info("Agent-1")
        assert info["role"] == "System Coordinator & Project Manager"
        assert info["emoji"] == "🎯"

        # Test message creation
        message = coordinator.create_onboarding_message("Agent-2", "simple")
        assert "Agent-2" in message
        assert "Technical Architect" in message

        # Test agent validation
        assert coordinator.validate_agent_name("Agent-3")
        assert not coordinator.validate_agent_name("Invalid-Agent")

        # Test agents summary
        summary = coordinator.get_all_agents_summary()
        assert len(summary) == 5
        assert "🎯 System Coordinator" in summary["Agent-1"]

        print("✅ OnboardingCoordinator Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ OnboardingCoordinator Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for OnboardingCoordinator testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Onboarding Coordinator CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--agent", help="Get onboarding info for agent")
    parser.add_argument("--message", help="Create message for agent")
    parser.add_argument(
        "--style",
        choices=["full", "ascii", "simple"],
        default="full",
        help="Message style",
    )
    parser.add_argument("--list", action="store_true", help="List all agents")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    coordinator = OnboardingCoordinator()

    if args.agent:
        if args.message:
            message = coordinator.create_onboarding_message(args.agent, args.style)
            print(message)
        else:
            info = coordinator.get_agent_onboarding_info(args.agent)
            print(f"Agent: {info['name']}")
            print(f"Role: {info['role']}")
            print(f"Emoji: {info['emoji']}")
            print(f"Leadership: {info['leadership']}")
            print("Responsibilities:")
            for resp in info["responsibilities"]:
                print(f"  • {resp}")
    elif args.list:
        summary = coordinator.get_all_agents_summary()
        for name, desc in summary.items():
            print(f"{name}: {desc}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
