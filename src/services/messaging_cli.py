#!/usr/bin/env python3
"""
CLI Interface for Unified Messaging Service - Agent Cellphone V2
============================================================

Command-line interface for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import argparse
from .messaging_cli_handlers import (
    handle_contract_commands,
    handle_message_commands,
    handle_onboarding_commands,
    handle_utility_commands,
    handle_overnight_commands,
)


def create_enhanced_parser():
    """Create enhanced argument parser."""
    parser = argparse.ArgumentParser(description="Unified Messaging CLI")
    
    # Message arguments
    parser.add_argument("--message", "-m", help="Message content")
    parser.add_argument("--agent", "-a", help="Target agent")
    parser.add_argument("--sender", "-s", default="Captain Agent-4", help="Sender name")
    parser.add_argument("--bulk", action="store_true", help="Send to all agents")
    parser.add_argument("--mode", choices=["pyautogui", "inbox"], default="pyautogui", help="Delivery mode")
    
    # Message type and priority
    parser.add_argument("--type", "-t", default="text", help="Message type")
    parser.add_argument("--priority", "-p", default="regular", help="Message priority")
    parser.add_argument("--high-priority", action="store_true", help="Set high priority")
    
    # Utility commands
    parser.add_argument("--coordinates", action="store_true", help="Show agent coordinates")
    parser.add_argument("--check-status", action="store_true", help="Check agent status")
    parser.add_argument("--list-agents", action="store_true", help="List all agents")
    parser.add_argument("--history", action="store_true", help="Show message history")
    
    # Onboarding commands
    parser.add_argument("--onboarding", action="store_true", help="Send onboarding to all agents")
    parser.add_argument("--onboard", action="store_true", help="Send onboarding to specific agent")
    parser.add_argument("--onboarding-style", choices=["friendly", "professional"], default="friendly", help="Onboarding style")
    parser.add_argument("--compliance-mode", action="store_true", help="Activate compliance mode")
    parser.add_argument("--wrapup", action="store_true", help="Send wrapup message")
    parser.add_argument("--hard-onboarding", action="store_true", help="Send hard onboarding sequence")
    
    # Contract commands
    parser.add_argument("--get-next-task", action="store_true", help="Get next task for agent")
    parser.add_argument("--check-contracts", action="store_true", help="Check contract status")
    
    # Additional options
    parser.add_argument("--no-paste", action="store_true", help="Don't use paste method")
    parser.add_argument("--new-tab-method", choices=["ctrl_t", "ctrl_n"], default="ctrl_t", help="New tab method")
    
    # Overnight autonomous system
    parser.add_argument("--overnight", action="store_true", help="Start overnight autonomous work cycle system")
    
    return parser


def create_parser():
    """Create legacy parser for backward compatibility."""
    return create_enhanced_parser()


def main():
    """Main entry point for messaging CLI."""
    parser = create_enhanced_parser()
    args = parser.parse_args()

    # Handle overnight commands
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


if __name__ == "__main__":
    main()
