#!/usr/bin/env python3
"""
Agent Workflow Core Components
==============================

Core components for agent workflow automation and management.
V2 Compliance: ≤400 lines, focused functionality.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class WorkflowStep:
    """Represents a single step in a workflow."""
    
    step_id: str
    agent_id: str
    task: str
    dependencies: List[str] = None
    timeout_minutes: int = 30
    status: str = "pending"  # pending, in_progress, completed, failed, timeout
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert step to dictionary for serialization."""
        return {
            "step_id": self.step_id,
            "agent_id": self.agent_id,
            "task": self.task,
            "dependencies": self.dependencies,
            "timeout_minutes": self.timeout_minutes,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowStep':
        """Create step from dictionary."""
        step = cls(
            step_id=data["step_id"],
            agent_id=data["agent_id"],
            task=data["task"],
            dependencies=data.get("dependencies", []),
            timeout_minutes=data.get("timeout_minutes", 30)
        )
        step.status = data.get("status", "pending")
        step.result = data.get("result")
        step.error = data.get("error")
        
        if data.get("started_at"):
            step.started_at = datetime.fromisoformat(data["started_at"])
        if data.get("completed_at"):
            step.completed_at = datetime.fromisoformat(data["completed_at"])
            
        return step


@dataclass
class WorkflowDefinition:
    """Represents a complete workflow definition."""
    
    workflow_id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    created_at: datetime = None
    status: str = "pending"  # pending, running, completed, failed, cancelled
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary for serialization."""
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
            "created_at": self.created_at.isoformat(),
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowDefinition':
        """Create workflow from dictionary."""
        workflow = cls(
            workflow_id=data["workflow_id"],
            name=data["name"],
            description=data["description"],
            steps=[WorkflowStep.from_dict(step_data) for step_data in data["steps"]]
        )
        workflow.status = data.get("status", "pending")
        workflow.created_at = datetime.fromisoformat(data["created_at"])
        return workflow


class WorkflowValidator:
    """Validates workflow definitions and dependencies."""
    
    @staticmethod
    def validate_workflow(workflow: WorkflowDefinition) -> List[str]:
        """Validate a workflow definition and return list of errors."""
        errors = []
        
        # Check for duplicate step IDs
        step_ids = [step.step_id for step in workflow.steps]
        if len(step_ids) != len(set(step_ids)):
            errors.append("Duplicate step IDs found")
        
        # Check dependencies
        for step in workflow.steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    errors.append(f"Step {step.step_id} depends on non-existent step {dep}")
        
        # Check for circular dependencies
        if WorkflowValidator._has_circular_dependencies(workflow.steps):
            errors.append("Circular dependencies detected")
        
        return errors
    
    @staticmethod
    def _has_circular_dependencies(steps: List[WorkflowStep]) -> bool:
        """Check for circular dependencies using DFS."""
        visited = set()
        rec_stack = set()
        
        def has_cycle(step_id: str) -> bool:
            visited.add(step_id)
            rec_stack.add(step_id)
            
            step = next((s for s in steps if s.step_id == step_id), None)
            if step:
                for dep in step.dependencies:
                    if dep not in visited:
                        if has_cycle(dep):
                            return True
                    elif dep in rec_stack:
                        return True
            
            rec_stack.remove(step_id)
            return False
        
        for step in steps:
            if step.step_id not in visited:
                if has_cycle(step.step_id):
                    return True
        
        return False


class WorkflowScheduler:
    """Schedules workflow steps based on dependencies."""
    
    @staticmethod
    def get_execution_order(steps: List[WorkflowStep]) -> List[str]:
        """Get the order in which steps should be executed (topological sort)."""
        # Build dependency graph
        graph = {}
        in_degree = {}
        
        for step in steps:
            graph[step.step_id] = []
            in_degree[step.step_id] = 0
        
        for step in steps:
            for dep in step.dependencies:
                graph[dep].append(step.step_id)
                in_degree[step.step_id] += 1
        
        # Topological sort using Kahn's algorithm
        queue = [step_id for step_id, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            current = queue.pop(0)
            result.append(current)
            
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result


class WorkflowStatusTracker:
    """Tracks the status of workflow execution."""
    
    def __init__(self):
        self.active_workflows: Dict[str, WorkflowDefinition] = {}
        self.completed_workflows: Dict[str, WorkflowDefinition] = {}
    
    def start_workflow(self, workflow: WorkflowDefinition) -> bool:
        """Start tracking a workflow."""
        if workflow.workflow_id in self.active_workflows:
            logger.warning(f"Workflow {workflow.workflow_id} is already active")
            return False
        
        workflow.status = "running"
        self.active_workflows[workflow.workflow_id] = workflow
        logger.info(f"Started tracking workflow: {workflow.name}")
        return True
    
    def complete_workflow(self, workflow_id: str, success: bool = True) -> bool:
        """Mark a workflow as completed."""
        if workflow_id not in self.active_workflows:
            logger.warning(f"Workflow {workflow_id} is not active")
            return False
        
        workflow = self.active_workflows.pop(workflow_id)
        workflow.status = "completed" if success else "failed"
        self.completed_workflows[workflow_id] = workflow
        
        logger.info(f"Completed workflow: {workflow.name} (success: {success})")
        return True
    
    def get_workflow_status(self, workflow_id: str) -> Optional[str]:
        """Get the status of a workflow."""
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id].status
        elif workflow_id in self.completed_workflows:
            return self.completed_workflows[workflow_id].status
        return None
    
    def get_all_workflows(self) -> Dict[str, WorkflowDefinition]:
        """Get all workflows (active and completed)."""
        all_workflows = {}
        all_workflows.update(self.active_workflows)
        all_workflows.update(self.completed_workflows)
        return all_workflows




