#!/usr/bin/env python3
"""
Agent Get Started Tool
=====================

Quick start tool for agents to begin their cycle with automated devlog creation.

Usage:
    python tools/agent_get_started.py --agent Agent-4 --focus "Your focus area"
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.agent_devlog_automation import auto_create_cycle_start


async def main():
    """Quick start for agents."""
    parser = argparse.ArgumentParser(
        description="Agent Quick Start - Begin your cycle with automated devlog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/agent_get_started.py --agent Agent-4 --focus "V3 system coordination"
  python tools/agent_get_started.py --agent Agent-2 --focus "Architecture review"
  python tools/agent_get_started.py --agent Agent-6 --focus "Communication protocols"
        """,
    )

    parser.add_argument(
        "--agent",
        required=True,
        choices=[f"Agent-{i}" for i in range(1, 9)],
        help="Your agent ID (Agent-1 through Agent-8)",
    )

    parser.add_argument("--focus", required=True, help="Your focus area for this cycle")

    args = parser.parse_args()

    print(f"🚀 Starting cycle for {args.agent}...")
    print(f"🎯 Focus: {args.focus}")
    print()

    try:
        # Create cycle start devlog
        filepath, success = await auto_create_cycle_start(args.agent, args.focus)

        if success:
            print("✅ Cycle started successfully!")
            print(f"📄 Devlog created: {Path(filepath).name}")
            print(f"📢 Posted to {args.agent}'s Discord channel")
            print()
            print("🎉 You're ready to begin your cycle!")
            print("💡 Use 'python tools/agent_cycle_devlog.py --help' for more options")
            return 0
        else:
            print("❌ Failed to start cycle")
            return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
