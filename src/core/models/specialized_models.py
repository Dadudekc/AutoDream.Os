#!/usr/bin/env python3
"""
Specialized Models Module - Agent Cellphone V2

Provides specialized model types for health, performance, task,
workflow, and message management in the unified framework.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3J - Model & Enum Consolidation (V2 Compliance Refactoring)
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import uuid

try:
    from src.core.models.base_models import StatusModel, TypedModel, ConfigurableModel
    from src.core.models.unified_enums import UnifiedStatus, UnifiedPriority, UnifiedSeverity, UnifiedType
except ImportError:
    from base_models import StatusModel, TypedModel, ConfigurableModel
    from unified_enums import UnifiedStatus, UnifiedPriority, UnifiedSeverity, UnifiedType

logger = logging.getLogger(__name__)

# ============================================================================
# SPECIALIZED MODEL TYPES - Domain-specific model implementations
# ============================================================================

@dataclass
class HealthModel(StatusModel, TypedModel):
    """Health monitoring model with score, metrics, and threshold checking"""
    
    health_score: float = 100.0
    metrics: Dict[str, float] = field(default_factory=dict)
    thresholds: Dict[str, Dict[str, float]] = field(default_factory=dict)
    last_check: datetime = field(default_factory=datetime.now)
    check_interval: int = 300  # seconds
    
    def __post_init__(self):
        """Post-initialization setup"""
        super().__post_init__()
        self.model_type = UnifiedType.SYSTEM
        self.category = "health"
        
        # Set default thresholds
        if not self.thresholds:
            self.thresholds = {
                "cpu_usage": {"warning": 80.0, "critical": 95.0},
                "memory_usage": {"warning": 85.0, "critical": 95.0},
                "disk_usage": {"warning": 90.0, "critical": 95.0}
            }
    
    def update_health_score(self, new_score: float) -> None:
        """Update health score and status"""
        old_score = self.health_score
        self.health_score = max(0.0, min(100.0, new_score))
        self.last_check = datetime.now()
        self.update_timestamp()
        
        # Update status based on health score
        if self.health_score >= 90.0:
            self.update_status(UnifiedStatus.HEALTHY, f"Health score: {self.health_score}")
        elif self.health_score >= 70.0:
            self.update_status(UnifiedStatus.WARNING, f"Health score: {self.health_score}")
        else:
            self.update_status(UnifiedStatus.CRITICAL, f"Health score: {self.health_score}")
        
        logger.info(f"Health score updated: {old_score} → {self.health_score}")
    
    def add_metric(self, name: str, value: float) -> None:
        """Add or update a health metric"""
        self.metrics[name] = value
        self.update_timestamp()
    
    def check_thresholds(self) -> Dict[str, str]:
        """Check all metrics against thresholds"""
        violations = {}
        
        for metric_name, metric_value in self.metrics.items():
            if metric_name in self.thresholds:
                thresholds = self.thresholds[metric_name]
                
                if metric_value >= thresholds.get("critical", float('inf')):
                    violations[metric_name] = "CRITICAL"
                elif metric_value >= thresholds.get("warning", float('inf')):
                    violations[metric_name] = "WARNING"
        
        return violations
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        threshold_violations = self.check_thresholds()
        
        return {
            "health_score": self.health_score,
            "status": self.status.value,
            "metrics_count": len(self.metrics),
            "threshold_violations": threshold_violations,
            "last_check": self.last_check.isoformat(),
            "check_interval": self.check_interval
        }


@dataclass
class PerformanceModel(StatusModel, TypedModel):
    """Performance tracking model with benchmarks and optimization targets"""
    
    performance_score: float = 0.0
    benchmarks: Dict[str, float] = field(default_factory=dict)
    targets: Dict[str, float] = field(default_factory=dict)
    optimization_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization setup"""
        super().__post_init__()
        self.model_type = UnifiedType.SYSTEM
        self.category = "performance"
    
    def add_benchmark(self, name: str, value: float) -> None:
        """Add or update a performance benchmark"""
        self.benchmarks[name] = value
        self.update_timestamp()
        
        # Recalculate performance score
        self._calculate_performance_score()
    
    def set_target(self, name: str, target_value: float) -> None:
        """Set performance target for a benchmark"""
        self.targets[name] = target_value
        self.update_timestamp()
    
    def _calculate_performance_score(self) -> None:
        """Calculate overall performance score based on benchmarks vs targets"""
        if not self.benchmarks or not self.targets:
            return
        
        total_score = 0.0
        valid_metrics = 0
        
        for benchmark_name, benchmark_value in self.benchmarks.items():
            if benchmark_name in self.targets:
                target_value = self.targets[benchmark_name]
                if target_value > 0:
                    # Calculate percentage of target achieved
                    percentage = min(100.0, (benchmark_value / target_value) * 100)
                    total_score += percentage
                    valid_metrics += 1
        
        if valid_metrics > 0:
            self.performance_score = total_score / valid_metrics
            self.update_timestamp()
    
    def record_optimization(self, benchmark_name: str, old_value: float, new_value: float, 
                          improvement: float, method: str) -> None:
        """Record an optimization attempt"""
        optimization_record = {
            "timestamp": datetime.now().isoformat(),
            "benchmark": benchmark_name,
            "old_value": old_value,
            "new_value": new_value,
            "improvement": improvement,
            "method": method
        }
        
        self.optimization_history.append(optimization_record)
        self.update_timestamp()
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        return {
            "performance_score": self.performance_score,
            "benchmarks_count": len(self.benchmarks),
            "targets_count": len(self.targets),
            "optimizations_count": len(self.optimization_history),
            "recent_optimizations": self.optimization_history[-5:] if self.optimization_history else []
        }


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


