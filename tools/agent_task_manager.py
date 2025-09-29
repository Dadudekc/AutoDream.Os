#!/usr/bin/env python3
"""
Agent Task Manager Tool
======================

Command-line tool for managing agent tasks (future tasks, working tasks, etc.).
This tool allows agents and coordinators to:
- Create and assign tasks
- View task status
- Manage task priorities
- Coordinate task dependencies
- Generate task reports

Usage:
    python tools/agent_task_manager.py --agent Agent-4 --list-tasks
    python tools/agent_task_manager.py --agent Agent-2 --create-task --description "Review architecture" --priority high
    python tools/agent_task_manager.py --agent Agent-6 --assign-task --target Agent-4 --description "Coordinate messaging"
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class AgentTaskManager:
    """Task manager for agent tasks."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.workspace_dir = Path(f"agent_workspaces/{agent_id}")
        self.working_tasks_file = self.workspace_dir / "working_tasks.json"
        self.future_tasks_file = self.workspace_dir / "future_tasks.json"

        # Ensure workspace exists
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

    def list_tasks(self) -> dict[str, Any]:
        """List all tasks for the agent."""
        result = {
            "agent_id": self.agent_id,
            "current_task": None,
            "pending_tasks": [],
            "completed_tasks": [],
            "task_summary": {},
        }

        # Load working tasks
        if self.working_tasks_file.exists():
            with open(self.working_tasks_file) as f:
                working_tasks = json.load(f)
                result["current_task"] = working_tasks.get("current_task")
                result["completed_tasks"] = working_tasks.get("completed_tasks", [])

        # Load future tasks
        if self.future_tasks_file.exists():
            with open(self.future_tasks_file) as f:
                future_tasks = json.load(f)
                result["pending_tasks"] = future_tasks.get("pending_tasks", [])

        # Generate summary
        result["task_summary"] = {
            "current_tasks": 1 if result["current_task"] else 0,
            "pending_tasks": len(result["pending_tasks"]),
            "completed_tasks": len(result["completed_tasks"]),
            "total_tasks": len(result["pending_tasks"])
            + len(result["completed_tasks"])
            + (1 if result["current_task"] else 0),
        }

        return result

    def create_task(
        self,
        description: str,
        priority: str = "normal",
        assigned_by: str = "system",
        dependencies: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a new task."""
        task = {
            "id": f"TASK_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": description,
            "priority": priority.lower(),
            "assigned_by": assigned_by,
            "created_time": datetime.now().isoformat(),
            "dependencies": dependencies or [],
            "status": "pending",
        }

        # Load existing future tasks
        if self.future_tasks_file.exists():
            with open(self.future_tasks_file) as f:
                future_tasks = json.load(f)
        else:
            future_tasks = {"pending_tasks": [], "completed_future_tasks": []}

        # Add new task
        future_tasks["pending_tasks"].append(task)

        # Save back
        with open(self.future_tasks_file, "w") as f:
            json.dump(future_tasks, f, indent=2)

        return task

    def assign_task(
        self, target_agent: str, description: str, priority: str = "normal"
    ) -> dict[str, Any]:
        """Assign a task to another agent."""
        target_manager = AgentTaskManager(target_agent)
        task = target_manager.create_task(description, priority, self.agent_id)

        return {"assigned_to": target_agent, "assigned_by": self.agent_id, "task": task}

    def complete_task(self, task_id: str) -> bool:
        """Complete a current task."""
        if not self.working_tasks_file.exists():
            return False

        try:
            with open(self.working_tasks_file) as f:
                working_tasks = json.load(f)

            current_task = working_tasks.get("current_task")
            if not current_task or current_task.get("task_id") != task_id:
                return False

            # Mark as completed
            current_task["status"] = "completed"
            current_task["completion_time"] = datetime.now().isoformat()

            # Move to completed tasks
            completed_tasks = working_tasks.get("completed_tasks", [])
            completed_tasks.append(current_task)
            working_tasks["completed_tasks"] = completed_tasks
            working_tasks["current_task"] = None

            # Save back
            with open(self.working_tasks_file, "w") as f:
                json.dump(working_tasks, f, indent=2)

            return True

        except Exception:
            return False

    def get_task_status(self) -> str:
        """Get current task status."""
        if not self.working_tasks_file.exists():
            return "no_tasks"

        try:
            with open(self.working_tasks_file) as f:
                working_tasks = json.load(f)

            current_task = working_tasks.get("current_task")
            if not current_task:
                return "no_current_task"

            return current_task.get("status", "unknown")

        except Exception:
            return "error"

    def generate_report(self) -> str:
        """Generate a task report."""
        tasks = self.list_tasks()

        report = f"""
🤖 Agent Task Report: {self.agent_id}
{'=' * 50}

📊 Task Summary:
  • Current Tasks: {tasks['task_summary']['current_tasks']}
  • Pending Tasks: {tasks['task_summary']['pending_tasks']}
  • Completed Tasks: {tasks['task_summary']['completed_tasks']}
  • Total Tasks: {tasks['task_summary']['total_tasks']}

📋 Current Task:
"""

        if tasks["current_task"]:
            task = tasks["current_task"]
            report += f"  • ID: {task.get('task_id', 'Unknown')}\n"
            report += f"  • Description: {task.get('description', 'No description')}\n"
            report += f"  • Status: {task.get('status', 'Unknown')}\n"
            report += f"  • Priority: {task.get('priority', 'Unknown')}\n"
            report += f"  • Started: {task.get('start_time', 'Unknown')}\n"
        else:
            report += "  • No current task\n"

        report += "\n📝 Pending Tasks:\n"
        if tasks["pending_tasks"]:
            for i, task in enumerate(tasks["pending_tasks"], 1):
                report += f"  {i}. {task.get('description', 'No description')} (Priority: {task.get('priority', 'normal')})\n"
        else:
            report += "  • No pending tasks\n"

        report += "\n✅ Recent Completed Tasks:\n"
        if tasks["completed_tasks"]:
            for i, task in enumerate(tasks["completed_tasks"][-5:], 1):  # Last 5
                report += f"  {i}. {task.get('description', 'No description')} (Completed: {task.get('completion_time', 'Unknown')})\n"
        else:
            report += "  • No completed tasks\n"

        return report


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Agent Task Manager - Manage agent tasks and workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/agent_task_manager.py --agent Agent-4 --list-tasks
  python tools/agent_task_manager.py --agent Agent-2 --create-task --description "Review architecture" --priority high
  python tools/agent_task_manager.py --agent Agent-6 --assign-task --target Agent-4 --description "Coordinate messaging"
  python tools/agent_task_manager.py --agent Agent-1 --report
        """,
    )

    parser.add_argument(
        "--agent",
        required=True,
        choices=[f"Agent-{i}" for i in range(1, 9)],
        help="Agent ID (Agent-1 through Agent-8)",
    )

    # Task operations
    parser.add_argument("--list-tasks", action="store_true", help="List all tasks for the agent")

    parser.add_argument("--create-task", action="store_true", help="Create a new task")

    parser.add_argument("--assign-task", action="store_true", help="Assign a task to another agent")

    parser.add_argument("--complete-task", help="Complete a task by ID")

    parser.add_argument("--report", action="store_true", help="Generate a task report")

    # Task parameters
    parser.add_argument("--description", help="Task description")

    parser.add_argument(
        "--priority",
        choices=["low", "normal", "high", "critical"],
        default="normal",
        help="Task priority (default: normal)",
    )

    parser.add_argument(
        "--assigned-by", default="system", help="Who assigned the task (default: system)"
    )

    parser.add_argument(
        "--target",
        choices=[f"Agent-{i}" for i in range(1, 9)],
        help="Target agent for task assignment",
    )

    args = parser.parse_args()

    manager = AgentTaskManager(args.agent)

    try:
        if args.list_tasks:
            tasks = manager.list_tasks()
            print(json.dumps(tasks, indent=2))

        elif args.create_task:
            if not args.description:
                print("❌ Error: --description is required for creating tasks")
                return 1

            task = manager.create_task(args.description, args.priority, args.assigned_by)
            print(f"✅ Task created: {task['id']}")
            print(f"📝 Description: {task['description']}")
            print(f"🎯 Priority: {task['priority']}")

        elif args.assign_task:
            if not args.target:
                print("❌ Error: --target is required for assigning tasks")
                return 1
            if not args.description:
                print("❌ Error: --description is required for assigning tasks")
                return 1

            assignment = manager.assign_task(args.target, args.description, args.priority)
            print(f"✅ Task assigned to {assignment['assigned_to']}")
            print(f"📝 Description: {assignment['task']['description']}")
            print(f"🎯 Priority: {assignment['task']['priority']}")

        elif args.complete_task:
            if manager.complete_task(args.complete_task):
                print(f"✅ Task {args.complete_task} completed")
            else:
                print(f"❌ Failed to complete task {args.complete_task}")
                return 1

        elif args.report:
            report = manager.generate_report()
            print(report)

        else:
            print("❌ Error: No operation specified")
            print("Use --help to see available operations")
            return 1

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
