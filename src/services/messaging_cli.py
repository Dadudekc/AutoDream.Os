#!/usr/bin/env python3
"""
CLI Interface for Unified Messaging Service - Agent Cellphone V2
============================================================

Command-line interface for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
from typing import Dict, Any

from .messaging_core import UnifiedMessagingCore
from .cli_validator import CLIValidator, create_enhanced_parser
from .validation_models import ValidationError
from .messaging_cli_config import load_config_with_precedence
from .messaging_cli_handlers import (
    handle_utility_commands,
    handle_contract_commands,
    handle_onboarding_commands,
    handle_message_commands
)


def create_parser():
    """Create legacy parser for backward compatibility."""
    return create_enhanced_parser()


def main():
    """Main CLI entry point."""
    try:
        # Load configuration with precedence
        config = load_config_with_precedence()
        
        # Create and configure parser
        parser = create_parser()
        args = parser.parse_args()
        
        # Initialize messaging service
        service = UnifiedMessagingCore()
        
        # Handle utility commands first
        if handle_utility_commands(args, service):
            return
        
        # Handle contract commands
        if handle_contract_commands(args):
            return
        
        # Handle onboarding commands
        if handle_onboarding_commands(args, service):
            return
        
        # Handle regular message commands
        if handle_message_commands(args, service):
            return
        
        # If no commands were handled, show help
        parser.print_help()
        
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
