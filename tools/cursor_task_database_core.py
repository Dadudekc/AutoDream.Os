#!/usr/bin/env python3
"""
Cursor Task Database Integration - Core Logic
============================================

Core integration logic for cursor task database system.
V2 Compliant: ≤400 lines, imports from modular components.

Features:
- Project scanner integration
- FSM integration
- Hard onboarding tasks
- Captain execution orders
- System integration reports

Extracted from main integration module for V2 compliance.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Import our modular components
from .cursor_task_database_models import CursorTask, TaskPriority, TaskStatus
from .cursor_task_database_operations import CursorTaskDatabaseOperations

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

    class AgentState:  # minimal fallback
        ONBOARDING = "ONBOARDING"
        ACTIVE = "ACTIVE"


class CursorTaskIntegrationManager:
    """Manages cursor task database integration with project systems."""

    def __init__(self, db_path: str | None = None):
        """Initialize the integration manager."""
        if db_path is None:
            db_path = "unified.db"

        self.db_path = Path(db_path)
        self.runtime_memory_path = Path("runtime/memory")

        self.project_scanner = ProjectScanner() if ProjectScanner else None
        self.fsm_integration = FSMMessagingIntegration() if FSMMessagingIntegration else None

        # Initialize database operations
        self.db_ops = CursorTaskDatabaseOperations(db_path)

    def create_task_from_project_scan(
        self,
        agent_id: str,
        description: str,
        source_file: str | None = None,
        scan_context: dict[str, Any] | None = None,
        priority: TaskPriority = TaskPriority.NORMAL,
    ) -> CursorTask:
        """Create a task from project scan results."""
        task_id = f"scan_{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        task = CursorTask(
            task_id=task_id,
            agent_id=agent_id,
            description=description,
            status=TaskStatus.CREATED,
            priority=priority,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            source_file=source_file,
            scan_context=scan_context or {},
            metadata={"source": "project_scan", "created_by": "scanner"}
        )

        self.db_ops._insert_cursor_task(task)
        return task

    def create_hard_onboarding_task(self, agent_id: str) -> CursorTask:
        """Create a hard onboarding task for an agent."""
        task_id = f"onboard_{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        task = CursorTask(
            task_id=task_id,
            agent_id=agent_id,
            description=f"Hard onboarding for {agent_id}",
            status=TaskStatus.CREATED,
            priority=TaskPriority.HIGH,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={
                "type": "hard_onboarding",
                "created_by": "system",
                "onboarding_type": "pyautogui"
            }
        )

        self.db_ops._insert_cursor_task(task)
        return task

    def assign_task_with_workflow_integration(self, task_id: str, assigned_by: str = "system") -> bool:
        """Assign task with workflow integration."""
        task = self.db_ops.get_task(task_id)
        if not task:
            return False

        # Update task status
        success = self.db_ops.assign_task(task_id, task.agent_id, assigned_by)
        
        if success and self.fsm_integration:
            # Update FSM state
            self.db_ops.update_task_fsm_state(task_id, AgentState.ACTIVE.name, "task_assigned")
        
        return success

    def update_task_fsm_state(self, task_id: str, new_state: str, transition_reason: str = "") -> bool:
        """Update task FSM state."""
        return self.db_ops.update_task_fsm_state(task_id, new_state, transition_reason)

    def execute_project_scan_with_task_creation(self, agent_id: str) -> list[CursorTask]:
        """Execute project scan and create tasks from results."""
        if not self.project_scanner:
            print("⚠️ Project scanner not available")
            return []

        try:
            # Run project scan
            scan_results = self.project_scanner.scan_project()
            tasks_created = []

            # Create tasks from scan results
            for result in scan_results.get("files", []):
                if result.get("complexity_score", 0) > 5:  # High complexity files
                    task = self.create_task_from_project_scan(
                        agent_id=agent_id,
                        description=f"Refactor high complexity file: {result['file_path']}",
                        source_file=result["file_path"],
                        scan_context=result,
                        priority=TaskPriority.HIGH
                    )
                    tasks_created.append(task)

            return tasks_created

        except Exception as e:
            print(f"❌ Project scan failed: {e}")
            return []

    def generate_captain_execution_orders(self) -> dict[str, Any]:
        """Generate execution orders for Captain agent."""
        try:
            # Get active tasks
            active_tasks = self.db_ops.get_tasks_by_status(TaskStatus.ASSIGNED)
            
            # Group by agent
            agent_assignments = {}
            for task in active_tasks:
                if task.agent_id not in agent_assignments:
                    agent_assignments[task.agent_id] = []
                agent_assignments[task.agent_id].append(task)

            # Generate captain directives
            captain_directives = []
            for agent_id, tasks in agent_assignments.items():
                captain_directives.append({
                    "agent_id": agent_id,
                    "task_count": len(tasks),
                    "priority_tasks": [t.task_id for t in tasks if t.priority in [TaskPriority.CRITICAL, TaskPriority.HIGH]],
                    "directive": f"Execute {len(tasks)} assigned tasks"
                })

            return {
                "active_tasks": len(active_tasks),
                "agent_assignments": {agent_id: len(tasks) for agent_id, tasks in agent_assignments.items()},
                "captain_directives": captain_directives,
                "generated_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Failed to generate execution orders: {e}")
            return {"error": str(e)}

    def export_integration_report(self) -> dict[str, Any]:
        """Export comprehensive integration system report."""
        try:
            # Get task statistics
            task_stats = self.db_ops.get_task_statistics()
            
            # Get FSM states if available
            fsm_states = {}
            if self.fsm_integration:
                try:
                    fsm_states = self.fsm_integration.get_all_agent_states()
                except Exception as e:
                    fsm_states = {"error": str(e)}

            # Get scan integration status
            scan_integration = {
                "available": self.project_scanner is not None,
                "last_scan": "unknown"
            }

            return {
                "integration_status": {
                    "project_scanner": self.project_scanner is not None,
                    "fsm_integration": self.fsm_integration is not None,
                    "database": True
                },
                "cursor_tasks": task_stats,
                "fsm_states": fsm_states,
                "scan_integration": scan_integration,
                "exported_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Failed to export integration report: {e}")
            return {"error": str(e)}

    def get_task(self, task_id: str) -> CursorTask | None:
        """Get a task by ID."""
        return self.db_ops.get_task(task_id)

    def list_tasks(self, status: TaskStatus | None = None) -> list[CursorTask]:
        """List tasks, optionally filtered by status."""
        return self.db_ops.list_tasks(status)

    def get_tasks_by_agent(self, agent_id: str) -> list[CursorTask]:
        """Get all tasks assigned to an agent."""
        return self.db_ops.get_tasks_by_agent(agent_id)

    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update task status."""
        return self.db_ops.update_task_status(task_id, status)

    def update_task_metadata(self, task_id: str, metadata: dict) -> bool:
        """Update task metadata."""
        return self.db_ops.update_task_metadata(task_id, metadata)

