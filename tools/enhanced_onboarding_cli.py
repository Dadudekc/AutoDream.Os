#!/usr/bin/env python3
"""
Enhanced Onboarding CLI Tool
===========================

Command-line interface for enhanced agent onboarding with 7-step sequence.
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
    from src.services.enhanced_onboarding import EnhancedOnboardingService
except ImportError:
    print("❌ Enhanced onboarding service not available")
    sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Enhanced Agent Onboarding CLI")
    parser.add_argument("--agent", help="Agent ID to onboard (e.g., Agent-4)")
    parser.add_argument("--role", help="Role assignment (e.g., CAPTAIN, DATA_ANALYST)")
    parser.add_argument("--onboard-all", action="store_true", help="Onboard all active agents")
    parser.add_argument("--test-sequence", action="store_true", help="Show onboarding sequence")
    parser.add_argument(
        "--list-agents", action="store_true", help="List available agents and roles"
    )

    args = parser.parse_args()

    service = EnhancedOnboardingService()

    if args.test_sequence:
        print("🧪 Enhanced Onboarding Sequence:")
        print("=" * 50)
        print("1. Click chat input coordinates (get agent IDE attention)")
        print("2. Press Ctrl+Shift+Backspace (stop running agents)")
        print("3. Press Ctrl+Enter (save all changes)")
        print("4. Press Ctrl+N (open new chat)")
        print("5. Navigate to onboarding coordinates")
        print("6. Paste onboarding message with role assignment")
        print("7. Press Enter (send onboarding message)")
        print("\n📋 Onboarding message includes:")
        print("  • Role assignment and protocols")
        print("  • Reference to AGENTS.md for system overview")
        print("  • Instructions to begin onboarding protocols")
        print("  • V2 compliance requirements")

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

        print(f"🚀 Starting enhanced onboarding for {args.agent} with role {args.role}")
        print("📋 Following 7-step sequence...")

        success = service.execute_enhanced_onboarding(args.agent, args.role)

        if success:
            print(f"✅ Enhanced onboarding completed for {args.agent}")
            print(f"🎭 Role assigned: {args.role}")
            print("📚 Agent should now review AGENTS.md and begin protocols")
        else:
            print(f"❌ Enhanced onboarding failed for {args.agent}")
            sys.exit(1)

    elif args.onboard_all:
        print("🚀 Starting enhanced onboarding for all active agents...")
        print("📋 This will onboard Agent-4, Agent-5, Agent-6, Agent-7, Agent-8")
        print("⏱️ Each agent will have a 2-second delay between onboarding")

        confirm = input("\n🤔 Continue with enhanced onboarding? (y/N): ")
        if confirm.lower() != "y":
            print("❌ Onboarding cancelled")
            sys.exit(0)

        results = service.onboard_all_active_agents()

        print("\n📊 Enhanced Onboarding Results:")
        print("=" * 40)
        success_count = 0
        for agent_id, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"📱 {agent_id}: {status}")
            if success:
                success_count += 1

        print(f"\n🎯 Summary: {success_count}/{len(results)} agents onboarded successfully")

        if success_count == len(results):
            print("🐝 All agents ready for V2_SWARM coordination!")
        else:
            print("⚠️ Some agents failed onboarding - check coordinates and retry")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
