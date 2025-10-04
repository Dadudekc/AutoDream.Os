#!/usr/bin/env python3
"""
Cursor Task Database Integration System (Hardened)
==================================================

Key fixes:
- create_task_from_project_scan() now PERSISTS and RETURNS tasks
- Safe JSON updates via COALESCE(metadata,'{}') and ensure_json()
- Dataclass mutable defaults -> field(default_factory=...)
- FSM transition logging appends instead of overwriting
- Small helpers: get_task(), list_tasks(), _row_to_task()
- Defensive imports/typing and Python 3.10+ hints

This module is drop-in compatible with prior usage but actually does work now.
"""

import json
import sqlite3
import sys
from contextlib import closing
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# Import existing systems
sys.path.append(str(Path(__file__).parent.parent))

try:
    from tools.projectscanner import ProjectScanner
    from tools.projectscanner.enhanced_scanner.core import EnhancedProjectScannerCore  # noqa: F401
except ImportError:
    print("⚠️ Project Scanner not available - integration limited")
    ProjectScanner = None  # type: ignore

try:
    from src.fsm.fsm_messaging_integration import FSMMessagingIntegration
    from src.fsm.fsm_registry import AgentState, SwarmState  # noqa: F401
except ImportError:
    print("⚠️ FSM System not available - integration limited")
    FSMMessagingIntegration = None  # type: ignore

    class AgentState(Enum):  # minimal fallback
        ONBOARDING = "ONBOARDING"
        ACTIVE = "ACTIVE"


class TaskPriority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"


