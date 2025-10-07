"""
Workflow CLI - V2 Compliant
==========================

Command-line interface for workflow management.
Provides commands for creating, executing, and monitoring workflows.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Workflow Orchestration Specialist
License: MIT
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from .engine import WorkflowEngine
from .models import ResponseType, WorkflowState
from .steps import (
    AutonomousLoopBuilder,
    ConversationLoopBuilder,
    DecisionTreeBuilder,
    MultiAgentOrchestrationBuilder,
)
from .models import CoordinationStrategy


def create_workflow_parser() -> argparse.ArgumentParser:
    """Create argument parser for workflow CLI."""
    parser = argparse.ArgumentParser(
        description="Advanced Workflows System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create workflow
    create_parser = subparsers.add_parser("create", help="Create a new workflow")
    create_parser.add_argument("--name", required=True, help="Workflow name")
    create_parser.add_argument("--type", required=True, 
                              choices=["conversation", "orchestration", "decision", "autonomous"],
                              help="Workflow type")

    # Conversation loop arguments
    create_parser.add_argument("--agent-a", help="First agent (for conversation)")
    create_parser.add_argument("--agent-b", help="Second agent (for conversation)")
    create_parser.add_argument("--topic", help="Conversation topic")
    create_parser.add_argument("--iterations", type=int, default=3, help="Number of iterations")

    # Multi-agent orchestration arguments
    create_parser.add_argument("--agents", nargs="+", help="List of agent IDs")
    create_parser.add_argument("--task", help="Task description")
    create_parser.add_argument("--strategy", choices=["parallel", "sequential"], 
                              default="parallel", help="Coordination strategy")

    # Decision tree arguments
    create_parser.add_argument("--decision-point", help="Decision point description")
    create_parser.add_argument("--branches", help="JSON string of branch configurations")

    # Autonomous loop arguments
    create_parser.add_argument("--goal", help="Goal description")
    create_parser.add_argument("--max-loops", type=int, default=10, help="Maximum loops")

    # Execute workflow
    execute_parser = subparsers.add_parser("execute", help="Execute a workflow")
    execute_parser.add_argument("--name", required=True, help="Workflow name")

    # List workflows
    subparsers.add_parser("list", help="List all workflows")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get workflow status")
    status_parser.add_argument("--name", required=True, help="Workflow name")

    # Pause/resume commands
    pause_parser = subparsers.add_parser("pause", help="Pause workflow")
    pause_parser.add_argument("--name", required=True, help="Workflow name")

    resume_parser = subparsers.add_parser("resume", help="Resume workflow")
    resume_parser.add_argument("--name", required=True, help="Workflow name")

    return parser


async def create_workflow(args: argparse.Namespace) -> None:
    """Create a new workflow based on arguments."""
    engine = WorkflowEngine(args.name)

    if args.type == "conversation":
        if not all([args.agent_a, args.agent_b, args.topic]):
            print("Error: conversation workflow requires --agent-a, --agent-b, and --topic")
            sys.exit(1)

        builder = ConversationLoopBuilder()
        steps = builder.create_conversation_loop(
            args.agent_a, args.agent_b, args.topic, args.iterations
        )
        for step in steps:
            engine.add_step(step)

    elif args.type == "orchestration":
        if not all([args.agents, args.task]):
            print("Error: orchestration workflow requires --agents and --task")
            sys.exit(1)

        builder = MultiAgentOrchestrationBuilder()
        strategy = CoordinationStrategy.PARALLEL if args.strategy == "parallel" else CoordinationStrategy.SEQUENTIAL
        steps = builder.create_multi_agent_orchestration(args.task, args.agents, strategy)
        for step in steps:
            engine.add_step(step)

    elif args.type == "decision":
        if not all([args.decision_point, args.branches]):
            print("Error: decision workflow requires --decision-point and --branches")
            sys.exit(1)

        try:
            branches = json.loads(args.branches)
        except json.JSONDecodeError:
            print("Error: --branches must be valid JSON")
            sys.exit(1)

        builder = DecisionTreeBuilder()
        steps = builder.create_decision_tree(args.decision_point, branches)
        for step in steps:
            engine.add_step(step)

    elif args.type == "autonomous":
        if not args.goal:
            print("Error: autonomous workflow requires --goal")
            sys.exit(1)

        builder = AutonomousLoopBuilder()
        steps = builder.create_autonomous_loop(args.goal, args.max_loops)
        for step in steps:
            engine.add_step(step)

    # Save workflow
    engine.save_state()
    print(f"✅ Workflow '{args.name}' created with {len(engine.steps)} steps")


async def execute_workflow(args: argparse.Namespace) -> None:
    """Execute a workflow."""
    # Load workflow state
    state_dir = Path("workflow_states")
    workflow_files = list(state_dir.glob(f"{args.name}_*.json"))

    if not workflow_files:
        print(f"Error: Workflow '{args.name}' not found")
        sys.exit(1)

    # Use most recent state file
    latest_file = max(workflow_files, key=lambda f: f.stat().st_mtime)

    with open(latest_file) as f:
        state_data = json.load(f)

    # Create engine and restore state
    engine = WorkflowEngine(args.name)
    # Note: Full state restoration would be implemented here

    print(f"▶️ Executing workflow '{args.name}'...")
    await engine.start()


def list_workflows() -> None:
    """List all available workflows."""
    state_dir = Path("workflow_states")

    if not state_dir.exists():
        print("No workflows found")
        return

    workflows = {}
    for state_file in state_dir.glob("*.json"):
        try:
            with open(state_file) as f:
                data = json.load(f)
                workflow_name = data.get("workflow_name")

                if workflow_name not in workflows:
                    workflows[workflow_name] = []

                workflows[workflow_name].append(
                    {
                        "state": data.get("state"),
                        "steps": len(data.get("steps", [])),
                        "completed": len(data.get("completed_steps", [])),
                        "failed": len(data.get("failed_steps", [])),
                        "file": state_file.name,
                    }
                )
        except Exception:
            continue

    if not workflows:
        print("No workflows found")
        return

    print("\n📋 Available Workflows:\n")
    for name, states in workflows.items():
        print(f"Workflow: {name}")
        latest = states[-1]
        print(
            f"  State: {latest['state']} | Steps: {latest['steps']} | "
            f"Completed: {latest['completed']} | Failed: {latest['failed']}"
        )
        print()


def main():
    """Main CLI entry point."""
    parser = create_workflow_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "create":
            asyncio.run(create_workflow(args))
        elif args.command == "execute":
            asyncio.run(execute_workflow(args))
        elif args.command == "list":
            list_workflows()
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

