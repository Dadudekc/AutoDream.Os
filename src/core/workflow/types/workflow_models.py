#!/usr/bin/env python3
"""
Workflow Models - Unified Data Structures
========================================

Consolidated workflow data models from multiple implementations.
Follows V2 standards: ≤150 LOC, single responsibility.

Author: Agent-3 (Workflow Unification)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from .workflow_enums import WorkflowStatus, TaskStatus, WorkflowType, TaskPriority, AgentCapability


@dataclass
class WorkflowStep:
    """Unified workflow step definition - consolidated from multiple sources"""
    
    step_id: str
    name: str
    step_type: str
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    required_capabilities: List[AgentCapability] = field(default_factory=list)
    estimated_duration: float = 0.0
    timeout: float = 300.0
    retry_policy: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # V2 specific fields
    agent_target: str = ""
    prompt_template: str = ""
    expected_response_type: str = "text"
    completion_criteria: Dict[str, Any] = field(default_factory=dict)
    resource_requirements: Dict[str, Any] = field(default_factory=dict)
    
    # Execution tracking fields
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    assigned_agent: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
    def is_ready(self, completed_steps: Set[str]) -> bool:
        """Check if step dependencies are satisfied"""
        return all(dep in completed_steps for dep in self.dependencies)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert step to dictionary for serialization"""
        return {
            "step_id": self.step_id,
            "name": self.name,
            "step_type": self.step_type,
            "description": self.description,
            "dependencies": self.dependencies,
            "required_capabilities": [cap.value for cap in self.required_capabilities],
            "estimated_duration": self.estimated_duration,
            "timeout": self.timeout,
            "retry_policy": self.retry_policy,
            "metadata": self.metadata,
            "agent_target": self.agent_target,
            "prompt_template": self.prompt_template,
            "expected_response_type": self.expected_response_type,
            "completion_criteria": self.completion_criteria,
            "resource_requirements": self.resource_requirements,
            "status": self.status.value if self.status else None,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "assigned_agent": self.assigned_agent,
            "result": self.result,
            "error_message": self.error_message
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowStep':
        """Create step from dictionary"""
        # Convert capability strings back to enums
        if 'required_capabilities' in data:
            data['required_capabilities'] = [
                AgentCapability(cap) if isinstance(cap, str) else cap 
                for cap in data['required_capabilities']
            ]
        
        # Convert status string back to enum
        if 'status' in data and data['status']:
            data['status'] = TaskStatus(data['status'])
        
        return cls(**data)


@dataclass
class WorkflowTask:
    """Unified workflow task - consolidated from multiple sources"""
    
    task_id: str
    name: str
    description: str
    task_type: str = "general"  # Type of task (computation, data_processing, decision, integration)
    agent_id: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    estimated_duration: int = 60  # seconds
    actual_duration: Optional[int] = None
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    required_resources: List[str] = field(default_factory=list)
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # V2 specific fields
    workflow_id: Optional[str] = None
    step_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    child_tasks: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    resource_requirements: List[Any] = field(default_factory=list)
    
    def is_completed(self) -> bool:
        """Check if task is completed"""
        return self.status == TaskStatus.COMPLETED
    
    def is_failed(self) -> bool:
        """Check if task has failed"""
        return self.status == TaskStatus.FAILED
    
    def can_retry(self) -> bool:
        """Check if task can be retried"""
        return self.retry_count < self.max_retries and self.status in [
            TaskStatus.FAILED, TaskStatus.TIMEOUT
        ]
    
    def get_duration(self) -> Optional[int]:
        """Get actual or estimated duration"""
        if self.actual_duration is not None:
            return self.actual_duration
        return self.estimated_duration


@dataclass
class WorkflowExecution:
    """Unified workflow execution instance - consolidated from multiple sources"""
    
    execution_id: str
    workflow_id: str
    workflow_name: str
    status: WorkflowStatus = WorkflowStatus.CREATED
    tasks: List[WorkflowTask] = field(default_factory=list)
    steps: List[WorkflowStep] = field(default_factory=list)
    current_task_index: int = 0
    completed_tasks: List[str] = field(default_factory=list)
    failed_tasks: List[str] = field(default_factory=list)
    execution_path: List[str] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_duration: Optional[int] = None
    error_count: int = 0
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # V2 specific fields
    agent_id: Optional[str] = None
    step_results: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    optimization_history: List[Dict[str, Any]] = field(default_factory=list)
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    
    def get_progress(self) -> float:
        """Calculate workflow progress percentage"""
        if not self.tasks:
            return 0.0
        completed = len(self.completed_tasks)
        total = len(self.tasks)
        return (completed / total) * 100.0 if total > 0 else 0.0
    
    def get_active_tasks(self) -> List[WorkflowTask]:
        """Get currently active tasks"""
        return [task for task in self.tasks if TaskStatus.is_active(task.status)]
    
    def get_failed_tasks(self) -> List[WorkflowTask]:
        """Get failed tasks"""
        return [task for task in self.tasks if task.is_failed()]
    
    def is_completed(self) -> bool:
        """Check if workflow is completed"""
        return self.status == WorkflowStatus.COMPLETED
    
    def is_failed(self) -> bool:
        """Check if workflow has failed"""
        return self.status == WorkflowStatus.FAILED


@dataclass
class WorkflowDefinition:
    """Unified workflow definition - consolidated from multiple sources"""
    
    workflow_id: str
    workflow_type: WorkflowType
    name: str
    description: str
    version: str = "1.0.0"
    steps: List[WorkflowStep] = field(default_factory=list)
    required_agents: List[str] = field(default_factory=list)
    estimated_duration: int = 3600  # seconds
    priority: TaskPriority = TaskPriority.MEDIUM
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # V2 specific fields
    optimization_enabled: bool = True
    scalability_target: Optional[str] = None
    validation_rules: List[str] = field(default_factory=list)
    resource_constraints: Dict[str, Any] = field(default_factory=dict)
    retry_policies: Dict[str, Any] = field(default_factory=dict)
    
    def get_step_by_id(self, step_id: str) -> Optional[WorkflowStep]:
        """Get workflow step by ID"""
        for step in self.steps:
            if step.step_id == step_id:
                return step
        return None
    
    def validate_structure(self) -> List[str]:
        """Validate workflow structure and return errors"""
        errors = []
        
        # Check for circular dependencies
        for step in self.steps:
            if step.step_id in step.dependencies:
                errors.append(f"Circular dependency detected in step {step.step_id}")
        
        # Check for missing dependencies
        step_ids = {step.step_id for step in self.steps}
        for step in self.steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    errors.append(f"Missing dependency {dep} for step {step.step_id}")
        
        return errors


@dataclass
class WorkflowCondition:
    """Unified workflow condition - consolidated from multiple sources"""
    
    condition_id: str
    name: str
    condition_type: str  # "if", "while", "for", "switch"
    condition_expression: str
    true_branch: List[str]  # Task IDs to execute if true
    false_branch: List[str] = field(default_factory=list)
    loop_condition: Optional[str] = None  # For loop workflows
    max_iterations: int = 100  # Prevent infinite loops
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # V2 specific fields
    evaluation_context: Dict[str, Any] = field(default_factory=dict)
    timeout: float = 30.0  # seconds
    retry_on_failure: bool = False
    fallback_actions: List[str] = field(default_factory=list)
    
    def is_loop_condition(self) -> bool:
        """Check if this is a loop condition"""
        return self.condition_type in ["while", "for"]
    
    def get_branch_tasks(self, condition_result: bool) -> List[str]:
        """Get tasks to execute based on condition result"""
        return self.true_branch if condition_result else self.false_branch


@dataclass
class AgentCapabilityInfo:
    """Agent capability information - consolidated from multiple sources"""
    
    agent_id: str
    capabilities: List[AgentCapability] = field(default_factory=list)
    current_load: int = 0
    max_concurrent_tasks: int = 5
    performance_score: float = 1.0
    availability: bool = True
    last_heartbeat: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # V2 specific fields
    workflow_specializations: List[str] = field(default_factory=list)
    resource_limits: Dict[str, Any] = field(default_factory=dict)
    performance_history: List[Dict[str, float]] = field(default_factory=list)
    error_rate: float = 0.0
    success_rate: float = 1.0
    
    def can_handle_workflow(self, workflow_type: WorkflowType) -> bool:
        """Check if agent can handle specific workflow type"""
        return workflow_type.value in self.workflow_specializations
    
    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has specific capability"""
        return capability in self.capabilities
    
    def is_available(self) -> bool:
        """Check if agent is available for new tasks"""
        return self.availability and self.current_load < self.max_concurrent_tasks
    
    def get_utilization_percentage(self) -> float:
        """Get current utilization percentage"""
        return (self.current_load / self.max_concurrent_tasks) * 100.0 if self.max_concurrent_tasks > 0 else 0.0


@dataclass
class ResourceRequirement:
    """Resource requirement definition - consolidated from multiple sources"""
    
    resource_id: str
    resource_type: str  # "cpu", "memory", "storage", "network", "custom"
    required_amount: float
    unit: str
    priority: TaskPriority = TaskPriority.MEDIUM
    current_availability: float = 0.0
    expected_duration: Optional[float] = None  # Expected duration in seconds
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # V2 specific fields
    resource_pool: Optional[str] = None
    allocation_strategy: str = "first_available"  # "first_available", "round_robin", "least_used"
    reservation_timeout: float = 300.0  # seconds
    fallback_resources: List[str] = field(default_factory=list)
    
    def is_satisfied(self) -> bool:
        """Check if resource requirement is satisfied"""
        return self.current_availability >= self.required_amount
    
    def get_shortage(self) -> float:
        """Get resource shortage amount"""
        return max(0, self.required_amount - self.current_availability)
    
    def get_utilization_percentage(self) -> float:
        """Get resource utilization percentage"""
        return (self.current_availability / self.required_amount) * 100.0 if self.required_amount > 0 else 0.0
