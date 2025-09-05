#!/usr/bin/env python3
"""
Vector Enhanced Contracts Models - V2 Compliance Module
======================================================

Data models and enums for vector enhanced contracts operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class ContractStatus(Enum):
    """Contract status enumeration."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class PriorityLevel(Enum):
    """Priority level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(Enum):
    """Task type enumeration."""
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    OPTIMIZATION = "optimization"
    INTEGRATION = "integration"
    DEBUGGING = "debugging"
    FEATURE_DEVELOPMENT = "feature_development"
    MAINTENANCE = "maintenance"


class AssignmentStrategy(Enum):
    """Assignment strategy enumeration."""
    ROUND_ROBIN = "round_robin"
    CAPABILITY_BASED = "capability_based"
    LOAD_BALANCED = "load_balanced"
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    RANDOM = "random"


@dataclass
class AgentCapability:
    """Agent capability information."""
    
    agent_id: str
    capabilities: List[str] = field(default_factory=list)
    expertise_areas: List[str] = field(default_factory=list)
    performance_score: float = 0.0
    availability: bool = True
    current_load: float = 0.0
    preferred_task_types: List[TaskType] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "capabilities": self.capabilities,
            "expertise_areas": self.expertise_areas,
            "performance_score": self.performance_score,
            "availability": self.availability,
            "current_load": self.current_load,
            "preferred_task_types": [tt.value for tt in self.preferred_task_types],
            "last_updated": self.last_updated.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class TaskRecommendation:
    """Task recommendation structure."""
    
    recommendation_id: str
    agent_id: str
    task_type: TaskType
    priority: PriorityLevel
    confidence_score: float
    reasoning: str
    expected_duration: float
    required_capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "recommendation_id": self.recommendation_id,
            "agent_id": self.agent_id,
            "task_type": self.task_type.value,
            "priority": self.priority.value,
            "confidence_score": self.confidence_score,
            "reasoning": self.reasoning,
            "expected_duration": self.expected_duration,
            "required_capabilities": self.required_capabilities,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ContractAssignment:
    """Contract assignment structure."""
    
    assignment_id: str
    contract_id: str
    agent_id: str
    task_type: TaskType
    priority: PriorityLevel
    status: ContractStatus
    assigned_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress_percentage: float = 0.0
    estimated_duration: float = 0.0
    actual_duration: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "assignment_id": self.assignment_id,
            "contract_id": self.contract_id,
            "agent_id": self.agent_id,
            "task_type": self.task_type.value,
            "priority": self.priority.value,
            "status": self.status.value,
            "assigned_at": self.assigned_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "progress_percentage": self.progress_percentage,
            "estimated_duration": self.estimated_duration,
            "actual_duration": self.actual_duration,
            "metadata": self.metadata
        }


@dataclass
class PerformanceMetrics:
    """Performance metrics structure."""
    
    agent_id: str
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    average_completion_time: float = 0.0
    success_rate: float = 0.0
    quality_score: float = 0.0
    efficiency_score: float = 0.0
    collaboration_score: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "average_completion_time": self.average_completion_time,
            "success_rate": self.success_rate,
            "quality_score": self.quality_score,
            "efficiency_score": self.efficiency_score,
            "collaboration_score": self.collaboration_score,
            "last_updated": self.last_updated.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class PerformanceTrend:
    """Performance trend analysis."""
    
    agent_id: str
    trend_type: str
    trend_direction: str  # "improving", "declining", "stable"
    trend_strength: float  # 0.0 to 1.0
    key_factors: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "trend_type": self.trend_type,
            "trend_direction": self.trend_direction,
            "trend_strength": self.trend_strength,
            "key_factors": self.key_factors,
            "recommendations": self.recommendations,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class OptimizationResult:
    """Optimization result structure."""
    
    optimization_id: str
    optimization_type: str
    before_metrics: Dict[str, Any] = field(default_factory=dict)
    after_metrics: Dict[str, Any] = field(default_factory=dict)
    improvement_percentage: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    implementation_effort: str = "medium"
    expected_impact: str = "medium"
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "optimization_id": self.optimization_id,
            "optimization_type": self.optimization_type,
            "before_metrics": self.before_metrics,
            "after_metrics": self.after_metrics,
            "improvement_percentage": self.improvement_percentage,
            "recommendations": self.recommendations,
            "implementation_effort": self.implementation_effort,
            "expected_impact": self.expected_impact,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }
