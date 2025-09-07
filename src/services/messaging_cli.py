#!/usr/bin/env python3
"""
CLI Interface for Unified Messaging Service - Agent Cellphone V2
============================================================

Command-line interface for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import argparse
def create_enhanced_parser():
    """Create enhanced argument parser."""
    parser = argparse.ArgumentParser(description="Unified Messaging CLI")

    # Message arguments
    parser.add_argument("--message", "-m", help="Message content")
    parser.add_argument("--agent", "-a", help="Target agent")
    parser.add_argument("--sender", "-s", default="Captain Agent-4", help="Sender name")
    parser.add_argument("--bulk", action="store_true", help="Send to all agents")
    parser.add_argument(
        "--delivery-mode",
        choices=["pyautogui", "inbox"],
        default="pyautogui",
        help="Delivery mode",
    )

    # Message type and priority
    parser.add_argument("--type", "-t", default="text", help="Message type")
    parser.add_argument("--priority", "-p", default="regular", help="Message priority")
    parser.add_argument(
        "--high-priority", action="store_true", help="Set high priority"
    )

    # Utility commands
    parser.add_argument(
        "--coordinates", action="store_true", help="Show agent coordinates"
    )
    parser.add_argument(
        "--check-status", action="store_true", help="Check agent status"
    )
    parser.add_argument("--list-agents", action="store_true", help="List all agents")
    parser.add_argument("--history", action="store_true", help="Show message history")

    # Onboarding commands
    parser.add_argument(
        "--onboarding", action="store_true", help="Send onboarding to all agents"
    )
    parser.add_argument(
        "--onboard", action="store_true", help="Send onboarding to specific agent"
    )
    parser.add_argument(
        "--onboarding-style",
        choices=["friendly", "professional", "architectural"],
        default="friendly",
        help="Onboarding style (architectural enables principle-based onboarding)",
    )
    parser.add_argument(
        "--architectural-principle",
        choices=["SRP", "OCP", "LSP", "ISP", "DIP", "SSOT", "DRY", "KISS", "TDD"],
        help="Specific architectural principle for onboarding (overrides agent assignment)",
    )
    parser.add_argument(
        "--compliance-mode", action="store_true", help="Activate compliance mode"
    )
    parser.add_argument("--wrapup", action="store_true", help="Send wrapup message")

    # Hard onboarding with safety options
    parser.add_argument(
        "--hard-onboarding",
        action="store_true",
        help="Run hard onboarding sequence for agents",
    )
    parser.add_argument(
        "--audit-cleanup",
        action="store_true",
        help="After onboarding, run cleanup auditor and fail on guard",
    )
    parser.add_argument(
        "--agents",
        type=str,
        default="",
        help="Comma-separated agent IDs to scope the operation",
    )
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompts")
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without making changes"
    )
    parser.add_argument(
        "--timeout", type=int, default=30, help="Per-agent timeout seconds"
    )

    # UI mode
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Use PyAutoGUI to deliver onboarding via UI automation",
    )
    parser.add_argument(
        "--ui-retries", type=int, default=1, help="UI validation retries"
    )
    parser.add_argument(
        "--ui-tolerance", type=int, default=3, help="Pixel tolerance for UI validation"
    )

    # NEW: Onboarding Modes & Proof
    parser.add_argument(
        "--onboarding-mode",
        type=str,
        default="quality-suite",
        choices=["quality-suite", "solid", "ssot", "dry", "kiss", "tdd"],
        help="Role assignment mode for onboarding",
    )
    parser.add_argument(
        "--assign-roles",
        type=str,
        default="",
        help="Explicit role map: 'Agent-1:SOLID,Agent-2:DRY'",
    )
    parser.add_argument(
        "--proof", action="store_true", help="Emit TDD proof ledger after onboarding"
    )

    # Contract commands
    parser.add_argument(
        "--get-next-task", action="store_true", help="Get next task for agent"
    )
    parser.add_argument(
        "--check-contracts", action="store_true", help="Check contract status"
    )

    # Additional options
    parser.add_argument(
        "--no-paste", action="store_true", help="Don't use paste method"
    )
    parser.add_argument(
        "--new-tab-method",
        choices=["ctrl_t", "ctrl_n"],
        default="ctrl_t",
        help="New tab method",
    )

    # Overnight autonomous system
    parser.add_argument(
        "--overnight",
        action="store_true",
        help="Start overnight autonomous work cycle system",
    )

    return parser


def create_parser():
    """Create legacy parser for backward compatibility."""
    return create_enhanced_parser()


def handle_contract_commands(args):
    """Lazy import wrapper for contract commands."""
    from .messaging_cli_handlers import (
        handle_contract_commands as _handle_contract_commands,
    )

    return _handle_contract_commands(args)


def handle_message_commands(args):
    """Lazy import wrapper for message commands."""
    from .messaging_cli_handlers import (
        handle_message_commands as _handle_message_commands,
    )

    return _handle_message_commands(args)


def handle_onboarding_commands(args):
    """Lazy import wrapper for onboarding commands."""
    from .messaging_cli_handlers import (
        handle_onboarding_commands as _handle_onboarding_commands,
    )

    return _handle_onboarding_commands(args)


def handle_utility_commands(args):
    """Lazy import wrapper for utility commands."""
    from .messaging_cli_handlers import (
        handle_utility_commands as _handle_utility_commands,
    )

    return _handle_utility_commands(args)


def handle_overnight_commands(args):
    """Lazy import wrapper for overnight commands."""
    from .messaging_cli_handlers import (
        handle_overnight_commands as _handle_overnight_commands,
    )

    return _handle_overnight_commands(args)


def main():
    """Main entry point for messaging CLI."""
    parser = create_enhanced_parser()
    args = parser.parse_args()

    if handle_overnight_commands(args):
        return

    # Handle utility commands first
    if handle_utility_commands(args):
        return

    # Handle contract commands
    if handle_contract_commands(args):
        return

    # Handle onboarding commands
    if handle_onboarding_commands(args):
        return

    # Handle regular message commands (only if message is provided)
    if args.message:
        if handle_message_commands(args):
            return

    # If no specific command was handled, show help
    parser.print_help()


import sys
import os

from .models.messaging_models import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)
from .messaging_core import UnifiedMessagingCore
from .contract_service import ContractService


def create_parser():
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Unified Messaging Service - Agent Cellphone V2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send message to specific agent
  python -m src.services.messaging_cli --agent Agent-5 --message "Hello from Captain" --sender "Captain Agent-4"
  
  # Send bulk message to all agents
  python -m src.services.messaging_cli --bulk --message "System update" --sender "Captain Agent-4"
  
  # Send onboarding to all agents
  python -m src.services.messaging_cli --onboarding --onboarding-style friendly
  
  # List all agents
  python -m src.services.messaging_cli --list-agents
  
  # Show coordinates
  python -m src.services.messaging_cli --coordinates
  
  # Show message history
  python -m src.services.messaging_cli --history
        """
    )
    
    # Message sending options
    parser.add_argument("--message", "-m", help="Message content to send")
    parser.add_argument("--sender", "-s", default="Captain Agent-4", help="Message sender (default: Captain Agent-4)")
    parser.add_argument("--agent", "-a", help="Specific agent to send message to")
    parser.add_argument("--bulk", action="store_true", help="Send message to all agents")
    
    # Message properties
    parser.add_argument("--type", "-t", default="text", choices=["text", "broadcast", "onboarding"],
                       help="Message type (default: text)")
    parser.add_argument("--priority", "-p", default="normal", choices=["normal", "urgent"],
                       help="Message priority (default: normal)")
    parser.add_argument("--high-priority", action="store_true", help="Set message as high priority (overrides --priority)")
    
    # Delivery options
    parser.add_argument("--mode", default="pyautogui", choices=["pyautogui", "inbox"],
                       help="Delivery mode (default: pyautogui)")
    parser.add_argument("--no-paste", action="store_true", help="Disable paste mode (use typing instead)")
    parser.add_argument("--new-tab-method", default="ctrl_t", choices=["ctrl_t", "ctrl_n"],
                       help="New tab method for PyAutoGUI mode (default: ctrl_t)")
    
    # Utility commands
    parser.add_argument("--list-agents", action="store_true", help="List all available agents")
    parser.add_argument("--coordinates", action="store_true", help="Show agent coordinates")
    parser.add_argument("--history", action="store_true", help="Show message history")
    parser.add_argument("--get-next-task", action="store_true", help="Get next task for a specific agent")
    parser.add_argument("--check-status", action="store_true", help="Check status of all agents and contract availability")
    
    # Onboarding commands
    parser.add_argument("--onboarding", action="store_true", help="Send onboarding message to all agents (SSOT template)")
    parser.add_argument("--onboard", action="store_true", help="Send onboarding message to specific agent (SSOT template)")
    parser.add_argument("--onboarding-style", default="friendly", choices=["friendly", "professional"],
                       help="Onboarding message style (default: friendly)")
    
    # Wrapup command
    parser.add_argument("--wrapup", action="store_true", help="Send wrapup message to all agents")
    
    return parser


