#!/usr/bin/env python3
"""
Discord Commander Launcher
==========================

Comprehensive launcher for the Discord Commander system.
Starts both the Discord bot and the web controller interface.

Usage:
    python run_discord_commander.py

Features:
- Automatic Discord bot startup with configuration validation
- Web-based controller interface on port 8080
- Real-time monitoring and control
- Comprehensive logging and error handling
- Environment validation and setup guidance
"""

import sys
from discord_commander_launcher_core import DiscordCommanderLauncher


def main():
    """Main function."""
    launcher = DiscordCommanderLauncher()
    success = launcher.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()