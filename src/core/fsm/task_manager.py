#!/usr/bin/env python3
"""
Task Manager - V2 Modular Architecture
=====================================

Task management functionality for the FSM system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4I - FSM System Modularization
License: MIT
"""

import logging
import json
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .models import FSMTask, TaskState, TaskPriority, FSMUpdate
from .types import FSMConfig


logger = logging.getLogger(__name__)


class TaskManager:
    """
    Task Manager - FSM Task Management
    
    Single responsibility: Manage FSM tasks, including creation,
    assignment, tracking, and state updates following V2 architecture standards.
    """
    
    def __init__(self, config: Optional[FSMConfig] = None):
        """Initialize task manager."""
        self.logger = logging.getLogger(f"{__name__}.TaskManager")
        
        # Configuration
        self.config = config or FSMConfig()
        
        # Task storage
        self._tasks: Dict[str, FSMTask] = {}
        self._task_updates: List[FSMUpdate] = []
        
        # Performance tracking
        self._task_execution_history: List[Dict[str, Any]] = []
        self._state_transition_history: List[Dict[str, Any]] = []
        
        # Initialize task system
        self._initialize_task_workspace()
        self._load_existing_tasks()
        
        self.logger.info("✅ Task Manager initialized successfully")
    
    # ============================================================================
    # TASK MANAGEMENT
    # ============================================================================
    
    def create_task(
        self,
        title: str,
        description: str,
        assigned_agent: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a new FSM task."""
        try:
            task_id = str(uuid.uuid4())
            now = datetime.now().isoformat()

            task = FSMTask(
                id=task_id,
                title=title,
                description=description,
                state=TaskState.NEW,
                priority=priority,
                assigned_agent=assigned_agent,
                created_at=now,
                updated_at=now,
                metadata=metadata or {},
            )

            # Store task
            self._tasks[task_id] = task
            self._save_task(task)

            # Send FSM update
            self._send_fsm_update(
                task_id, assigned_agent, TaskState.NEW, f"New task assigned: {title}"
            )

            self.logger.info(f"Created FSM task: {task_id}")
            return task_id

        except Exception as e:
            self.logger.error(f"Failed to create FSM task: {e}")
            return ""
    
    def update_task_state(
        self,
        task_id: str,
        new_state: TaskState,
        agent_id: str,
        summary: str,
        evidence: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update task state."""
        try:
            if task_id not in self._tasks:
                self.logger.error(f"Task not found: {task_id}")
                return False

            task = self._tasks[task_id]
            old_state = task.state
            
            # Update task state
            task.update_state(new_state)
            if evidence:
                task.add_evidence(agent_id, evidence)

            # Save updated task
            self._save_task(task)

            # Record state transition
            transition_record = {
                "timestamp": time.time(),
                "task_id": task_id,
                "from_state": old_state.value,
                "to_state": new_state.value,
                "agent_id": agent_id,
                "summary": summary
            }
            self._state_transition_history.append(transition_record)

            # Send FSM update
            self._send_fsm_update(task_id, agent_id, new_state, summary)

            self.logger.info(f"Updated task {task_id} state: {old_state.value} -> {new_state.value}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update task state: {e}")
            return False
    
    def get_task(self, task_id: str) -> Optional[FSMTask]:
        """Get task by ID."""
        return self._tasks.get(task_id)
    
    def get_tasks_by_agent(self, agent_id: str) -> List[FSMTask]:
        """Get all tasks assigned to an agent."""
        return [task for task in self._tasks.values() if task.assigned_agent == agent_id]
    
    def get_tasks_by_state(self, state: TaskState) -> List[FSMTask]:
        """Get all tasks in a specific state."""
        return [task for task in self._tasks.values() if task.state == state]
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[FSMTask]:
        """Get all tasks with a specific priority."""
        return [task for task in self._tasks.values() if task.priority == priority]
    
    def get_all_tasks(self) -> List[FSMTask]:
        """Get all tasks."""
        return list(self._tasks.values())
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        try:
            if task_id not in self._tasks:
                self.logger.warning(f"Task not found: {task_id}")
                return False
            
            # Remove from storage
            task_file = self.workspace_path / f"task_{task_id}.json"
            if task_file.exists():
                task_file.unlink()
            
            # Remove from memory
            del self._tasks[task_id]
            
            self.logger.info(f"✅ Deleted task: {task_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete task {task_id}: {e}")
            return False
    
    # ============================================================================
    # TASK ANALYSIS AND REPORTING
    # ============================================================================
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """Get comprehensive task statistics."""
        try:
            total_tasks = len(self._tasks)
            if total_tasks == 0:
                return {
                    "total_tasks": 0,
                    "active_tasks": 0,
                    "completed_tasks": 0,
                    "failed_tasks": 0,
                    "success_rate": 0.0,
                    "priority_distribution": {},
                    "state_distribution": {},
                    "agent_distribution": {}
                }
            
            # Calculate basic statistics
            active_tasks = len([t for t in self._tasks.values() if t.state in [TaskState.IN_PROGRESS, TaskState.ONBOARDING]])
            completed_tasks = len([t for t in self._tasks.values() if t.state == TaskState.COMPLETED])
            failed_tasks = len([t for t in self._tasks.values() if t.state == TaskState.FAILED])
            
            # Calculate distributions
            priority_distribution = {}
            state_distribution = {}
            agent_distribution = {}
            
            for task in self._tasks.values():
                priority_distribution[task.priority.value] = priority_distribution.get(task.priority.value, 0) + 1
                state_distribution[task.state.value] = state_distribution.get(task.state.value, 0) + 1
                agent_distribution[task.assigned_agent] = agent_distribution.get(task.assigned_agent, 0) + 1
            
            return {
                "total_tasks": total_tasks,
                "active_tasks": active_tasks,
                "completed_tasks": completed_tasks,
                "failed_tasks": failed_tasks,
                "success_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
                "priority_distribution": priority_distribution,
                "state_distribution": state_distribution,
                "agent_distribution": agent_distribution,
                "total_updates": len(self._task_updates),
                "total_transitions": len(self._state_transition_history)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get task statistics: {e}")
            return {"error": str(e)}
    
    def get_agent_performance(self, agent_id: str) -> Dict[str, Any]:
        """Get performance metrics for a specific agent."""
        try:
            agent_tasks = self.get_tasks_by_agent(agent_id)
            if not agent_tasks:
                return {
                    "agent_id": agent_id,
                    "total_tasks": 0,
                    "completed_tasks": 0,
                    "failed_tasks": 0,
                    "success_rate": 0.0,
                    "average_completion_time": 0.0
                }
            
            total_tasks = len(agent_tasks)
            completed_tasks = len([t for t in agent_tasks if t.state == TaskState.COMPLETED])
            failed_tasks = len([t for t in agent_tasks if t.state == TaskState.FAILED])
            
            # Calculate average completion time for completed tasks
            completion_times = []
            for task in agent_tasks:
                if task.state == TaskState.COMPLETED:
                    try:
                        created = datetime.fromisoformat(task.created_at)
                        updated = datetime.fromisoformat(task.updated_at)
                        completion_time = (updated - created).total_seconds() / 3600  # hours
                        completion_times.append(completion_time)
                    except:
                        pass
            
            avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0.0
            
            return {
                "agent_id": agent_id,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "failed_tasks": failed_tasks,
                "success_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
                "average_completion_time": avg_completion_time,
                "current_active_tasks": len([t for t in agent_tasks if t.state in [TaskState.IN_PROGRESS, TaskState.ONBOARDING]])
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get agent performance: {e}")
            return {"error": str(e)}
    
    def get_task_summary(self) -> Dict[str, Any]:
        """Get task summary for reporting."""
        try:
            stats = self.get_task_statistics()
            
            # Get recent tasks
            recent_tasks = sorted(self._tasks.values(), key=lambda t: t.updated_at, reverse=True)[:10]
            
            # Get high priority and blocked tasks
            high_priority_tasks = [t.id for t in self._tasks.values() if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]]
            blocked_tasks = [t.id for t in self._tasks.values() if t.state == TaskState.BLOCKED]
            
            return {
                "summary": stats,
                "recent_tasks": [{"id": t.id, "title": t.title, "state": t.state.value, "agent": t.assigned_agent} for t in recent_tasks],
                "high_priority_tasks": high_priority_tasks,
                "blocked_tasks": blocked_tasks,
                "recommendations": self._generate_task_recommendations(stats)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get task summary: {e}")
            return {"error": str(e)}
    
    def _generate_task_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """Generate task management recommendations."""
        recommendations = []
        
        total_tasks = stats.get("total_tasks", 0)
        if total_tasks > 0:
            active_ratio = stats.get("active_tasks", 0) / total_tasks
            failure_ratio = stats.get("failed_tasks", 0) / total_tasks
            
            if active_ratio > 0.8:
                recommendations.append("High active task ratio - consider task prioritization")
            if failure_ratio > 0.2:
                recommendations.append("High failure rate - investigate task complexity or agent capabilities")
            if stats.get("success_rate", 0) < 0.7:
                recommendations.append("Low success rate - review task assignment and agent skills")
        
        return recommendations
    
    # ============================================================================
    # TASK UPDATES AND COMMUNICATION
    # ============================================================================
    
    def _send_fsm_update(
        self,
        task_id: str,
        agent_id: str,
        state: TaskState,
        summary: str,
    ) -> None:
        """Send FSM update notification."""
        try:
            update = FSMUpdate(
                update_id=str(uuid.uuid4()),
                task_id=task_id,
                agent_id=agent_id,
                state=state,
                summary=summary,
                timestamp=datetime.now().isoformat(),
            )
            
            self._task_updates.append(update)
            self.logger.debug(f"FSM update sent: {update.update_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to send FSM update: {e}")
    
    def get_task_updates(self, task_id: Optional[str] = None, agent_id: Optional[str] = None) -> List[FSMUpdate]:
        """Get task updates with optional filtering."""
        updates = self._task_updates

        if task_id:
            updates = [u for u in updates if u.task_id == task_id]
        if agent_id:
            updates = [u for u in updates if u.agent_id == agent_id]

        return updates
    
    def get_state_transition_history(self, task_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get state transition history with optional filtering."""
        transitions = self._state_transition_history
        
        if task_id:
            transitions = [t for t in transitions if t.get("task_id") == task_id]
        
        return transitions
    
    # ============================================================================
    # STORAGE AND PERSISTENCE
    # ============================================================================
    
    def _initialize_task_workspace(self):
        """Initialize task workspace."""
        self.workspace_path = Path("fsm_workspaces")
        self.workspace_path.mkdir(exist_ok=True)
        self.logger.info("Task workspace initialized")
    
    def _load_existing_tasks(self):
        """Load existing FSM tasks from storage."""
        try:
            # Load tasks from workspace
            task_files = list(self.workspace_path.glob("task_*.json"))
            for task_file in task_files:
                try:
                    with open(task_file, 'r') as f:
                        task_data = json.load(f)
                        task = FSMTask.from_dict(task_data)
                        self._tasks[task.id] = task
                except Exception as e:
                    self.logger.warning(f"Failed to load task from {task_file}: {e}")
            
            self.logger.info(f"Loaded {len(self._tasks)} existing FSM tasks")
        except Exception as e:
            self.logger.error(f"Failed to load existing tasks: {e}")
    
    def _save_task(self, task: FSMTask) -> None:
        """Save task to storage."""
        try:
            task_file = self.workspace_path / f"task_{task.id}.json"
            with open(task_file, 'w') as f:
                json.dump(task.to_dict(), f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save task {task.id}: {e}")
    
    # ============================================================================
    # CLEANUP AND MAINTENANCE
    # ============================================================================
    
    def cleanup_completed_tasks(self) -> int:
        """Clean up completed tasks if auto-cleanup is enabled."""
        try:
            if not self.config.auto_cleanup_completed:
                return 0
            
            completed_tasks = [t for t in self._tasks.values() if t.state == TaskState.COMPLETED]
            cleaned_count = 0
            
            for task in completed_tasks:
                try:
                    del self._tasks[task.id]
                    task_file = self.workspace_path / f"task_{task.id}.json"
                    if task_file.exists():
                        task_file.unlink()
                    cleaned_count += 1
                except Exception as e:
                    self.logger.warning(f"Failed to cleanup task {task.id}: {e}")
            
            if cleaned_count > 0:
                self.logger.info(f"Cleaned up {cleaned_count} completed tasks")
            
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup completed tasks: {e}")
            return 0
    
    def cleanup(self):
        """Cleanup task manager resources."""
        try:
            # Clean up completed tasks
            self.cleanup_completed_tasks()
            
            self.logger.info("TaskManager cleanup completed")
        except Exception as e:
            self.logger.error(f"TaskManager cleanup failed: {e}")

