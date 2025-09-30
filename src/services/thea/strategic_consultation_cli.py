#!/usr/bin/env python3
"""
Strategic Consultation CLI - Thea Integration Tool
================================================

Command-line interface for strategic consultation with Commander Thea.
Provides structured context delivery and consultation management.

Usage:
    python src/services/thea/strategic_consultation_cli.py consult --question "What should be our next priority?"
    python src/services/thea/strategic_consultation_cli.py consult --template priority_guidance
    python src/services/thea/strategic_consultation_cli.py status-report
    python src/services/thea/strategic_consultation_cli.py emergency --issue "System degradation detected"
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.thea.context_templates import STRATEGIC_TEMPLATES, ProjectContextManager
from src.services.thea.thea_autonomous_system import send_thea_message_autonomous


def consult_command(args):
    """Handle consultation command."""
    context_manager = ProjectContextManager()

    if args.template:
        # Use pre-defined template
        if args.template not in STRATEGIC_TEMPLATES:
            print(f"❌ Invalid template: {args.template}")
            print(f"Available templates: {', '.join(STRATEGIC_TEMPLATES.keys())}")
            return 1

        question = STRATEGIC_TEMPLATES[args.template]
        print(f"📋 Using template: {args.template}")
        print(f"📝 Question: {question}")
    else:
        # Use custom question
        question = args.question
        print(f"📝 Custom question: {question}")

    # Create consultation message
    context_level = args.context_level or "standard"
    message = context_manager.create_strategic_consultation(question, context_level)

    # Show message preview
    print(f"\n📤 Consultation Message ({len(message)} characters):")
    print("-" * 50)
    print(message)
    print("-" * 50)

    # Autonomous operation - no confirmation needed
    print("\n🤖 Autonomous consultation mode - sending automatically...")

    # Send message
    print("\n📤 Sending consultation to Commander Thea...")
    try:
        response = send_thea_message_autonomous(message, headless=not args.visible)

        if response:
            print("\n✅ SUCCESS: Received response from Commander Thea")
            print(f"📋 Response ({len(response)} characters):")
            print("-" * 50)
            print(response)
            print("-" * 50)

            # Save consultation log
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = f"thea_responses/strategic_consultation_{timestamp}.md"

            with open(log_file, "w", encoding="utf-8") as f:
                f.write("# Strategic Consultation Log\n")
                f.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## Question\n{question}\n\n")
                f.write(f"## Message Sent\n```\n{message}\n```\n\n")
                f.write(f"## Commander Thea's Response\n```\n{response}\n```\n\n")
                f.write("## Analysis\n- [Add your analysis here]\n")
                f.write("- [Key insights from Thea's response]\n")
                f.write("- [Next steps based on guidance]\n")

            print(f"📝 Consultation log saved: {log_file}")
            return 0
        else:
            print("❌ FAILED: No response received from Commander Thea")
            return 1

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 1


def status_report_command(args):
    """Handle status report command."""
    context_manager = ProjectContextManager()

    # Create status report
    additional_status = {}
    if args.additional_status:
        for status_item in args.additional_status:
            if ":" in status_item:
                key, value = status_item.split(":", 1)
                additional_status[key.strip()] = value.strip()

    message = context_manager.create_status_report(additional_status)

    # Show message preview
    print(f"\n📊 Status Report ({len(message)} characters):")
    print("-" * 50)
    print(message)
    print("-" * 50)

    # Autonomous operation - no confirmation needed
    print("\n🤖 Autonomous status report mode - sending automatically...")

    # Send message
    print("\n📤 Sending status report to Commander Thea...")
    try:
        response = send_thea_message_autonomous(message, headless=not args.visible)

        if response:
            print("\n✅ SUCCESS: Received response from Commander Thea")
            print(f"📋 Response ({len(response)} characters):")
            print("-" * 50)
            print(response)
            print("-" * 50)
            return 0
        else:
            print("❌ FAILED: No response received from Commander Thea")
            return 1

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 1


def emergency_command(args):
    """Handle emergency consultation command."""
    context_manager = ProjectContextManager()

    # Create emergency message
    message = context_manager.create_emergency_consultation(args.issue)

    # Show message preview
    print(f"\n🚨 EMERGENCY CONSULTATION ({len(message)} characters):")
    print("-" * 50)
    print(message)
    print("-" * 50)

    # Autonomous operation - no confirmation needed
    print("\n🤖 Autonomous emergency consultation mode - sending automatically...")

    # Send message
    print("\n🚨 Sending EMERGENCY consultation to Commander Thea...")
    try:
        response = send_thea_message_autonomous(message, headless=not args.visible)

        if response:
            print("\n✅ SUCCESS: Received EMERGENCY response from Commander Thea")
            print(f"📋 Response ({len(response)} characters):")
            print("-" * 50)
            print(response)
            print("-" * 50)
            return 0
        else:
            print("❌ FAILED: No response received from Commander Thea")
            return 1

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 1


def paste_message_command(args):
    """Handle direct message pasting to THEA with validation."""
    print("🤖 THEA Direct Message Mode")
    print("=" * 50)
    print("📋 Instructions:")
    print("1. Prepare your message with project context")
    print("2. Copy the message to clipboard")
    print("3. Press Enter to validate and send to THEA")
    print("=" * 50)

    if not args.auto_validate:
        input("Press Enter when ready to validate and send message to THEA...")

    # Get message from clipboard (simplified approach)
    try:
        import pyperclip

        message = pyperclip.paste()
        if not message.strip():
            print("❌ No message found in clipboard")
            return 1
    except ImportError:
        print("❌ pyperclip not available. Please install: pip install pyperclip")
        return 1

    # Validate message before sending
    print(f"\n🔍 MESSAGE VALIDATION ({len(message)} characters):")
    print("-" * 50)
    
    # Character limit validation
    max_chars = 32000  # ChatGPT character limit
    if len(message) > max_chars:
        print(f"⚠️  WARNING: Message exceeds {max_chars} character limit")
        print(f"   Current: {len(message)} characters")
        print(f"   Excess: {len(message) - max_chars} characters")
        
        if args.auto_validate:
            # Auto-truncate for autonomous operation
            message = message[:max_chars-100] + "\n... [TRUNCATED DUE TO CHARACTER LIMIT]"
            print(f"✅ Message auto-truncated to {len(message)} characters")
        else:
            # Ask if user wants to truncate
            truncate = input(f"\n❓ Truncate message to {max_chars} characters? (y/n): ").lower().strip()
            if truncate == 'y':
                message = message[:max_chars-100] + "\n... [TRUNCATED DUE TO CHARACTER LIMIT]"
                print(f"✅ Message truncated to {len(message)} characters")
            else:
                print("❌ Message too long. Please reduce size and try again.")
                return 1
    
    # Content validation
    if len(message.strip()) < 10:
        print("⚠️  WARNING: Message seems too short (< 10 characters)")
        if args.auto_validate:
            print("✅ Auto-validation: Proceeding with short message")
        else:
            proceed = input("❓ Proceed anyway? (y/n): ").lower().strip()
            if proceed != 'y':
                print("❌ Message validation failed. Please provide a more substantial message.")
                return 1
    
    # Check for common issues
    if message.count('\n') > 100:
        print("⚠️  WARNING: Message has many line breaks (> 100)")
        if args.auto_validate:
            print("✅ Auto-validation: Proceeding with many line breaks")
        else:
            proceed = input("❓ Proceed anyway? (y/n): ").lower().strip()
            if proceed != 'y':
                print("❌ Message validation failed. Please format message better.")
                return 1
    
    # Show validated message preview
    print(f"\n📤 VALIDATED MESSAGE TO SEND ({len(message)} characters):")
    print("-" * 50)
    print(message[:500] + "..." if len(message) > 500 else message)
    print("-" * 50)
    
    # Final confirmation (skip if auto-validate)
    if not args.auto_validate:
        confirm = input("\n❓ Send this validated message to Commander Thea? (y/n): ").lower().strip()
        if confirm != 'y':
            print("❌ Message sending cancelled by user.")
            return 1

    # Send message
    print("\n📤 Sending validated message to Commander Thea...")
    try:
        response = send_thea_message_autonomous(message, headless=not args.visible)

        if response:
            print("\n✅ SUCCESS: Received response from Commander Thea")
            print(f"📋 Response ({len(response)} characters):")
            print("-" * 50)
            print(response)
            print("-" * 50)
            return 0
        else:
            print("❌ FAILED: No response received from Commander Thea")
            return 1

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 1

    """Handle project scan consultation command."""
    context_manager = ProjectContextManager()

    # Read project scan JSON file
    try:
        with open(args.scan_file, encoding="utf-8") as f:
            project_scan_json = f.read()
        print(f"📊 Loaded project scan from: {args.scan_file}")
    except Exception as e:
        print(f"❌ Failed to read project scan file: {e}")
        return 1

    # Create consultation message with project scan context
    message = context_manager.create_project_scan_context(args.question, project_scan_json)

    # Show message preview
    print(f"\n📤 Project Scan Consultation ({len(message)} characters):")
    print("-" * 50)
    print(message)
    print("-" * 50)

    # Autonomous operation - no confirmation needed
    print("\n🤖 Autonomous project scan consultation mode - sending automatically...")

    # Send message
    print("\n📤 Sending project scan consultation to Commander Thea...")
    try:
        response = send_thea_message_autonomous(message, headless=not args.visible)

        if response:
            print("\n✅ SUCCESS: Received response from Commander Thea")
            print(f"📋 Response ({len(response)} characters):")
            print("-" * 50)
            print(response)
            print("-" * 50)
            return 0
        else:
            print("❌ FAILED: No response received from Commander Thea")
            return 1

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 1

    """List available consultation templates."""
    print("📋 Available Strategic Consultation Templates:")
    print("=" * 60)

    for key, question in STRATEGIC_TEMPLATES.items():
        print(f"🔹 {key}")
        print(f"   Question: {question}")
        print()

    print("Usage examples:")
    print(
        "  python src/services/thea/strategic_consultation_cli.py consult --template priority_guidance"
    )
    print(
        "  python src/services/thea/strategic_consultation_cli.py consult --template system_enhancement"
    )


def test_limits_command(args):
    """Test character limits and context delivery."""
    print("🧪 Testing Thea System Limits")
    print("=" * 40)

    context_manager = ProjectContextManager()

    # Test different context levels
    test_cases = [
        ("Essential", context_manager.create_essential_context("Test question")),
        ("Standard", context_manager.create_standard_context("Test question")),
        ("Detailed", context_manager.create_detailed_context("Test question")),
    ]

    for level, message in test_cases:
        print(f"\n📏 {level} Context:")
        print(f"   Characters: {len(message)}")
        print(f"   Words: {len(message.split())}")
        print(f"   Lines: {len(message.split(chr(10)))}")
        print(f"   Preview: {message[:100]}...")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Strategic Consultation CLI for Commander Thea",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick consultation with template
  python src/services/thea/strategic_consultation_cli.py consult --template priority_guidance

  # Custom consultation
  python src/services/thea/strategic_consultation_cli.py consult --question "What should we prioritize?"

  # Status report
  python src/services/thea/strategic_consultation_cli.py status-report

  # Emergency consultation
  python src/services/thea/strategic_consultation_cli.py emergency --issue "System failure detected"

  # List available templates
  python src/services/thea/strategic_consultation_cli.py list-templates

  # Test character limits
  python src/services/thea/strategic_consultation_cli.py test-limits
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Consult command
    consult_parser = subparsers.add_parser(
        "consult", help="Strategic consultation with Commander Thea"
    )
    consult_group = consult_parser.add_mutually_exclusive_group(required=True)
    consult_group.add_argument("--question", help="Custom consultation question")
    consult_group.add_argument("--template", help="Use pre-defined consultation template")
    consult_parser.add_argument(
        "--context-level",
        choices=["essential", "standard", "detailed"],
        default="standard",
        help="Context detail level",
    )
    consult_parser.add_argument("--visible", action="store_true", help="Run in visible mode")
    consult_parser.add_argument(
        "--auto-send", action="store_true", help="Send without confirmation"
    )

    # Status report command
    status_parser = subparsers.add_parser(
        "status-report", help="Send status report to Commander Thea"
    )
    status_parser.add_argument(
        "--additional-status", action="append", help="Additional status items (format: key:value)"
    )
    status_parser.add_argument("--visible", action="store_true", help="Run in visible mode")
    status_parser.add_argument("--auto-send", action="store_true", help="Send without confirmation")

    # Emergency command
    emergency_parser = subparsers.add_parser(
        "emergency", help="Emergency consultation with Commander Thea"
    )
    emergency_parser.add_argument("--issue", required=True, help="Emergency issue description")
    emergency_parser.add_argument("--visible", action="store_true", help="Run in visible mode")

    # Paste message command
    paste_parser = subparsers.add_parser(
        "paste", help="Send message directly from clipboard to THEA"
    )
    paste_parser.add_argument("--visible", action="store_true", help="Run in visible mode")
    paste_parser.add_argument("--auto-validate", action="store_true", help="Auto-validate and send without prompts")
    emergency_parser.add_argument(
        "--auto-send", action="store_true", help="Send without confirmation"
    )

    # List templates command
    subparsers.add_parser("list-templates", help="List available consultation templates")

    # Test limits command
    subparsers.add_parser("test-limits", help="Test character limits and context delivery")

    args = parser.parse_args()

    # Import datetime here to avoid issues

    # Route to appropriate command handler
    if args.command == "consult":
        return consult_command(args)
    elif args.command == "status-report":
        return status_report_command(args)
    elif args.command == "emergency":
        return emergency_command(args)
    elif args.command == "project-scan":
        return project_scan_command(args)
    elif args.command == "paste":
        return paste_message_command(args)
    elif args.command == "list-templates":
        return list_templates_command(args)
    elif args.command == "test-limits":
        return test_limits_command(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
