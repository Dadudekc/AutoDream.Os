#!/usr/bin/env python3
"""
CLI Interface for Unified Messaging Service - Agent Cellphone V2
============================================================

Command-line interface for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import argparse
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