def handle_utility_commands(args, service):
    """Handle utility commands that don't require message content."""
    if args.list_agents:
        service.list_agents()
        return True

    if args.coordinates:
        service.show_coordinates()
        return True

    if args.history:
        service.show_message_history()
        return True

    return False


def handle_contract_commands(args):
    """Handle contract system commands."""
    if args.get_next_task:
        return handle_get_next_task(args)
    elif args.check_status:
        return handle_check_status()
    return False


def handle_get_next_task(args):
    """Handle get-next-task command with contract assignment."""
    if not args.agent:
        print("❌ ERROR: --agent is required with --get-next-task")
        print("Usage: python -m src.services.messaging_cli --agent Agent-X --get-next-task")
        sys.exit(1)

    print(f"🎯 CONTRACT TASK ASSIGNMENT - {args.agent}")
    print("=" * 50)

    contract_service = get_contract_service()
    contract = contract_service.get_contract(args.agent)

    if contract:
        contract_service.display_contract_assignment(args.agent, contract)
    else:
        contracts = contract_service.contracts
        print(f"❌ ERROR: No contracts available for {args.agent}")
        print("Available agents: " + ", ".join(contracts.keys()))
    return True


def get_contract_service():
    """Get initialized contract service."""
    return ContractService()


def handle_check_status():
    """Handle check-status command."""
    contract_service = get_contract_service()
    contract_service.check_agent_status()
    return True


