#!/usr/bin/env python3
"""
Discord Commander Setup Script - V2 Compliant (Refactored)
=========================================================

Refactored Discord Commander setup importing from modular components.
Maintains backward compatibility while achieving V2 compliance.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import sys
from pathlib import Path

from discord_commander_setup_core import DiscordCommanderSetupCore

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    """Main entry point for Discord Commander setup."""
    print("🚀 Starting Discord Commander Setup")
    
    # Initialize setup core
    setup_core = DiscordCommanderSetupCore()
    
    # Run setup
    success = setup_core.run_setup()
    
    if success:
        print("\n✅ Discord Commander setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Discord Commander setup failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()