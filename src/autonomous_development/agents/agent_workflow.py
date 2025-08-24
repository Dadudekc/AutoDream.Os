#!/usr/bin/env python3
"""
Agent Workflow - Agent Cellphone V2
==================================

Agent workflow and execution management.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from ..core.enums import TaskStatus, WorkflowState
from ..core.models import DevelopmentTask


@dataclass
class WorkflowStep:
    """Individual workflow step"""
    step_id: str
    name: str
    description: str
    action: Callable
    required_skills: List[str]
    estimated_duration_minutes: int
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class AgentWorkflow:
    """Manages individual agent workflows and execution"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)
        self.current_task: Optional[DevelopmentTask] = None
        self.workflow_steps: List[WorkflowStep] = []
        self.current_step_index: int = 0
        self.workflow_state = WorkflowState.IDLE
        self.execution_history: List[Dict] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
        self._initialize_default_steps()
    
    def _initialize_default_steps(self):
        """Initialize default workflow steps"""
        self.workflow_steps = [
            WorkflowStep(
                step_id="analyze",
                name="Task Analysis",
                description="Analyze task requirements and plan approach",
                action=self._analyze_task,
                required_skills=["analysis", "planning"],
                estimated_duration_minutes=15
            ),
            WorkflowStep(
                step_id="implement",
                name="Implementation",
                description="Implement the required functionality",
                action=self._implement_task,
                required_skills=["implementation", "coding"],
                estimated_duration_minutes=120
            ),
            WorkflowStep(
                step_id="test",
                name="Testing",
                description="Test the implementation",
                action=self._test_implementation,
                required_skills=["testing", "validation"],
                estimated_duration_minutes=30
            ),
            WorkflowStep(
                step_id="review",
                name="Code Review",
                description="Review code quality and standards",
                action=self._review_code,
                required_skills=["code_review", "quality_assurance"],
                estimated_duration_minutes=20
            )
        ]
    
    def start_workflow(self, task: DevelopmentTask) -> bool:
        """Start workflow for a specific task"""
        if self.workflow_state != WorkflowState.IDLE:
            self.logger.warning(f"Workflow already in progress: {self.workflow_state.value}")
            return False
        
        self.current_task = task
        self.current_step_index = 0
        self.workflow_state = WorkflowState.ACTIVE
        self.start_time = datetime.now()
        
        self.logger.info(f"🚀 Started workflow for task {task.task_id}")
        return True
    
    def stop_workflow(self) -> bool:
        """Stop the current workflow"""
        if self.workflow_state == WorkflowState.IDLE:
            return False
        
        self.workflow_state = WorkflowState.IDLE
        self.end_time = datetime.now()
        
        # Record execution history
        if self.start_time:
            duration = self.end_time - self.start_time
            self.execution_history.append({
                "task_id": self.current_task.task_id if self.current_task else None,
                "start_time": self.start_time.isoformat(),
                "end_time": self.end_time.isoformat(),
                "duration_minutes": duration.total_seconds() / 60,
                "completed_steps": self.current_step_index,
                "total_steps": len(self.workflow_steps)
            })
        
        self.logger.info(f"⏹️ Stopped workflow for task {self.current_task.task_id if self.current_task else 'None'}")
        return True
    
    def execute_next_step(self) -> bool:
        """Execute the next workflow step"""
        if self.workflow_state != WorkflowState.ACTIVE:
            return False
        
        if self.current_step_index >= len(self.workflow_steps):
            self.logger.info("✅ All workflow steps completed")
            self.stop_workflow()
            return True
        
        current_step = self.workflow_steps[self.current_step_index]
        self.logger.info(f"🔄 Executing step {current_step.name} ({current_step.step_id})")
        
        try:
            # Execute the step
            step_result = current_step.action()
            
            if step_result:
                self.logger.info(f"✅ Step {current_step.name} completed successfully")
                self.current_step_index += 1
                
                # Update task progress
                if self.current_task:
                    progress_percentage = (self.current_step_index / len(self.workflow_steps)) * 100
                    self.current_task.update_progress(progress_percentage)
                
                return True
            else:
                self.logger.error(f"❌ Step {current_step.name} failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error executing step {current_step.name}: {e}")
            return False
    
    def execute_all_steps(self) -> bool:
        """Execute all remaining workflow steps"""
        while self.workflow_state == WorkflowState.ACTIVE:
            if not self.execute_next_step():
                return False
        
        return True
    
    def get_current_step(self) -> Optional[WorkflowStep]:
        """Get the current workflow step"""
        if (self.workflow_state == WorkflowState.ACTIVE and 
            0 <= self.current_step_index < len(self.workflow_steps)):
            return self.workflow_steps[self.current_step_index]
        return None
    
    def get_workflow_progress(self) -> Dict[str, any]:
        """Get current workflow progress"""
        if not self.current_task:
            return {"status": "no_task", "progress": 0.0}
        
        total_steps = len(self.workflow_steps)
        completed_steps = self.current_step_index
        
        return {
            "status": self.workflow_state.value,
            "progress_percentage": (completed_steps / total_steps) * 100 if total_steps > 0 else 0,
            "current_step": completed_steps + 1,
            "total_steps": total_steps,
            "current_step_name": self.get_current_step().name if self.get_current_step() else None,
            "estimated_remaining_minutes": self._estimate_remaining_time()
        }
    
    def _estimate_remaining_time(self) -> float:
        """Estimate remaining time for workflow completion"""
        if self.workflow_state != WorkflowState.ACTIVE:
            return 0.0
        
        remaining_steps = self.workflow_steps[self.current_step_index:]
        total_minutes = sum(step.estimated_duration_minutes for step in remaining_steps)
        
        return total_minutes
    
    def _analyze_task(self) -> bool:
        """Analyze task requirements"""
        if not self.current_task:
            return False
        
        # Simulate task analysis
        time.sleep(0.1)  # Simulate work
        self.logger.debug(f"Analyzed task: {self.current_task.title}")
        return True
    
    def _implement_task(self) -> bool:
        """Implement the task"""
        if not self.current_task:
            return False
        
        # Simulate implementation
        time.sleep(0.1)  # Simulate work
        self.logger.debug(f"Implemented task: {self.current_task.title}")
        return True
    
    def _test_implementation(self) -> bool:
        """Test the implementation"""
        if not self.current_task:
            return False
        
        # Simulate testing
        time.sleep(0.1)  # Simulate work
        self.logger.debug(f"Tested implementation for: {self.current_task.title}")
        return True
    
    def _review_code(self) -> bool:
        """Review code quality"""
        if not self.current_task:
            return False
        
        # Simulate code review
        time.sleep(0.1)  # Simulate work
        self.logger.debug(f"Reviewed code for: {self.current_task.title}")
        return True
    
    def add_custom_step(self, step: WorkflowStep) -> bool:
        """Add a custom workflow step"""
        try:
            self.workflow_steps.append(step)
            self.logger.info(f"Added custom step: {step.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add custom step: {e}")
            return False
    
    def get_execution_history(self) -> List[Dict]:
        """Get workflow execution history"""
        return self.execution_history.copy()
    
    def get_workflow_statistics(self) -> Dict[str, any]:
        """Get workflow statistics"""
        total_executions = len(self.execution_history)
        
        if total_executions == 0:
            return {"total_executions": 0}
        
        # Calculate average execution time
        total_duration = sum(execution["duration_minutes"] for execution in self.execution_history)
        avg_duration = total_duration / total_executions
        
        # Calculate completion rate
        completed_executions = sum(1 for execution in self.execution_history 
                                 if execution["completed_steps"] == execution["total_steps"])
        completion_rate = (completed_executions / total_executions) * 100
        
        return {
            "total_executions": total_executions,
            "completed_executions": completed_executions,
            "completion_rate_percent": completion_rate,
            "average_duration_minutes": avg_duration,
            "total_duration_minutes": total_duration
        }
