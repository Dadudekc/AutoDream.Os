#!/usr/bin/env python3
"""
Consolidated AI/ML Models - Agent Cellphone V2
==============================================

Unified data structures for AI/ML operations. Consolidates all AI/ML
data models into a single, maintainable location.

Author: Agent-5 (REFACTORING MANAGER)
License: MIT
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import json


class ModelType(Enum):
    """AI model types"""
    LLM = "llm"
    EMBEDDING = "embedding"
    VISION = "vision"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"
    CODE = "code"
    REASONING = "reasoning"


class Provider(Enum):
    """AI service providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta"
    LOCAL = "local"
    CUSTOM = "custom"


class AgentType(Enum):
    """AI agent types"""
    COORDINATOR = "coordinator"
    LEARNER = "learner"
    OPTIMIZER = "optimizer"
    PERFORMANCE_TUNER = "performance_tuner"
    KNOWLEDGE_MANAGER = "knowledge_manager"
    TASK_EXECUTOR = "task_executor"
    WORKFLOW_MANAGER = "workflow_manager"


class WorkflowType(Enum):
    """Workflow types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"
    OPTIMIZATION = "optimization"
    MAINTENANCE = "maintenance"


class TaskStatus(Enum):
    """Task status values"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


@dataclass
class ModelCapability:
    """AI model capability"""
    name: str
    description: str
    version: str
    is_supported: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelMetrics:
    """AI model performance metrics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    last_request: Optional[datetime] = None
    error_rate: float = 0.0
    throughput: float = 0.0  # requests per second


@dataclass
class AIModel:
    """Unified AI model representation"""
    model_id: str
    name: str
    model_type: ModelType
    provider: Provider
    version: str
    capabilities: List[ModelCapability]
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    usage_count: int = 0
    metrics: ModelMetrics = field(default_factory=ModelMetrics)
    
    # Configuration
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    
    # Resource requirements
    memory_requirement: Optional[str] = None
    gpu_requirement: Optional[str] = None
    storage_requirement: Optional[str] = None
    
    def __post_init__(self):
        """Post-initialization setup"""
        if isinstance(self.model_type, str):
            self.model_type = ModelType(self.model_type)
        if isinstance(self.provider, str):
            self.provider = Provider(self.provider)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def update_metrics(self, success: bool, response_time: float):
        """Update model metrics"""
        self.metrics.total_requests += 1
        if success:
            self.metrics.successful_requests += 1
        else:
            self.metrics.failed_requests += 1
        
        # Update average response time
        if self.metrics.total_requests == 1:
            self.metrics.average_response_time = response_time
        else:
            self.metrics.average_response_time = (
                (self.metrics.average_response_time * (self.metrics.total_requests - 1) + response_time) /
                self.metrics.total_requests
            )
        
        # Update error rate
        self.metrics.error_rate = self.metrics.failed_requests / self.metrics.total_requests
        
        # Update last request time
        self.metrics.last_request = datetime.now()
        
        # Update usage count
        self.usage_count += 1
        self.last_used = datetime.now()


@dataclass
class AgentSkill:
    """AI agent skill"""
    name: str
    level: int = 0  # 0-100 scale
    description: str = ""
    last_updated: datetime = field(default_factory=datetime.now)
    usage_count: int = 0
    success_rate: float = 0.0
    
    def adjust_level(self, delta: int) -> int:
        """Adjust skill level by delta clamped to 0-100"""
        self.level = max(0, min(100, self.level + delta))
        self.last_updated = datetime.now()
        return self.level


@dataclass
class AgentPerformance:
    """AI agent performance metrics"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    average_task_time: float = 0.0
    last_task: Optional[datetime] = None
    success_rate: float = 0.0
    efficiency_score: float = 0.0  # 0-100 scale
    
    def update_metrics(self, task_success: bool, task_time: float):
        """Update agent performance metrics"""
        self.total_tasks += 1
        if task_success:
            self.completed_tasks += 1
        else:
            self.failed_tasks += 1
        
        # Update average task time
        if self.total_tasks == 1:
            self.average_task_time = task_time
        else:
            self.average_task_time = (
                (self.average_task_time * (self.total_tasks - 1) + task_time) /
                self.total_tasks
            )
        
        # Update success rate
        self.success_rate = self.completed_tasks / self.total_tasks
        
        # Update efficiency score (based on success rate and task time)
        self.efficiency_score = min(100, self.success_rate * 100 - (self.average_task_time / 10))
        
        # Update last task time
        self.last_task = datetime.now()


