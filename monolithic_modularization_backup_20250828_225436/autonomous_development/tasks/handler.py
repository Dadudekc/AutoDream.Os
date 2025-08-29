#!/usr/bin/env python3
"""
Autonomous Development Task Handler
==================================

This module handles task management and execution for autonomous development.
Follows SRP by focusing solely on task handling and progress management.
"""

import random
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from src.utils.stability_improvements import stability_manager, safe_import
# Use type hints with strings to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.autonomous_development.core import DevelopmentTask
    from src.core.task_manager import DevelopmentTaskManager as TaskManager


class TaskHandler:
    """Handles task management and execution for autonomous development"""

    def __init__(self, task_manager: "TaskManager"):
        self.task_manager = task_manager
        self.logger = logging.getLogger(__name__)

    def create_development_task(
        self,
        title: str,
        description: str,
        complexity: str,
        priority: int,
        estimated_hours: float,
        required_skills: List[str],
    ) -> str:
        """Create a new development task with proper validation"""
        # Validate complexity
        if complexity not in ["low", "medium", "high"]:
            raise ValueError("Complexity must be 'low', 'medium', or 'high'")

        # Validate priority
        if not (1 <= priority <= 10):
            raise ValueError("Priority must be between 1 and 10")

        # Validate hours
        if estimated_hours <= 0:
            raise ValueError("Hours must be positive")

        # Generate skills based on complexity if not provided
        if not required_skills:
            required_skills = self._generate_skills_for_complexity(complexity)

        # Create the task
        task_id = self.task_manager.create_task(
            title=title,
            description=description,
            complexity=complexity,
            priority=priority,
            estimated_hours=estimated_hours,
            required_skills=required_skills,
        )

        self.logger.info(f"Created task {task_id}: {title}")
        return task_id

    def _generate_skills_for_complexity(self, complexity: str) -> List[str]:
        """Generate appropriate skills based on task complexity"""
        if complexity == "low":
            skills = random.sample(
                ["documentation", "markdown", "testing", "git"], 2
            )
        elif complexity == "medium":
            skills = random.sample(
                ["code_analysis", "optimization", "debugging", "refactoring"], 3
            )
        else:  # high
            skills = random.sample(
                [
                    "performance_analysis",
                    "security_analysis",
                    "architecture",
                    "profiling",
                ],
                4,
            )
        return skills

    def claim_task(self, task_id: str, agent_id: str) -> bool:
        """Claim a task for an agent"""
        try:
            success = self.task_manager.claim_task(task_id, agent_id)
            if success:
                self.logger.info(f"Task {task_id} claimed by {agent_id}")
            return success
        except Exception as e:
            self.logger.error(f"Failed to claim task {task_id}: {e}")
            return False

    def start_task_work(self, task_id: str) -> bool:
        """Start work on a claimed task"""
        try:
            task = self.task_manager.tasks.get(task_id)
            if task and task.status == "claimed":
                task.status = "in_progress"
                task.started_at = datetime.now()
                self.logger.info(f"Started work on task {task_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to start task {task_id}: {e}")
            return False

    def update_task_progress(
        self, task_id: str, progress_percentage: float, blockers: List[str] = None
    ) -> bool:
        """Update task progress and handle blockers"""
        try:
            task = self.task_manager.tasks.get(task_id)
            if not task:
                return False

            # Update progress
            task.progress_percentage = min(100.0, max(0.0, progress_percentage))
            task.last_updated = datetime.now()

            # Handle blockers
            if blockers:
                task.blockers = blockers
                if task.status != "blocked":
                    task.status = "blocked"
                    self.logger.warning(f"Task {task_id} blocked: {', '.join(blockers)}")
            else:
                # Clear blockers if none exist
                if task.blockers:
                    task.blockers = []
                    if task.status == "blocked":
                        task.status = "in_progress"

            # Check if task is complete
            if task.progress_percentage >= 100.0:
                self._complete_task(task_id)

            self.logger.info(f"Updated task {task_id} progress to {progress_percentage:.1f}%")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update task {task_id} progress: {e}")
            return False

    def _complete_task(self, task_id: str):
        """Mark a task as completed"""
        try:
            task = self.task_manager.tasks.get(task_id)
            if task:
                task.status = "completed"
                task.completed_at = datetime.now()
                
                # Calculate actual time taken
                if task.started_at:
                    time_taken = task.completed_at - task.started_at
                    task.actual_hours = time_taken.total_seconds() / 3600
                
                self.logger.info(f"Task {task_id} completed successfully")
                
                # Update workflow stats
                self.task_manager.workflow_stats["total_tasks_completed"] += 1
        except Exception as e:
            self.logger.error(f"Failed to complete task {task_id}: {e}")

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of a specific task"""
        try:
            task = self.task_manager.tasks.get(task_id)
            if not task:
                return None

            return {
                "task_id": task.task_id,
                "title": task.title,
                "status": task.status,
                "progress_percentage": task.progress_percentage,
                "claimed_by": task.claimed_by,
                "priority": task.priority,
                "complexity": task.complexity,
                "estimated_hours": task.estimated_hours,
                "actual_hours": getattr(task, 'actual_hours', None),
                "required_skills": task.required_skills,
                "blockers": task.blockers or [],
                "created_at": task.created_at,
                "started_at": getattr(task, 'started_at', None),
                "completed_at": getattr(task, 'completed_at', None),
                "last_updated": getattr(task, 'last_updated', None),
            }
        except Exception as e:
            self.logger.error(f"Failed to get task status for {task_id}: {e}")
            return None

    def get_tasks_by_status(self, status: str) -> List["DevelopmentTask"]:
        """Get all tasks with a specific status"""
        try:
            return [
                task for task in self.task_manager.tasks.values()
                if task.status == status
            ]
        except Exception as e:
            self.logger.error(f"Failed to get tasks by status {status}: {e}")
            return []

    def get_tasks_by_agent(self, agent_id: str) -> List["DevelopmentTask"]:
        """Get all tasks claimed by a specific agent"""
        try:
            return [
                task for task in self.task_manager.tasks.values()
                if task.claimed_by == agent_id
            ]
        except Exception as e:
            self.logger.error(f"Failed to get tasks by agent {agent_id}: {e}")
            return []

    def get_blocked_tasks(self) -> List["DevelopmentTask"]:
        """Get all blocked tasks"""
        return self.get_tasks_by_status("blocked")

    def resolve_task_blocker(self, task_id: str, blocker: str) -> bool:
        """Resolve a specific blocker for a task"""
        try:
            task = self.task_manager.tasks.get(task_id)
            if not task or not task.blockers:
                return False

            if blocker in task.blockers:
                task.blockers.remove(blocker)
                
                # If no more blockers, unblock the task
                if not task.blockers and task.status == "blocked":
                    task.status = "in_progress"
                
                self.logger.info(f"Resolved blocker '{blocker}' for task {task_id}")
                return True
            
            return False
        except Exception as e:
            self.logger.error(f"Failed to resolve blocker for task {task_id}: {e}")
            return False

    def get_task_completion_estimate(self, task_id: str) -> Optional[float]:
        """Estimate remaining time to complete a task"""
        try:
            task = self.task_manager.tasks.get(task_id)
            if not task or task.status in ["completed", "blocked"]:
                return None

            if task.progress_percentage <= 0:
                return task.estimated_hours

            # Calculate remaining time based on progress and estimated hours
            remaining_percentage = 100.0 - task.progress_percentage
            if task.progress_percentage > 0:
                # Estimate based on current progress rate
                elapsed_hours = getattr(task, 'actual_hours', 0) or 0
                if elapsed_hours > 0:
                    progress_rate = task.progress_percentage / elapsed_hours
                    remaining_hours = remaining_percentage / progress_rate if progress_rate > 0 else task.estimated_hours
                else:
                    remaining_hours = task.estimated_hours * (remaining_percentage / 100.0)
            else:
                remaining_hours = task.estimated_hours

            return max(0.1, remaining_hours)  # Minimum 0.1 hours

        except Exception as e:
            self.logger.error(f"Failed to estimate completion time for task {task_id}: {e}")
            return None

    def get_task_statistics(self) -> Dict[str, Any]:
        """Get comprehensive task statistics"""
        try:
            tasks = list(self.task_manager.tasks.values())
            if not tasks:
                return {
                    "total_tasks": 0,
                    "tasks_by_status": {},
                    "average_completion_time": 0.0,
                    "blocker_statistics": {},
                }

            # Count by status
            status_counts = {}
            for task in tasks:
                status = task.status
                status_counts[status] = status_counts.get(status, 0) + 1

            # Calculate completion times
            completion_times = []
            for task in tasks:
                if task.status == "completed" and hasattr(task, 'started_at') and hasattr(task, 'completed_at'):
                    if task.started_at and task.completed_at:
                        time_taken = task.completed_at - task.started_at
                        completion_times.append(time_taken.total_seconds() / 3600)

            # Blocker statistics
            blocker_stats = {}
            for task in tasks:
                if task.blockers:
                    for blocker in task.blockers:
                        blocker_stats[blocker] = blocker_stats.get(blocker, 0) + 1

            return {
                "total_tasks": len(tasks),
                "tasks_by_status": status_counts,
                "average_completion_time": sum(completion_times) / len(completion_times) if completion_times else 0.0,
                "blocker_statistics": blocker_stats,
                "completion_rate": (status_counts.get("completed", 0) / len(tasks)) * 100 if tasks else 0.0,
            }

        except Exception as e:
            self.logger.error(f"Failed to get task statistics: {e}")
            return {}
