#!/usr/bin/env python3
"""
Vector Enhanced Contracts Core Models - V2 Compliance Module
============================================================

Core data models for vector enhanced contracts operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

from .vector_enhanced_contracts_enums import TaskType, PriorityLevel, ContractStatus


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