@dataclass
class AIAgent:
    """Unified AI agent representation"""
    agent_id: str
    name: str
    agent_type: AgentType
    skills: List[AgentSkill]
    workload_capacity: int
    current_workload: int = 0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: Optional[datetime] = None
    performance: AgentPerformance = field(default_factory=AgentPerformance)
    
    # Configuration
    max_concurrent_tasks: int = 1
    task_timeout: Optional[float] = None
    retry_policy: Dict[str, Any] = field(default_factory=dict)
    
    # Resource requirements
    memory_requirement: Optional[str] = None
    cpu_requirement: Optional[str] = None
    network_requirement: Optional[str] = None
    
    def __post_init__(self):
        """Post-initialization setup"""
        if isinstance(self.agent_type, str):
            self.agent_type = AgentType(self.agent_type)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def can_accept_task(self, task_complexity: int) -> bool:
        """Check if agent can accept a task"""
        return (self.is_active and 
                self.current_workload + task_complexity <= self.workload_capacity and
                self.current_workload < self.max_concurrent_tasks)
    
    def assign_task(self, task_complexity: int) -> bool:
        """Assign a task to this agent"""
        if self.can_accept_task(task_complexity):
            self.current_workload += task_complexity
            self.last_activity = datetime.now()
            return True
        return False
    
    def complete_task(self, task_complexity: int, success: bool, task_time: float):
        """Complete a task"""
        self.current_workload = max(0, self.current_workload - task_complexity)
        self.last_activity = datetime.now()
        self.performance.update_metrics(success, task_time)


@dataclass
class APIKeyPermissions:
    """API key permissions"""
    read: bool = True
    write: bool = True
    delete: bool = False
    admin: bool = False
    custom_permissions: List[str] = field(default_factory=list)


