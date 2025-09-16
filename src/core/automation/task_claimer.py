#!/usr/bin/env python3
"""
Task Claimer - Automated task claiming system
=============================================

Handles automated task claiming from future tasks based on agent capabilities
and current workload.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 compliance modularization
License: MIT
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class TaskClaimer:
    """Handles automated task claiming."""

    def __init__(self, agent_workspace: Path, agent_id: str) -> None:
        """Initialize task claimer."""
        self.agent_workspace = agent_workspace
        self.agent_id = agent_id
        self.working_tasks_path = agent_workspace / "working_tasks.json"
        self.future_tasks_path = agent_workspace / "future_tasks.json"

    def can_claim_task(self) -> bool:
        """Check if agent can claim a new task."""
        try:
            if not self.working_tasks_path.exists():
                return True
            
            with open(self.working_tasks_path, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
            
            current_task = tasks.get("current_task")
            if not current_task:
                return True
            
            # Check if current task is completed
            if current_task.get("status") == "completed":
                return True
            
            # Check if current task is in progress
            if current_task.get("status") == "in_progress":
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking task claim eligibility: {e}")
            return False

    def get_available_tasks(self) -> list[dict[str, Any]]:
        """Get list of available tasks."""
        try:
            if not self.future_tasks_path.exists():
                return []
            
            with open(self.future_tasks_path, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
            
            available_tasks = []
            for task in tasks.get("tasks", []):
                if self._is_task_suitable(task):
                    available_tasks.append(task)
            
            return available_tasks
            
        except Exception as e:
            logger.error(f"Error getting available tasks: {e}")
            return []

    def claim_task(self, task: dict[str, Any]) -> bool:
        """Claim a specific task."""
        try:
            # Update working tasks
            if self.working_tasks_path.exists():
                with open(self.working_tasks_path, 'r', encoding='utf-8') as f:
                    working_tasks = json.load(f)
            else:
                working_tasks = {"current_task": None, "completed_tasks": []}
            
            # Set current task
            task["claimed_at"] = datetime.now().isoformat()
            task["claimed_by"] = self.agent_id
            task["status"] = "in_progress"
            
            working_tasks["current_task"] = task
            
            with open(self.working_tasks_path, 'w', encoding='utf-8') as f:
                json.dump(working_tasks, f, indent=2, ensure_ascii=False)
            
            # Remove from future tasks
            self._remove_from_future_tasks(task)
            
            logger.info(f"Task claimed: {task.get('id', 'unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Error claiming task: {e}")
            return False

    def auto_claim_task(self) -> dict[str, Any] | None:
        """Automatically claim the best available task."""
        if not self.can_claim_task():
            return None
        
        available_tasks = self.get_available_tasks()
        if not available_tasks:
            return None
        
        # Select best task based on priority and agent capabilities
        best_task = self._select_best_task(available_tasks)
        if best_task and self.claim_task(best_task):
            return best_task
        
        return None

    def complete_current_task(self, result: str = "completed") -> bool:
        """Mark current task as completed."""
        try:
            if not self.working_tasks_path.exists():
                return False
            
            with open(self.working_tasks_path, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
            
            current_task = tasks.get("current_task")
            if not current_task:
                return False
            
            # Mark as completed
            current_task["status"] = "completed"
            current_task["completed_at"] = datetime.now().isoformat()
            current_task["result"] = result
            
            # Move to completed tasks
            if "completed_tasks" not in tasks:
                tasks["completed_tasks"] = []
            tasks["completed_tasks"].append(current_task)
            tasks["current_task"] = None
            
            with open(self.working_tasks_path, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Task completed: {current_task.get('id', 'unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            return False

    def _is_task_suitable(self, task: dict[str, Any]) -> bool:
        """Check if task is suitable for this agent."""
        # Check agent capabilities
        required_skills = task.get("required_skills", [])
        agent_skills = self._get_agent_skills()
        
        if required_skills:
            if not any(skill in agent_skills for skill in required_skills):
                return False
        
        # Check priority
        priority = task.get("priority", "normal")
        if priority == "urgent":
            return True
        
        # Check dependencies
        dependencies = task.get("dependencies", [])
        if dependencies:
            if not self._check_dependencies(dependencies):
                return False
        
        return True

    def _select_best_task(self, tasks: list[dict[str, Any]]) -> dict[str, Any] | None:
        """Select the best task from available tasks."""
        if not tasks:
            return None
        
        # Sort by priority and complexity
        def task_score(task):
            priority_scores = {"urgent": 3, "high": 2, "normal": 1, "low": 0}
            priority = task.get("priority", "normal")
            complexity = task.get("complexity", "medium")
            complexity_scores = {"low": 1, "medium": 2, "high": 3}
            
            return priority_scores.get(priority, 1) + complexity_scores.get(complexity, 2)
        
        return max(tasks, key=task_score)

    def _get_agent_skills(self) -> list[str]:
        """Get agent skills based on agent ID."""
        skill_map = {
            "Agent-1": ["integration", "services", "consolidation"],
            "Agent-2": ["architecture", "design", "coordination"],
            "Agent-3": ["infrastructure", "devops", "automation"],
            "Agent-4": ["captain", "coordination", "oversight"],
            "Agent-5": ["business_intelligence", "analytics", "data"],
            "Agent-6": ["communication", "messaging", "coordination"],
            "Agent-7": ["web_development", "frontend", "ui"],
            "Agent-8": ["operations", "workflow", "process"]
        }
        return skill_map.get(self.agent_id, [])

    def _check_dependencies(self, dependencies: list[str]) -> bool:
        """Check if task dependencies are met."""
        # Simple dependency check - in real implementation would check actual dependencies
        return True

    def _remove_from_future_tasks(self, task: dict[str, Any]) -> None:
        """Remove task from future tasks."""
        try:
            if not self.future_tasks_path.exists():
                return
            
            with open(self.future_tasks_path, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
            
            task_id = task.get("id")
            if task_id:
                tasks["tasks"] = [t for t in tasks.get("tasks", []) if t.get("id") != task_id]
                
                with open(self.future_tasks_path, 'w', encoding='utf-8') as f:
                    json.dump(tasks, f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            logger.error(f"Error removing task from future tasks: {e}")
