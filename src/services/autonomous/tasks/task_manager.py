#!/usr/bin/env python3
"""
Task Manager
=============

Manages task status evaluation and task claiming.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from ...agent_devlog_automation import auto_create_devlog

logger = logging.getLogger(__name__)


class TaskManager:
    """Manages task operations for autonomous agents."""
    
    def __init__(self, agent_id: str, workspace_dir: Path):
        """Initialize task manager."""
        self.agent_id = agent_id
        self.workspace_dir = workspace_dir
        self.working_tasks_file = workspace_dir / "working_tasks.json"
        self.future_tasks_file = workspace_dir / "future_tasks.json"
        self.status_file = workspace_dir / "status.json"
    
    async def evaluate_task_status(self) -> str:
        """Evaluate current task status."""
        try:
            if not self.working_tasks_file.exists():
                return "no_current_task"
            
            with open(self.working_tasks_file, 'r') as f:
                working_tasks = json.load(f)
            
            current_task = working_tasks.get("current_task")
            if not current_task:
                return "no_current_task"
            
            status = current_task.get("status", "unknown")
            
            if status == "completed":
                return "task_completed"
            elif status == "in_progress":
                return "task_in_progress"
            elif status == "blocked":
                return "task_blocked"
            else:
                return "task_unknown_status"
                
        except Exception as e:
            logger.error(f"{self.agent_id}: Error evaluating task status: {e}")
            return "error"
    
    async def claim_task(self) -> Optional[Dict[str, Any]]:
        """Claim a new task from future tasks."""
        try:
            if not self.future_tasks_file.exists():
                logger.info(f"{self.agent_id}: No future tasks file found")
                return None
            
            with open(self.future_tasks_file, 'r') as f:
                future_tasks = json.load(f)
            
            available_tasks = future_tasks.get("tasks", [])
            if not available_tasks:
                logger.info(f"{self.agent_id}: No available tasks to claim")
                return None
            
            # Find highest priority task
            claimed_task = self._select_task_to_claim(available_tasks)
            if not claimed_task:
                logger.info(f"{self.agent_id}: No suitable task found to claim")
                return None
            
            # Move task to working tasks
            await self._move_task_to_working(claimed_task, available_tasks)
            
            # Create devlog for task claiming
            await auto_create_devlog(
                self.agent_id,
                "Task claimed successfully",
                "completed",
                {"task_title": claimed_task.get('title'), "priority": claimed_task.get('priority')}
            )
            
            return claimed_task
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error claiming task: {e}")
            return None
    
    def _select_task_to_claim(self, available_tasks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Select the best task to claim based on priority and dependencies."""
        if not available_tasks:
            return None
        
        # Filter tasks with no dependencies or satisfied dependencies
        claimable_tasks = []
        for task in available_tasks:
            dependencies = task.get('dependencies', [])
            if not dependencies or self._are_dependencies_satisfied(dependencies):
                claimable_tasks.append(task)
        
        if not claimable_tasks:
            return None
        
        # Sort by priority (highest first)
# SECURITY: Key placeholder - replace with environment variable
        
        return claimable_tasks[0]
    
    def _are_dependencies_satisfied(self, dependencies: List[str]) -> bool:
        """Check if task dependencies are satisfied."""
        # Simplified dependency checking - in real implementation, would check completed tasks
        return True
    
    def _get_priority_score(self, priority: str) -> int:
        """Get numeric priority score for sorting."""
        priority_scores = {
            "critical": 5,
            "high": 4,
            "medium": 3,
            "normal": 2,
            "low": 1
        }
        return priority_scores.get(priority.lower(), 2)
    
    async def _move_task_to_working(self, task: Dict[str, Any], available_tasks: List[Dict[str, Any]]) -> None:
        """Move task from future tasks to working tasks."""
        try:
            # Remove from future tasks
            available_tasks.remove(task)
            
            # Update future tasks file
            with open(self.future_tasks_file, 'w') as f:
                json.dump({"tasks": available_tasks}, f, indent=2)
            
            # Add to working tasks
            working_task = {
                "current_task": {
                    "id": task.get('id'),
                    "title": task.get('title'),
                    "description": task.get('description'),
                    "priority": task.get('priority'),
                    "status": "in_progress",
                    "claimed_at": task.get('created_at'),
                    "progress": 0
                }
            }
            
            with open(self.working_tasks_file, 'w') as f:
                json.dump(working_task, f, indent=2)
                
        except Exception as e:
            logger.error(f"{self.agent_id}: Error moving task to working: {e}")
    
    async def continue_current_task(self) -> str:
        """Continue working on current task."""
        try:
            if not self.working_tasks_file.exists():
                return "no_current_task"
            
            with open(self.working_tasks_file, 'r') as f:
                working_tasks = json.load(f)
            
            current_task = working_tasks.get("current_task")
            if not current_task:
                return "no_current_task"
            
            # Simulate task progress
            current_progress = current_task.get("progress", 0)
            new_progress = min(current_progress + 10, 100)
            
            # Update progress
            current_task["progress"] = new_progress
            if new_progress >= 100:
                current_task["status"] = "completed"
            
            # Save updated task
            with open(self.working_tasks_file, 'w') as f:
                json.dump(working_tasks, f, indent=2)
            
            # Create devlog for task progress
            await auto_create_devlog(
                self.agent_id,
                "Task progress updated",
                "completed",
                {"task_title": current_task.get('title'), "progress": new_progress}
            )
            
            return f"Task progress: {new_progress}%"
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error continuing task: {e}")
            return "error"


