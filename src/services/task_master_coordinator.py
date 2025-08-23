#!/usr/bin/env python3
"""
Task Master Coordinator
Maintains a single master task list and sends tailored notifications:
- Agent-5 (Captain): curate and maintain the master task list
- Other agents: pick tasks from the master list and execute

CLI examples:
  python task_master_coordinator.py --init
  python task_master_coordinator.py --add "Improve V2 broadcast reliability"
  python task_master_coordinator.py --list
  python task_master_coordinator.py --notify
"""

from __future__ import annotations

import json
import os
import sys
import argparse
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


MASTER_LIST_PATH = Path(__file__).resolve().parents[2] / "runtime" / "master_tasks.json"


@dataclass
class MasterTask:
    title: str
    description: str = ""
    priority: str = "normal"  # low, normal, high, urgent
    created_at: str = ""
    created_by: str = "system"
    status: str = "open"  # open, in_progress, done, blocked
    id: str = ""
    assignee: Optional[str] = None  # agent_1..agent_8
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    last_update: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        from uuid import uuid4

        data = asdict(self)
        now_iso = datetime.utcnow().isoformat()
        if not data["created_at"]:
            data["created_at"] = now_iso
        if not data.get("id"):
            data["id"] = str(uuid4())
        data["last_update"] = now_iso
        return data


