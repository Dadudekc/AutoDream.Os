#!/usr/bin/env python3
"""
Simple Workflow Automation Tool
==============================

Streamlines common agent workflow operations:
- Task assignment automation
- Message forwarding automation
- Status check automation
- Project coordination automation

Addresses the repetitive workflow issues we've been experiencing.
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

logger = logging.getLogger(__name__)


class SimpleWorkflowAutomation:
    """Simple workflow automation system."""

    def __init__(self):
        self.workflow_log = Path("workflows/automation_log.json")
        self.workflow_log.parent.mkdir(exist_ok=True)

    def assign_task(
        self,
        task_id: str,
        title: str,
        description: str,
        assigned_to: str,
        assigned_by: str,
        priority: str = "normal",
    ) -> bool:
        """Automatically assign task to agent."""
        try:
            # Create working task file
            agent_dir = Path(f"agent_workspaces/{assigned_to}")
            agent_dir.mkdir(parents=True, exist_ok=True)

            working_task = {
                "agent_id": assigned_to,
                "current_task": {
                    "task_id": task_id,
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "status": "in_progress",
                    "claimed_at": datetime.now().isoformat(),
                    "assigned_by": assigned_by,
                },
                "last_updated": datetime.now().isoformat(),
            }

            working_file = agent_dir / "working_tasks.json"
            with open(working_file, "w") as f:
                json.dump(working_task, f, indent=2)

            # Create notification message
            self._create_task_notification(
                assigned_to, task_id, title, description, priority, assigned_by
            )

            # Log workflow
            self._log_workflow(
                "task_assignment",
                {
                    "task_id": task_id,
                    "assigned_to": assigned_to,
                    "assigned_by": assigned_by,
                    "status": "success",
                },
            )

            logger.info(f"Task assigned: {task_id} to {assigned_to}")
            return True

        except Exception as e:
            logger.error(f"Task assignment failed: {e}")
            return False

    def forward_message(
        self,
        from_agent: str,
        to_agent: str,
        message: str,
        priority: str = "normal",
        project: str = None,
    ) -> bool:
        """Automatically forward message between agents."""
        try:
            timestamp = datetime.now()
            message_id = f"MSG_{timestamp.strftime('%Y%m%d_%H%M%S')}"

            # Create message file
            agent_dir = Path(f"agent_workspaces/{to_agent}")
            message_file = agent_dir / "inbox" / f"{message_id}.md"
            message_file.parent.mkdir(exist_ok=True)

            message_content = f"""# Message from {from_agent}

**From**: {from_agent}
**To**: {to_agent}
**Priority**: {priority.upper()}
**Message ID**: {message_id}
**Timestamp**: {timestamp.isoformat()}
**Project**: {project or 'General'}

---

{message}

---

*Message delivered via Simple Workflow Automation*
"""

            with open(message_file, "w") as f:
                f.write(message_content)

            # Log workflow
            self._log_workflow(
                "message_forwarding",
                {
                    "message_id": message_id,
                    "from_agent": from_agent,
                    "to_agent": to_agent,
                    "status": "success",
                },
            )

            logger.info(f"Message forwarded: {from_agent} -> {to_agent}")
            return True

        except Exception as e:
            logger.error(f"Message forwarding failed: {e}")
            return False

    def request_status_check(
        self, requesting_agent: str, target_agents: list[str], project: str = None
    ) -> bool:
        """Request status check from multiple agents."""
        try:
            timestamp = datetime.now()
            request_id = f"STATUS_{timestamp.strftime('%Y%m%d_%H%M%S')}"

            for agent_id in target_agents:
                agent_dir = Path(f"agent_workspaces/{agent_id}")
                message_file = agent_dir / "inbox" / f"{request_id}_{agent_id}.md"
                message_file.parent.mkdir(exist_ok=True)

                message_content = f"""# Status Check Request

**From**: {requesting_agent}
**To**: {agent_id}
**Priority**: NORMAL
**Request ID**: {request_id}
**Timestamp**: {timestamp.isoformat()}
**Project**: {project or 'General'}

---

## Status Check Details

**Please provide**:
- Current task status
- Progress update
- Any blockers or issues
- Next actions planned

---

