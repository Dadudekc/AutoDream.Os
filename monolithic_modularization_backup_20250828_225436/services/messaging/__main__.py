#!/usr/bin/env python3
"""
Main Entry Point - Agent Cellphone V2 Messaging
===============================================

Main entry point for the messaging service.
Single responsibility: Main execution only.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys

from src.utils.stability_improvements import stability_manager, safe_import
from .cli_interface import MessagingCLI


def main():
    """Main entry point for the messaging service"""
    try:
        cli = MessagingCLI()
        success = cli.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
