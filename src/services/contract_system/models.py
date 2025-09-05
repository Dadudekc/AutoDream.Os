"""
Contract System Models - V2 Compliant Module
============================================

Data models for the contract system.
Defines task types, priorities, and contract structures.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict


class TaskType(Enum):
    """Available task types for contracts."""
    V2_COMPLIANCE = "v2_compliance"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    OPTIMIZATION = "optimization"
    BUG_FIX = "bug_fix"
    FEATURE_DEVELOPMENT = "feature_development"
    MAINTENANCE = "maintenance"
    COORDINATION = "coordination"
    EMERGENCY_INTERVENTION = "emergency_intervention"


class PriorityLevel(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class TaskStatus(Enum):
    """Task status states."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


@dataclass
class Task:
    """Individual task within a contract."""
    task_id: str
    title: str
    description: str
    task_type: TaskType
    priority: PriorityLevel
    status: TaskStatus
    assigned_agent: Optional[str] = None
    created_at: datetime = None
    assigned_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration: str = "1 cycle"
    actual_duration: Optional[str] = None
    completion_notes: Optional[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.dependencies is None:
            self.dependencies = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        data = asdict(self)
        # Convert datetime objects to strings
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, Enum):
                data[key] = value.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary."""
        # Convert string values back to enums and datetime
        if 'task_type' in data and isinstance(data['task_type'], str):
            data['task_type'] = TaskType(data['task_type'])
        if 'priority' in data and isinstance(data['priority'], str):
            data['priority'] = PriorityLevel(data['priority'])
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = TaskStatus(data['status'])
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'assigned_at' in data and isinstance(data['assigned_at'], str):
            data['assigned_at'] = datetime.fromisoformat(data['assigned_at'])
        if 'completed_at' in data and isinstance(data['completed_at'], str):
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])
        
        return cls(**data)


@dataclass
class Contract:
    """Contract containing multiple tasks."""
    contract_id: str
    title: str
    description: str
    agent_id: str
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    tasks: List[Task] = None
    total_points: int = 0
    completed_points: int = 0
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.tasks is None:
            self.tasks = []
    
    def add_task(self, task: Task) -> None:
        """Add task to contract."""
        self.tasks.append(task)
        self.total_points += self._calculate_task_points(task)
    
    def _calculate_task_points(self, task: Task) -> int:
        """Calculate points for a task based on type and priority."""
        base_points = {
            TaskType.V2_COMPLIANCE: 50,
            TaskType.REFACTORING: 40,
            TaskType.TESTING: 30,
            TaskType.DOCUMENTATION: 20,
            TaskType.OPTIMIZATION: 35,
            TaskType.BUG_FIX: 25,
            TaskType.FEATURE_DEVELOPMENT: 60,
            TaskType.MAINTENANCE: 15,
            TaskType.COORDINATION: 10,
            TaskType.EMERGENCY_INTERVENTION: 100
        }
        
        priority_multiplier = {
            PriorityLevel.LOW: 0.5,
            PriorityLevel.MEDIUM: 1.0,
            PriorityLevel.HIGH: 1.5,
            PriorityLevel.URGENT: 2.0,
            PriorityLevel.CRITICAL: 3.0
        }
        
        return int(base_points.get(task.task_type, 30) * priority_multiplier.get(task.priority, 1.0))
    
    def update_status(self) -> None:
        """Update contract status based on task statuses."""
        if not self.tasks:
            self.status = TaskStatus.PENDING
            return
        
        completed_tasks = [t for t in self.tasks if t.status == TaskStatus.COMPLETED]
        self.completed_points = sum(self._calculate_task_points(t) for t in completed_tasks)
        
        if all(t.status == TaskStatus.COMPLETED for t in self.tasks):
            self.status = TaskStatus.COMPLETED
            self.completed_at = datetime.now()
        elif any(t.status == TaskStatus.IN_PROGRESS for t in self.tasks):
            self.status = TaskStatus.IN_PROGRESS
        elif any(t.status == TaskStatus.ASSIGNED for t in self.tasks):
            self.status = TaskStatus.ASSIGNED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert contract to dictionary."""
        data = asdict(self)
        # Convert datetime objects to strings
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, Enum):
                data[key] = value.value
            elif key == 'tasks':
                data[key] = [task.to_dict() for task in value]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contract':
        """Create contract from dictionary."""
        # Convert string values back to enums and datetime
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = TaskStatus(data['status'])
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'completed_at' in data and isinstance(data['completed_at'], str):
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])
        if 'tasks' in data:
            data['tasks'] = [Task.from_dict(task_data) for task_data in data['tasks']]
        
        return cls(**data)


@dataclass
class AgentContractSummary:
    """Summary of agent's contract status."""
    agent_id: str
    total_contracts: int
    active_contracts: int
    completed_contracts: int
    total_points: int
    completed_points: int
    completion_rate: float
    current_tasks: List[Task]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary."""
        data = asdict(self)
        data['current_tasks'] = [task.to_dict() for task in data['current_tasks']]
        return data
