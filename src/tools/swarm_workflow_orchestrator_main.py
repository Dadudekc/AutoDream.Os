#!/usr/bin/env python3
"""
Swarm Workflow Orchestrator - Templates
========================================

Workflow templates and CLI interface for swarm orchestration.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, workflow templates
"""

import argparse

from .swarm_workflow_orchestrator_core import SwarmWorkflowOrchestratorCore
from .swarm_workflow_orchestrator_utils import SwarmWorkflowUtils


class SwarmWorkflowOrchestrator:
    """Orchestrates complex workflows across the entire agent swarm."""

    def __init__(self, project_root: str = None):
        self.core = SwarmWorkflowOrchestratorCore(project_root)
        self.utils = SwarmWorkflowUtils(self.core.agent_workspaces, self.core.devlogs)

    def create_workflow(self, name: str, description: str, phases: list[dict]) -> dict:
        """Create a new workflow definition."""
        return self.core.create_workflow(name, description, phases)

    def execute_workflow(self, workflow_name: str, dry_run: bool = False) -> dict:
        """Execute a workflow across all agents."""
        return self.core.execute_workflow(workflow_name, dry_run)

    def list_workflows(self) -> list[dict]:
        """List all available workflows."""
        return self.core.list_workflows()

    def get_workflow_status(self, workflow_name: str) -> dict:
        """Get the current status of a workflow."""
        return self.core.get_workflow_status(workflow_name)

    def _send_agent_message(self, agent: str, message: str, priority: str, tags: list[str]) -> str:
        """Send a message to a specific agent."""
        return self.utils.send_agent_message(agent, message, priority, tags)

    def _create_task_file(self, agent: str, tasks: list[dict], priority: str) -> str:
        """Create a task file for an agent."""
        return self.utils.create_task_file(agent, tasks, priority)

    def _create_devlog(self, title: str, content: str, priority: str) -> str:
        """Create a devlog entry."""
        return self.utils.create_devlog(title, content, priority)

    def _wait_for_agent_completion(self, agent: str, timeout: int) -> str:
        """Wait for an agent to complete their tasks."""
        return self.utils.wait_for_agent_completion(agent, timeout)


def create_v2_trading_robot_workflow(orchestrator: SwarmWorkflowOrchestrator) -> dict:
    """Create the V2 Trading Robot workflow."""
    phases = [
        {
            "name": "Foundation Phase",
            "description": "Core systems and V2 compliance framework",
            "tasks": [
                {
                    "type": "send_message",
                    "agent": "Agent-1",
                    "message": "V2 Trading Robot Foundation Phase - Refactor core systems into modular components (≤400 lines each). Focus on data pipeline optimization, trading engine refactoring, and real-time data streaming.",
                    "priority": "HIGH",
                    "tags": ["V2_COMPLIANCE", "CORE_SYSTEMS", "FOUNDATION"],
                },
                {
                    "type": "send_message",
                    "agent": "Agent-4",
                    "message": "V2 Trading Robot Foundation Phase - Set up V2 compliance framework, testing standards, and quality metrics. Coordinate with Agent-1 for foundation work.",
                    "priority": "HIGH",
                    "tags": ["V2_COMPLIANCE", "QUALITY", "FOUNDATION"],
                },
                {
                    "type": "create_task_file",
                    "agent": "Agent-1",
                    "priority": "HIGH",
                    "tasks": [
                        {
                            "task_id": "V2-TR-001",
                            "title": "Data Pipeline Optimization",
                            "description": "Create modular data pipeline with real-time streaming",
                            "priority": "HIGH",
                            "estimated_duration": "2 cycles",
                        },
                        {
                            "task_id": "V2-TR-002",
                            "title": "Trading Engine Refactoring",
                            "description": "Split monolithic trading robot into modular components",
                            "priority": "HIGH",
                            "estimated_duration": "3 cycles",
                        },
                    ],
                },
            ],
        },
        {
            "name": "Specialization Phase",
            "description": "UI excellence and ML intelligence",
            "tasks": [
                {
                    "type": "send_message",
                    "agent": "Agent-2",
                    "message": "V2 Trading Robot Specialization Phase - Create modular UI components (≤200 lines each), advanced data visualization, and professional trading interface.",
                    "priority": "HIGH",
                    "tags": ["V2_COMPLIANCE", "UI_EXCELLENCE", "SPECIALIZATION"],
                },
                {
                    "type": "send_message",
                    "agent": "Agent-3",
                    "message": "V2 Trading Robot Specialization Phase - Implement database architecture, ML models, backtesting engine, and sentiment analysis.",
                    "priority": "HIGH",
                    "tags": ["V2_COMPLIANCE", "ML_INTELLIGENCE", "SPECIALIZATION"],
                },
                {
                    "type": "create_task_file",
                    "agent": "Agent-2",
                    "priority": "HIGH",
                    "tasks": [
                        {
                            "task_id": "V2-TR-005",
                            "title": "Modular UI Components",
                            "description": "Create modular PyQt5 components with V2 compliance",
                            "priority": "HIGH",
                            "estimated_duration": "3 cycles",
                        }
                    ],
                },
                {
                    "type": "create_task_file",
                    "agent": "Agent-3",
                    "priority": "HIGH",
                    "tasks": [
                        {
                            "task_id": "V2-TR-009",
                            "title": "Database Architecture",
                            "description": "Design and implement SQLite database",
                            "priority": "HIGH",
                            "estimated_duration": "2 cycles",
                        }
                    ],
                },
            ],
        },
        {
            "name": "Integration Phase",
            "description": "System integration and final testing",
            "tasks": [
                {
                    "type": "send_message",
                    "agent": "Agent-4",
                    "message": "V2 Trading Robot Integration Phase - Coordinate final integration, comprehensive testing, security audit, and deployment preparation.",
                    "priority": "CRITICAL",
                    "tags": ["V2_COMPLIANCE", "INTEGRATION", "QUALITY"],
                },
                {
                    "type": "send_message",
                    "agent": "Agent-1",
                    "message": "V2 Trading Robot Integration Phase - Finalize core systems integration and prepare for production deployment.",
                    "priority": "HIGH",
                    "tags": ["V2_COMPLIANCE", "INTEGRATION", "CORE_SYSTEMS"],
                },
                {
                    "type": "create_devlog",
                    "title": "V2 Trading Robot Integration Complete",
                    "content": "All agents have completed their specialized tasks. System integration and final testing in progress.",
                    "priority": "HIGH",
                },
            ],
        },
    ]

    return orchestrator.create_workflow(
        "V2 Trading Robot",
        "Transform Tesla Trading Robot into V2-compliant masterpiece using collective intelligence",
        phases,
    )


