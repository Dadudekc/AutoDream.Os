#!/usr/bin/env python3
"""
CLI Validator for Messaging System - Agent Cellphone V2
======================================================

Streamlined CLI validation using modular components for V2 compliance.

This module now serves as a lightweight facade over specialized validation
modules, achieving V2 compliance through component orchestration.

Features:
- Modular validation architecture
- Comprehensive error handling
- Structured error reporting
- Enhanced help UX

Exit Codes:
- 0: Success
- 2: Invalid flags/combination
- 3: Dependency missing
- 4: Mode mismatch
- 7: Lock timeout
- 8: Queue full
- 9: Internal error

@maintainer Agent-1 (Integration & Core Systems Specialist)
@license MIT
"""

import argparse
import sys
from typing import Tuple, Optional

from .cli_validator_core import CLIValidatorCore
from .validation_models import ValidationError


class CLIValidator:
    """
    Streamlined CLI validator using modular validation components.

    This class serves as a facade over the modular validation system,
    achieving V2 compliance through component orchestration.
    """

    def __init__(self):
        """Initialize validator with modular core."""
        self.core = CLIValidatorCore()

    def validate_args(self, args: argparse.Namespace) -> Tuple[bool, Optional[ValidationError]]:
        """
        Validate CLI arguments using modular validation components.

        Args:
            args: Parsed CLI arguments

        Returns:
            Tuple of (is_valid, error_details)
        """
        return self.core.validate_args(args)

    def report_error(self, error: ValidationError) -> None:
        """Report validation error to user."""
        self.core.report_error(error)

    def exit_with_error(self, error: ValidationError) -> None:
        """Exit with appropriate error code."""
        self.core.exit_with_error(error)


