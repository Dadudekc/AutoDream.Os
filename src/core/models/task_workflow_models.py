#!/usr/bin/env python3
"""
Task & Workflow Models Module - Agent Cellphone V2

Provides task management and workflow execution models
for the unified framework.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3J - Model & Enum Consolidation (V2 Compliance Refactoring)
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

try:
    from src.core.models.base_models import StatusModel, TypedModel
    from src.core.models.unified_enums import UnifiedStatus, UnifiedPriority, UnifiedType
except ImportError:
    from base_models import StatusModel, TypedModel
    from unified_enums import UnifiedStatus, UnifiedPriority, UnifiedType

logger = logging.getLogger(__name__)

# ============================================================================
# TASK & WORKFLOW MODELS - Domain-specific implementations
# ============================================================================

@dataclass
class TaskModel(StatusModel, TypedModel):
    """Task management model with assignment, due dates, and progress tracking"""
    
    title: str = ""
    description: str = ""
    assigned_to: str = ""
    priority: UnifiedPriority = UnifiedPriority.MEDIUM
    due_date: Optional[datetime] = None
    progress: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    subtasks: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization setup"""
        super().__post_init__()
        self.model_type = UnifiedType.TASK
        self.category = "task"
    
    def update_progress(self, new_progress: float, reason: str = None) -> None:
        """Update task progress"""
        old_progress = self.progress
        self.progress = max(0.0, min(100.0, new_progress))
        self.update_timestamp()
        
        # Update status based on progress
        if self.progress >= 100.0:
            self.update_status(UnifiedStatus.COMPLETED, f"Task completed: {reason}")
        elif self.progress > 0.0:
            self.update_status(UnifiedStatus.IN_PROGRESS, f"Progress: {self.progress}%")
        else:
            self.update_status(UnifiedStatus.PENDING, f"Task pending: {reason}")
        
        logger.info(f"Task progress updated: {old_progress}% → {self.progress}%")
    
    def add_dependency(self, task_id: str) -> None:
        """Add a task dependency"""
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
            self.update_timestamp()
    
    def add_subtask(self, subtask_id: str) -> None:
        """Add a subtask"""
        if subtask_id not in self.subtasks:
            self.subtasks.append(subtask_id)
            self.update_timestamp()
    
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if self.due_date and self.progress < 100.0:
            return datetime.now() > self.due_date
        return False
    
    def get_task_summary(self) -> Dict[str, Any]:
        """Get comprehensive task summary"""
        return {
            "title": self.title,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "priority": self.priority.value,
            "progress": self.progress,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "is_overdue": self.is_overdue(),
            "dependencies_count": len(self.dependencies),
            "subtasks_count": len(self.subtasks)
        }


@dataclass
class WorkflowModel(StatusModel, TypedModel):
    """Workflow execution model with steps, progress, and data management"""
    
    workflow_name: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    current_step: int = 0
    workflow_data: Dict[str, Any] = field(default_factory=dict)
    execution_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization setup"""
        super().__post_init__()
        self.model_type = UnifiedType.WORKFLOW
        self.category = "workflow"
    
    def add_step(self, step_name: str, step_type: str, **kwargs) -> int:
        """Add a workflow step"""
        step = {
            "id": len(self.steps),
            "name": step_name,
            "type": step_type,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            **kwargs
        }
        
        self.steps.append(step)
        self.update_timestamp()
        return step["id"]
    
    def execute_step(self, step_id: int, result: Any = None, error: str = None) -> bool:
        """Execute a workflow step"""
        if step_id >= len(self.steps):
            return False
        
        step = self.steps[step_id]
        step["status"] = "completed" if not error else "failed"
        step["result"] = result
        step["error"] = error
        step["executed_at"] = datetime.now().isoformat()
        
        # Record execution
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "step_id": step_id,
            "step_name": step["name"],
            "status": step["status"],
            "result": result,
            "error": error
        }
        self.execution_history.append(execution_record)
        
        # Update current step
        if step_id == self.current_step:
            self.current_step = min(self.current_step + 1, len(self.steps))
        
        self.update_timestamp()
        
        # Update workflow status
        if self.current_step >= len(self.steps):
            self.update_status(UnifiedStatus.COMPLETED, "All steps completed")
        else:
            self.update_status(UnifiedStatus.IN_PROGRESS, f"Step {self.current_step + 1}/{len(self.steps)}")
        
        return True
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get comprehensive workflow summary"""
        completed_steps = sum(1 for step in self.steps if step.get("status") == "completed")
        failed_steps = sum(1 for step in self.steps if step.get("status") == "failed")
        
        return {
            "workflow_name": self.workflow_name,
            "total_steps": len(self.steps),
            "current_step": self.current_step,
            "completed_steps": completed_steps,
            "failed_steps": failed_steps,
            "progress": (completed_steps / len(self.steps) * 100) if self.steps else 0.0,
            "executions_count": len(self.execution_history)
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_task_model(**kwargs) -> TaskModel:
    """Create a task model with specified parameters"""
    return TaskModel(**kwargs)


def create_workflow_model(**kwargs) -> WorkflowModel:
    """Create a workflow model with specified parameters"""
    return WorkflowModel(**kwargs)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for task & workflow models module"""
    print("🚀 TASK & WORKFLOW MODELS MODULE - TASK 3J V2 Refactoring")
    print("=" * 60)
    
    # Create example models
    task_model = create_task_model(title="Example Task", priority=UnifiedPriority.HIGH)
    workflow_model = create_workflow_model(workflow_name="Example Workflow")
    
    print(f"✅ Task Model Created: {task_model.id}")
    print(f"✅ Workflow Model Created: {workflow_model.id}")
    
    # Test functionality
    task_model.update_progress(50.0, "Halfway complete")
    workflow_model.add_step("Step 1", "validation")
    
    print(f"\n✅ Task Progress: {task_model.progress}%")
    print(f"✅ Workflow Steps: {len(workflow_model.steps)}")
    
    print("\n🎯 Task & Workflow Models Module Ready!")
    return 0


if __name__ == "__main__":
    exit(main())
