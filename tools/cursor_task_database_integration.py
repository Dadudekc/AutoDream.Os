#!/usr/bin/env python3
"""
Cursor Task Database Integration System - Main Interface
========================================================

Main interface for cursor task database integration system.
V2 Compliant: ≤100 lines, imports from modular components.

Key fixes:
- create_task_from_project_scan() now PERSISTS and RETURNS tasks
- Safe JSON updates via COALESCE(metadata,'{}') and ensure_json()
- Dataclass mutable defaults -> field(default_factory=...)
- FSM transition logging appends instead of overwriting
- Small helpers: get_task(), list_tasks(), _row_to_task()
- Defensive imports/typing and Python 3.10+ hints

This module is drop-in compatible with prior usage but actually does work now.

Usage:
    python cursor_task_database_integration.py
    from tools.cursor_task_database_integration import CursorTaskIntegrationManager
"""

# Import main components from modular files
from .cursor_task_database_core import CursorTaskIntegrationManager
from .cursor_task_database_models import CursorTask, TaskPriority, TaskStatus

# Re-export main classes for backward compatibility
__all__ = [
    "CursorTaskIntegrationManager",
    "CursorTask",
    "TaskPriority", 
    "TaskStatus",
]


def main() -> int:
    """Main CLI function."""
    print("🎯 CURSOR TASK DATABASE INTEGRATION SYSTEM")
    print("=" * 50)

    manager = CursorTaskIntegrationManager()

    print("🔧 System Integration Status:")
    print(f"  • Project Scanner: {'✅ Available' if manager.project_scanner else '⚠️ Limited'}")
    print(f"  • FSM Integration: {'✅ Available' if manager.fsm_integration else '⚠️ Limited'}")
    print(f"  • Cursor Database: ✅ {manager.db_path}")

    # Seed a hard onboarding task (ensures DB writes work)
    seed = manager.create_hard_onboarding_task("Agent-4")

    print("\n🔍 Executing project scan task creation...")
    tasks_created = manager.execute_project_scan_with_task_creation("Agent-6")
    print(f"📊 Created {len(tasks_created)} tasks from project scan")

    # Move one task to ACTIVE via assign + state update
    if tasks_created:
        t0 = tasks_created[0]
        manager.assign_task_with_workflow_integration(t0.task_id, assigned_by="Captain")
        manager.update_task_fsm_state(
            t0.task_id, "ACTIVE", "auto-activation for demo"
        )

    print("\n🎯 Generating Captain execution orders...")
    execution_orders = manager.generate_captain_execution_orders()
    print("📋 Generated execution orders:")
    print(f"  • Active Tasks: {execution_orders.get('active_tasks', 0)}")
    print(f"  • Agent Buckets: {len(execution_orders.get('agent_assignments', {}))}")
    print(f"  • Captain Directives: {len(execution_orders.get('captain_directives', []))}")

    print("\n📊 Exporting integration system report...")
    integration_report = manager.export_integration_report()
    print(f"  • Status Keys: {list(integration_report['integration_status'].keys())}")
    print(f"  • Task Summary: {integration_report['cursor_tasks']}")
    print(f"  • FSM Summary: {integration_report['fsm_states']}")
    print(f"  • Scan Summary: {integration_report['scan_integration']}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())