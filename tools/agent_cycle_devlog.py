#!/usr/bin/env python3
"""
Agent Cycle Devlog Tool
======================

Tool for agents to automatically create and post devlogs during their cycles.
Replaces manual devlog reminders with automatic posting to agent-specific channels.

Features:
- Automatic devlog creation for cycle actions
- Agent-specific channel routing
- Integration with existing agent workflows
- V2 compliance maintained

Usage:
    python tools/agent_cycle_devlog.py --agent Agent-4 --action "Tools cleanup completed" --status completed
    python tools/agent_cycle_devlog.py --agent Agent-2 --cycle-start --focus "Architecture review"
    python tools/agent_cycle_devlog.py --agent Agent-6 --cycle-complete --action "Coordination" --results "All agents coordinated"
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.agent_devlog_automation import AgentDevlogAutomation

logger = logging.getLogger(__name__)


async def main():
    """Main entry point for agent cycle devlog tool."""
    parser = argparse.ArgumentParser(
        description="Agent Cycle Devlog Tool - Automatic devlog creation and posting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic devlog creation
  python tools/agent_cycle_devlog.py --agent Agent-4 --action "Mission completed" --status completed

  # Cycle start
  python tools/agent_cycle_devlog.py --agent Agent-2 --cycle-start --focus "Architecture review"

  # Cycle completion
  python tools/agent_cycle_devlog.py --agent Agent-6 --cycle-complete --action "Coordination" --results "All agents coordinated"

  # Task assignment
  python tools/agent_cycle_devlog.py --agent Agent-1 --task-assignment --task "System integration" --assigned-by "Agent-4"

  # Coordination
  python tools/agent_cycle_devlog.py --agent Agent-4 --coordination --message "Status update needed" --target Agent-2
        """,
    )

    # Agent selection
    parser.add_argument(
        "--agent",
        required=True,
        choices=[f"Agent-{i}" for i in range(1, 9)],
        help="Agent ID (Agent-1 through Agent-8)",
    )

    # Action types
    parser.add_argument("--action", type=str, help="Action description for devlog")

    parser.add_argument(
        "--status",
        type=str,
        default="completed",
        choices=["completed", "in_progress", "assigned", "failed"],
        help="Status of the action",
    )

    parser.add_argument("--details", type=str, help="Additional details for the devlog")

    # Cycle-specific actions
    parser.add_argument("--cycle-start", action="store_true", help="Create cycle start devlog")

    parser.add_argument("--focus", type=str, help="Focus area for cycle start")

    parser.add_argument(
        "--cycle-complete", action="store_true", help="Create cycle completion devlog"
    )

    parser.add_argument("--results", type=str, help="Results for cycle completion")

    # Task assignment
    parser.add_argument(
        "--task-assignment", action="store_true", help="Create task assignment devlog"
    )

    parser.add_argument("--task", type=str, help="Task description for assignment")

    parser.add_argument("--assigned-by", type=str, help="Agent who assigned the task")

    # Coordination
    parser.add_argument("--coordination", action="store_true", help="Create coordination devlog")

    parser.add_argument("--message", type=str, help="Coordination message")

    parser.add_argument("--target", type=str, help="Target agent for coordination")

    # Options
    parser.add_argument(
        "--no-discord", action="store_true", help="Create devlog file only, don't post to Discord"
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        # Initialize automation
        automation = AgentDevlogAutomation()
        success = await automation.initialize()

        if not success:
            print("❌ Failed to initialize devlog automation")
            return 1

        devlog_filepath = None
        discord_success = False

        # Handle different action types
        if args.cycle_start:
            if not args.focus:
                print("❌ --focus required for cycle start")
                return 1

            print(f"🚀 Creating cycle start devlog for {args.agent}...")
            devlog_filepath, discord_success = await automation.create_cycle_start_devlog(
                args.agent, args.focus
            )

        elif args.cycle_complete:
            if not args.action or not args.results:
                print("❌ --action and --results required for cycle completion")
                return 1

            print(f"✅ Creating cycle completion devlog for {args.agent}...")
            devlog_filepath, discord_success = await automation.create_cycle_completion_devlog(
                args.agent, args.action, args.results
            )

        elif args.task_assignment:
            if not args.task or not args.assigned_by:
                print("❌ --task and --assigned-by required for task assignment")
                return 1

            print(f"📋 Creating task assignment devlog for {args.agent}...")
            devlog_filepath, discord_success = await automation.create_task_assignment_devlog(
                args.agent, args.task, args.assigned_by
            )

        elif args.coordination:
            if not args.message or not args.target:
                print("❌ --message and --target required for coordination")
                return 1

            print(f"🤝 Creating coordination devlog for {args.agent}...")
            devlog_filepath, discord_success = await automation.create_coordination_devlog(
                args.agent, args.message, args.target
            )

        else:
            # Basic devlog creation
            if not args.action:
                print("❌ --action required for basic devlog creation")
                return 1

            print(f"📝 Creating devlog for {args.agent}...")
            details = {"summary": args.details} if args.details else None
            devlog_filepath, discord_success = await automation.create_cycle_devlog(
                agent_id=args.agent,
                action=args.action,
                status=args.status,
                details=details,
                post_to_discord=not args.no_discord,
            )

        # Report results
        if devlog_filepath:
            print(f"✅ Devlog created: {Path(devlog_filepath).name}")

            if not args.no_discord:
                if discord_success:
                    print(f"📢 Posted to {args.agent}'s Discord channel")
                else:
                    print("⚠️  Discord posting failed (check bot permissions)")
            else:
                print("📄 File-only mode (Discord posting disabled)")

            return 0
        else:
            print("❌ Failed to create devlog")
            return 1

    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
        return 1
    finally:
        if "automation" in locals():
            await automation.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
