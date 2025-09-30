#!/usr/bin/env python3
"""
Unified Onboarding CLI Tool
==========================

Command-line interface for both hard and soft agent onboarding.
V2 Compliant: ≤400 lines, unified onboarding functionality.

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
    from src.services.enhanced_onboarding import EnhancedOnboardingService
    from src.services.soft_onboarding import SoftOnboardingService
except ImportError:
    print("❌ Onboarding services not available")
    sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Unified Agent Onboarding CLI")

    # Onboarding type selection
    parser.add_argument(
        "--type",
        choices=["hard", "soft"],
        default="soft",
        help="Onboarding type: hard (7-step) or soft (6-step)",
    )

    # Agent selection
    parser.add_argument("--agent", help="Agent ID to onboard (e.g., Agent-4)")
    parser.add_argument("--role", help="Role assignment (e.g., CAPTAIN, DATA_ANALYST)")

    # Bulk operations
    parser.add_argument("--onboard-all", action="store_true", help="Onboard all active agents")

    # Information and testing
    parser.add_argument("--test-sequence", action="store_true", help="Show onboarding sequence")
    parser.add_argument(
        "--list-agents", action="store_true", help="List available agents and roles"
    )
    parser.add_argument(
        "--compare-methods", action="store_true", help="Compare hard vs soft onboarding"
    )

    args = parser.parse_args()

    # Initialize services
    hard_service = EnhancedOnboardingService()
    soft_service = SoftOnboardingService()

    if args.compare_methods:
        print("🔍 Hard vs Soft Onboarding Comparison:")
        print("=" * 60)
        print("\n🚀 HARD ONBOARDING (7-step sequence):")
        print("  1. Click chat input coordinates")
        print("  2. Press Ctrl+Shift+Backspace (stop running agents)")
        print("  3. Press Ctrl+Enter (save all changes)")
        print("  4. Press Ctrl+N (open completely new chat)")
        print("  5. Navigate to onboarding coordinates")
        print("  6. Paste onboarding message")
        print("  7. Press Enter (send message)")
        print("  ⚡ More thorough reset, stops all agents")
        print("  🎯 Best for: Fresh start, troubleshooting")

        print("\n🌱 SOFT ONBOARDING (6-step sequence):")
        print("  1. Click chat input coordinates")
        print("  2. Press Ctrl+Enter (save all changes)")
        print("  3. Press Ctrl+T (open new chat window)")
        print("  4. Navigate to onboarding coordinates")
        print("  5. Paste onboarding message")
        print("  6. Press Enter (send message)")
        print("  🌿 Gentler approach, preserves existing state")
        print("  🎯 Best for: Regular onboarding, preserving work")

    elif args.test_sequence:
        if args.type == "hard":
            print("🧪 Hard Onboarding Sequence:")
            print("=" * 40)
            print("1. Click chat input coordinates")
            print("2. Press Ctrl+Shift+Backspace (stop agents)")
            print("3. Press Ctrl+Enter (save changes)")
            print("4. Press Ctrl+N (new chat)")
            print("5. Navigate to onboarding coordinates")
            print("6. Paste onboarding message")
            print("7. Press Enter (send message)")
        else:
            print("🧪 Soft Onboarding Sequence:")
            print("=" * 40)
            print("1. Click chat input coordinates")
            print("2. Press Ctrl+Enter (save changes)")
            print("3. Press Ctrl+T (new chat window)")
            print("4. Navigate to onboarding coordinates")
            print("5. Paste onboarding message")
            print("6. Press Enter (send message)")

    elif args.list_agents:
        print("🤖 Available Agents and Default Roles:")
        print("=" * 50)
        agents = soft_service.coordinates.get("agents", {})
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

        print(f"🚀 Starting {args.type} onboarding for {args.agent} with role {args.role}")

        if args.type == "hard":
            print("📋 Following 7-step hard sequence...")
            success = hard_service.execute_enhanced_onboarding(args.agent, args.role)
        else:
            print("📋 Following 6-step soft sequence...")
            success = soft_service.execute_soft_onboarding(args.agent, args.role)

        if success:
            print(f"✅ {args.type.capitalize()} onboarding completed for {args.agent}")
            print(f"🎭 Role assigned: {args.role}")
            print("📚 Agent should now review AGENTS.md and begin protocols")
        else:
            print(f"❌ {args.type.capitalize()} onboarding failed for {args.agent}")
            sys.exit(1)

    elif args.onboard_all:
        print(f"🚀 Starting {args.type} onboarding for all active agents...")
        print("📋 This will onboard Agent-4, Agent-5, Agent-6, Agent-7, Agent-8")

        if args.type == "hard":
            print("⏱️ Each agent will have a 2-second delay between onboarding")
            print("⚡ Hard onboarding: thorough reset, stops all agents")
        else:
            print("⏱️ Each agent will have a 1.5-second delay between onboarding")
            print("🌱 Soft onboarding: gentle approach, preserves existing state")

        confirm = input(f"\n🤔 Continue with {args.type} onboarding? (y/N): ")
        if confirm.lower() != "y":
            print(f"❌ {args.type.capitalize()} onboarding cancelled")
            sys.exit(0)

        if args.type == "hard":
            results = hard_service.onboard_all_active_agents()
        else:
            results = soft_service.soft_onboard_all_active_agents()

        print(f"\n📊 {args.type.capitalize()} Onboarding Results:")
        print("=" * 40)
        success_count = 0
        for agent_id, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"📱 {agent_id}: {status}")
            if success:
                success_count += 1

        print(
            f"\n🎯 Summary: {success_count}/{len(results)} agents {args.type} onboarded successfully"
        )

        if success_count == len(results):
            print("🐝 All agents ready for V2_SWARM coordination!")
        else:
            print(f"⚠️ Some agents failed {args.type} onboarding - check coordinates and retry")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
