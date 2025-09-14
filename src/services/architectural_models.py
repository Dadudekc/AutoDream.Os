#!/usr/bin/env python3
"""
Architectural Models - V2 Compliant Module
==========================================

Simple architectural models for the consolidated agent management service.

V2 Compliance: < 400 lines, single responsibility for architectural models.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ArchitecturalPrinciple(Enum):
    """Architectural principles for agent management."""
    SINGLE_RESPONSIBILITY = "single_responsibility"
    OPEN_CLOSED = "open_closed"
    LISKOV_SUBSTITUTION = "liskov_substitution"
    INTERFACE_SEGREGATION = "interface_segregation"
    DEPENDENCY_INVERSION = "dependency_inversion"
    DRY = "dry"
    KISS = "kiss"
    YAGNI = "yagni"


class AgentStatus(Enum):
    """Agent status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class TaskPriority(Enum):
    """Task priority enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ArchitecturalModel:
    """Base architectural model."""
    
    def __init__(self, name: str, principle: ArchitecturalPrinciple):
        self.name = name
        self.principle = principle
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "principle": self.principle.value,
            "created_at": self.created_at.isoformat()
        }


class AgentModel(ArchitecturalModel):
    """Agent architectural model."""
    
    def __init__(self, agent_id: str, status: AgentStatus = AgentStatus.IDLE):
        super().__init__(agent_id, ArchitecturalPrinciple.SINGLE_RESPONSIBILITY)
        self.agent_id = agent_id
        self.status = status
        self.tasks: List[str] = []
        self.capabilities: List[str] = []
    
    def add_task(self, task: str) -> None:
        """Add a task to the agent."""
        self.tasks.append(task)
    
    def add_capability(self, capability: str) -> None:
        """Add a capability to the agent."""
        self.capabilities.append(capability)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "agent_id": self.agent_id,
            "status": self.status.value,
            "tasks": self.tasks,
            "capabilities": self.capabilities
        })
        return base_dict


class TaskModel(ArchitecturalModel):
    """Task architectural model."""
    
    def __init__(self, task_id: str, description: str, priority: TaskPriority = TaskPriority.MEDIUM):
        super().__init__(task_id, ArchitecturalPrinciple.SINGLE_RESPONSIBILITY)
        self.task_id = task_id
        self.description = description
        self.priority = priority
        self.assigned_agent: Optional[str] = None
        self.status = "pending"
    
    def assign_to_agent(self, agent_id: str) -> None:
        """Assign task to an agent."""
        self.assigned_agent = agent_id
        self.status = "assigned"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "task_id": self.task_id,
            "description": self.description,
            "priority": self.priority.value,
            "assigned_agent": self.assigned_agent,
            "status": self.status
        })
        return base_dict


class SystemModel(ArchitecturalModel):
    """System architectural model."""
    
    def __init__(self, system_name: str):
        super().__init__(system_name, ArchitecturalPrinciple.SINGLE_RESPONSIBILITY)
        self.system_name = system_name
        self.agents: List[AgentModel] = []
        self.tasks: List[TaskModel] = []
        self.performance_metrics: Dict[str, Any] = {}
    
    def add_agent(self, agent: AgentModel) -> None:
        """Add an agent to the system."""
        self.agents.append(agent)
    
    def add_task(self, task: TaskModel) -> None:
        """Add a task to the system."""
        self.tasks.append(task)
    
    def update_metrics(self, metrics: Dict[str, Any]) -> None:
        """Update system performance metrics."""
        self.performance_metrics.update(metrics)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "system_name": self.system_name,
            "agents": [agent.to_dict() for agent in self.agents],
            "tasks": [task.to_dict() for task in self.tasks],
            "performance_metrics": self.performance_metrics
        })
        return base_dict


# Factory functions for creating models
def create_agent_model(agent_id: str, status: AgentStatus = AgentStatus.IDLE) -> AgentModel:
    """Create a new agent model."""
    return AgentModel(agent_id, status)


def create_task_model(task_id: str, description: str, priority: TaskPriority = TaskPriority.MEDIUM) -> TaskModel:
    """Create a new task model."""
    return TaskModel(task_id, description, priority)


def create_system_model(system_name: str) -> SystemModel:
    """Create a new system model."""
    return SystemModel(system_name)


# Utility functions
def validate_architectural_principle(principle: ArchitecturalPrinciple) -> bool:
    """Validate an architectural principle."""
    return principle in ArchitecturalPrinciple


def get_principle_description(principle: ArchitecturalPrinciple) -> str:
    """Get description of an architectural principle."""
    descriptions = {
        ArchitecturalPrinciple.SINGLE_RESPONSIBILITY: "A class should have only one reason to change",
        ArchitecturalPrinciple.OPEN_CLOSED: "Software entities should be open for extension, but closed for modification",
        ArchitecturalPrinciple.LISKOV_SUBSTITUTION: "Objects of a superclass should be replaceable with objects of a subclass",
        ArchitecturalPrinciple.INTERFACE_SEGREGATION: "No client should be forced to depend on methods it does not use",
        ArchitecturalPrinciple.DEPENDENCY_INVERSION: "Depend on abstractions, not concretions",
        ArchitecturalPrinciple.DRY: "Don't Repeat Yourself",
        ArchitecturalPrinciple.KISS: "Keep It Simple, Stupid",
        ArchitecturalPrinciple.YAGNI: "You Aren't Gonna Need It"
    }
    return descriptions.get(principle, "Unknown principle")


# Export main classes and functions
__all__ = [
    "ArchitecturalPrinciple",
    "AgentStatus", 
    "TaskPriority",
    "ArchitecturalModel",
    "AgentModel",
    "TaskModel", 
    "SystemModel",
    "create_agent_model",
    "create_task_model",
    "create_system_model",
    "validate_architectural_principle",
    "get_principle_description"
]
