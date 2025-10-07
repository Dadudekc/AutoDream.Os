"""
Overnight Runner CLI - V2 Compliant
===================================

Command-line interface for overnight autonomous operations.
Provides commands for starting, monitoring, and managing overnight execution.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Autonomous Operations Specialist
License: MIT
"""

import argparse
import asyncio
import json
import sys

from .orchestrator import OvernightOrchestrator
from .scheduler import TaskScheduler
from .monitor import ProgressMonitor
from .recovery import RecoverySystem


def create_overnight_parser() -> argparse.ArgumentParser:
    """Create argument parser for overnight CLI."""
    parser = argparse.ArgumentParser(
        description="Overnight Autonomous Runner CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start overnight operations")
    start_parser.add_argument(
        "--cycles", type=int, default=60, help="Maximum cycles (default: 60)"
    )
    start_parser.add_argument(
        "--interval", type=int, default=10, help="Cycle interval in minutes (default: 10)"
    )
    start_parser.add_argument("--workflow", action="store_true", help="Enable workflow integration")
    start_parser.add_argument("--vision", action="store_true", help="Enable vision monitoring")

    # Status command
    subparsers.add_parser("status", help="Get overnight operations status")

    # Stop command
    subparsers.add_parser("stop", help="Stop overnight operations")

    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Monitor progress")
    monitor_parser.add_argument(
        "--interval", type=int, default=60, help="Status check interval in seconds"
    )

    # Tasks command
    tasks_parser = subparsers.add_parser("tasks", help="Manage tasks")
    tasks_parser.add_argument(
        "--action",
        required=True,
        choices=["add", "list", "complete", "fail"],
        help="Task action",
    )
    tasks_parser.add_argument("--task-id", help="Task ID")
    tasks_parser.add_argument("--task-type", help="Task type")
    tasks_parser.add_argument("--agent", help="Agent ID")
    tasks_parser.add_argument("--priority", type=int, help="Task priority")

    # Recovery command
    recovery_parser = subparsers.add_parser("recovery", help="Recovery system status")

    # Info command
    subparsers.add_parser("info", help="Show overnight system capabilities")

    return parser


async def start_overnight(args: argparse.Namespace) -> None:
    """Start overnight operations."""
    config = {
        "overnight": {
            "enabled": True,
            "cycle_interval": args.interval,
            "max_cycles": args.cycles,
            "integration": {
                "workflow_engine": args.workflow,
                "vision_system": args.vision,
                "messaging_system": True,
                "coordinate_system": True,
            },
        }
    }

    orchestrator = OvernightOrchestrator(config)

    try:
        print(f"🚀 Starting overnight operations:")
        print(f"   Cycles: {args.cycles}")
        print(f"   Interval: {args.interval} minutes")
        print(f"   Workflow: {'enabled' if args.workflow else 'disabled'}")
        print(f"   Vision: {'enabled' if args.vision else 'disabled'}")
        print("\nPress Ctrl+C to stop\n")

        await orchestrator.start()

    except KeyboardInterrupt:
        print("\n\n⏸️ Stopping overnight operations...")
        await orchestrator.stop()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def show_status() -> None:
    """Show overnight operations status."""
    # This would load the current orchestrator state
    print("\n📊 Overnight Operations Status:\n")
    print("Status: Not running")
    print("Current Cycle: 0")
    print("Completed Tasks: 0")
    print()


async def monitor_progress(args: argparse.Namespace) -> None:
    """Monitor overnight progress."""
    monitor = ProgressMonitor()

    try:
        print("🔍 Monitoring overnight operations")
        print(f"Checking every {args.interval} seconds")
        print("Press Ctrl+C to stop\n")

        while True:
            report = monitor.generate_status_report()

            print(f"\n[{report['timestamp']}] Status Report:")
            print(f"  Cycle: {report['current_cycle']}")
            print(f"  Uptime: {report['uptime_seconds']:.1f}s")

            perf = report.get("performance_metrics", {})
            print(f"  Tasks: {perf.get('completed_tasks', 0)}/{perf.get('total_tasks', 0)}")

            await asyncio.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped")


def manage_tasks(args: argparse.Namespace) -> None:
    """Manage scheduler tasks."""
    scheduler = TaskScheduler()

    if args.action == "list":
        status = scheduler.get_scheduler_status()
        print(f"\n📋 Task Scheduler Status:\n")
        print(f"Strategy: {status['strategy']}")
        print(f"Queue Size: {status['queue_size']}")
        print(f"Completed: {status['completed_tasks']}")
        print(f"Failed: {status['failed_tasks']}")
        print()

    elif args.action == "add":
        if not all([args.task_id, args.task_type, args.agent]):
            print("Error: add action requires --task-id, --task-type, and --agent")
            sys.exit(1)

        success = scheduler.add_task(
            task_id=args.task_id,
            task_type=args.task_type,
            agent_id=args.agent,
            data={},
            priority=args.priority,
        )

        if success:
            print(f"✅ Task added: {args.task_id}")
        else:
            print(f"❌ Failed to add task: {args.task_id}")

    else:
        print(f"Task action '{args.action}' not yet implemented")


def show_recovery_status() -> None:
    """Show recovery system status."""
    recovery = RecoverySystem()
    status = recovery.get_recovery_status()

    print("\n🛡️ Recovery System Status:\n")
    print(f"Auto Recovery: {status['auto_recovery']}")
    print(f"Agent Rescue: {status['agent_rescue']}")
    print(f"Max Retries: {status['max_retries']}")
    print(f"Escalation Threshold: {status['escalation_threshold']}")
    print(f"Failure History: {status['failure_history_count']}")
    print(f"Escalated Issues: {status['escalated_issues_count']}")
    print()


def show_info() -> None:
    """Show overnight system capabilities."""
    orchestrator = OvernightOrchestrator()
    status = orchestrator.get_orchestrator_status()

    print("\n📊 Overnight System Capabilities:\n")
    print(f"Enabled: {status['enabled']}")
    print(f"Max Cycles: {status['max_cycles']}")
    print(f"Cycle Interval: {status['cycle_interval']} minutes")
    print(f"Workflow Integration: {status['workflow_integration']}")
    print(f"Vision Integration: {status['vision_integration']}")
    print(f"Messaging Integration: {status['messaging_integration']}")
    print(f"Auto Restart: {status['auto_restart']}")
    print()


def main():
    """Main CLI entry point."""
    parser = create_overnight_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "start":
            asyncio.run(start_overnight(args))
        elif args.command == "status":
            show_status()
        elif args.command == "monitor":
            asyncio.run(monitor_progress(args))
        elif args.command == "tasks":
            manage_tasks(args)
        elif args.command == "recovery":
            show_recovery_status()
        elif args.command == "info":
            show_info()
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

