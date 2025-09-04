#!/usr/bin/env python3
"""
Unified Entry Point System - Agent Cellphone V2
==============================================

Unified entry point for all CLI applications.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import asyncio
import sys
from typing import Any, Dict

from .unified_logging_system import get_logger


async def main():
    """Main CLI entry point."""
    try:
        # Load configuration with precedence
        from ..services.messaging_cli_config import load_config_with_precedence
        config = load_config_with_precedence()

        # Create and configure parser
        from ..services.messaging_cli import create_parser
        parser = create_parser()
        args = parser.parse_args()

        # Initialize messaging service with configuration
        from ..services.messaging_core_orchestrator import MessagingCoreOrchestrator
        service = MessagingCoreOrchestrator(config=config)

        # Handle utility commands first
        from ..services.messaging_cli_handlers import handle_utility_commands
        if await handle_utility_commands(args, service):
            return

        # Handle contract commands
        from ..services.messaging_cli_handlers import handle_contract_commands
        if handle_contract_commands(args):
            return

        # Handle onboarding commands
        from ..services.messaging_cli_handlers import handle_onboarding_commands
        if await handle_onboarding_commands(args, service):
            return

        # Handle regular message commands (only if message is provided)
        if args.message:
            from ..services.messaging_cli_handlers import handle_message_commands
            if await handle_message_commands(args, service):
                return

        # If no commands were handled, show help
        parser.print_help()

    except KeyboardInterrupt:
        get_logger(__name__).info("\n⚠️ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        get_logger(__name__).info(f"❌ UNEXPECTED ERROR: {e}")
        sys.exit(1)