def create_enhanced_parser() -> argparse.ArgumentParser:
    """Create enhanced argument parser with improved help UX."""
    parser = argparse.ArgumentParser(
        prog="python -m src.services.messaging_cli",
        description="""
🚀 Agent Cellphone V2 - Unified Messaging System

Send messages, manage agents, monitor system health, and process queues.

EXAMPLES:
  # Send to specific agent
  python -m src.services.messaging_cli --agent Agent-7 --message "Hello"

  # System broadcast
  python -m src.services.messaging_cli --bulk --message "System update"

  # Queue management
  python -m src.services.messaging_cli --queue-stats
  python -m src.services.messaging_cli --start-queue-processor

  # Agent management
  python -m src.services.messaging_cli --onboarding
  python -m src.services.messaging_cli --agent Agent-7 --get-next-task
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXIT CODES:
  0: Success
  2: Invalid flag combination
  3: Missing required dependency
  4: Mode mismatch (pyautogui flags with inbox mode)
  7: Lock timeout (message queued)
  8: Queue full
  9: Internal error

For detailed documentation: see docs/messaging_flags_guide_v2.md
        """
    )

    # Message Content Section
    content_group = parser.add_argument_group('📝 Message Content')
    content_group.add_argument(
        "--message", "-m",
        help="Message content to send (required for standard messages)"
    )
    content_group.add_argument(
        "--sender", "-s", default="Captain Agent-4",
        help="Message sender identity (default: Captain Agent-4)"
    )

    # Recipient Selection Section
    recipient_group = parser.add_argument_group('👥 Recipient Selection (Choose One)')
    recipient_group.add_argument(
        "--agent", "-a",
        help="Send to specific agent (e.g., --agent Agent-7)"
    )
    recipient_group.add_argument(
        "--bulk",
        action="store_true",
        help="Send to all agents simultaneously"
    )

    # Message Properties Section
    props_group = parser.add_argument_group('⚙️ Message Properties')
    props_group.add_argument(
        "--type", "-t",
        choices=["text", "broadcast", "onboarding"],
        default="text",
        help="Message category: text (default), broadcast, or onboarding"
    )
    props_group.add_argument(
        "--priority", "-p",
        choices=["regular", "urgent"],
        default="regular",
        help="Delivery priority: regular (DEFAULT - use this) or urgent (EMERGENCY ONLY)"
    )
    props_group.add_argument(
        "--high-priority",
        action="store_true",
        help="⚠️ FORCE URGENT PRIORITY (EMERGENCY USE ONLY - disrupts agent workflow)"
    )

    # Delivery Mode Section
    mode_group = parser.add_argument_group('📨 Delivery Mode')
    mode_group.add_argument(
        "--mode",
        choices=["pyautogui", "inbox"],
        default="pyautogui",
        help="Delivery method: pyautogui (interactive) or inbox (file-based)"
    )
    mode_group.add_argument(
        "--no-paste",
        action="store_true",
        help="[PyAutoGUI only] Use keystroke typing instead of clipboard paste"
    )
    mode_group.add_argument(
        "--new-tab-method",
        choices=["ctrl_t", "ctrl_n"],
        default="ctrl_t",
        help="[PyAutoGUI only] Tab creation: ctrl_t (new tab) or ctrl_n (new window)"
    )

    # Utility/Information Section
    util_group = parser.add_argument_group('🔍 Utility & Information')
    util_group.add_argument(
        "--list-agents",
        action="store_true",
        help="Display all available agents with details"
    )
    util_group.add_argument(
        "--coordinates",
        action="store_true",
        help="Show PyAutoGUI coordinate positions for agents"
    )
    util_group.add_argument(
        "--history",
        action="store_true",
        help="Show message delivery history and audit trail"
    )
    util_group.add_argument(
        "--check-status",
        action="store_true",
        help="Check status of all agents and contract availability"
    )

    # Queue Management Section
    queue_group = parser.add_argument_group('📊 Queue Management')
    queue_group.add_argument(
        "--queue-stats",
        action="store_true",
        help="Display message queue statistics (pending/processing/delivered/failed)"
    )
    queue_group.add_argument(
        "--process-queue",
        action="store_true",
        help="Process one batch of queued messages immediately"
    )
    queue_group.add_argument(
        "--start-queue-processor",
        action="store_true",
        help="Start continuous background queue processor"
    )
    queue_group.add_argument(
        "--stop-queue-processor",
        action="store_true",
        help="Stop continuous background queue processor"
    )

    # Onboarding Section
    onboard_group = parser.add_argument_group('🎓 Onboarding & Training')
    onboard_group.add_argument(
        "--onboarding",
        action="store_true",
        help="Send onboarding message to ALL agents (bulk operation)"
    )
    onboard_group.add_argument(
        "--onboard",
        action="store_true",
        help="[Requires --agent] Send onboarding message to specific agent"
    )
    onboard_group.add_argument(
        "--onboarding-style",
        choices=["friendly", "professional"],
        default="friendly",
        help="Onboarding message tone: friendly (casual) or professional (formal)"
    )
    onboard_group.add_argument(
        "--compliance-mode",
        action="store_true",
        help="🎯 AUTONOMOUS DEVELOPMENT MODE: Onboard all agents for autonomous development with compliance protocols (technical debt elimination, V2 standards, 8x efficiency)"
    )

    # Contract/Task Section
    task_group = parser.add_argument_group('📋 Contract & Task Management')
    task_group.add_argument(
        "--get-next-task",
        action="store_true",
        help="[Requires --agent] Claim next contract task for specified agent"
    )
    task_group.add_argument(
        "--wrapup",
        action="store_true",
        help="Send system wrapup message to ALL agents (bulk closure)"
    )

    return parser


def validate_and_parse_args() -> Tuple[argparse.Namespace, CLIValidator]:
    """Parse and validate CLI arguments with enhanced error handling."""
    parser = create_enhanced_parser()
    args = parser.parse_args()

    # Initialize validator
    validator = CLIValidator()

    # Validate arguments
    is_valid, error = validator.validate_args(args)

    if not is_valid and error:
        validator.exit_with_error(error)

    return args, validator
