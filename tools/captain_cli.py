#!/usr/bin/env python3
"""
Captain CLI - V2 Compliant
=========================

Command-line interface for Captain to monitor and manage agents.
Provides agent status monitoring and high-priority messaging.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import argparse
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.fsm.activity_monitor import get_activity_monitor
from src.fsm.captain_dashboard import get_captain_dashboard
from src.services.messaging.service import MessagingService

# V2 Compliance: File under 400 lines, functions under 30 lines


def show_agent_status():
    """Show comprehensive agent status."""
    dashboard = get_captain_dashboard()
    report = dashboard.generate_captain_report()
    print(report)


def show_inactive_agents():
    """Show inactive agents requiring attention."""
    dashboard = get_captain_dashboard()
    inactive_agents = dashboard.get_inactive_agents()

    if not inactive_agents:
        print("✅ All agents are active - no action needed")
        return

    print("🚨 INACTIVE AGENTS REQUIRING ATTENTION:")
    print("=" * 50)

    for agent in inactive_agents:
        print(f"\n🔴 {agent['agent_id']}: {agent['status']}")
        print(f"   Reason: {agent['reason']}")
        print(f"   Action Needed: {agent['action_needed']}")
        print(f"   Last Activity: {agent['last_activity'] or 'Never'}")


def send_high_priority_message(agent_id: str, message: str = None):
    """Send high-priority message to agent."""
    dashboard = get_captain_dashboard()
    activity_monitor = get_activity_monitor()
    messaging_service = MessagingService()

    # Get inactivity reason
    is_inactive, reason = activity_monitor.check_agent_inactivity(agent_id)
    is_messaging_inactive, messaging_reason = activity_monitor.check_messaging_inactivity(agent_id)

    # Generate message if not provided
    if not message:
        if is_inactive:
            message = dashboard.get_high_priority_message_template(agent_id, reason)
        elif is_messaging_inactive:
            message = dashboard.get_high_priority_message_template(agent_id, messaging_reason)
        else:
            message = f"🚨 HIGH PRIORITY MESSAGE - IMMEDIATE RESPONSE REQUIRED\n\nAgent {agent_id}, please respond immediately to confirm you are active and operational.\n\n📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"

    # Send high-priority message
    success = messaging_service.send(agent_id, message, priority="HIGH", high_priority=True)

    if success:
        print(f"✅ High-priority message sent to {agent_id}")
        print("🚨 Message bypassed normal queue with ctrl+enter")
    else:
        print(f"❌ Failed to send high-priority message to {agent_id}")


def onboard_agent(agent_id: str):
    """Onboard agent with high-priority message."""
    onboarding_message = f"""🚨 ONBOARDING REQUIRED - IMMEDIATE ACTION

Agent {agent_id}, you need to complete onboarding protocol.

📋 REQUIRED ACTIONS:
1. Review onboarding documentation in your workspace
2. Read ONBOARDING_PROTOCOL.md file
3. Update your status to ACTIVE
4. Send confirmation message to Captain (Agent-4)

📁 ONBOARDING FILES TO REVIEW:
• docs/fsm/OVERVIEW.md - FSM system overview
• AGENT_QUICK_START_GUIDE.md - Quick start guide
• AGENT_WORK_GUIDELINES.md - Work guidelines
• V2_COMPLIANCE_REPORT.md - V2 compliance standards

🎯 COMPLETION REQUIRED:
Complete onboarding protocol and confirm with Captain.

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"""

    send_high_priority_message(agent_id, onboarding_message)


def generate_report():
    """Generate and save captain report."""
    dashboard = get_captain_dashboard()
    report = dashboard.generate_captain_report()
    report_path = dashboard.save_report(report)

    print(f"📊 Captain report generated: {report_path}")
    print("\n" + report)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Captain CLI for agent management")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    subparsers.add_parser("status", help="Show agent status")

    # Inactive command
    subparsers.add_parser("inactive", help="Show inactive agents")

    # High-priority message command
    msg_parser = subparsers.add_parser("high-priority", help="Send high-priority message")
    msg_parser.add_argument("agent_id", help="Agent ID to send message to")
    msg_parser.add_argument("--message", help="Custom message (optional)")

    # Onboard command
    onboard_parser = subparsers.add_parser("onboard", help="Onboard agent")
    onboard_parser.add_argument("agent_id", help="Agent ID to onboard")

    # Report command
    subparsers.add_parser("report", help="Generate captain report")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "status":
            show_agent_status()
        elif args.command == "inactive":
            show_inactive_agents()
        elif args.command == "high-priority":
            send_high_priority_message(args.agent_id, args.message)
        elif args.command == "onboard":
            onboard_agent(args.agent_id)
        elif args.command == "report":
            generate_report()

        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
