"""Argument parser for messaging CLI commands."""

from __future__ import annotations

import argparse
from typing import List

from .interfaces import MessagingMode, MessageType
from .config import DEFAULT_MODE, DEFAULT_COORDINATE_MODE


def create_parser(argv: List[str] | None = None) -> argparse.ArgumentParser:
    """Create the argument parser for the messaging CLI."""
    parser = argparse.ArgumentParser(
        description="Unified Messaging Service CLI - Agent Communication System",
        epilog="""
Examples:
  # Send message to specific agent
  python -m src.services.messaging --agent Agent-1 --message "Hello Agent-1!"
  
  # Send to all agents
  python -m src.services.messaging --bulk --message "Message to all agents"
  
  # High priority message
  python -m src.services.messaging --agent Agent-1 --message "URGENT!" --high-priority
  
  # Onboard all agents
  python -m src.services.messaging --onboard
  
  # Onboard with specific style
  python -m src.services.messaging --onboard --onboarding-style strict
  
  # Execute wrapup sequence
  python -m src.services.messaging --wrapup
  
  # Check agent statuses
  python -m src.services.messaging --check-status
  
  # Get next task
  python -m src.services.messaging --get-next-task
  
  # Send to Captain
  python -m src.services.messaging --captain --message "Status update"
  
  # Show coordinates
  python -m src.services.messaging --coordinates
  
  # Validate coordinates
  python -m src.services.messaging --validate
        """
    )
    
    # Custom help flag with enhanced description
    parser.add_argument(
        "--help", "-h",
        action="store_true",
        help="Show detailed help information with examples and usage patterns"
    )
    
    # Quick help flag for common operations
    parser.add_argument(
        "--quick-help", "-q",
        action="store_true",
        help="Show quick reference for most common messaging operations"
    )

    # Mode selection
    parser.add_argument(
        "--mode",
        type=str,
        choices=[m.value for m in MessagingMode],
        default=DEFAULT_MODE,
        help="Messaging mode",
    )

    # Coordinate mode selection
    parser.add_argument(
        "--coordinate-mode",
        type=str,
        default=DEFAULT_COORDINATE_MODE,
        help="Coordinate mode to use",
    )

    # Message content
    parser.add_argument("--message", type=str, help="Message content to send")

    # Recipient options
    parser.add_argument("--agent", type=str, help="Send to specific agent")
    parser.add_argument(
        "--bulk", action="store_true", help="Send to all agents in 8-agent mode"
    )
    parser.add_argument(
        "--campaign", action="store_true", help="Campaign mode (election broadcast)"
    )
    parser.add_argument(
        "--yolo", action="store_true", help="YOLO mode (automatic activation)"
    )

    # Message type
    parser.add_argument(
        "--type",
        type=str,
        choices=[t.value for t in MessageType],
        default="text",
        help="Message type",
    )

    # High priority flag
    parser.add_argument(
        "--high-priority",
        action="store_true",
        help="Send as HIGH PRIORITY message (Ctrl+Enter 2x)",
    )

    # Onboarding flags
    parser.add_argument(
        "--onboarding",
        action="store_true",
        help="Send as onboarding message (new chat sequence)",
    )
    parser.add_argument(
        "--new-chat",
        action="store_true",
        help="Send as new chat message (onboarding sequence)",
    )
    parser.add_argument(
        "--onboard",
        action="store_true",
        help="Automatically onboard all agents with contract assignment and simplified system overview",
    )
    parser.add_argument(
        "--onboarding-style",
        type=str,
        choices=["friendly", "strict"],
        default="friendly",
        help="Onboarding style: friendly (warm guidance) or strict (authoritative compliance)",
    )
    parser.add_argument(
        "--wrapup",
        action="store_true",
        help="Execute wrapup sequence: validate implementations, check for duplication, ensure coding standards compliance, and clean up technical debt",
    )
    parser.add_argument(
        "--check-status",
        action="store_true",
        help="Check all agent statuses from their status.json files",
    )

    # Coordinate validation
    parser.add_argument("--validate", action="store_true", help="Validate coordinates")

    # Contract automation flags
    parser.add_argument("--claim-contract", type=str, help="Claim a contract by ID")
    parser.add_argument(
        "--complete-contract", type=str, help="Complete a contract by ID"
    )
    parser.add_argument(
        "--get-next-task",
        action="store_true",
        help="Get next available task from queue",
    )
    parser.add_argument(
        "--contract-status",
        action="store_true",
        help="Show contract claiming status",
    )

    # Captain communication flags
    parser.add_argument(
        "--captain",
        action="store_true",
        help="Send message directly to Captain (Agent-4) with automatic agent identification and contract generation prompt",
    )

    # Resume system flags
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume perpetual motion system with automatic workflow restoration messages",
    )
    parser.add_argument(
        "--resume-captain",
        action="store_true",
        help="Send Captain resume message for strategic oversight",
    )
    parser.add_argument(
        "--resume-agents",
        action="store_true",
        help="Send Agent resume message for perpetual motion workflow",
    )

    # Coordinate management flags
    parser.add_argument(
        "--coordinates",
        action="store_true",
        help="Show coordinate mapping for all agents",
    )
    parser.add_argument(
        "--map-mode",
        type=str,
        default=DEFAULT_COORDINATE_MODE,
        help="Coordinate mode to map",
    )
    parser.add_argument(
        "--consolidate",
        action="store_true",
        help="Consolidate coordinate files from multiple sources",
    )
    parser.add_argument(
        "--calibrate",
        nargs=5,
        metavar=("AGENT", "INPUT_X", "INPUT_Y", "STARTER_X", "STARTER_Y"),
        help="Calibrate coordinates for a specific agent (AGENT INPUT_X INPUT_Y STARTER_X STARTER_Y)",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run interactive coordinate capture for all agents",
    )
    parser.add_argument(
        "--interactive-mode",
        type=str,
        default=DEFAULT_COORDINATE_MODE,
        help="Mode for interactive coordinate capture",
    )

    return parser
