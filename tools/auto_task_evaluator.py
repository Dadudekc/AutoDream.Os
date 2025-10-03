#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

def auto_evaluate_tasks(agent_id):
    workspace_dir = Path(f"agent_workspaces/{agent_id}")
    working_tasks_file = workspace_dir / "working_tasks.json"
    future_tasks_file = workspace_dir / "future_tasks.json"
    
    # Auto-update task progress
    if working_tasks_file.exists():
        with open(working_tasks_file) as f:
            task_data = json.load(f)
        
        if "current_task" in task_data:
            task = task_data["current_task"]
            if task.get("status") == "in_progress":
                # Auto-increment progress
                current_progress = task.get("progress", 0)
                if current_progress < 100:
                    task["progress"] = min(current_progress + 10, 100)
                    task["last_updated"] = datetime.now().isoformat()
                    
                    with open(working_tasks_file, "w") as f:
                        json.dump(task_data, f, indent=2)
    
    # Auto-claim tasks
    if future_tasks_file.exists() and not task_data.get("current_task"):
        with open(future_tasks_file) as f:
            future_tasks = json.load(f)
        
        if future_tasks:
            task_to_claim = future_tasks.pop(0)
            task_data["current_task"] = {
                **task_to_claim,
                "status": "in_progress",
                "progress": 0,
                "claimed_at": datetime.now().isoformat(),
                "assigned_by": "AUTO_CLAIM"
            }
            
            with open(working_tasks_file, "w") as f:
                json.dump(task_data, f, indent=2)
            
            with open(future_tasks_file, "w") as f:
                json.dump(future_tasks, f, indent=2)

if __name__ == "__main__":
    import sys
    agent_id = sys.argv[1] if len(sys.argv) > 1 else "Agent-7"
    auto_evaluate_tasks(agent_id)
    print("Task evaluation automated")
