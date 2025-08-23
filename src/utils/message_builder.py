"""
Message Builder Module - Onboarding Message Creation

This module creates onboarding messages for agents.
Follows Single Responsibility Principle - only manages message creation.

Architecture: Single Responsibility Principle - message building only
LOC: 150 lines (under 200 limit)
"""

from typing import Dict, Optional
from .agent_info import AgentInfoManager


class MessageBuilder:
    """
    Builds onboarding messages for agents.

    Responsibilities:
    - Create onboarding messages
    - Format messages with different styles
    - Manage message templates
    """

    def __init__(self):
        self.agent_info_manager = AgentInfoManager()

    def create_onboarding_message(self, agent_name: str, style: str = "full") -> str:
        """
        Create a comprehensive onboarding message for the specified agent

        Args:
            agent_name: Name of the agent (e.g., "Agent-1")
            style: Message style - "full" (with emojis), "ascii" (ASCII only), "simple" (no emojis)

        Returns:
            Formatted onboarding message
        """
        agent_info = self.agent_info_manager.get_agent_info(agent_name)

        # Choose formatting based on style
        if style == "ascii":
            bullet = "* "
            emoji = ""
        else:
            bullet = "• "
            emoji = agent_info.emoji if style == "full" else ""

        # Build the message header
        if style == "full":
            message = f"""{emoji} WELCOME TO DREAM.OS - COMPREHENSIVE ONBOARDING

🎯 YOUR ROLE: {agent_name} - {agent_info.role}

{agent_info.leadership} Your role is essential to our autonomous agent system success.

📋 YOUR KEY RESPONSIBILITIES:
"""
        else:
            message = f"""WELCOME TO DREAM.OS - COMPREHENSIVE ONBOARDING

YOUR ROLE: {agent_name} - {agent_info.role}

{agent_info.leadership} Your role is essential to our autonomous agent system success.

YOUR KEY RESPONSIBILITIES:
"""

        # Add responsibilities
        for resp in agent_info.key_responsibilities:
            message += f"{bullet}{resp}\n"

        # Add system overview
        if style == "full":
            message += f"""
🏗️ SYSTEM OVERVIEW:
Dream.OS is an autonomous multi-agent system where agents work together to:
{bullet}Coordinate tasks and projects autonomously
{bullet}Communicate through structured messaging protocols
{bullet}Maintain individual workspaces and status tracking
{bullet}Collaborate on complex technical projects
{bullet}Self-manage and validate their work

🌐 ENVIRONMENT MODEL (Cursor + shared repo/files):
{bullet}Agents are Cursor-based. ACP types messages directly into each agent's Cursor input box using calibrated coordinates.
{bullet}All agents work on the same repositories/files on disk (e.g., D:\\repositories\\...). Use repo-relative paths in prompts.
{bullet}Coordinate using each repo's TASK_LIST.md and status.json; avoid duplication; prefer reuse/refactor; commit small, verifiable edits.
{bullet}Messaging channels: (1) Visible UI typing via ACP, (2) Silent JSON file inbox at agent_workspaces/Agent-N/inbox/.
{bullet}Run tools from D:\\Agent_Cellphone so paths resolve correctly.

📚 YOUR ONBOARDING MATERIALS (READ THESE IN ORDER):
1. MAIN GUIDE: {agent_info.onboarding_path}
   - Complete system overview and getting started

2. YOUR ROLE: {agent_info.priority_docs[0]}
   - Detailed role-specific responsibilities and expectations

3. DEVELOPMENT STANDARDS: {agent_info.priority_docs[1]}
   - Code quality, testing, and development practices

4. ADDITIONAL RESOURCES: {agent_info.priority_docs[2]}
   - Tools, technologies, and best practices

🚀 GETTING STARTED:
{bullet}Read your onboarding materials in order
{bullet}Set up your workspace at agent_workspaces/{agent_name}/
{bullet}Review current project status and TASK_LIST.md
{bullet}Introduce yourself to the team
{bullet}Begin with small, focused tasks to build momentum

💡 PRO TIPS:
{bullet}Always commit small, verifiable changes
{bullet}Use clear, descriptive commit messages
{bullet}Coordinate with other agents to avoid duplication
{bullet}Ask questions when you need clarification
{bullet}Focus on your core responsibilities first

🎯 NEXT STEPS:
1. Complete your onboarding reading
2. Set up your development environment
3. Review current project status
4. Identify your first contribution opportunity
5. Begin active participation

Welcome to the team! Your expertise in {agent_info.role.lower()} is crucial to our success.

{emoji} {agent_name} - Ready to contribute! 🚀"""
        else:
            message += f"""

SYSTEM OVERVIEW:
Dream.OS is an autonomous multi-agent system where agents work together to:
{bullet}Coordinate tasks and projects autonomously
{bullet}Communicate through structured messaging protocols
{bullet}Maintain individual workspaces and status tracking
{bullet}Collaborate on complex technical projects
{bullet}Self-manage and validate their work

ENVIRONMENT MODEL:
{bullet}Agents are Cursor-based with calibrated coordinates
{bullet}All agents work on the same repositories/files on disk
{bullet}Coordinate using TASK_LIST.md and status.json
{bullet}Messaging via UI typing and JSON file inboxes
{bullet}Run tools from D:\\Agent_Cellphone

ONBOARDING MATERIALS:
1. MAIN GUIDE: {agent_info.onboarding_path}
2. YOUR ROLE: {agent_info.priority_docs[0]}
3. DEVELOPMENT STANDARDS: {agent_info.priority_docs[1]}
4. ADDITIONAL RESOURCES: {agent_info.priority_docs[2]}

GETTING STARTED:
{bullet}Read onboarding materials in order
{bullet}Set up workspace at agent_workspaces/{agent_name}/
{bullet}Review project status and TASK_LIST.md
{bullet}Begin with small, focused tasks

Welcome to the team! Your expertise in {agent_info.role.lower()} is crucial to our success.

{agent_name} - Ready to contribute!"""

        return message

    def create_simple_message(self, agent_name: str) -> str:
        """Create a simple welcome message"""
        agent_info = self.agent_info_manager.get_agent_info(agent_name)
        return f"Welcome {agent_name}! You are the {agent_info.role}. {agent_info.leadership}"

    def create_role_summary(self, agent_name: str) -> str:
        """Create a role summary message"""
        agent_info = self.agent_info_manager.get_agent_info(agent_name)
        return f"{agent_info.emoji} {agent_name}: {agent_info.role}\nResponsibilities: {', '.join(agent_info.key_responsibilities[:2])}..."


