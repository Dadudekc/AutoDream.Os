#!/usr/bin/env python3
"""
🐝 UNIFIED MESSAGING CLI - SWARM COMMAND CENTER
==============================================

V2 Compliance: Refactored to <300 lines
SOLID Principles: Single Responsibility, Open-Closed

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
"""

import logging
import sys
from pathlib import Path

from src.services.messaging_cli_handlers import (
    handle_consolidation,
    handle_coordinates,
    handle_leaderboard,
    handle_message,
    handle_save,
    handle_start_agents,
    handle_survey,
)
from src.services.messaging_cli_parser import create_messaging_parser

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from src.core.messaging_core import (
        UnifiedMessagePriority,
        UnifiedMessageTag,
        UnifiedMessageType,
        send_message,
    )

    MESSAGING_AVAILABLE = True
except ImportError as e:
    logger.error(f"❌ Messaging system not available: {e}")
    MESSAGING_AVAILABLE = False


class MessagingCLI:
    """Command-line interface for messaging operations."""

    def __init__(self):
        self.parser = create_messaging_parser()

    def execute(self, args=None):
        """Execute CLI command based on arguments."""
        if not MESSAGING_AVAILABLE:
            return 1

        parsed_args = self.parser.parse_args(args)

        try:
            if parsed_args.message or parsed_args.broadcast:
                return handle_message(parsed_args, self.parser)
            elif parsed_args.survey_coordination:
                return handle_survey()
            elif parsed_args.consolidation_coordination:
                return handle_consolidation(parsed_args)
            elif parsed_args.coordinates:
                return handle_coordinates()
            elif parsed_args.start:
                return handle_start_agents(parsed_args)
            elif parsed_args.save:
                return handle_save(parsed_args, self.parser)
            elif parsed_args.leaderboard:
                return handle_leaderboard()
            else:
                self.parser.print_help()
                return 0
        except Exception as e:
            logger.error(f"❌ CLI execution error: {e}")
            return 1


def main() -> int:
    """Main entry point."""
    cli = MessagingCLI()
    return cli.execute()


if __name__ == "__main__":
    exit_code = main()
    print()  # Add line break for agent coordination
    print("🐝 WE. ARE. SWARM. ⚡️🔥")  # Completion indicator
    sys.exit(exit_code)
