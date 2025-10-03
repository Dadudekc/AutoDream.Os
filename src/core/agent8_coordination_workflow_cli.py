#!/usr/bin/env python3
"""
Agent-8 Coordination Workflow CLI
================================
Command-line interface for Agent-8 coordination workflow
V2 Compliant: ≤400 lines, focused CLI operations
"""

import argparse
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.agent8_coordination_workflow_core import (
    Agent8CoordinationWorkflowCore,
    CoordinationStatus,
    TaskPriority,
)


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Agent-8 Coordination Workflow CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Register agent command
    register_parser = subparsers.add_parser("register", help="Register agent")
    register_parser.add_argument("agent_id", help="Agent ID")
    register_parser.add_argument("capabilities", nargs="*", help="Agent capabilities")
    register_parser.add_argument("--capacity", type=int, default=5, help="Max capacity")

    # Create task command
    create_parser = subparsers.add_parser("create", help="Create task")
    create_parser.add_argument("agent_id", help="Agent ID")
    create_parser.add_argument("description", help="Task description")
    create_parser.add_argument(
        "--priority",
        choices=[p.value for p in TaskPriority],
        default="medium",
        help="Task priority",
    )
    create_parser.add_argument("--dependencies", nargs="*", help="Task dependencies")

    # Assign task command
    assign_parser = subparsers.add_parser("assign", help="Assign task")
    assign_parser.add_argument("task_id", help="Task ID")
    assign_parser.add_argument("--agent", help="Specific agent ID")

    # Complete task command
    complete_parser = subparsers.add_parser("complete", help="Complete task")
    complete_parser.add_argument("task_id", help="Task ID")
    complete_parser.add_argument(
        "--success", action="store_true", default=True, help="Mark as successful"
    )
    complete_parser.add_argument("--failure", action="store_true", help="Mark as failed")

    # List tasks command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "--status", choices=[s.value for s in CoordinationStatus], help="Filter by status"
    )
    list_parser.add_argument("--agent", help="Filter by agent")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show workflow status")

    # Performance command
    perf_parser = subparsers.add_parser("performance", help="Show agent performance")
    perf_parser.add_argument("--agent", help="Specific agent ID")

    # Auto-assign command
    auto_parser = subparsers.add_parser("auto-assign", help="Auto-assign pending tasks")

    return parser


def handle_register(args, workflow: Agent8CoordinationWorkflowCore) -> None:
    """Handle register command"""
    capabilities = args.capabilities or ["general"]

    workflow.manage_workflow_operations(
        "register_agent",
        agent_id=args.agent_id,
        capabilities=capabilities,
        max_capacity=args.capacity,
    )

    print(f"✅ Successfully registered agent {args.agent_id}")
    print(f"   Capabilities: {', '.join(capabilities)}")
    print(f"   Max capacity: {args.capacity}")


def handle_create(args, workflow: Agent8CoordinationWorkflowCore) -> None:
    """Handle create command"""
    priority = TaskPriority(args.priority)

    task_id = workflow.manage_workflow_operations(
        "create_task",
        agent_id=args.agent_id,
        description=args.description,
        priority=priority,
        dependencies=args.dependencies,
    )

    print(f"✅ Successfully created task {task_id}")
    print(f"   Agent: {args.agent_id}")
    print(f"   Description: {args.description}")
    print(f"   Priority: {priority.value}")
    if args.dependencies:
        print(f"   Dependencies: {', '.join(args.dependencies)}")


def handle_assign(args, workflow: Agent8CoordinationWorkflowCore) -> None:
    """Handle assign command"""
    success = workflow.manage_workflow_operations(
        "assign_task", task_id=args.task_id, agent_id=args.agent
    )

    if success:
        print(f"✅ Successfully assigned task {args.task_id}")
    else:
        print(f"❌ Failed to assign task {args.task_id}")
        sys.exit(1)


def handle_complete(args, workflow: Agent8CoordinationWorkflowCore) -> None:
    """Handle complete command"""
    success = not args.failure

    result = workflow.manage_workflow_operations(
        "complete_task", task_id=args.task_id, success=success
    )

    if result:
        status = "completed successfully" if success else "marked as failed"
        print(f"✅ Task {args.task_id} {status}")
    else:
        print(f"❌ Failed to complete task {args.task_id}")
        sys.exit(1)


