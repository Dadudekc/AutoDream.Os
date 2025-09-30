#!/usr/bin/env python3
"""
Soft Onboarding CLI Tool
=======================

Command-line interface for soft agent onboarding with 6-step sequence.
V2 Compliant: ≤400 lines, focused CLI functionality.

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import argparse
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from src.services.soft_onboarding import SoftOnboardingService
except ImportError:
    print("❌ Soft onboarding service not available")
    sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Soft Agent Onboarding CLI")
    parser.add_argument("--agent", help="Agent ID to soft onboard (e.g., Agent-4)")
    parser.add_argument("--role", help="Role assignment (e.g., CAPTAIN, DATA_ANALYST)")
    parser.add_argument(
        "--soft-onboard-all", action="store_true", help="Soft onboard all active agents"
    )
    parser.add_argument(
        "--test-sequence", action="store_true", help="Show soft onboarding sequence"
    )
    parser.add_argument(
        "--list-agents", action="store_true", help="List available agents and roles"
    )

    args = parser.parse_args()

    service = SoftOnboardingService()

    if args.test_sequence:
        print("🧪 Soft Onboarding Sequence:")
        print("=" * 50)
        print("1. Click chat input coordinates (get agent IDE attention)")
        print("2. Press Ctrl+Enter (save all changes)")
        print("3. Press Ctrl+T (open new chat window)")
        print("4. Navigate to onboarding coordinates")
        print("5. Paste soft onboarding message with role assignment")
        print("6. Press Enter (send onboarding message)")
        print("\n📋 Soft onboarding message includes:")
        print("  • Role assignment and protocols")
        print("  • Reference to AGENTS.md for system overview")
        print("  • Instructions to begin onboarding protocols")
        print("  • V2 compliance requirements")
        print("  • Gentle initialization (preserves existing state)")

    elif args.list_agents:
        print("🤖 Available Agents and Default Roles:")
        print("=" * 50)
        agents = service.coordinates.get("agents", {})
        default_roles = {
            "Agent-4": "CAPTAIN",
            "Agent-5": "DATA_ANALYST",
            "Agent-6": "QUALITY_ASSURANCE",
            "Agent-7": "WEB_DEVELOPER",
            "Agent-8": "SSOT_MANAGER",
        }

        for agent_id, agent_info in agents.items():
            if agent_info.get("active", False):
                role = default_roles.get(agent_id, "TASK_EXECUTOR")
                desc = agent_info.get("description", "Unknown")
                chat_coords = agent_info.get("chat_input_coordinates", [0, 0])
                onboard_coords = agent_info.get("onboarding_coordinates", [0, 0])

                print(f"📱 {agent_id}: {desc}")
                print(f"   Role: {role}")
                print(f"   Chat: {chat_coords}")
                print(f"   Onboard: {onboard_coords}")
                print()

    elif args.agent:
        if not args.role:
            print("⚠️ Warning: No role specified, using default TASK_EXECUTOR")
            args.role = "TASK_EXECUTOR"

        print(f"🚀 Starting soft onboarding for {args.agent} with role {args.role}")
        print("📋 Following 6-step gentle sequence...")

        success = service.execute_soft_onboarding(args.agent, args.role)

        if success:
            print(f"✅ Soft onboarding completed for {args.agent}")
            print(f"🎭 Role assigned: {args.role}")
            print("📚 Agent should now review AGENTS.md and begin protocols")
            print("🌱 Soft onboarding preserves existing agent state")
        else:
            print(f"❌ Soft onboarding failed for {args.agent}")
            sys.exit(1)

    elif args.soft_onboard_all:
        print("🚀 Starting soft onboarding for all active agents...")
        print("📋 This will soft onboard Agent-4, Agent-5, Agent-6, Agent-7, Agent-8")
        print("⏱️ Each agent will have a 1.5-second delay between onboarding")
        print("🌱 Soft onboarding preserves existing agent states")

        confirm = input("\n🤔 Continue with soft onboarding? (y/N): ")
        if confirm.lower() != "y":
            print("❌ Soft onboarding cancelled")
            sys.exit(0)

        results = service.soft_onboard_all_active_agents()

        print("\n📊 Soft Onboarding Results:")
        print("=" * 40)
        success_count = 0
        for agent_id, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"📱 {agent_id}: {status}")
            if success:
                success_count += 1

        print(f"\n🎯 Summary: {success_count}/{len(results)} agents soft onboarded successfully")

        if success_count == len(results):
            print("🐝 All agents ready for gentle V2_SWARM coordination!")
        else:
            print("⚠️ Some agents failed soft onboarding - check coordinates and retry")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
