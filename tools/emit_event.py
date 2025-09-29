#!/usr/bin/env python3
"""
Manual Event Emitter CLI
========================
Command-line tool for posting events to Discord webhooks.
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.discord_line_emitter import DiscordLineEmitter
from src.services.event_format import blocker, cycle_done, integration_scan, ssot_validation


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Emit events to Discord webhooks")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-1)")
    parser.add_argument(
        "--type",
        required=True,
        choices=["CYCLE_DONE", "BLOCKER", "SSOT", "INTEGRATION"],
        help="Event type",
    )

    # CYCLE_DONE arguments
    parser.add_argument("--summary", help="Cycle summary")
    parser.add_argument("--next", help="Next intent")

    # BLOCKER arguments
    parser.add_argument("--reason", help="Blocking reason")
    parser.add_argument("--need", help="What is needed")
    parser.add_argument("--severity", default="med", choices=["low", "med", "high"])

    # SSOT arguments
    parser.add_argument("--scope", help="Validation scope")
    parser.add_argument("--passed", action="store_true", help="Validation passed")
    parser.add_argument("--notes", help="Additional notes")

    # INTEGRATION arguments
    parser.add_argument("--systems", help="Systems scanned")
    parser.add_argument("--depth", type=int, default=1, help="Scan depth")
    parser.add_argument("--result", help="Scan result")

    args = parser.parse_args()

    emitter = DiscordLineEmitter()

    # Format event based on type
    if args.type == "CYCLE_DONE":
        line = cycle_done(args.agent, args.summary or "", args.next or "")
    elif args.type == "BLOCKER":
        line = blocker(args.agent, args.reason or "", args.need or "", args.severity)
    elif args.type == "SSOT":
        line = ssot_validation(args.agent, args.scope or "", args.passed, args.notes or "")
    else:  # INTEGRATION
        line = integration_scan(args.agent, args.systems or "", args.depth, args.result or "")

    # Emit event
    success = await emitter.emit_event(args.agent, line)

    if success:
        print("✅ Event posted successfully")
        print(f"📝 {line}")
    else:
        print("❌ Failed to post event")
        print(f"🔍 Check webhook URL for {args.agent}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
