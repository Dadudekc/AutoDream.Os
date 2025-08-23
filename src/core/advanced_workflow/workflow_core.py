"""
Workflow Core Data Models - V2 Compliant Core Classes

This module contains all workflow-related data models and core classes.
Follows V2 standards with ≤200 LOC and single responsibility for data structures.
"""

import time
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict, field
from datetime import datetime

from .workflow_types import WorkflowStatus, AgentCapability


@dataclass
class WorkflowStep:
    """Advanced workflow step definition - consolidated from multiple sources"""
    
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
    
    def is_ready(self, completed_steps: set) -> bool:
        """Check if step dependencies are satisfied - from V2 workflow engine"""
        return all(dep in completed_steps for dep in self.dependencies)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert step to dictionary for serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowStep':
        """Create step from dictionary"""
        return cls(**data)


@dataclass
class WorkflowExecution:
    """Workflow execution instance - consolidated from multiple sources"""
    
    execution_id: str
    workflow_id: str
    status: WorkflowStatus
    current_step: str
    completed_steps: List[str]
    failed_steps: List[str]
    start_time: str
    estimated_completion: str
    actual_completion: Optional[str]
    performance_metrics: Dict[str, float]
    optimization_history: List[Dict[str, Any]]
    
    # Additional fields from execution engine
    agent_id: Optional[str] = None
    step_results: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert execution to dictionary for serialization"""
        data = asdict(self)
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowExecution':
        """Create execution from dictionary"""
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = WorkflowStatus(data['status'])
        return cls(**data)


@dataclass
class WorkflowOptimization:
    """Workflow optimization result"""
    
    optimization_id: str
    workflow_id: str
    strategy: str
    before_metrics: Dict[str, float]
    after_metrics: Dict[str, float]
    improvement_percentage: float
    optimization_timestamp: str
    applied_changes: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert optimization to dictionary for serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowOptimization':
        """Create optimization from dictionary"""
        return cls(**data)


@dataclass
class V2Workflow:
    """V2 workflow definition - integrated from V2 workflow engine"""
    
    workflow_id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    created_at: str
    status: WorkflowStatus
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary for serialization"""
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
            "created_at": self.created_at,
            "status": self.status.value,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'V2Workflow':
        """Create workflow from dictionary"""
        # Convert steps back to WorkflowStep objects
        if 'steps' in data:
            steps = [WorkflowStep.from_dict(step_data) for step_data in data['steps']]
            data['steps'] = steps
        
        # Convert status string to enum
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = WorkflowStatus(data['status'])
        
        return cls(**data)


@dataclass
class AIResponse:
    """Captured AI response from V2 system - integrated from V2 workflow engine"""
    
    agent: str
    text: str
    timestamp: float
    message_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary for serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIResponse':
        """Create response from dictionary"""
        return cls(**data)


@dataclass
class WorkflowMetrics:
    """Workflow performance metrics container"""
    
    execution_time: float = 0.0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    response_time: float = 0.0
    throughput: float = 0.0
    error_rate: float = 0.0
    
    def update(self, **kwargs):
        """Update metrics with new values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, float]:
        """Convert metrics to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'WorkflowMetrics':
        """Create metrics from dictionary"""
        return cls(**data)