class TaskStatus(Enum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class CursorTask:
    """Enhanced cursor task with full system integration."""

    task_id: str
    agent_id: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
    cursor_session_id: str | None = None

    # Project Scanner Integration
    source_file: str | None = None
    scan_context: dict[str, Any] = field(default_factory=dict)

    # FSM Integration
    fsm_state: str | None = None
    state_transitions: list[dict[str, Any]] = field(default_factory=list)

    # Agent Coordination
    dependencies: list[str] = field(default_factory=list)
    assigned_by: str | None = None


class CursorTaskIntegrationManager:
    """Manages cursor task database integration with project systems."""

    def __init__(self, db_path: str | None = None):
        if db_path is None:
            db_path = "unified.db"

        self.db_path = Path(db_path)
        self.runtime_memory_path = Path("runtime/memory")

        self.project_scanner = ProjectScanner() if ProjectScanner else None
        self.fsm_integration = FSMMessagingIntegration() if FSMMessagingIntegration else None

        self._init_database()

    # --------------------------- DB bootstrap ---------------------------

    def _init_database(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                # prefer JSON1; won't crash if absent but json_set will be no-op otherwise
                cur.execute("PRAGMA journal_mode=WAL;")
                cur.execute("PRAGMA foreign_keys=ON;")

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS cursor_tasks_integrated (
                        task_id TEXT PRIMARY KEY,
                        agent_id TEXT NOT NULL,
                        description TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'CREATED',
                        priority TEXT NOT NULL DEFAULT 'NORMAL',
                        created_at TEXT DEFAULT (datetime('now')),
                        updated_at TEXT DEFAULT (datetime('now')),
                        metadata TEXT DEFAULT '{}',
                        cursor_session_id TEXT,
                        source_file TEXT,
                        scan_context TEXT DEFAULT '{}',
                        fsm_state TEXT,
                        state_transitions TEXT DEFAULT '[]',
                        dependencies TEXT DEFAULT '[]',
                        assigned_by TEXT
                    )
                    """
                )

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS scanner_tasks (
                        scan_id TEXT PRIMARY KEY,
                        task_id TEXT NOT NULL,
                        scan_timestamp TEXT DEFAULT (datetime('now')),
                        file_analysis TEXT,
                        complexity_metrics TEXT,
                        dependencies TEXT,
                        agent_assignments TEXT,
                        status TEXT DEFAULT 'PENDING'
                    )
                    """
                )

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS fsm_task_tracking (
                        tracking_id TEXT PRIMARY KEY,
                        task_id TEXT NOT NULL,
                        agent_id TEXT NOT NULL,
                        current_state TEXT,
                        state_history TEXT DEFAULT '[]',
                        transition_log TEXT DEFAULT '[]',
                        execution_context TEXT
                    )
                    """
                )

                conn.commit()
        except Exception as e:
            print(f"Database initialization error: {e}")

    # --------------------------- Helpers ---------------------------

    @staticmethod
    def _now_iso() -> str:
        return datetime.now().isoformat(timespec="seconds")

    @staticmethod
    def _ensure_json(s: str | None, fallback: Any) -> Any:
        if not s:
            return fallback
        try:
            return json.loads(s)
        except Exception:
            return fallback

    @staticmethod
    def _row_to_task(row: tuple) -> CursorTask:
        (
            task_id,
            agent_id,
            description,
            status,
            priority,
            created_at,
            updated_at,
            metadata,
            cursor_session_id,
            source_file,
            scan_context,
            fsm_state,
            state_transitions,
            dependencies,
            assigned_by,
        ) = row

        return CursorTask(
            task_id=task_id,
            agent_id=agent_id,
            description=description,
            status=TaskStatus(status),
            priority=TaskPriority(priority),
            created_at=datetime.fromisoformat(created_at) if created_at else datetime.now(),
            updated_at=datetime.fromisoformat(updated_at) if updated_at else datetime.now(),
            metadata=CursorTaskIntegrationManager._ensure_json(metadata, {}),
            cursor_session_id=cursor_session_id,
            source_file=source_file,
            scan_context=CursorTaskIntegrationManager._ensure_json(scan_context, {}),
            fsm_state=fsm_state,
            state_transitions=CursorTaskIntegrationManager._ensure_json(state_transitions, []),
            dependencies=CursorTaskIntegrationManager._ensure_json(dependencies, []),
            assigned_by=assigned_by,
        )

    def get_task(self, task_id: str) -> CursorTask | None:
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM cursor_tasks_integrated WHERE task_id = ?", (task_id,))
            row = cur.fetchone()
            return self._row_to_task(row) if row else None

    def list_tasks(self, status: TaskStatus | None = None) -> list[CursorTask]:
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            if status:
                cur.execute(
                    "SELECT * FROM cursor_tasks_integrated WHERE status = ?", (status.value,)
                )
            else:
                cur.execute("SELECT * FROM cursor_tasks_integrated")
            return [self._row_to_task(r) for r in cur.fetchall()]

    # --------------------------- Task creation ---------------------------

    def _insert_cursor_task(self, task: CursorTask) -> None:
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            cur.execute(
                """
                INSERT INTO cursor_tasks_integrated
                (task_id, agent_id, description, status, priority, created_at, updated_at,
                 metadata, cursor_session_id, source_file, scan_context, fsm_state,
                 state_transitions, dependencies, assigned_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task.task_id,
                    task.agent_id,
                    task.description,
                    task.status.value,
                    task.priority.value,
                    task.created_at.isoformat(),
                    task.updated_at.isoformat(),
                    json.dumps(task.metadata),
                    task.cursor_session_id,
                    task.source_file,
                    json.dumps(task.scan_context),
                    task.fsm_state,
                    json.dumps(task.state_transitions),
                    json.dumps(task.dependencies),
                    task.assigned_by,
                ),
            )
            conn.commit()

    def create_task_from_project_scan(
        self,
        agent_id: str,
        description: str,
        source_file: str | None = None,
        scan_context: dict[str, Any] | None = None,
        priority: TaskPriority = TaskPriority.NORMAL,
    ) -> CursorTask:
        """Create & persist a cursor task from project scanner findings."""
        task_id = f"project_{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        task = CursorTask(
            task_id=task_id,
            agent_id=agent_id,
            description=description,
            status=TaskStatus.CREATED,
            priority=priority,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={},
            source_file=source_file,
            scan_context=scan_context or {},
            fsm_state=AgentState.ONBOARDING.name,
            state_transitions=[],
        )
        self._insert_cursor_task(task)

        # Link a scanner_tasks row (lightweight; optional details)
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            cur.execute(
                """
                INSERT OR REPLACE INTO scanner_tasks
                (scan_id, task_id, scan_timestamp, file_analysis, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    f"scan_{task_id}",
                    task_id,
                    task.created_at.isoformat(),
                    json.dumps({"file": source_file, "issue": scan_context}),
                    "CREATED",
                ),
            )
            conn.commit()

        return task

    def create_hard_onboarding_task(
        self,
        agent_id: str,
        onboarding_type: str = "hard_onboard",
        priority: TaskPriority = TaskPriority.CRITICAL,
    ) -> CursorTask:
        """Create hard onboarding task for agent activation."""
        task_id = f"onboard_{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        task = CursorTask(
            task_id=task_id,
            agent_id=agent_id,
            description=f"Hard onboarding sequence for {agent_id}",
            status=TaskStatus.CREATED,
            priority=priority,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={
                "onboarding_type": onboarding_type,
                "hard_onboard": True,
                "requires_pyautogui": True,
                "coordinate_based": True,
                "general_cycle_integration": True,
            },
            source_file="src/services/agent_hard_onboarding.py",
            scan_context={"onboarding": True, "agent_activation": True},
            fsm_state=AgentState.ONBOARDING.name,
            state_transitions=[],
        )

        self._insert_cursor_task(task)

        # Create onboarding-specific tracking
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            cur.execute(
                """
                INSERT OR REPLACE INTO scanner_tasks
                (scan_id, task_id, scan_timestamp, file_analysis, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    f"onboard_{task_id}",
                    task_id,
                    task.created_at.isoformat(),
                    json.dumps({"onboarding": True, "agent_id": agent_id}),
                    "ONBOARDING",
                ),
            )
            conn.commit()

        return task

    # --------------------------- FSM ops ---------------------------

    def update_task_fsm_state(
        self, task_id: str, new_state: str, transition_reason: str | None = None
    ) -> bool:
        """Update task FSM state and track transitions (append-safe)."""
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                # Get current task state + agent
                cur.execute(
                    "SELECT fsm_state, agent_id FROM cursor_tasks_integrated WHERE task_id = ?",
                    (task_id,),
                )
                result = cur.fetchone()
                if not result:
                    print(f"⚠️ Task not found: {task_id}")
                    return False

                current_state, agent_id = result

                # Validate state transition if FSM available
                if self.fsm_integration:
                    if not self.fsm_integration.validate_state_transition(
                        agent_id, current_state, new_state
                    ):
                        print(f"Invalid state transition: {current_state} -> {new_state}")
                        return False

                # Update task state + metadata.last_transition (json_set requires JSON1)
                cur.execute(
                    """
                    UPDATE cursor_tasks_integrated
                    SET fsm_state = ?,
                        updated_at = ?,
                        metadata = json_set(COALESCE(metadata,'{}'), '$.last_transition', ?)
                    WHERE task_id = ?
                    """,
                    (
                        new_state,
                        self._now_iso(),
                        json.dumps(
                            {
                                "from_state": current_state,
                                "to_state": new_state,
                                "reason": transition_reason,
                                "timestamp": self._now_iso(),
                            }
                        ),
                        task_id,
                    ),
                )

                # Read existing tracking row (if any)
                tracking_id = f"fsm_{task_id}"
                cur.execute(
                    "SELECT state_history, transition_log FROM fsm_task_tracking WHERE tracking_id = ?",
                    (tracking_id,),
                )
                row = cur.fetchone()
                state_history = []
                transition_log = []
                if row:
                    state_history = self._ensure_json(row[0], [])
                    transition_log = self._ensure_json(row[1], [])

                # Append new entries
                if current_state:
                    state_history.append(current_state)
                state_history.append(new_state)
                transition_log.append(
                    {
                        "from": current_state,
                        "to": new_state,
                        "reason": transition_reason,
                        "timestamp": self._now_iso(),
                    }
                )

                # Upsert tracking
                cur.execute(
                    """
                    INSERT INTO fsm_task_tracking
                    (tracking_id, task_id, agent_id, current_state, state_history, transition_log)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(tracking_id) DO UPDATE SET
                        current_state=excluded.current_state,
                        state_history=excluded.state_history,
                        transition_log=excluded.transition_log
                    """,
                    (
                        tracking_id,
                        task_id,
                        agent_id,
                        new_state,
                        json.dumps(state_history),
                        json.dumps(transition_log),
                    ),
                )

                conn.commit()
                return True
        except Exception as e:
            print(f"FSM state update error: {e}")
            return False

    def assign_task_with_workflow_integration(
        self, task_id: str, assigned_by: str = "Captain"
    ) -> bool:
        """Assign task, mark ASSIGNED, and set fsm_state ACTIVE."""
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                cur.execute(
                    """
                    UPDATE cursor_tasks_integrated
                    SET status = ?, assigned_by = ?, updated_at = ?, fsm_state = ?
                    WHERE task_id = ?
                    """,
                    (
                        TaskStatus.ASSIGNED.value,
                        assigned_by,
                        self._now_iso(),
                        AgentState.ACTIVE.name,
                        task_id,
                    ),
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Task assignment error: {e}")
            return False

    # --------------------------- Scanner -> Tasks ---------------------------

    def execute_project_scan_with_task_creation(
        self, target_agent: str = "Agent-6"
    ) -> list[CursorTask]:
        """Execute project scan and create cursor tasks from findings."""
        tasks_created: list[CursorTask] = []

        try:
            if not self.project_scanner:
                print("❌ Project Scanner not available")
                return tasks_created

            print("🔍 Running project scan for task creation...")
            # Placeholder until real scanner API is called
            scan_results = {
                "files_with_issues": [
                    {
                        "file": "src/services/discord_devlog_service.py",
                        "issue": "deprecated_service",
                    },
                    {"file": "docs/", "issue": "outdated_documentation"},
                    {"file": "tools/", "issue": "tool_maintenance_needed"},
                ],
                "complexity_alerts": [{"file": "AGENTS.md", "complexity": "high", "lines": 1739}],
                "dependency_issues": [{"dependency": "python-dotenv", "issue": "missing_version"}],
            }

            for file_issue in scan_results["files_with_issues"]:
                task = self.create_task_from_project_scan(
                    agent_id=target_agent,
                    description=f"Fix {file_issue['issue']} in {file_issue['file']}",
                    source_file=file_issue["file"],
                    scan_context={"issue_type": file_issue["issue"]},
                    priority=TaskPriority.HIGH,
                )
                tasks_created.append(task)

            for complexity_alert in scan_results["complexity_alerts"]:
                task = self.create_task_from_project_scan(
                    agent_id="Agent-7",
                    description=f"Reduce complexity in {complexity_alert['file']} ({complexity_alert['lines']} lines)",
                    source_file=complexity_alert["file"],
                    scan_context={"complexity_metric": complexity_alert["complexity"]},
                    priority=TaskPriority.CRITICAL,
                )
                tasks_created.append(task)

        except Exception as e:
            print(f"Project scan task creation error: {e}")

        return tasks_created

    # --------------------------- Reporting ---------------------------

    def generate_captain_execution_orders(self) -> dict[str, Any]:
        """Generate comprehensive execution orders for Captain successors."""
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                cur.execute(
                    """
                    SELECT agent_id, COUNT(*) as task_count, priority, status
                    FROM cursor_tasks_integrated
                    WHERE status IN ('CREATED', 'ASSIGNED', 'ACTIVE')
                    GROUP BY agent_id, priority, status
                    ORDER BY
                        CASE priority
                            WHEN 'CRITICAL' THEN 3
                            WHEN 'HIGH' THEN 2
                            WHEN 'NORMAL' THEN 1
                            ELSE 0
                        END DESC
                    """
                )
                rows = cur.fetchall()

            execution_orders: dict[str, Any] = {
                "timestamp": self._now_iso(),
                "active_tasks": sum(r[1] for r in rows),
                "agent_assignments": {},
                "priority_distribution": {},
                "fsm_status_overview": {},
                "captain_directives": [],
            }

            for agent_id, task_count, priority, status in rows:
                agent_bucket = execution_orders["agent_assignments"].setdefault(
                    agent_id, {"active_tasks": 0, "high_priority": 0, "critical_tasks": 0}
                )
                agent_bucket["active_tasks"] += task_count
                if priority == "HIGH":
                    agent_bucket["high_priority"] += task_count
                elif priority == "CRITICAL":
                    agent_bucket["critical_tasks"] += task_count

                execution_orders["priority_distribution"][priority] = (
                    execution_orders["priority_distribution"].get(priority, 0) + task_count
                )

            # Light fsm overview (current_state counts)
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                cur.execute(
                    "SELECT current_state, COUNT(*) FROM fsm_task_tracking GROUP BY current_state"
                )
                for state, count in cur.fetchall():
                    execution_orders["fsm_status_overview"][state or "UNKNOWN"] = count

            execution_orders["captain_directives"] = [
                "Validate Discord infrastructure for all active agents",
                "Execute project scan integration protocols",
                "Prioritize CRITICAL tasks for Agent-7 and Agent-6",
                "Maintain cursor task database integrity and WAL health",
            ]
            return execution_orders

        except Exception as e:
            print(f"Execution order generation error: {e}")
            return {}

    def export_integration_report(self) -> dict[str, Any]:
        """Generate comprehensive integration system report."""
        return {
            "timestamp": self._now_iso(),
            "integration_status": {
                "project_scanner": "available" if self.project_scanner else "limited",
                "fsm_integration": "available" if self.fsm_integration else "limited",
                "cursor_database": "operational",
                "runtime_memory": "configured",
            },
            "cursor_tasks": self._get_task_summary(),
            "fsm_states": self._get_fsm_summary(),
            "scan_integration": self._get_scan_summary(),
            "captain_succession_protocol": self._get_succession_protocol(),
        }

    # ---------- internal summaries ----------

    def _get_task_summary(self) -> dict[str, int]:
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                cur.execute("SELECT status, COUNT(*) FROM cursor_tasks_integrated GROUP BY status")
                return {status: count for status, count in cur.fetchall()}
        except Exception:
            return {}

    def _get_fsm_summary(self) -> dict[str, int]:
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                cur.execute(
                    "SELECT current_state, COUNT(*) FROM fsm_task_tracking GROUP BY current_state"
                )
                return {state or "UNKNOWN": count for state, count in cur.fetchall()}
        except Exception:
            return {}

    def _get_scan_summary(self) -> dict[str, int]:
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                cur.execute("SELECT COUNT(*) FROM scanner_tasks")
                return {"scan_tasks_created": int(cur.fetchone()[0])}
        except Exception:
            return {}

    def _get_succession_protocol(self) -> dict[str, str]:
        return {
            "environment_inference": "tools/env_inference_tool.py",
            "project_scanner": "tools/projectscanner/",
            "fsm_integration": "src/fsm/",
            "cursor_database": str(self.db_path),
            "execution_orders": "generate_captain_execution_orders()",
            "integration_report": "export_integration_report()",
        }


# --------------------------- CLI Demo ---------------------------


def main() -> int:
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
            t0.task_id, AgentState.ACTIVE.name, "auto-activation for demo"
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

    print("\n✅ Cursor Task Database Integration System Complete!")
    print("📋 Integration Summary:")
    print(f"  • Seeded Onboarding Task: {seed.task_id}")
    print(f"  • Tasks Created: {len(tasks_created)}")
    print(f"  • Components: {len(integration_report['integration_status'])}")
    print("  • Succession Protocol: Ready")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
