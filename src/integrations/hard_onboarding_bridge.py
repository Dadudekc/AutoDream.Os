#!/usr/bin/env python3
"""
Hard Onboarding Integration Bridge
==================================

Integration glue between cursor task database, FSM state management,
and PyAutoGUI onboarder for complete hard onboarding automation.

V2 Compliance: ≤400 lines, focused integration module
Author: Agent-4 (Captain) - Strategic Oversight & Emergency Intervention
"""

from __future__ import annotations

import json
import sqlite3

# Import existing systems
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.services.agent_hard_onboarding import process_hard_onboard_command
from tools.cursor_task_database_integration import (
    CursorTaskIntegrationManager,
    TaskPriority,
)

# Configuration
DB_PATH = "unified.db"


def _now() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat(timespec="seconds")


def ensure_db() -> None:
    """Ensure database schema exists by running the manager bootstrap."""
    try:
        CursorTaskIntegrationManager(DB_PATH)
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise


def create_and_assign_onboarding(agent_id: str, *, assigned_by: str = "Captain") -> str:
    """
    Create hard onboarding task and assign it to agent.

    Args:
        agent_id: Target agent identifier
        assigned_by: Agent creating the task

    Returns:
        task_id: Created task identifier
    """
    manager = CursorTaskIntegrationManager(DB_PATH)

    # Create hard onboarding task
    task = manager.create_hard_onboarding_task(
        agent_id=agent_id, onboarding_type="hard_onboard", priority=TaskPriority.CRITICAL
    )

    # Assign task and set to ACTIVE
    manager.assign_task_with_workflow_integration(task.task_id, assigned_by=assigned_by)
    manager.update_task_fsm_state(task.task_id, "ACTIVE", "hard_onboarding_initiated")

    return task.task_id


def execute_hard_onboarding(agent_id: str, *, dry_run: bool = False) -> dict[str, Any]:
    """
    Execute PyAutoGUI hard onboarding sequence.

    Args:
        agent_id: Target agent identifier
        dry_run: If True, simulate without actual clicks

    Returns:
        Execution result dictionary
    """
    return process_hard_onboard_command(agent_id, dry_run=dry_run)


def mark_onboarding_result(task_id: str, success: bool, note: str | None = None) -> bool:
    """
    Mark onboarding task as completed or failed.

    Args:
        task_id: Task identifier
        success: Whether onboarding succeeded
        note: Optional note about the result

    Returns:
        True if update succeeded
    """
    manager = CursorTaskIntegrationManager(DB_PATH)

    # Update FSM state
    new_state = "COMPLETED" if success else "FAILED"
    fsm_success = manager.update_task_fsm_state(
        task_id, new_state, f"onboarding_{'ok' if success else 'fail'}: {note or 'no details'}"
    )

    # Update task status
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "UPDATE cursor_tasks_integrated SET status=?, updated_at=? WHERE task_id=?",
                (new_state, _now(), task_id),
            )
            conn.commit()
        return fsm_success
    except Exception as e:
        print(f"Task status update error: {e}")
        return False


def captain_hard_onboard(agent_id: str, *, dry_run: bool = False) -> dict[str, Any]:
    """
    One-shot orchestrator for complete hard onboarding flow.

    Flow:
    1) Create onboarding task
    2) Assign + set ACTIVE
    3) Run hard onboarder (dry_run optional)
    4) Mark result + return summary

    Args:
        agent_id: Target agent identifier
        dry_run: If True, simulate without actual clicks

    Returns:
        Complete execution summary
    """
    try:
        # Ensure database is ready
        ensure_db()

        # Step 1: Create and assign onboarding task
        task_id = create_and_assign_onboarding(agent_id)

        # Step 2: Execute hard onboarding
        exec_result = execute_hard_onboarding(agent_id, dry_run=dry_run)

        # Step 3: Mark result based on execution success
        success = bool(exec_result.get("success", False))
        mark_onboarding_result(task_id, success, note=exec_result.get("message"))

        # Step 4: Generate comprehensive report
        manager = CursorTaskIntegrationManager(DB_PATH)
        execution_orders = manager.generate_captain_execution_orders()

        return {
            "task_id": task_id,
            "agent_id": agent_id,
            "success": success,
            "exec_result": exec_result,
            "execution_orders": execution_orders,
            "timestamp": _now(),
            "dry_run": dry_run,
        }

    except Exception as e:
        return {
            "task_id": None,
            "agent_id": agent_id,
            "success": False,
            "error": str(e),
            "timestamp": _now(),
            "dry_run": dry_run,
        }


def get_onboarding_status(agent_id: str) -> dict[str, Any]:
    """
    Get current onboarding status for an agent.

    Args:
        agent_id: Target agent identifier

    Returns:
        Status information dictionary
    """
    try:
        manager = CursorTaskIntegrationManager(DB_PATH)

        # Get tasks for this agent
        agent_tasks = manager.list_tasks()
        onboarding_tasks = [
            task
            for task in agent_tasks
            if task.agent_id == agent_id and "onboarding" in task.description.lower()
        ]

        # Get FSM tracking
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT current_state, state_history FROM fsm_task_tracking WHERE agent_id = ?",
                (agent_id,),
            )
            fsm_data = cur.fetchone()

        return {
            "agent_id": agent_id,
            "onboarding_tasks": len(onboarding_tasks),
            "latest_task": onboarding_tasks[-1].task_id if onboarding_tasks else None,
            "fsm_state": fsm_data[0] if fsm_data else None,
            "state_history": json.loads(fsm_data[1]) if fsm_data and fsm_data[1] else [],
            "timestamp": _now(),
        }

    except Exception as e:
        return {"agent_id": agent_id, "error": str(e), "timestamp": _now()}


def main() -> int:
    """CLI entry point for testing integration bridge."""
    import argparse

    parser = argparse.ArgumentParser(description="Hard Onboarding Integration Bridge")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-6)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--status", action="store_true", help="Check status only")

    args = parser.parse_args()

    if args.status:
        status = get_onboarding_status(args.agent)
        print(json.dumps(status, indent=2))
        return 0

    # Execute hard onboarding
    result = captain_hard_onboard(args.agent, dry_run=args.dry_run)
    print(json.dumps(result, indent=2))

    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