def run_smoke_test():
    """Run basic functionality test for MessageBuilder"""
    print("🧪 Running MessageBuilder Smoke Test...")

    try:
        builder = MessageBuilder()

        # Test message creation
        message = builder.create_onboarding_message("Agent-1", "full")
        assert "Agent-1" in message
        assert "System Coordinator" in message
        assert "🎯" in message

        # Test simple message
        simple = builder.create_simple_message("Agent-2")
        assert "Agent-2" in simple
        assert "Technical Architect" in simple

        # Test role summary
        summary = builder.create_role_summary("Agent-3")
        assert "Agent-3" in summary
        assert "📊" in summary

        print("✅ MessageBuilder Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ MessageBuilder Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for MessageBuilder testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Message Builder CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--agent", help="Create message for specific agent")
    parser.add_argument(
        "--style",
        choices=["full", "ascii", "simple"],
        default="full",
        help="Message style",
    )
    parser.add_argument("--simple", help="Create simple message for agent")
    parser.add_argument("--summary", help="Create role summary for agent")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    builder = MessageBuilder()

    if args.agent:
        message = builder.create_onboarding_message(args.agent, args.style)
        print(message)
    elif args.simple:
        message = builder.create_simple_message(args.simple)
        print(message)
    elif args.summary:
        message = builder.create_role_summary(args.summary)
        print(message)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