@dataclass
class APIKeyUsage:
    """API key usage tracking"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    last_request: Optional[datetime] = None
    rate_limit_remaining: Optional[int] = None
    rate_limit_reset: Optional[datetime] = None
    
    def update_usage(self, success: bool):
        """Update API key usage"""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        self.last_request = datetime.now()


@dataclass
class APIKey:
    """Unified API key representation"""
    key_id: str
    service: str
    description: str
    key_hash: str
    permissions: APIKeyPermissions
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool = True
    usage_count: int = 0
    last_used: Optional[datetime] = None
    usage: APIKeyUsage = field(default_factory=APIKeyUsage)
    
    # Security
    ip_whitelist: Optional[List[str]] = None
    user_agent_whitelist: Optional[List[str]] = None
    rate_limit: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def is_valid(self) -> bool:
        """Check if API key is valid"""
        if not self.is_active:
            return False
        
        if self.expires_at and self.expires_at < datetime.now():
            return False
        
        return True
    
    def update_usage(self, success: bool):
        """Update API key usage"""
        self.usage_count += 1
        self.last_used = datetime.now()
        self.usage.update_usage(success)


@dataclass
class WorkflowStep:
    """Workflow step definition"""
    step_id: str
    name: str
    description: str
    order: int
    step_type: str  # 'action', 'decision', 'wait', 'parallel'
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    timeout: Optional[float] = None
    retry_policy: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExecution:
    """Workflow execution instance"""
    execution_id: str
    workflow_id: str
    status: str = "pending"  # pending, running, completed, failed, cancelled
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    current_step: Optional[str] = None
    step_results: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time: Optional[float] = None


@dataclass
class Workflow:
    """Unified workflow representation"""
    workflow_id: str
    name: str
    description: str
    workflow_type: WorkflowType
    steps: List[WorkflowStep]
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_executed: Optional[datetime] = None
    execution_count: int = 0
    
    # Configuration
    max_execution_time: Optional[float] = None
    max_retries: int = 3
    parallel_execution: bool = False
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    author: Optional[str] = None
    
    def __post_init__(self):
        """Post-initialization setup"""
        if isinstance(self.workflow_type, str):
            self.workflow_type = WorkflowType(self.workflow_type)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def get_step_by_id(self, step_id: str) -> Optional[WorkflowStep]:
        """Get workflow step by ID"""
        for step in self.steps:
            if step.step_id == step_id:
                return step
        return None
    
    def get_next_steps(self, current_step_id: str) -> List[WorkflowStep]:
        """Get next steps after current step"""
        current_step = self.get_step_by_id(current_step_id)
        if not current_step:
            return []
        
        # Find steps that depend on current step
        next_steps = []
        for step in self.steps:
            if current_step_id in step.dependencies:
                next_steps.append(step)
        
        return next_steps


@dataclass
class OrchestrationTask:
    """AI/ML orchestration task"""
    task_id: str
    task_type: str  # 'model_management', 'agent_coordination', 'workflow_execution'
    priority: TaskPriority
    data: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    result: Optional[Any] = None
    
    # Task metadata
    timeout: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    
    def __post_init__(self):
        """Post-initialization setup"""
        if isinstance(self.priority, int):
            self.priority = TaskPriority(self.priority)
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def can_retry(self) -> bool:
        """Check if task can be retried"""
        return self.retry_count < self.max_retries and self.status in [TaskStatus.FAILED, TaskStatus.CANCELLED]
    
    def mark_for_retry(self) -> bool:
        """Mark task for retry"""
        if self.can_retry():
            self.retry_count += 1
            self.status = TaskStatus.PENDING
            self.assigned_agent = None
            self.result = None
            self.error_message = None
            return True
        return False


@dataclass
class SystemHealth:
    """AI/ML system health status"""
    overall_health: str  # healthy, warning, critical, error
    models_health: str
    agents_health: str
    api_keys_health: str
    workflows_health: str
    last_check: datetime = field(default_factory=datetime.now)
    issues: List[str] = field(default_factory=list)
    
    # Health scores (0-100)
    models_score: float = 0.0
    agents_score: float = 0.0
    api_keys_score: float = 0.0
    workflows_score: float = 0.0
    overall_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def calculate_overall_score(self):
        """Calculate overall health score"""
        scores = [self.models_score, self.agents_score, self.api_keys_score, self.workflows_score]
        valid_scores = [s for s in scores if s > 0]
        
        if valid_scores:
            self.overall_score = sum(valid_scores) / len(valid_scores)
        else:
            self.overall_score = 0.0
        
        # Update overall health based on score
        if self.overall_score >= 80:
            self.overall_health = "healthy"
        elif self.overall_score >= 60:
            self.overall_health = "warning"
        elif self.overall_score >= 40:
            self.overall_health = "critical"
        else:
            self.overall_health = "error"


@dataclass
class PerformanceMetrics:
    """Performance metrics for AI/ML system"""
    task_processing: Dict[str, Any] = field(default_factory=lambda: {
        "total": 0,
        "successful": 0,
        "failed": 0,
        "avg_time": 0.0,
        "throughput": 0.0
    })
    
    system_health: Dict[str, Any] = field(default_factory=lambda: {
        "checks": 0,
        "issues_found": 0,
        "last_optimization": None,
        "optimization_count": 0
    })
    
    resource_utilization: Dict[str, Any] = field(default_factory=lambda: {
        "models": 0.0,
        "agents": 0.0,
        "workflows": 0.0,
        "api_keys": 0.0
    })
    
    response_times: Dict[str, Any] = field(default_factory=lambda: {
        "p50": 0.0,
        "p90": 0.0,
        "p95": 0.0,
        "p99": 0.0
    })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def update_task_metrics(self, success: bool, processing_time: float):
        """Update task processing metrics"""
        self.task_processing["total"] += 1
        if success:
            self.task_processing["successful"] += 1
        else:
            self.task_processing["failed"] += 1
        
        # Update average processing time
        total = self.task_processing["total"]
        current_avg = self.task_processing["avg_time"]
        self.task_processing["avg_time"] = (current_avg * (total - 1) + processing_time) / total
        
        # Update throughput (tasks per second)
        # This would need to be calculated over a time window
        self.task_processing["throughput"] = self.task_processing["total"] / 3600  # per hour for now


# Utility functions for model operations
def create_model_from_dict(data: Dict[str, Any]) -> AIModel:
    """Create AIModel from dictionary"""
    return AIModel(**data)


def create_agent_from_dict(data: Dict[str, Any]) -> AIAgent:
    """Create AIAgent from dictionary"""
    return AIAgent(**data)


def create_workflow_from_dict(data: Dict[str, Any]) -> Workflow:
    """Create Workflow from dictionary"""
    return Workflow(**data)


def create_api_key_from_dict(data: Dict[str, Any]) -> APIKey:
    """Create APIKey from dictionary"""
    return APIKey(**data)


def validate_model_data(data: Dict[str, Any]) -> bool:
    """Validate model data"""
    required_fields = ["model_id", "name", "model_type", "provider", "version", "capabilities"]
    return all(field in data for field in required_fields)


def validate_agent_data(data: Dict[str, Any]) -> bool:
    """Validate agent data"""
    required_fields = ["agent_id", "name", "agent_type", "skills", "workload_capacity"]
    return all(field in data for field in required_fields)


def validate_workflow_data(data: Dict[str, Any]) -> bool:
    """Validate workflow data"""
    required_fields = ["workflow_id", "name", "description", "workflow_type", "steps"]
    return all(field in data for field in required_fields)


def validate_api_key_data(data: Dict[str, Any]) -> bool:
    """Validate API key data"""
    required_fields = ["key_id", "service", "description", "key_hash", "permissions", "created_at"]
    return all(field in data for field in required_fields)


# Export all models
__all__ = [
    "ModelType", "Provider", "AgentType", "WorkflowType", "TaskStatus", "TaskPriority",
    "ModelCapability", "ModelMetrics", "AIModel", "AgentSkill", "AgentPerformance", "AIAgent",
    "APIKeyPermissions", "APIKeyUsage", "APIKey", "WorkflowStep", "WorkflowExecution", "Workflow",
    "OrchestrationTask", "SystemHealth", "PerformanceMetrics",
    "create_model_from_dict", "create_agent_from_dict", "create_workflow_from_dict", "create_api_key_from_dict",
    "validate_model_data", "validate_agent_data", "validate_workflow_data", "validate_api_key_data"
]
