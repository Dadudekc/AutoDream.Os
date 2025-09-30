#!/usr/bin/env python3
"""
Agent Mode Switcher
==================

Simple utility to switch between different agent modes using the 8-agent framework.

Usage:
    python switch_agent_mode.py four_agent_mode_a    # Switch to Infrastructure & Core Team
    python switch_agent_mode.py four_agent_mode_b    # Switch to Foundation Team
    python switch_agent_mode.py five_agent           # Switch to Quality Focus Team
    python switch_agent_mode.py eight_agent          # Switch to Full Swarm
    python switch_agent_mode.py --status             # Show current mode

Author: Agent-8 (Integration Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, comprehensive error handling
"""

import argparse
from agent_mode_switcher_core import AgentModeSwitcher


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Agent Mode Switcher")
    parser.add_argument("mode", nargs="?", help="Mode to switch to")
    parser.add_argument("--status", action="store_true", help="Show current status")

    args = parser.parse_args()

    switcher = AgentModeSwitcher()

    if args.status:
        switcher.show_status()
    elif args.mode:
        switcher.switch_mode(args.mode)
    else:
        switcher.show_help()


if __name__ == "__main__":
    main()