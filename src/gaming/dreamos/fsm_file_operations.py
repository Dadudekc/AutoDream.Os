#!/usr/bin/env python3
"""
FSM File Operations Module
==========================

File operations for FSM orchestrator task persistence.
Extracted from fsm_orchestrator.py for better performance and modularity.

Features:
- Task file persistence
- Evidence management
- Verification message emission
- File-based task storage

Author: Agent-3 (Infrastructure & DevOps) - Infrastructure Optimization
License: MIT
"""

import json
import logging
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .fsm_models import Task

logger = logging.getLogger(__name__)


class FSMFileOperations:
    """Handles all file operations for FSM orchestrator."""

    def __init__(self, fsm_root: Path, inbox_root: Path, outbox_root: Path):
        """Initialize file operations handler.

        Args:
            fsm_root: Root directory for FSM data
            inbox_root: Root directory for agent inboxes
            outbox_root: Root directory for agent outboxes
        """
        self.fsm_root = Path(fsm_root)
        self.inbox_root = Path(inbox_root)
        self.outbox_root = Path(outbox_root)

        # Create necessary directories
        self.tasks_dir = self.fsm_root / "tasks"
        self.workflows_dir = self.fsm_root / "workflows"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.workflows_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"FSMFileOperations initialized with root: {self.fsm_root}")

    def save_task(self, task: Task) -> bool:
        """Save task to disk.

        Args:
            task: Task to save

        Returns:
            True if save successful
        """
        try:
            task_file = self.tasks_dir / f"{task.id}.json"
            with open(task_file, "w", encoding="utf-8") as f:
                json.dump(asdict(task), f, indent=2, default=str)
            return True
        except Exception as e:
            logger.error(f"Error saving task {task.id}: {e}")
            return False

    def load_task(self, task_id: str) -> Task | None:
        """Load task from disk.

        Args:
            task_id: Task identifier

        Returns:
            Task if found, None otherwise
        """
        task_file = self.tasks_dir / f"{task_id}.json"
        if not task_file.exists():
            return None

        try:
            with open(task_file, encoding="utf-8") as f:
                data = json.load(f)
                return Task(**data)
        except Exception as e:
            logger.error(f"Error loading task {task_id}: {e}")
            return None

    def emit_verification_message(self, task: Task, status: str) -> bool:
        """Emit verification message for task completion.

        Args:
            task: Task to verify
            status: Verification status

        Returns:
            True if message emitted successfully
        """
        try:
            if not task.assigned_agent:
                logger.warning(f"No assigned agent for task {task.id}")
                return False

            verification_msg = {
                "type": "verification",
                "task_id": task.id,
                "status": status,
                "timestamp": datetime.utcnow().isoformat(),
                "evidence_count": len(task.evidence),
                "metadata": task.metadata or {},
            }

            # Write to agent's inbox
            agent_inbox = self.inbox_root / task.assigned_agent / "inbox"
            agent_inbox.mkdir(parents=True, exist_ok=True)

            verification_file = agent_inbox / f"verification_{task.id}_{int(time.time())}.json"
            with open(verification_file, "w", encoding="utf-8") as f:
                json.dump(verification_msg, f, indent=2)

            logger.info(f"Emitted verification message for task {task.id}")
            return True

        except Exception as e:
            logger.error(f"Error emitting verification message: {e}")
            return False

    def get_all_task_files(self) -> list[Path]:
        """Get list of all task files.

        Returns:
            List of task file paths
        """
        try:
            return list(self.tasks_dir.glob("*.json"))
        except Exception as e:
            logger.error(f"Error getting task files: {e}")
            return []

    def check_agent_reports(self) -> list[Path]:
        """Check for new agent reports in inboxes.

        Returns:
            List of report file paths
        """
        report_files = []
        try:
            for agent_dir in self.inbox_root.iterdir():
                if not agent_dir.is_dir():
                    continue

                inbox_dir = agent_dir / "inbox"
                if not inbox_dir.exists():
                    continue

                # Look for report files
                report_files.extend(inbox_dir.glob("report_*.json"))

        except Exception as e:
            logger.error(f"Error checking agent reports: {e}")

        return report_files

    def move_to_processed(self, report_file: Path) -> bool:
        """Move report file to processed folder.

        Args:
            report_file: Report file path

        Returns:
            True if moved successfully
        """
        try:
            processed_dir = report_file.parent / "processed"
            processed_dir.mkdir(exist_ok=True)
            report_file.rename(processed_dir / report_file.name)
            return True
        except Exception as e:
            logger.error(f"Error moving report file {report_file}: {e}")
            return False
