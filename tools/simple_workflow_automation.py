#!/usr/bin/env python3
"""
Simple Workflow Automation - Main Interface
===========================================

Main interface for workflow automation system.
V2 Compliant: ≤100 lines, imports from modular components.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from workflow_automation.task_assignment import create_task_assignment_automation
from workflow_automation.message_forwarding import create_message_forwarding_automation
from workflow_automation.project_coordination import create_project_coordination_automation

logger = logging.getLogger(__name__)


class SimpleWorkflowAutomation:
    """Main workflow automation system."""

    def __init__(self):
        """Initialize workflow automation."""
        self.workflow_log = Path("workflows/automation_log.json")
        self.workflow_log.parent.mkdir(exist_ok=True)
        
        # Initialize automation components
        self.task_automation = create_task_assignment_automation(self.workflow_log)
        self.message_automation = create_message_forwarding_automation(self.workflow_log)
        self.project_automation = create_project_coordination_automation(self.workflow_log)

    def assign_task(self, task_id: str, title: str, description: str, assigned_to: str, assigned_by: str, priority: str = "normal") -> bool:
        """Assign task to agent."""
        return self.task_automation.assign_task(task_id, title, description, assigned_to, assigned_by, priority)

    def forward_message(self, from_agent: str, to_agent: str, message: str, priority: str = "normal", project: str = None) -> bool:
        """Forward message between agents."""
        return self.message_automation.forward_message(from_agent, to_agent, message, priority, project)

    def coordinate_project(self, project_name: str, coordinator: str, participating_agents: list[str], tasks: list[dict]) -> bool:
        """Coordinate project across multiple agents."""
        return self.project_automation.coordinate_project(project_name, coordinator, participating_agents, tasks)

    def get_workflow_summary(self) -> dict:
        """Get workflow summary."""
        try:
            if not self.workflow_log.exists():
                return {"workflows": [], "total_count": 0}

            with open(self.workflow_log, "r") as f:
                log_data = json.load(f)

            workflows = log_data.get("workflows", [])
            return {
                "workflows": workflows[-10:],  # Last 10 workflows
                "total_count": len(workflows),
                "last_updated": workflows[-1]["timestamp"] if workflows else None
            }

        except Exception as e:
            logger.error(f"Failed to get workflow summary: {e}")
            return {"error": str(e)}


def main():
    """CLI interface for workflow automation."""
    parser = argparse.ArgumentParser(description="Simple Workflow Automation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Task assignment command
    assign_parser = subparsers.add_parser("assign", help="Assign task")
    assign_parser.add_argument("--task-id", required=True, help="Task ID")
    assign_parser.add_argument("--title", required=True, help="Task title")
    assign_parser.add_argument("--description", required=True, help="Task description")
    assign_parser.add_argument("--to", required=True, help="Target agent")
    assign_parser.add_argument("--from", required=True, help="Assigning agent")
    assign_parser.add_argument("--priority", choices=["low", "normal", "high", "urgent"], default="normal")

    # Message forwarding command
    msg_parser = subparsers.add_parser("message", help="Forward message")
    msg_parser.add_argument("--from", required=True, help="From agent")
    msg_parser.add_argument("--to", required=True, help="To agent")
    msg_parser.add_argument("--content", required=True, help="Message content")
    msg_parser.add_argument("--priority", choices=["low", "normal", "high", "urgent"], default="normal")
    msg_parser.add_argument("--project", help="Project name")

    # Project coordination command
    project_parser = subparsers.add_parser("project", help="Coordinate project")
    project_parser.add_argument("--name", required=True, help="Project name")
    project_parser.add_argument("--coordinator", required=True, help="Coordinator agent")
    project_parser.add_argument("--agents", required=True, nargs="+", help="Participating agents")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Get workflow summary")

    args = parser.parse_args()

    automation = SimpleWorkflowAutomation()

    if args.command == "assign":
        success = automation.assign_task(
            task_id=args.task_id,
            title=args.title,
            description=args.description,
            assigned_to=args.to,
            assigned_by=getattr(args, "from"),
            priority=args.priority,
        )
        print(f"Task assignment: {'SUCCESS' if success else 'FAILED'}")

    elif args.command == "message":
        success = automation.forward_message(
            from_agent=getattr(args, "from"),
            to_agent=args.to,
            message=args.content,
            priority=args.priority,
            project=args.project,
        )
        print(f"Message forwarding: {'SUCCESS' if success else 'FAILED'}")

    elif args.command == "project":
        success = automation.coordinate_project(
            project_name=args.name,
            coordinator=args.coordinator,
            participating_agents=args.agents,
            tasks=[],
        )
        print(f"Project coordination: {'SUCCESS' if success else 'FAILED'}")

    elif args.command == "summary":
        summary = automation.get_workflow_summary()
        print(json.dumps(summary, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()