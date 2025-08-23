#!/usr/bin/env python3
"""
Task Manager - Agent Cellphone V2
================================

Manages development tasks and autonomous workflow.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from ..core.models import DevelopmentTask
from ..core.enums import TaskPriority, TaskComplexity, TaskStatus


class TaskManager:
    """Manages development tasks and autonomous workflow"""
    
    def __init__(self):
        self.tasks: Dict[str, DevelopmentTask] = {}
        self.task_counter = 0
        self.logger = logging.getLogger(__name__)
        self.workflow_stats = {
            "total_tasks_created": 0,
            "total_tasks_completed": 0,
            "total_tasks_claimed": 0,
            "overnight_cycles": 0,
            "autonomous_hours": 0,
        }
        
        # Initialize with sample tasks for overnight development
        self._initialize_sample_tasks()
    
    def _initialize_sample_tasks(self):
        """Initialize with sample development tasks"""
        sample_tasks = [
            {
                "title": "Repository Cleanup and Optimization",
                "description": "Clean up unused files, optimize imports, and improve code structure",
                "complexity": TaskComplexity.MEDIUM,
                "priority": TaskPriority.HIGH,
                "estimated_hours": 2.0,
                "required_skills": ["git", "code_analysis", "optimization"],
            },
            {
                "title": "Documentation Update",
                "description": "Update README files, add inline comments, and improve API documentation",
                "complexity": TaskComplexity.LOW,
                "priority": TaskPriority.MEDIUM,
                "estimated_hours": 1.5,
                "required_skills": ["documentation", "markdown", "api_design"],
            },
            {
                "title": "Test Coverage Improvement",
                "description": "Increase test coverage, add missing unit tests, and improve test quality",
                "complexity": TaskComplexity.MEDIUM,
                "priority": TaskPriority.HIGH,
                "estimated_hours": 3.0,
                "required_skills": ["testing", "unittest", "coverage"],
            },
            {
                "title": "Performance Optimization",
                "description": "Identify and fix performance bottlenecks, optimize algorithms",
                "complexity": TaskComplexity.HIGH,
                "priority": TaskPriority.MEDIUM,
                "estimated_hours": 4.0,
                "required_skills": ["profiling", "optimization", "algorithms"],
            },
            {
                "title": "Security Audit",
                "description": "Review code for security vulnerabilities and implement fixes",
                "complexity": TaskComplexity.HIGH,
                "priority": TaskPriority.CRITICAL,
                "estimated_hours": 5.0,
                "required_skills": ["security", "code_review", "vulnerability_assessment"],
            }
        ]
        
        for task_data in sample_tasks:
            self.create_task(**task_data)
    
    def create_task(self, title: str, description: str, complexity: TaskComplexity,
                   priority: TaskPriority, estimated_hours: float, 
                   required_skills: List[str], tags: Optional[List[str]] = None) -> str:
        """Create a new development task"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter:04d}"
        
        task = DevelopmentTask(
            task_id=task_id,
            title=title,
            description=description,
            complexity=complexity,
            priority=priority,
            estimated_hours=estimated_hours,
            required_skills=required_skills,
            tags=tags or []
        )
        
        self.tasks[task_id] = task
        self.workflow_stats["total_tasks_created"] += 1
        
        self.logger.info(f"Created task {task_id}: {title}")
        return task_id
    
    def get_task(self, task_id: str) -> Optional[DevelopmentTask]:
        """Get a task by ID"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[DevelopmentTask]:
        """Get all tasks"""
        return list(self.tasks.values())
    
    def get_available_tasks(self) -> List[DevelopmentTask]:
        """Get tasks available for claiming"""
        return [task for task in self.tasks.values() if task.is_available()]
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[DevelopmentTask]:
        """Get tasks by status"""
        return [task for task in self.tasks.values() if task.status == status]
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[DevelopmentTask]:
        """Get tasks by priority"""
        return [task for task in self.tasks.values() if task.priority == priority]
    
    def get_tasks_by_complexity(self, complexity: TaskComplexity) -> List[DevelopmentTask]:
        """Get tasks by complexity"""
        return [task for task in self.tasks.values() if task.complexity == complexity]
    
    def get_tasks_by_agent(self, agent_id: str) -> List[DevelopmentTask]:
        """Get tasks claimed by a specific agent"""
        return [task for task in self.tasks.values() if task.claimed_by == agent_id]
    
    def claim_task(self, task_id: str, agent_id: str) -> bool:
        """Claim a task for an agent"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        if task.claim(agent_id):
            self.workflow_stats["total_tasks_claimed"] += 1
            self.logger.info(f"Agent {agent_id} claimed task {task_id}")
            return True
        
        return False
    
    def start_task(self, task_id: str) -> bool:
        """Start working on a task"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        return task.start_work()
    
    def update_task_progress(self, task_id: str, percentage: float) -> bool:
        """Update task progress"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        return task.update_progress(percentage)
    
    def complete_task(self, task_id: str) -> bool:
        """Complete a task"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        if task.complete():
            self.workflow_stats["total_tasks_completed"] += 1
            self.logger.info(f"Task {task_id} completed by {task.claimed_by}")
            return True
        
        return False
    
    def block_task(self, task_id: str, reason: str) -> bool:
        """Block a task with a reason"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        return task.block(reason)
    
    def unblock_task(self, task_id: str) -> bool:
        """Unblock a task"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        return task.unblock()
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        return task.cancel()
    
    def get_task_statistics(self) -> Dict[str, any]:
        """Get task statistics"""
        total_tasks = len(self.tasks)
        available_tasks = len(self.get_available_tasks())
        claimed_tasks = len(self.get_tasks_by_status(TaskStatus.CLAIMED))
        in_progress_tasks = len(self.get_tasks_by_status(TaskStatus.IN_PROGRESS))
        completed_tasks = len(self.get_tasks_by_status(TaskStatus.COMPLETED))
        blocked_tasks = len(self.get_tasks_by_status(TaskStatus.BLOCKED))
        
        # Calculate average completion time
        completed_task_times = []
        for task in self.get_tasks_by_status(TaskStatus.COMPLETED):
            elapsed = task.get_elapsed_time()
            if elapsed is not None:
                completed_task_times.append(elapsed)
        
        avg_completion_time = sum(completed_task_times) / len(completed_task_times) if completed_tasks > 0 else 0
        
        return {
            "total_tasks": total_tasks,
            "available_tasks": available_tasks,
            "claimed_tasks": claimed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
            "blocked_tasks": blocked_tasks,
            "avg_completion_time_hours": avg_completion_time,
            "workflow_stats": self.workflow_stats.copy()
        }
    
    def get_priority_distribution(self) -> Dict[str, int]:
        """Get distribution of tasks by priority"""
        distribution = {}
        for priority in TaskPriority:
            distribution[priority.name] = len(self.get_tasks_by_priority(priority))
        return distribution
    
    def get_complexity_distribution(self) -> Dict[str, int]:
        """Get distribution of tasks by complexity"""
        distribution = {}
        for complexity in TaskComplexity:
            distribution[complexity.name] = len(self.get_tasks_by_complexity(complexity))
        return distribution
    
    def cleanup_completed_tasks(self, days_old: int = 30) -> int:
        """Remove completed tasks older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        removed_count = 0
        
        task_ids_to_remove = []
        for task_id, task in self.tasks.items():
            if (task.is_completed() and task.completed_at and 
                task.completed_at < cutoff_date):
                task_ids_to_remove.append(task_id)
        
        for task_id in task_ids_to_remove:
            del self.tasks[task_id]
            removed_count += 1
        
        self.logger.info(f"Removed {removed_count} old completed tasks")
        return removed_count
    
    def export_tasks(self) -> List[Dict[str, any]]:
        """Export all tasks to dictionary format"""
        return [task.to_dict() for task in self.tasks.values()]
    
    def import_tasks(self, tasks_data: List[Dict[str, any]]) -> int:
        """Import tasks from dictionary format"""
        imported_count = 0
        
        for task_data in tasks_data:
            try:
                task = DevelopmentTask.from_dict(task_data)
                self.tasks[task.task_id] = task
                imported_count += 1
            except Exception as e:
                self.logger.error(f"Failed to import task: {e}")
        
        self.logger.info(f"Imported {imported_count} tasks")
        return imported_count