def main():
    """Main CLI interface for the Swarm Workflow Orchestrator."""
    parser = argparse.ArgumentParser(description="Swarm Workflow Orchestrator")
    parser.add_argument("--project-root", default=".", help="Project root directory")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create workflow command
    create_parser = subparsers.add_parser("create", help="Create a new workflow")
    create_parser.add_argument("--name", required=True, help="Workflow name")
    create_parser.add_argument("--description", required=True, help="Workflow description")
    create_parser.add_argument(
        "--template", choices=["v2_trading_robot"], help="Use a predefined template"
    )

    # Execute workflow command
    execute_parser = subparsers.add_parser("execute", help="Execute a workflow")
    execute_parser.add_argument("--workflow", required=True, help="Workflow name to execute")
    execute_parser.add_argument("--dry-run", action="store_true", help="Dry run mode")

    # List workflows command
    list_parser = subparsers.add_parser("list", help="List available workflows")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get workflow status")
    status_parser.add_argument("--workflow", required=True, help="Workflow name")

    args = parser.parse_args()

    orchestrator = SwarmWorkflowOrchestrator(args.project_root)

    if args.command == "create":
        if args.template == "v2_trading_robot":
            workflow = create_v2_trading_robot_workflow(orchestrator)
            print(f"✅ Created V2 Trading Robot workflow: {workflow['name']}")
        else:
            print("❌ Please specify a template or create a custom workflow")

    elif args.command == "execute":
        try:
            results = orchestrator.execute_workflow(args.workflow, args.dry_run)
            if results["success"]:
                print(f"✅ Workflow '{args.workflow}' executed successfully")
                print(f"📊 Duration: {results['duration']}")
                print(f"📋 Phases executed: {len(results['phases_executed'])}")
            else:
                print(f"❌ Workflow '{args.workflow}' failed")
                for error in results["errors"]:
                    print(f"   • {error}")
        except Exception as e:
            print(f"❌ Error executing workflow: {e}")

    elif args.command == "list":
        workflows = orchestrator.list_workflows()
        if workflows:
            print("📋 Available Workflows:")
            for workflow in workflows:
                print(
                    f"   • {workflow['name']} ({workflow['phases']} phases, {workflow['agents']} agents)"
                )
        else:
            print("📋 No workflows found")

    elif args.command == "status":
        try:
            status = orchestrator.get_workflow_status(args.workflow)
            print(f"📊 Workflow Status: {args.workflow}")
            print(f"   • Progress: {status['overall_progress']:.1f}%")
            print(f"   • Current Phase: {status['current_phase']}/{status['total_phases']}")
            print(f"   • Completed Phases: {status['completed_phases']}")
        except Exception as e:
            print(f"❌ Error getting status: {e}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
