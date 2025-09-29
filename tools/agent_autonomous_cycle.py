#!/usr/bin/env python3
"""
Agent Autonomous Cycle Tool
==========================

Command-line tool for agents to run their autonomous workflow cycles.
This tool implements the complete autonomous agent workflow including:
- Mailbox checking and message processing
- Task status evaluation and progression
- Task claiming from future tasks
- Blocker resolution
- Autonomous operation
- Automated devlog creation

Usage:
    python tools/agent_autonomous_cycle.py --agent Agent-4
    python tools/agent_autonomous_cycle.py --agent Agent-2 --continuous
    python tools/agent_autonomous_cycle.py --agent Agent-6 --cycles 5
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.agent_autonomous_workflow import run_agent_autonomous_cycle


async def main():
    """Run autonomous cycle for agent."""
    parser = argparse.ArgumentParser(
        description="Agent Autonomous Cycle - Run complete autonomous workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/agent_autonomous_cycle.py --agent Agent-4
  python tools/agent_autonomous_cycle.py --agent Agent-2 --continuous
  python tools/agent_autonomous_cycle.py --agent Agent-6 --cycles 5
  python tools/agent_autonomous_cycle.py --agent Agent-1 --verbose
        """,
    )

    parser.add_argument(
        "--agent",
        required=True,
        choices=[f"Agent-{i}" for i in range(1, 9)],
        help="Agent ID (Agent-1 through Agent-8)",
    )

    parser.add_argument(
        "--continuous", action="store_true", help="Run continuous cycles (until interrupted)"
    )

    parser.add_argument(
        "--cycles", type=int, default=1, help="Number of cycles to run (default: 1)"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Interval between cycles in seconds (default: 300 = 5 minutes)",
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    parser.add_argument("--output", help="Output file for cycle results (JSON format)")

    args = parser.parse_args()

    if args.verbose:
        import logging

        logging.basicConfig(level=logging.INFO)

    print(f"🤖 Starting autonomous cycle for {args.agent}")
    print(f"🔄 Mode: {'Continuous' if args.continuous else f'{args.cycles} cycle(s)'}")
    if args.continuous or args.cycles > 1:
        print(f"⏱️  Interval: {args.interval} seconds")
    print()

    cycle_results = []

    try:
        if args.continuous:
            cycle_count = 0
            while True:
                cycle_count += 1
                print(f"🔄 Cycle {cycle_count} starting...")

                result = await run_agent_autonomous_cycle(args.agent)
                cycle_results.append(result)

                print(f"✅ Cycle {cycle_count} completed")
                print(f"📊 Actions: {len(result.get('actions_taken', []))}")
                print(f"📨 Messages: {result.get('messages_processed', 0)}")
                print(f"📋 Tasks: {result.get('tasks_processed', 0)}")
                print(f"📝 Devlogs: {result.get('devlogs_created', 0)}")

                if result.get("error"):
                    print(f"❌ Error: {result['error']}")

                print(f"⏳ Waiting {args.interval} seconds until next cycle...")
                print("-" * 50)

                await asyncio.sleep(args.interval)

        else:
            for cycle in range(1, args.cycles + 1):
                print(f"🔄 Cycle {cycle}/{args.cycles} starting...")

                result = await run_agent_autonomous_cycle(args.agent)
                cycle_results.append(result)

                print(f"✅ Cycle {cycle} completed")
                print(f"📊 Actions: {len(result.get('actions_taken', []))}")
                print(f"📨 Messages: {result.get('messages_processed', 0)}")
                print(f"📋 Tasks: {result.get('tasks_processed', 0)}")
                print(f"📝 Devlogs: {result.get('devlogs_created', 0)}")

                if result.get("error"):
                    print(f"❌ Error: {result['error']}")

                if cycle < args.cycles:
                    print(f"⏳ Waiting {args.interval} seconds until next cycle...")
                    print("-" * 50)
                    await asyncio.sleep(args.interval)

        # Save results if requested
        if args.output:
            with open(args.output, "w") as f:
                json.dump(cycle_results, f, indent=2)
            print(f"📄 Results saved to {args.output}")

        print(f"🎉 Autonomous cycles completed for {args.agent}")
        return 0

        # SECURITY: Key placeholder - replace with environment variable
        print(f"\n⏹️  Autonomous cycles interrupted for {args.agent}")
        if args.output and cycle_results:
            with open(args.output, "w") as f:
                json.dump(cycle_results, f, indent=2)
            print(f"📄 Partial results saved to {args.output}")
        return 0

    except Exception as e:
        print(f"❌ Error running autonomous cycles: {e}")
        if args.output and cycle_results:
            with open(args.output, "w") as f:
                json.dump(cycle_results, f, indent=2)
            print(f"📄 Partial results saved to {args.output}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
