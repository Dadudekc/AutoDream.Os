#!/usr/bin/env python3
"""
Workflow Engine - Agent Cellphone V2
===================================

Orchestrates autonomous development workflow.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from ..core.enums import WorkflowState, TaskStatus, TaskPriority
from ..core.models import DevelopmentTask
from core.task_manager import DevelopmentTaskManager as TaskManager
from ..agents.agent_coordinator import AgentCoordinator


class WorkflowEngine:
    """Orchestrates autonomous development workflow"""
    
    def __init__(self, task_manager: TaskManager, agent_coordinator: AgentCoordinator):
        self.task_manager = task_manager
        self.agent_coordinator = agent_coordinator
        self.logger = logging.getLogger(__name__)
        self.state = WorkflowState.IDLE
        self.workflow_stats = {
            "cycles_completed": 0,
            "tasks_processed": 0,
            "successful_assignments": 0,
            "failed_assignments": 0,
            "total_runtime_hours": 0.0,
            "start_time": None,
            "last_cycle_time": None
        }
        self.cycle_callbacks: List[Callable] = []
        self.is_running = False
    
    def start_workflow(self) -> bool:
        """Start the autonomous workflow"""
        if self.is_running:
            self.logger.warning("Workflow already running")
            return False
        
        self.is_running = True
        self.state = WorkflowState.ACTIVE
        self.workflow_stats["start_time"] = datetime.now()
        
        self.logger.info("🚀 Autonomous development workflow started")
        return True
    
    def stop_workflow(self) -> bool:
        """Stop the autonomous workflow"""
        if not self.is_running:
            self.logger.warning("Workflow not running")
            return False
        
        self.is_running = False
        self.state = WorkflowState.IDLE
        
        # Calculate total runtime
        if self.workflow_stats["start_time"]:
            runtime = datetime.now() - self.workflow_stats["start_time"]
            self.workflow_stats["total_runtime_hours"] += runtime.total_seconds() / 3600.0
        
        self.logger.info("⏹️ Autonomous development workflow stopped")
        return True
    
    def pause_workflow(self) -> bool:
        """Pause the workflow"""
        if not self.is_running:
            return False
        
        self.state = WorkflowState.PAUSED
        self.logger.info("⏸️ Workflow paused")
        return True
    
    def resume_workflow(self) -> bool:
        """Resume the workflow"""
        if not self.is_running or self.state != WorkflowState.PAUSED:
            return False
        
        self.state = WorkflowState.ACTIVE
        self.logger.info("▶️ Workflow resumed")
        return True
    
    def run_cycle(self) -> bool:
        """Run one workflow cycle"""
        if not self.is_running or self.state != WorkflowState.ACTIVE:
            return False
        
        cycle_start = datetime.now()
        self.logger.info("🔄 Starting workflow cycle")
        
        try:
            # Step 1: Process available tasks
            available_tasks = self.task_manager.get_available_tasks()
            self.logger.info(f"Found {len(available_tasks)} available tasks")
            
            # Step 2: Assign tasks to agents
            assignments_made = self._assign_available_tasks(available_tasks)
            
            # Step 3: Monitor progress
            progress_updated = self._monitor_task_progress()
            
            # Step 4: Handle blocked tasks
            blocked_resolved = self._handle_blocked_tasks()
            
            # Update cycle statistics
            cycle_time = datetime.now() - cycle_start
            self.workflow_stats["last_cycle_time"] = cycle_time
            self.workflow_stats["cycles_completed"] += 1
            self.workflow_stats["tasks_processed"] += len(available_tasks)
            
            self.logger.info(f"✅ Cycle completed in {cycle_time.total_seconds():.2f}s")
            self.logger.info(f"  - Tasks assigned: {assignments_made}")
            self.logger.info(f"  - Progress updates: {progress_updated}")
            self.logger.info(f"  - Blocked resolved: {blocked_resolved}")
            
            # Notify cycle callbacks
            self._notify_cycle_callbacks(assignments_made, progress_updated, blocked_resolved)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Workflow cycle failed: {e}")
            self.state = WorkflowState.ERROR
            return False
    
    def _assign_available_tasks(self, available_tasks: List[DevelopmentTask]) -> int:
        """Assign available tasks to agents"""
        assignments_made = 0
        
        for task in available_tasks:
            # Find best agent for the task
            best_agent = self.agent_coordinator.find_best_agent_for_task(task)
            
            if best_agent:
                # Assign task to agent
                if self.agent_coordinator.assign_task_to_agent(task, best_agent.agent_id):
                    assignments_made += 1
                    self.workflow_stats["successful_assignments"] += 1
                    self.logger.debug(f"Assigned task {task.task_id} to {best_agent.agent_id}")
                else:
                    self.workflow_stats["failed_assignments"] += 1
                    self.logger.warning(f"Failed to assign task {task.task_id} to {best_agent.agent_id}")
            else:
                self.logger.debug(f"No suitable agent found for task {task.task_id}")
        
        return assignments_made
    
    def _monitor_task_progress(self) -> int:
        """Monitor and update task progress"""
        progress_updates = 0
        in_progress_tasks = self.task_manager.get_tasks_by_status(TaskStatus.IN_PROGRESS)
        
        for task in in_progress_tasks:
            # Simulate progress updates (in real system, agents would report progress)
            if task.started_at:
                elapsed_hours = task.get_elapsed_time() or 0
                if elapsed_hours > 0:
                    # Estimate progress based on elapsed time vs estimated time
                    estimated_completion = task.estimated_hours
                    if estimated_completion > 0:
                        estimated_progress = min(100.0, (elapsed_hours / estimated_completion) * 100)
                        
                        # Add some randomness to simulate real progress
                        import random
                        actual_progress = estimated_progress + random.uniform(-5, 10)
                        actual_progress = max(0.0, min(100.0, actual_progress))
                        
                        if abs(actual_progress - task.progress_percentage) > 5:
                            if self.task_manager.update_task_progress(task.task_id, actual_progress):
                                progress_updates += 1
        
        return progress_updates
    
    def _handle_blocked_tasks(self) -> int:
        """Handle blocked tasks and attempt resolution"""
        blocked_resolved = 0
        blocked_tasks = self.task_manager.get_tasks_by_status(TaskStatus.BLOCKED)
        
        for task in blocked_tasks:
            # Simple unblocking logic (in real system, would check dependencies)
            if len(task.blockers) > 0:
                # Check if blockers are resolved
                if self._are_blockers_resolved(task):
                    if self.task_manager.unblock_task(task.task_id):
                        blocked_resolved += 1
                        self.logger.info(f"Unblocked task {task.task_id}")
        
        return blocked_resolved
    
    def _are_blockers_resolved(self, task: DevelopmentTask) -> bool:
        """Check if task blockers are resolved"""
        # Simple implementation - in real system would check actual dependencies
        # For now, randomly resolve some blockers
        import random
        return random.random() < 0.3  # 30% chance of resolution
    
    def add_cycle_callback(self, callback: Callable):
        """Add a callback to be called after each cycle"""
        self.cycle_callbacks.append(callback)
    
    def remove_cycle_callback(self, callback: Callable):
        """Remove a cycle callback"""
        if callback in self.cycle_callbacks:
            self.cycle_callbacks.remove(callback)
    
    def _notify_cycle_callbacks(self, assignments: int, progress: int, blocked: int):
        """Notify all cycle callbacks"""
        for callback in self.cycle_callbacks:
            try:
                callback(assignments, progress, blocked)
            except Exception as e:
                self.logger.error(f"Cycle callback failed: {e}")
    
    def get_workflow_status(self) -> Dict[str, any]:
        """Get current workflow status"""
        return {
            "state": self.state.value,
            "is_running": self.is_running,
            "workflow_stats": self.workflow_stats.copy(),
            "task_stats": self.task_manager.get_task_statistics(),
            "agent_stats": self.agent_coordinator.get_agent_statistics()
        }
    
    def get_workflow_summary(self) -> Dict[str, any]:
        """Get workflow summary for reporting"""
        status = self.get_workflow_status()
        
        # Calculate efficiency metrics
        total_assignments = status["workflow_stats"]["successful_assignments"] + status["workflow_stats"]["failed_assignments"]
        success_rate = (status["workflow_stats"]["successful_assignments"] / total_assignments * 100) if total_assignments > 0 else 0
        
        # Calculate throughput
        runtime_hours = status["workflow_stats"]["total_runtime_hours"]
        tasks_per_hour = (status["workflow_stats"]["tasks_processed"] / runtime_hours) if runtime_hours > 0 else 0
        
        return {
            "status": status["state"],
            "is_running": status["is_running"],
            "total_cycles": status["workflow_stats"]["cycles_completed"],
            "total_tasks_processed": status["workflow_stats"]["tasks_processed"],
            "success_rate_percent": success_rate,
            "tasks_per_hour": tasks_per_hour,
            "total_runtime_hours": runtime_hours,
            "last_cycle_time_seconds": status["workflow_stats"]["last_cycle_time"].total_seconds() if status["workflow_stats"]["last_cycle_time"] else None
        }
    
    def run_continuous_workflow(self, cycle_interval_seconds: int = 60, max_cycles: Optional[int] = None):
        """Run workflow continuously with specified interval"""
        if not self.start_workflow():
            return False
        
        cycle_count = 0
        try:
            while self.is_running and (max_cycles is None or cycle_count < max_cycles):
                if self.state == WorkflowState.ACTIVE:
                    self.run_cycle()
                    cycle_count += 1
                
                # Wait for next cycle
                time.sleep(cycle_interval_seconds)
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Workflow interrupted by user")
        except Exception as e:
            self.logger.error(f"❌ Workflow error: {e}")
        finally:
            self.stop_workflow()
        
        return True
