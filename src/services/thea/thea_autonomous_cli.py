#!/usr/bin/env python3
"""
Thea Autonomous CLI - Command Line Interface for Agent-Friendly Thea
====================================================================

A simple command-line interface for the autonomous Thea system.
Allows agents to interact with Thea without human intervention.

Usage:
    python -m src.services.thea.thea_autonomous_cli send "Hello Thea!"
    python -m src.services.thea.thea_autonomous_cli status
    python -m src.services.thea.thea_autonomous_cli test
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.thea.thea_autonomous_system import (
    TheaAutonomousSystem,
    send_thea_message_autonomous,
)


def send_message_command(message: str, headless: bool = True):
    """Send a message to Thea autonomously."""
    print("🤖 Sending autonomous message to Thea...")
    print(f"📤 Message: {message}")
    print(f"🫥 Headless mode: {headless}")
    print("-" * 50)

    response = send_thea_message_autonomous(message, headless=headless)

    if response:
        print("✅ SUCCESS: Received response from Thea")
        print(f"📝 Response length: {len(response)} characters")
        print(f"📄 Response preview: {response[:300]}...")
        return True
    else:
        print("❌ FAILED: No response received from Thea")
        return False


def status_command():
    """Get system status."""
    print("📊 Thea Autonomous System Status")
    print("=" * 40)

    try:
        thea = TheaAutonomousSystem(headless=True)
        status = thea.get_system_status()

        print(f"🔧 Initialized: {status['initialized']}")
        print(f"🫥 Headless mode: {status['headless_mode']}")
        print(f"🍪 Valid cookies: {status['has_valid_cookies']}")
        print(f"🌐 Browser available: {status['browser_available']}")
        print(f"⏰ Last activity: {status['last_activity']}")
        print(f"🔄 Max retries: {status['max_retries']}")
        print(f"⏳ Retry delay: {status['retry_delay']}s")

        return True

    except Exception as e:
        print(f"❌ Error getting status: {e}")
        return False


def test_command():
    """Run a test message to verify system functionality."""
    test_message = "Hello Thea! This is an autonomous test from Agent-2. Please respond with a brief acknowledgment."

    print("🧪 Running Thea Autonomous System Test")
    print("=" * 45)

    return send_message_command(test_message, headless=True)


def interactive_command():
    """Run in interactive mode for testing."""
    print("🎮 Thea Autonomous Interactive Mode")
    print("=" * 40)
    print("Type messages to send to Thea (or 'quit' to exit)")
    print("-" * 40)

    try:
        with TheaAutonomousSystem(headless=False) as thea:
            while True:
                message = input("\n📤 Enter message: ").strip()

                if message.lower() in ["quit", "exit", "q"]:
                    print("👋 Goodbye!")
                    break

                if not message:
                    print("⚠️  Please enter a message")
                    continue

                print(f"📤 Sending: {message}")
                response = thea.send_message_autonomous(message)

                if response:
                    print(f"✅ Response: {response[:500]}...")
                else:
                    print("❌ No response received")

    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"❌ Error in interactive mode: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Thea Autonomous System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s send "Hello Thea!"
  %(prog)s status
  %(prog)s test
  %(prog)s interactive
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Send command
    send_parser = subparsers.add_parser("send", help="Send a message to Thea")
    send_parser.add_argument("message", help="Message to send to Thea")
    send_parser.add_argument(
        "--visible", action="store_true", help="Run browser in visible mode (default: headless)"
    )

    # Status command
    subparsers.add_parser("status", help="Get system status")

    # Test command
    subparsers.add_parser("test", help="Run a test message")

    # Interactive command
    subparsers.add_parser("interactive", help="Run in interactive mode")

    # Conversation management commands
    conv_parser = subparsers.add_parser("conversation", help="Manage conversations")
    conv_subparsers = conv_parser.add_subparsers(dest="conv_action", required=True)

    # List conversations
    conv_subparsers.add_parser("list", help="List all conversations")

    # Show active conversation
    conv_subparsers.add_parser("active", help="Show active conversation info")

    # Start new conversation
    conv_subparsers.add_parser("new", help="Start a new conversation")

    # Load specific conversation
    load_parser = conv_subparsers.add_parser("load", help="Load a specific conversation")
    load_parser.add_argument("conversation_link", help="Conversation link to load")

    # Analytics reporting commands
    analytics_parser = subparsers.add_parser("analytics", help="Send analytics reports to Thea")
    analytics_parser.add_argument(
        "--report", action="store_true", help="Send comprehensive analytics report"
    )
    analytics_parser.add_argument(
        "--new-conversation", action="store_true", help="Start new conversation for report"
    )
    analytics_parser.add_argument(
        "--status", action="store_true", help="Show analytics reporter status"
    )
    # Removed --visible flag - agents should run headless by default

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "send":
            headless = not args.visible
            success = send_message_command(args.message, headless=headless)
            return 0 if success else 1

        elif args.command == "status":
            success = status_command()
            return 0 if success else 1

        elif args.command == "test":
            success = test_command()
            return 0 if success else 1

        elif args.command == "interactive":
            interactive_command()
            return 0

        elif args.command == "conversation":
            return conversation_command(args)

        elif args.command == "analytics":
            return analytics_command(args)

        else:
            print(f"❌ Unknown command: {args.command}")
            return 1

    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def conversation_command(args):
    """Handle conversation management commands."""
    from src.services.thea.thea_conversation_manager import TheaConversationManager

    manager = TheaConversationManager()

    if args.conv_action == "list":
        print("📚 Thea Conversation History")
        print("=" * 50)

        history = manager.get_conversation_history()
        if not history:
            print("No conversations found.")
            return 0

        for i, conv in enumerate(history, 1):
            print(f"{i}. {conv['conversation_id']}")
            print(f"   Topic: {conv['topic']}")
            print(f"   Status: {conv['status']}")
            print(f"   Messages: {conv['message_count']}")
            print(f"   Created: {conv['created_at']}")
            print(f"   Last Accessed: {conv['last_accessed']}")
            print(f"   Link: {conv['link']}")
            print()

        return 0

    elif args.conv_action == "active":
        print("🔄 Active Conversation Status")
        print("=" * 50)

        status = manager.get_status()
        if status["active_conversation"]:
            active = status["active_conversation"]
            print(f"Active Conversation: {active['conversation_id']}")
            print(f"Topic: {active['topic']}")
            print(f"Messages: {active['message_count']}")
            print(f"Last Accessed: {active['last_accessed']}")
            print(f"Link: {active['link']}")
        else:
            print("No active conversation.")

        print(f"\nTotal Conversations: {status['total_conversations']}")
        return 0

    elif args.conv_action == "new":
        print("🆕 Starting New Conversation")
        print("=" * 50)

        # This would require browser interaction, so we'll just clear the active conversation
        manager.active_conversation_id = None
        manager._save_conversations()
        print("✅ Cleared active conversation. Next message will start a new conversation.")
        return 0

    elif args.conv_action == "load":
        print("🔄 Loading Conversation")
        print("=" * 50)

        success = manager.load_conversation(args.conversation_link)
        if success:
            print(f"✅ Loaded conversation: {args.conversation_link}")
        else:
            print(f"❌ Failed to load conversation: {args.conversation_link}")
            return 1

        return 0

    else:
        print(f"❌ Unknown conversation action: {args.conv_action}")
        return 1


def analytics_command(args):
    """Handle analytics reporting commands."""
    from src.services.thea.thea_analytics_reporter import TheaAnalyticsReporter

    reporter = TheaAnalyticsReporter()

    if args.status:
        print("📊 Thea Analytics Reporter Status")
        print("=" * 50)

        status = reporter.get_report_status()

        print(f"Analytics Available: {'✅ Yes' if status['analytics_available'] else '❌ No'}")
        print(f"Last Scan: {status['last_scan_timestamp'] or 'Never'}")
        print(f"V2 Compliance: {status['v2_compliance']:.1f}%")
        print(f"Violations: {status['violations_count']}")
        print(f"Reporter Ready: {'✅ Yes' if status['reporter_ready'] else '❌ No'}")

        if status["conversation_status"]["active_conversation"]:
            active = status["conversation_status"]["active_conversation"]
            print(f"\nActive Conversation: {active['conversation_id']}")
            print(f"Topic: {active['topic']}")
            print(f"Messages: {active['message_count']}")

        return 0

    elif args.report:
        print("📊 Sending Analytics Report to Commander Thea")
        print("=" * 50)

        # Check if reporter is ready
        status = reporter.get_report_status()
        if not status["reporter_ready"]:
            print("❌ Analytics reporter not ready - missing project analysis or analytics data")
            print("Please run a project scan first: python tools/run_project_scan.py")
            return 1

        print("🔄 Generating comprehensive analytics report...")
        print("📤 Sending to Commander Thea...")

        # Send report autonomously (headless by default for agents)
        success = reporter.send_analytics_report(
            force_new_conversation=args.new_conversation, visible=False
        )

        if success:
            print("✅ Analytics report sent successfully to Commander Thea")
            print("📋 Thea will provide strategic guidance based on current project analytics")
        else:
            print("❌ Failed to send analytics report")
            return 1

        return 0

    else:
        print("❌ Please specify --report, --status, or --help")
        return 1


if __name__ == "__main__":
    sys.exit(main())
