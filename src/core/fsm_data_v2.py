#!/usr/bin/env python3
"""
FSM Data Manager V2 - Agent Cellphone V2
=======================================

V2-compliant FSM data persistence.
Max 200 LOC, OOP design, SRP.
"""

import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Optional
from .fsm_task_v2 import FSMTask, FSMUpdate


class FSMDataManager:
    """
    FSM Data Manager V2 - Single responsibility: Data persistence.

    Manages task and update file storage with V2 compliance.
    """

    def __init__(self, fsm_data_path: str = "fsm_data"):
        """Initialize FSM Data Manager V2."""
        self.fsm_data_path = Path(fsm_data_path)
        self.logger = logging.getLogger("FSMDataManagerV2")

        # Create directories
        self.tasks_dir = self.fsm_data_path / "tasks"
        self.updates_dir = self.fsm_data_path / "updates"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.updates_dir.mkdir(parents=True, exist_ok=True)

    def save_task(self, task: FSMTask) -> bool:
        """Save task to disk."""
        try:
            task_file = self.tasks_dir / f"{task.id}.json"
            with open(task_file, "w") as f:
                json.dump(task.to_dict(), f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save task {task.id}: {e}")
            return False

    def load_task(self, task_id: str) -> Optional[FSMTask]:
        """Load task from disk."""
        try:
            task_file = self.tasks_dir / f"{task_id}.json"
            if not task_file.exists():
                return None

            with open(task_file, "r") as f:
                task_data = json.load(f)
            return FSMTask.from_dict(task_data)
        except Exception as e:
            self.logger.error(f"Failed to load task {task_id}: {e}")
            return None

    def load_all_tasks(self) -> Dict[str, FSMTask]:
        """Load all tasks from disk."""
        tasks = {}
        try:
            for task_file in self.tasks_dir.glob("*.json"):
                try:
                    with open(task_file, "r") as f:
                        task_data = json.load(f)
                    task = FSMTask.from_dict(task_data)
                    tasks[task.id] = task
                except Exception as e:
                    self.logger.error(f"Failed to load task from {task_file}: {e}")
            return tasks
        except Exception as e:
            self.logger.error(f"Failed to load FSM tasks: {e}")
            return {}

    def delete_task(self, task_id: str) -> bool:
        """Delete task from disk."""
        try:
            task_file = self.tasks_dir / f"{task_id}.json"
            if task_file.exists():
                task_file.unlink()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete task {task_id}: {e}")
            return False

    def save_update(self, update: FSMUpdate) -> bool:
        """Save update to disk."""
        try:
            update_file = self.updates_dir / f"{update.update_id}.json"
            with open(update_file, "w") as f:
                json.dump(update.to_dict(), f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save update {update.update_id}: {e}")
            return False

    def load_updates(self, task_id: Optional[str] = None) -> List[FSMUpdate]:
        """Load updates from disk."""
        updates = []
        try:
            for update_file in self.updates_dir.glob("*.json"):
                try:
                    with open(update_file, "r") as f:
                        update_data = json.load(f)
                    update = FSMUpdate.from_dict(update_data)
                    if task_id is None or update.task_id == task_id:
                        updates.append(update)
                except Exception as e:
                    self.logger.error(f"Failed to load update from {update_file}: {e}")
            updates.sort(key=lambda u: u.timestamp)
            return updates
        except Exception as e:
            self.logger.error(f"Failed to load FSM updates: {e}")
            return []

    def get_statistics(self) -> Dict[str, int]:
        """Get data statistics."""
        try:
            task_count = len(list(self.tasks_dir.glob("*.json")))
            update_count = len(list(self.updates_dir.glob("*.json")))
            return {
                "tasks": task_count,
                "updates": update_count,
                "total_files": task_count + update_count,
            }
        except Exception as e:
            self.logger.error(f"Failed to get statistics: {e}")
            return {"tasks": 0, "updates": 0, "total_files": 0}


def main():
    """CLI interface for FSM Data Manager V2 testing."""
    import argparse
    import uuid
    from datetime import datetime
    from .fsm_task_v2 import TaskState, TaskPriority

    parser = argparse.ArgumentParser(description="FSM Data Manager V2 Testing")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    args = parser.parse_args()

    print("🤖 FSM Data Manager V2 - Agent Cellphone V2")

    data_manager = FSMDataManager()

    if args.stats:
        stats = data_manager.get_statistics()
        print(f"Statistics: {stats}")

    if args.test:
        # Test task persistence
        test_task = FSMTask(
            id=str(uuid.uuid4()),
            title="Test Task",
            description="Test data persistence",
            state=TaskState.NEW,
            priority=TaskPriority.NORMAL,
            assigned_agent="Agent-Test",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        success = data_manager.save_task(test_task)
        print(f"Save task: {'✅ Success' if success else '❌ Failed'}")

        loaded_task = data_manager.load_task(test_task.id)
        print(f"Load task: {'✅ Success' if loaded_task else '❌ Failed'}")

        print("✅ All FSM data manager V2 tests completed!")


if __name__ == "__main__":
    main()
