"""
Autonomous Task Engine - CLI Interface
======================================
Command-line interface for autonomous task discovery and management.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-10-16
License: MIT
"""

import argparse
from collections import defaultdict
from .engine import AutonomousTaskEngine


def main():
    """CLI for Autonomous Task Engine"""
    parser = argparse.ArgumentParser(
        description="Autonomous Task Discovery & Selection Engine"
    )
    
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Discover all available tasks"
    )
    parser.add_argument(
        "--agent",
        help="Agent ID for personalized recommendations"
    )
    parser.add_argument(
        "--recommend",
        action="store_true",
        help="Get task recommendations for agent"
    )
    parser.add_argument(
        "--claim",
        help="Claim a task by ID"
    )
    parser.add_argument(
        "--start",
        help="Mark task as in progress"
    )
    parser.add_argument(
        "--complete",
        help="Mark task as complete"
    )
    parser.add_argument(
        "--effort",
        type=int,
        help="Actual effort in cycles (for complete)"
    )
    parser.add_argument(
        "--points",
        type=int,
        help="Actual points earned (for complete)"
    )
    
    args = parser.parse_args()
    
    engine = AutonomousTaskEngine()
    
    if args.discover:
        print("\n🔍 Discovering tasks...")
        tasks = engine.discover_tasks()
        print(f"✅ Discovered {len(tasks)} tasks!")
        print(f"   Saved to: {engine.tasks_db_path}")
        
        # Summary by type
        by_type = defaultdict(int)
        for t in tasks:
            by_type[t.task_type] += 1
        
        print("\nBreakdown:")
        for task_type, count in sorted(by_type.items()):
            print(f"  {task_type}: {count}")
    
    elif args.agent and args.recommend:
        print(engine.generate_autonomous_report(args.agent))
    
    elif args.claim and args.agent:
        success = engine.claim_task(args.claim, args.agent)
        if success:
            print(f"✅ Task {args.claim} claimed by {args.agent}!")
            print(f"To start: python tools/autonomous_task_engine.py --start {args.claim} --agent {args.agent}")
        else:
            print(f"❌ Failed to claim task {args.claim}")
    
    elif args.start and args.agent:
        success = engine.start_task(args.start, args.agent)
        if success:
            print(f"✅ Task {args.start} started by {args.agent}!")
        else:
            print(f"❌ Failed to start task {args.start}")
    
    elif args.complete and args.agent and args.effort and args.points:
        success = engine.complete_task(
            args.complete, args.agent, args.effort, args.points
        )
        if success:
            print(f"✅ Task {args.complete} completed by {args.agent}!")
            print(f"   Effort: {args.effort} cycles, Points: {args.points}")
        else:
            print(f"❌ Failed to complete task {args.complete}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

