#!/usr/bin/env python3
"""
Create V2 Tasks Script - Agent Cellphone V2
===========================================

This script creates V2 tasks using the task manager's create_task method.
"""

import sys

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from core.task_manager import TaskManager, TaskPriority
from core.workspace_manager import WorkspaceManager


def main():
    """Create V2 tasks for all agents."""
    print("🚀 Creating V2 Tasks for Agent Swarm...")

    try:
        # Initialize workspace manager
        workspace_manager = WorkspaceManager()

        # Initialize task manager
        task_manager = TaskManager(workspace_manager)

        # Create tasks for each agent
        tasks = [
            {
                "title": "Scanner Services Development",
                "description": "Create project_scanner_service.py, scanner_cache_service.py, and report_generator_service.py. Focus on functionality, not arbitrary constraints.",
                "assigned_to": "Agent-1",
                "created_by": "Captain-5",
                "priority": TaskPriority.HIGH,
            },
            {
                "title": "Core System Analysis",
                "description": "Analyze agent_cell_phone.py, agent_manager.py, and config_manager.py. Don't refactor just for the sake of refactoring.",
                "assigned_to": "Agent-2",
                "created_by": "Captain-5",
                "priority": TaskPriority.HIGH,
            },
            {
                "title": "Performance & Health Systems",
                "description": "Analyze performance_tracker.py, performance_monitor.py, and auto_recovery_system.py. Profile before optimizing.",
                "assigned_to": "Agent-3",
                "created_by": "Captain-5",
                "priority": TaskPriority.HIGH,
            },
            {
                "title": "Error & Health Systems",
                "description": "Analyze error_analytics_system.py, service_health_monitor.py, and health_monitoring_dashboard.py. Make systems work better.",
                "assigned_to": "Agent-4",
                "created_by": "Captain-5",
                "priority": TaskPriority.HIGH,
            },
        ]

        created_tasks = []
        for task_data in tasks:
            task_id = task_manager.create_task(**task_data)
            if task_id:
                created_tasks.append((task_id, task_data["assigned_to"]))
                print(
                    f"✅ Created task: {task_data['title']} -> {task_data['assigned_to']}"
                )
            else:
                print(f"❌ Failed to create task: {task_data['title']}")

        print(f"\n🎉 Successfully created {len(created_tasks)} V2 tasks!")

        # Show task summary
        print("\n📊 Task Summary:")
        for task_id, agent in created_tasks:
            print(f"  - {task_id} -> {agent}")

    except Exception as e:
        print(f"❌ Error creating tasks: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