class TaskMasterCoordinator:
    def __init__(self, file_path: Path = MASTER_LIST_PATH):
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.delivery_service = V2MessageDeliveryService()

    def load_tasks(self) -> List[Dict[str, Any]]:
        if not self.file_path.exists():
            return []
        try:
            return json.loads(self.file_path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        self.file_path.write_text(
            json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def init_list(self) -> None:
        if not self.file_path.exists():
            self.save_tasks([])

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "normal",
        created_by: str = "system",
    ) -> Dict[str, Any]:
        tasks = self.load_tasks()
        task = MasterTask(
            title=title,
            description=description,
            priority=priority,
            created_by=created_by,
        )
        tasks.append(task.to_dict())
        self.save_tasks(tasks)
        return task.to_dict()

    def list_tasks(self) -> List[Dict[str, Any]]:
        return self.load_tasks()

    # Notification helpers (thin wrappers around V2 delivery service CLI)
    def notify_captain(self) -> int:
        """Tell Agent-5 to curate and maintain the master task list."""
        try:
            message = (
                "CAPTAIN: Maintain the master task list at "
                f"{self.file_path}. Add high-leverage tasks, set priorities, and announce updates.\n"
                "- Curate tasks continuously\n"
                "- Assign or let agents self-select\n"
                "- Review progress and reprioritize\n"
                "- Report status every 15 minutes"
            )
            success = self.delivery_service.send_message("agent_5", "coordination", message)
            return 0 if success else 1
        except Exception:
            return 1

    def notify_agents_to_pick(self, agent_ids: Optional[List[str]] = None) -> int:
        """Tell all non-captain agents to pick tasks from the master list and execute."""
        try:
            agent_ids = agent_ids or [f"agent_{i}" for i in range(1, 9) if i != 5]
            message = (
                f"PICK TASKS: Use master task list {self.file_path}. Choose top-priority tasks, execute, and report to Captain.\n"
                "Workflow:\n"
                "- Select task from master list\n"
                "- Execute with high quality\n"
                "- Commit to 'agent' branch and push\n"
                "- Post update to Discord\n"
                "- Mark status in master list (done/in_progress/blocked)"
            )
            results = self.delivery_service.broadcast_message("coordination", message, agent_ids)
            success_count = sum(1 for success in results.values() if success)
            return 0 if success_count > 0 else 1
        except Exception:
            return 1

    # Assignment and lifecycle helpers
    def _save(self, tasks: List[Dict[str, Any]]):
        self.save_tasks(tasks)

    def _find_task(
        self, tasks: List[Dict[str, Any]], task_id_or_title: str
    ) -> Optional[Dict[str, Any]]:
        # Try by id exact
        for t in tasks:
            if t.get("id") == task_id_or_title:
                return t
        # Fallback: first title contains match (case-insensitive)
        needle = task_id_or_title.strip().lower()
        for t in tasks:
            if needle in t.get("title", "").lower():
                return t
        return None

    def assign_task(
        self, task_id_or_title: str, agent_id: str
    ) -> Optional[Dict[str, Any]]:
        tasks = self.load_tasks()
        task = self._find_task(tasks, task_id_or_title)
        if not task:
            return None
        now_iso = datetime.utcnow().isoformat()
        task["assignee"] = agent_id
        if task.get("status") == "open":
            task["status"] = "in_progress"
            task["started_at"] = now_iso
        task["last_update"] = now_iso
        self._save(tasks)
        return task

    def start_task(
        self, task_id_or_title: str, agent_id: str
    ) -> Optional[Dict[str, Any]]:
        tasks = self.load_tasks()
        task = self._find_task(tasks, task_id_or_title)
        if not task:
            return None
        now_iso = datetime.utcnow().isoformat()
        task["assignee"] = agent_id
        task["status"] = "in_progress"
        if not task.get("started_at"):
            task["started_at"] = now_iso
        task["last_update"] = now_iso
        self._save(tasks)
        return task

    def complete_task(
        self, task_id_or_title: str, agent_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        tasks = self.load_tasks()
        task = self._find_task(tasks, task_id_or_title)
        if not task:
            return None
        now_iso = datetime.utcnow().isoformat()
        if agent_id:
            task["assignee"] = agent_id
        task["status"] = "done"
        task["completed_at"] = now_iso
        task["last_update"] = now_iso
        self._save(tasks)
        # Auto-notify assignee to resume/pick next task
        assigned = (task.get("assignee") or "").strip() or (agent_id or "")
        if assigned:
            self._send_resume_to_agent(assigned, task.get("title", "task"))
        return task

    def _send_resume_to_agent(self, agent_id: str, task_title: str) -> int:
        try:
            message = f"TASK COMPLETE: '{task_title}'. Resume normal operations and pick your next task from the master list."
            success = self.delivery_service.send_message(agent_id, "coordination", message)
            return 0 if success else 1
        except Exception:
            return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Task Master Coordinator")
    parser.add_argument(
        "--init", action="store_true", help="Initialize master task list file"
    )
    parser.add_argument(
        "--add", metavar="TITLE", help="Add a task title to the master list"
    )
    parser.add_argument(
        "--desc", metavar="DESC", default="", help="Optional task description"
    )
    parser.add_argument(
        "--priority", choices=["low", "normal", "high", "urgent"], default="normal"
    )
    parser.add_argument("--list", action="store_true", help="List tasks")
    parser.add_argument(
        "--notify", action="store_true", help="Send notifications to captain and agents"
    )
    # Assignment lifecycle
    parser.add_argument(
        "--assign", metavar="TASK", help="Assign task (id or title substring) to agent"
    )
    parser.add_argument(
        "--start", metavar="TASK", help="Mark task started/in_progress for agent"
    )
    parser.add_argument(
        "--complete", metavar="TASK", help="Mark task complete and auto-notify assignee"
    )
    parser.add_argument("--agent", metavar="AGENT", help="Agent id (e.g., agent_1)")
    args = parser.parse_args()

    coord = TaskMasterCoordinator()

    if args.init:
        coord.init_list()
        print(f"Initialized master task list at: {coord.file_path}")
        return 0

    if args.add:
        coord.init_list()
        task = coord.add_task(
            args.add,
            description=args.desc,
            priority=args.priority,
            created_by="coordinator",
        )
        print("Added:", json.dumps(task, indent=2, ensure_ascii=False))
        return 0

    if args.list:
        tasks = coord.list_tasks()
        print(
            json.dumps(
                {"count": len(tasks), "tasks": tasks}, indent=2, ensure_ascii=False
            )
        )
        return 0

    if args.notify:
        coord.init_list()
        rc1 = coord.notify_captain()
        rc2 = coord.notify_agents_to_pick()
        print(f"Notify captain rc={rc1}, notify agents rc={rc2}")
        return 0 if rc1 == 0 and rc2 == 0 else 1

    # Lifecycle actions
    if args.assign:
        if not args.agent:
            print("--agent is required for --assign", file=sys.stderr)
            return 2
        coord.init_list()
        task = coord.assign_task(args.assign, args.agent)
        if not task:
            print("Task not found", file=sys.stderr)
            return 3
        print("Assigned:", json.dumps(task, indent=2, ensure_ascii=False))
        return 0

    if args.start:
        if not args.agent:
            print("--agent is required for --start", file=sys.stderr)
            return 2
        coord.init_list()
        task = coord.start_task(args.start, args.agent)
        if not task:
            print("Task not found", file=sys.stderr)
            return 3
        print("Started:", json.dumps(task, indent=2, ensure_ascii=False))
        return 0

    if args.complete:
        coord.init_list()
        task = coord.complete_task(args.complete, args.agent)
        if not task:
            print("Task not found", file=sys.stderr)
            return 3
        print("Completed:", json.dumps(task, indent=2, ensure_ascii=False))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
