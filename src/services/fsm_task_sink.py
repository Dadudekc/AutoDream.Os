#!/usr/bin/env python3
"""
FSM Task Sink
Lightweight bridge for FSM→Master Task List integration.

Usage examples:
  # Add task only
  python fsm_task_sink.py --title "FSM: Investigate auth logs" --desc "Triggered by state=ANOMALY_DETECTED" --priority high

  # Add and assign/start to agent_2
  python fsm_task_sink.py --title "FSM: Patch rollout" --agent agent_2 --start

  # Add from JSON file
  python fsm_task_sink.py --from-json event.json
  # JSON structure example:
  # {
  #   "title": "FSM: Re-index search",
  #   "description": "origin=fsm transition=RECOVERY_MODE",
  #   "priority": "normal",
  #   "agent": "agent_3",
  #   "start": true
  # }
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from task_master_coordinator import TaskMasterCoordinator


def load_payload(args: argparse.Namespace) -> Dict[str, Any]:
    if args.from_json:
        data = json.loads(Path(args.from_json).read_text(encoding="utf-8"))
        return {
            "title": data.get("title", "FSM: Untitled Task"),
            "description": data.get("description", ""),
            "priority": data.get("priority", "normal"),
            "agent": data.get("agent"),
            "start": bool(data.get("start", False)),
        }
    return {
        "title": args.title or "FSM: Untitled Task",
        "description": args.desc or "",
        "priority": args.priority,
        "agent": args.agent,
        "start": bool(args.start),
    }


def main() -> int:
    p = argparse.ArgumentParser(description="FSM → Master Task List sink")
    p.add_argument("--from-json", help="Read event payload from JSON file")
    p.add_argument("--title", help="Task title")
    p.add_argument("--desc", default="", help="Task description")
    p.add_argument(
        "--priority", choices=["low", "normal", "high", "urgent"], default="normal"
    )
    p.add_argument("--agent", help="Assignee agent id (e.g., agent_4)")
    p.add_argument(
        "--start", action="store_true", help="Mark started/in_progress for agent"
    )
    args = p.parse_args()

    payload = load_payload(args)

    coord = TaskMasterCoordinator()
    coord.init_list()

    # Add task
    task = coord.add_task(
        payload["title"], payload["description"], payload["priority"], created_by="fsm"
    )

    # Assign/start if requested
    agent = payload.get("agent")
    if agent and payload.get("start"):
        task = coord.start_task(task.get("id") or task.get("title"), agent) or task
    elif agent:
        task = coord.assign_task(task.get("id") or task.get("title"), agent) or task

    print(json.dumps({"status": "ok", "task": task}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