def handle_onboarding_commands(args, service):
    """Handle onboarding-related commands."""
    if args.onboarding:
        # Delegate to core bulk onboarding using SSOT template
        service.send_bulk_onboarding(style=args.onboarding_style, mode=args.mode, new_tab_method=args.new_tab_method)
        return True

    if args.onboard:
        if not args.agent:
            print("❌ ERROR: --agent is required with --onboard")
            print("Usage: python -m src.services.messaging_cli --onboard --agent Agent-X [--onboarding-style friendly|professional] [--mode inbox|pyautogui]")
            sys.exit(1)
        service.send_onboarding_message(agent_id=args.agent, style=args.onboarding_style, mode=args.mode, new_tab_method=args.new_tab_method)
        return True

    if args.wrapup:
        return handle_wrapup_command(args, service)

    return False


def handle_wrapup_command(args, service):
    """Handle wrapup command."""
    print("🏁 WRAPUP SEQUENCE ACTIVATED")
    wrapup_content = """🚨 **CAPTAIN AGENT-4 - AGENT ACTIVATION & WRAPUP** 🚨

**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager
**Status**: Agent activation and system wrapup
**Mode**: Optimized workflow with Ctrl+T

**AGENT ACTIVATION**:
- ✅ **New Tab Created**: Ready for agent input
- ✅ **System Integration**: Messaging system optimized
- ✅ **Contract System**: 40+ contracts available
- ✅ **Coordination**: PyAutoGUI messaging active

**READY FOR**: Agent response and task assignment

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**

**WE. ARE. SWARM.** ⚡️🔥"""

    service.send_to_all_agents(
        content=wrapup_content,
        sender="Captain Agent-4",
        message_type=UnifiedMessageType.BROADCAST,
        priority=UnifiedMessagePriority.NORMAL,
        tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.WRAPUP],
        mode=args.mode,
        use_paste=True,
    )
    return True


def handle_message_commands(args, service):
    """Handle regular message sending commands."""
    # Check if message is required for sending
    if not args.message:
        print("❌ ERROR: --message/-m is required for sending messages")
        print("Use --list-agents, --coordinates, --history, --onboarding, --onboard, or --wrapup for utility commands")
        sys.exit(1)

    # Determine message type and priority
    message_type = UnifiedMessageType(args.type)
    priority = UnifiedMessagePriority.URGENT if args.high_priority else UnifiedMessagePriority(args.priority)

    # Determine paste mode and new tab method
    use_paste = not args.no_paste
    new_tab_method = args.new_tab_method

    # Send message
    if args.bulk:
        # Send to all agents
        service.send_to_all_agents(
            content=args.message,
            sender=args.sender,
            message_type=message_type,
            priority=priority,
            tags=[UnifiedMessageTag.CAPTAIN],
            mode=args.mode,
            use_paste=use_paste,
            new_tab_method=new_tab_method,
            use_new_tab=False,  # Regular messages don't create new tabs
        )
    elif args.agent:
        # Send to specific agent
        service.send_message(
            content=args.message,
            sender=args.sender,
            recipient=args.agent,
            message_type=message_type,
            priority=priority,
            tags=[UnifiedMessageTag.CAPTAIN],
            mode=args.mode,
            use_paste=use_paste,
            new_tab_method=new_tab_method,
            use_new_tab=False,  # Regular messages don't create new tabs
        )
    else:
        print("❌ ERROR: Must specify --agent or --bulk")
        sys.exit(1)


def main():
    """Main CLI entry point - now clean and under 30 lines."""
    parser = create_parser()
    args = parser.parse_args()

    # Initialize messaging service
    service = UnifiedMessagingCore()

    # Handle commands in priority order
    if handle_utility_commands(args, service):
        return
    if handle_contract_commands(args):
        return
    if handle_onboarding_commands(args, service):
        return

    # Handle message commands (requires --message)
    handle_message_commands(args, service)


if __name__ == "__main__":
    main()
