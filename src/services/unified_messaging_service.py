#!/usr/bin/env python3
"""
Unified Messaging Service - Agent Cellphone V2 (V2 Compliant)
==========================================================

V2-compliant unified messaging service using modularized components.

Author: V2 SWARM CAPTAIN
License: MIT
"""

# Import modularized components
from .messaging_core import UnifiedMessagingCore
from .messaging_cli import create_parser, main as cli_main


class UnifiedMessagingService(UnifiedMessagingCore):
    """V2-compliant unified messaging service using modularized components."""
    
    def __init__(self):
        """Initialize the messaging service using core functionality."""
        super().__init__()


def main():
    """Main entry point for backward compatibility."""
    cli_main()


if __name__ == "__main__":
    main()