def handle_list(args, workflow: Agent8CoordinationWorkflowCore) -> None:
    """Handle list command"""
    tasks = list(workflow.tasks.values())

    # Filter by status if specified
    if args.status:
        status = CoordinationStatus(args.status)
        tasks = [t for t in tasks if t.status == status]

    # Filter by agent if specified
    if args.agent:
        tasks = [t for t in tasks if t.agent_id == args.agent]

    if not tasks:
        print("No tasks found matching your criteria.")
        return

    print(f"Found {len(tasks)} tasks:")
    for task in tasks:
        print(f"  📋 {task.task_id}")
        print(f"     Agent: {task.agent_id}")
        print(f"     Description: {task.description}")
        print(f"     Priority: {task.priority.value}")
        print(f"     Status: {task.status.value}")
        print(f"     Created: {task.created_at}")
        if task.assigned_at:
            print(f"     Assigned: {task.assigned_at}")
        if task.completed_at:
            print(f"     Completed: {task.completed_at}")
        if task.dependencies:
            print(f"     Dependencies: {', '.join(task.dependencies)}")
        print()


def handle_status(args, workflow: Agent8CoordinationWorkflowCore) -> None:
    """Handle status command"""
    status = workflow.manage_workflow_operations("get_status")

    print("📊 Workflow Status:")
    print(f"   Total tasks: {status['total_tasks']}")
    print(f"   Pending: {status['pending_tasks']}")
    print(f"   In progress: {status['in_progress_tasks']}")
    print(f"   Completed: {status['completed_tasks']}")
    print(f"   Failed: {status['failed_tasks']}")
    print(f"   Queue length: {status['task_queue_length']}")
    print(f"   Registered agents: {status['registered_agents']}")
    print(f"   Active agents: {status['active_agents']}")
    print(f"   Last updated: {status['last_updated']}")


def handle_performance(args, workflow: Agent8CoordinationWorkflowCore) -> None:
    """Handle performance command"""
    performance = workflow.manage_workflow_operations("get_performance", agent_id=args.agent)

    if args.agent:
        # Single agent performance
        if not performance:
            print(f"❌ Agent {args.agent} not found")
            sys.exit(1)

        print(f"📈 Agent {args.agent} Performance:")
        print(f"   Active tasks: {performance['active_tasks']}")
        print(f"   Completed tasks: {performance['completed_tasks']}")
        print(f"   Failed tasks: {performance['failed_tasks']}")
        print(f"   Success rate: {performance['success_rate']:.2%}")
        print(f"   Performance score: {performance['performance_score']:.2f}")
        print(f"   Last activity: {performance['last_activity']}")
        print(f"   Current capacity: {performance['current_capacity']}")
        print(f"   Max capacity: {performance['max_capacity']}")
    else:
        # All agents performance
        print("📈 All Agents Performance:")
        for agent_id, perf in performance.items():
            print(f"  🤖 {agent_id}:")
            print(f"     Active: {perf['active_tasks']}, Completed: {perf['completed_tasks']}")
            print(
                f"     Success rate: {perf['success_rate']:.2%}, Score: {perf['performance_score']:.2f}"
            )
        print()


def handle_auto_assign(args, workflow: Agent8CoordinationWorkflowCore) -> None:
    """Handle auto-assign command"""
    assigned_count = workflow.manage_workflow_operations("auto_assign")

    print(f"🤖 Auto-assigned {assigned_count} tasks")


def main():
    """Main CLI function"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize workflow
    workflow = Agent8CoordinationWorkflowCore()

    # Handle commands
    if args.command == "register":
        handle_register(args, workflow)
    elif args.command == "create":
        handle_create(args, workflow)
    elif args.command == "assign":
        handle_assign(args, workflow)
    elif args.command == "complete":
        handle_complete(args, workflow)
    elif args.command == "list":
        handle_list(args, workflow)
    elif args.command == "status":
        handle_status(args, workflow)
    elif args.command == "performance":
        handle_performance(args, workflow)
    elif args.command == "auto-assign":
        handle_auto_assign(args, workflow)


if __name__ == "__main__":
    main()
