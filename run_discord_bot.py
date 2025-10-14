#!/usr/bin/env python3
"""
Discord Bot Launcher
====================

Simple launcher for Discord Commander.

Usage:
    python run_discord_bot.py

Launches: run_discord_commander.py
"""

import subprocess
import sys

if __name__ == "__main__":
    sys.exit(subprocess.call([sys.executable, "run_discord_commander.py"]))
