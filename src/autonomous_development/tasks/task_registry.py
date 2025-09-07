#!/usr/bin/env python3
"""
Task Registry - Agent Cellphone V2
=================================

Task registry and persistence system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional
from pathlib import Path
from ..core.models import DevelopmentTask


class TaskRegistry:
    """Task registry for persistence and management"""
    
    def __init__(self, storage_path: str = "config/tasks.json"):
        self.storage_path = Path(storage_path)
        self.logger = logging.getLogger(__name__)
        self.tasks: Dict[str, DevelopmentTask] = {}
        self._ensure_storage_directory()
        self._load_tasks()
    
    def _ensure_storage_directory(self):
        """Ensure storage directory exists"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_tasks(self):
        """Load tasks from storage"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    tasks_data = json.load(f)
                
                for task_data in tasks_data:
                    try:
                        task = DevelopmentTask.from_dict(task_data)
                        self.tasks[task.task_id] = task
                    except Exception as e:
                        self.logger.error(f"Failed to load task: {e}")
                
                self.logger.info(f"Loaded {len(self.tasks)} tasks from storage")
                
            except Exception as e:
                self.logger.error(f"Failed to load tasks from storage: {e}")
    
    def _save_tasks(self):
        """Save tasks to storage"""
        try:
            tasks_data = [task.to_dict() for task in self.tasks.values()]
            
            with open(self.storage_path, 'w') as f:
                json.dump(tasks_data, f, indent=2)
            
            self.logger.debug(f"Saved {len(self.tasks)} tasks to storage")
            
        except Exception as e:
            self.logger.error(f"Failed to save tasks to storage: {e}")
    
    def register_task(self, task: DevelopmentTask) -> bool:
        """Register a task in the registry"""
        try:
            self.tasks[task.task_id] = task
            self._save_tasks()
            self.logger.info(f"Registered task {task.task_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register task {task.task_id}: {e}")
            return False
    
    def unregister_task(self, task_id: str) -> bool:
        """Unregister a task from the registry"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._save_tasks()
            self.logger.info(f"Unregistered task {task_id}")
            return True
        return False
    
    def get_task(self, task_id: str) -> Optional[DevelopmentTask]:
        """Get a task by ID"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[DevelopmentTask]:
        """Get all registered tasks"""
        return list(self.tasks.values())
    
    def update_task(self, task: DevelopmentTask) -> bool:
        """Update a task in the registry"""
        if task.task_id in self.tasks:
            self.tasks[task.task_id] = task
            self._save_tasks()
            return True
        return False
    
    def clear_registry(self):
        """Clear all tasks from registry"""
        self.tasks.clear()
        self._save_tasks()
        self.logger.info("Cleared task registry")
    
    def get_registry_stats(self) -> Dict[str, any]:
        """Get registry statistics"""
        return {
            "total_tasks": len(self.tasks),
            "storage_path": str(self.storage_path),
            "storage_exists": self.storage_path.exists()
        }