@dataclass
class MessageModel(StatusModel, TypedModel):
    """Communication model with sender, recipient, content, and status tracking"""
    
    sender: str = ""
    recipient: str = ""
    subject: str = ""
    content: str = ""
    message_type: str = "text"
    priority: UnifiedPriority = UnifiedPriority.MEDIUM
    delivery_status: str = "pending"
    read_status: bool = False
    attachments: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization setup"""
        super().__post_init__()
        self.model_type = UnifiedType.MESSAGE
        self.category = "communication"
    
    def mark_as_read(self) -> None:
        """Mark message as read"""
        if not self.read_status:
            self.read_status = True
            self.update_timestamp()
            self.update_status(UnifiedStatus.COMPLETED, "Message read")
    
    def update_delivery_status(self, status: str, details: str = None) -> None:
        """Update message delivery status"""
        self.delivery_status = status
        self.update_timestamp()
        
        # Update overall status based on delivery
        if status == "delivered":
            self.update_status(UnifiedStatus.COMPLETED, "Message delivered")
        elif status == "failed":
            self.update_status(UnifiedStatus.FAILED, f"Delivery failed: {details}")
        elif status == "pending":
            self.update_status(UnifiedStatus.PENDING, "Delivery pending")
    
    def add_attachment(self, attachment_id: str) -> None:
        """Add an attachment to the message"""
        if attachment_id not in self.attachments:
            self.attachments.append(attachment_id)
            self.update_timestamp()
    
    def get_message_summary(self) -> Dict[str, Any]:
        """Get comprehensive message summary"""
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "subject": self.subject,
            "message_type": self.message_type,
            "priority": self.priority.value,
            "delivery_status": self.delivery_status,
            "read_status": self.read_status,
            "attachments_count": len(self.attachments),
            "content_length": len(self.content)
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_health_model(**kwargs) -> HealthModel:
    """Create a health model with specified parameters"""
    return HealthModel(**kwargs)


def create_performance_model(**kwargs) -> PerformanceModel:
    """Create a performance model with specified parameters"""
    return PerformanceModel(**kwargs)


def create_task_model(**kwargs) -> TaskModel:
    """Create a task model with specified parameters"""
    return TaskModel(**kwargs)


def create_workflow_model(**kwargs) -> WorkflowModel:
    """Create a workflow model with specified parameters"""
    return WorkflowModel(**kwargs)


def create_message_model(**kwargs) -> MessageModel:
    """Create a message model with specified parameters"""
    return MessageModel(**kwargs)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for specialized models module"""
    print("🚀 SPECIALIZED MODELS MODULE - TASK 3J V2 Refactoring")
    print("=" * 50)
    
    # Create example models
    health_model = create_health_model(health_score=95.0)
    performance_model = create_performance_model()
    task_model = create_task_model(title="Example Task", priority=UnifiedPriority.HIGH)
    workflow_model = create_workflow_model(workflow_name="Example Workflow")
    message_model = create_message_model(subject="Test Message", sender="Agent-3")
    
    print(f"✅ Health Model Created: {health_model.id}")
    print(f"✅ Performance Model Created: {performance_model.id}")
    print(f"✅ Task Model Created: {task_model.id}")
    print(f"✅ Workflow Model Created: {workflow_model.id}")
    print(f"✅ Message Model Created: {message_model.id}")
    
    # Test functionality
    health_model.update_health_score(85.0)
    performance_model.add_benchmark("response_time", 150.0)
    task_model.update_progress(50.0, "Halfway complete")
    workflow_model.add_step("Step 1", "validation")
    message_model.mark_as_read()
    
    print(f"\n✅ Health Score: {health_model.health_score}")
    print(f"✅ Performance Benchmarks: {len(performance_model.benchmarks)}")
    print(f"✅ Task Progress: {task_model.progress}%")
    print(f"✅ Workflow Steps: {len(workflow_model.steps)}")
    print(f"✅ Message Read: {message_model.read_status}")
    
    print("\n🎯 Specialized Models Module Ready!")
    return 0


if __name__ == "__main__":
    exit(main())