*Status check requested via Simple Workflow Automation*
"""

                with open(message_file, "w") as f:
                    f.write(message_content)

            # Log workflow
            self._log_workflow(
                "status_check",
                {
                    "request_id": request_id,
                    "requesting_agent": requesting_agent,
                    "target_agents": target_agents,
                    "status": "success",
                },
            )

            logger.info(f"Status check requested from {len(target_agents)} agents")
            return True

        except Exception as e:
            logger.error(f"Status check request failed: {e}")
            return False

    def coordinate_project(
        self,
        project_name: str,
        coordinator: str,
        participating_agents: list[str],
        tasks: list[dict],
    ) -> bool:
        """Coordinate project across multiple agents."""
        try:
            timestamp = datetime.now()
            project_id = f"PROJECT_{project_name.upper()}_{timestamp.strftime('%Y%m%d_%H%M%S')}"

            # Create project directory
            project_dir = Path(f"projects/{project_name}")
            project_dir.mkdir(parents=True, exist_ok=True)

            # Create project coordination file
            coord_data = {
                "project_id": project_id,
                "project_name": project_name,
                "coordinator": coordinator,
                "participating_agents": participating_agents,
                "tasks": tasks,
                "status": "active",
                "created_at": timestamp.isoformat(),
            }

            coord_file = project_dir / "coordination.json"
            with open(coord_file, "w") as f:
                json.dump(coord_data, f, indent=2)

            # Notify all participating agents
            for agent_id in participating_agents:
                self._create_project_notification(agent_id, project_name, coordinator, project_id)

            # Log workflow
            self._log_workflow(
                "project_coordination",
                {
                    "project_id": project_id,
                    "project_name": project_name,
                    "coordinator": coordinator,
                    "participating_agents": participating_agents,
                    "status": "success",
                },
            )

            logger.info(
                f"Project coordinated: {project_name} with {len(participating_agents)} agents"
            )
            return True

        except Exception as e:
            logger.error(f"Project coordination failed: {e}")
            return False

    def get_workflow_summary(self) -> dict:
        """Get workflow automation summary."""
        if not self.workflow_log.exists():
            return {"total_workflows": 0, "recent_workflows": []}

        with open(self.workflow_log) as f:
            workflows = json.load(f)

        return {
            "total_workflows": len(workflows),
            "recent_workflows": workflows[-10:],  # Last 10 workflows
            "workflow_types": self._count_workflow_types(workflows),
        }

    def _create_task_notification(
        self,
        agent_id: str,
        task_id: str,
        title: str,
        description: str,
        priority: str,
        assigned_by: str,
    ) -> None:
        """Create task notification message."""
        agent_dir = Path(f"agent_workspaces/{agent_id}")
        message_file = agent_dir / "inbox" / f"TASK_ASSIGNMENT_{task_id}.md"
        message_file.parent.mkdir(exist_ok=True)

        message_content = f"""# Task Assignment: {title}

**From**: {assigned_by}
**To**: {agent_id}
**Priority**: {priority.upper()}
**Task ID**: {task_id}
**Timestamp**: {datetime.now().isoformat()}

---

## Task Details

**Description**: {description}

**Auto-assigned**: Yes

---

*Task assigned via Simple Workflow Automation*
"""

        with open(message_file, "w") as f:
            f.write(message_content)

    def _create_project_notification(
        self, agent_id: str, project_name: str, coordinator: str, project_id: str
    ) -> None:
        """Create project participation notification."""
        agent_dir = Path(f"agent_workspaces/{agent_id}")
        message_file = agent_dir / "inbox" / f"PROJECT_{project_id}.md"
        message_file.parent.mkdir(exist_ok=True)

        message_content = f"""# Project Participation: {project_name}

**From**: {coordinator}
**To**: {agent_id}
**Priority**: HIGH
**Project ID**: {project_id}
**Timestamp**: {datetime.now().isoformat()}

---

## Project Details

**Project Name**: {project_name}
**Coordinator**: {coordinator}
**Your Role**: Participant

---

*Project notification via Simple Workflow Automation*
"""

        with open(message_file, "w") as f:
            f.write(message_content)

    def _log_workflow(self, workflow_type: str, data: dict) -> None:
        """Log workflow execution."""
        workflows = []
        if self.workflow_log.exists():
            with open(self.workflow_log) as f:
                workflows = json.load(f)

        workflow_entry = {
            "type": workflow_type,
            "timestamp": datetime.now().isoformat(),
            "data": data,
        }

        workflows.append(workflow_entry)

        # Keep only last 100 workflows
        if len(workflows) > 100:
            workflows = workflows[-100:]

        with open(self.workflow_log, "w") as f:
            json.dump(workflows, f, indent=2)

    def _count_workflow_types(self, workflows: list[dict]) -> dict[str, int]:
        """Count workflow types."""
        types = {}
        for workflow in workflows:
            workflow_type = workflow.get("type", "unknown")
            types[workflow_type] = types.get(workflow_type, 0) + 1
        return types


def main():
    """Main function for simple workflow automation."""
    parser = argparse.ArgumentParser(description="Simple Workflow Automation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Task assignment command
    assign_parser = subparsers.add_parser("assign", help="Assign task to agent")
    assign_parser.add_argument("--task-id", required=True, help="Task ID")
    assign_parser.add_argument("--title", required=True, help="Task title")
    assign_parser.add_argument("--description", required=True, help="Task description")
    assign_parser.add_argument("--to", required=True, help="Target agent")
    assign_parser.add_argument("--from", required=True, help="Assigning agent")
    assign_parser.add_argument(
        "--priority", choices=["low", "normal", "high", "urgent"], default="normal"
    )

    # Message forwarding command
    msg_parser = subparsers.add_parser("message", help="Forward message")
    msg_parser.add_argument("--from", required=True, help="From agent")
    msg_parser.add_argument("--to", required=True, help="To agent")
    msg_parser.add_argument("--content", required=True, help="Message content")
    msg_parser.add_argument(
        "--priority", choices=["low", "normal", "high", "urgent"], default="normal"
    )
    msg_parser.add_argument("--project", help="Project name")

    # Status check command
    status_parser = subparsers.add_parser("status", help="Request status check")
    status_parser.add_argument("--requesting", required=True, help="Requesting agent")
    status_parser.add_argument("--targets", required=True, nargs="+", help="Target agents")
    status_parser.add_argument("--project", help="Project name")

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

    elif args.command == "status":
        success = automation.request_status_check(
            requesting_agent=args.requesting, target_agents=args.targets, project=args.project
        )
        print(f"Status check: {'SUCCESS' if success else 'FAILED'}")

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
    logging.basicConfig(level=logging.INFO)
    main()
