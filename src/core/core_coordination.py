#!/usr/bin/env python3
"""
Core Coordination - Consolidated Coordination System
===================================================

Consolidated coordination system providing unified coordination functionality for:
- Agent coordination
- Swarm coordination
- Task coordination
- Resource coordination

This module consolidates coordination systems for better organization and reduced complexity.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Union

# ============================================================================
# COORDINATION TYPES
# ============================================================================

class CoordinationStatus(Enum):
    """Coordination status enumeration."""
    IDLE = "idle"
    BUSY = "busy"
    COORDINATING = "coordinating"
    ERROR = "error"
    OFFLINE = "offline"


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ResourceStatus(Enum):
    """Resource status enumeration."""
    AVAILABLE = "available"
    ALLOCATED = "allocated"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"


# ============================================================================
# COORDINATION MODELS
# ============================================================================

@dataclass
class AgentInfo:
    """Agent information structure."""
    agent_id: str
    agent_name: str
    agent_type: str
    status: CoordinationStatus = CoordinationStatus.IDLE
    capabilities: List[str] = field(default_factory=list)
    last_seen: datetime = field(default_factory=datetime.now)
    current_tasks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_online(self, timeout_seconds: int = 300) -> bool:
        """Check if agent is online."""
        return (datetime.now() - self.last_seen).total_seconds() < timeout_seconds
    
    def can_accept_task(self) -> bool:
        """Check if agent can accept new tasks."""
        return self.status in [CoordinationStatus.IDLE, CoordinationStatus.BUSY] and len(self.current_tasks) < 5
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "status": self.status.value,
            "capabilities": self.capabilities,
            "last_seen": self.last_seen.isoformat(),
            "current_tasks": self.current_tasks,
            "metadata": self.metadata
        }


@dataclass
class Task:
    """Task structure."""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_name: str = ""
    task_type: str = ""
    priority: int = 0
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration: Optional[timedelta] = None
    actual_duration: Optional[timedelta] = None
    requirements: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def assign_to_agent(self, agent_id: str) -> bool:
        """Assign task to agent."""
        if self.status == TaskStatus.PENDING:
            self.assigned_agent = agent_id
            self.status = TaskStatus.ASSIGNED
            return True
        return False
    
    def start_task(self) -> bool:
        """Start task execution."""
        if self.status == TaskStatus.ASSIGNED:
            self.status = TaskStatus.IN_PROGRESS
            self.started_at = datetime.now()
            return True
        return False
    
    def complete_task(self) -> bool:
        """Complete task."""
        if self.status == TaskStatus.IN_PROGRESS:
            self.status = TaskStatus.COMPLETED
            self.completed_at = datetime.now()
            if self.started_at:
                self.actual_duration = self.completed_at - self.started_at
            return True
        return False
    
    def fail_task(self) -> bool:
        """Mark task as failed."""
        if self.status in [TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS]:
            self.status = TaskStatus.FAILED
            self.completed_at = datetime.now()
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_type": self.task_type,
            "priority": self.priority,
            "status": self.status.value,
            "assigned_agent": self.assigned_agent,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "estimated_duration": str(self.estimated_duration) if self.estimated_duration else None,
            "actual_duration": str(self.actual_duration) if self.actual_duration else None,
            "requirements": self.requirements,
            "metadata": self.metadata
        }


@dataclass
class Resource:
    """Resource structure."""
    resource_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    resource_name: str = ""
    resource_type: str = ""
    status: ResourceStatus = ResourceStatus.AVAILABLE
    allocated_to: Optional[str] = None
    capacity: int = 1
    current_usage: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_available(self) -> bool:
        """Check if resource is available."""
        return self.status == ResourceStatus.AVAILABLE and self.current_usage < self.capacity
    
    def allocate(self, agent_id: str) -> bool:
        """Allocate resource to agent."""
        if self.is_available():
            self.allocated_to = agent_id
            self.status = ResourceStatus.ALLOCATED
            self.current_usage += 1
            self.last_updated = datetime.now()
            return True
        return False
    
    def deallocate(self) -> bool:
        """Deallocate resource."""
        if self.status == ResourceStatus.ALLOCATED:
            self.allocated_to = None
            self.status = ResourceStatus.AVAILABLE
            self.current_usage = max(0, self.current_usage - 1)
            self.last_updated = datetime.now()
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "resource_id": self.resource_id,
            "resource_name": self.resource_name,
            "resource_type": self.resource_type,
            "status": self.status.value,
            "allocated_to": self.allocated_to,
            "capacity": self.capacity,
            "current_usage": self.current_usage,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "metadata": self.metadata
        }


# ============================================================================
# COORDINATION INTERFACES
# ============================================================================

class ICoordinator(ABC):
    """Base coordinator interface."""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize coordinator."""
        pass
    
    @abstractmethod
    def start(self) -> bool:
        """Start coordinator."""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """Stop coordinator."""
        pass
    
    @abstractmethod
    def get_status(self) -> CoordinationStatus:
        """Get coordinator status."""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """Clean up coordinator resources."""
        pass


class IAgentCoordinator(ICoordinator):
    """Agent coordination interface."""
    
    @abstractmethod
    def register_agent(self, agent: AgentInfo) -> bool:
        """Register an agent."""
        pass
    
    @abstractmethod
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        pass
    
    @abstractmethod
    def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        """Get agent information."""
        pass
    
    @abstractmethod
    def list_agents(self) -> List[AgentInfo]:
        """List all agents."""
        pass
    
    @abstractmethod
    def get_available_agents(self) -> List[AgentInfo]:
        """Get available agents."""
        pass


class ITaskCoordinator(ICoordinator):
    """Task coordination interface."""
    
    @abstractmethod
    def create_task(self, task: Task) -> bool:
        """Create a task."""
        pass
    
    @abstractmethod
    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign task to agent."""
        pass
    
    @abstractmethod
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task information."""
        pass
    
    @abstractmethod
    def list_tasks(self) -> List[Task]:
        """List all tasks."""
        pass
    
    @abstractmethod
    def get_pending_tasks(self) -> List[Task]:
        """Get pending tasks."""
        pass


class IResourceCoordinator(ICoordinator):
    """Resource coordination interface."""
    
    @abstractmethod
    def register_resource(self, resource: Resource) -> bool:
        """Register a resource."""
        pass
    
    @abstractmethod
    def unregister_resource(self, resource_id: str) -> bool:
        """Unregister a resource."""
        pass
    
    @abstractmethod
    def allocate_resource(self, resource_id: str, agent_id: str) -> bool:
        """Allocate resource to agent."""
        pass
    
    @abstractmethod
    def deallocate_resource(self, resource_id: str) -> bool:
        """Deallocate resource."""
        pass
    
    @abstractmethod
    def get_available_resources(self) -> List[Resource]:
        """Get available resources."""
        pass


# ============================================================================
# COORDINATION IMPLEMENTATIONS
# ============================================================================

class AgentCoordinator(IAgentCoordinator):
    """Agent coordination implementation."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.agents: Dict[str, AgentInfo] = {}
        self.status = CoordinationStatus.IDLE
    
    def initialize(self) -> bool:
        """Initialize agent coordinator."""
        self.status = CoordinationStatus.IDLE
        self.logger.info("Agent coordinator initialized")
        return True
    
    def start(self) -> bool:
        """Start agent coordinator."""
        self.status = CoordinationStatus.COORDINATING
        self.logger.info("Agent coordinator started")
        return True
    
    def stop(self) -> bool:
        """Stop agent coordinator."""
        self.status = CoordinationStatus.IDLE
        self.logger.info("Agent coordinator stopped")
        return True
    
    def get_status(self) -> CoordinationStatus:
        """Get coordinator status."""
        return self.status
    
    def cleanup(self) -> bool:
        """Clean up coordinator resources."""
        self.agents.clear()
        self.status = CoordinationStatus.IDLE
        self.logger.info("Agent coordinator cleaned up")
        return True
    
    def register_agent(self, agent: AgentInfo) -> bool:
        """Register an agent."""
        try:
            self.agents[agent.agent_id] = agent
            self.logger.info(f"Registered agent: {agent.agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent.agent_id}: {e}")
            return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        try:
            if agent_id in self.agents:
                del self.agents[agent_id]
                self.logger.info(f"Unregistered agent: {agent_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to unregister agent {agent_id}: {e}")
            return False
    
    def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        """Get agent information."""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[AgentInfo]:
        """List all agents."""
        return list(self.agents.values())
    
    def get_available_agents(self) -> List[AgentInfo]:
        """Get available agents."""
        return [agent for agent in self.agents.values() if agent.can_accept_task()]


class TaskCoordinator(ITaskCoordinator):
    """Task coordination implementation."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tasks: Dict[str, Task] = {}
        self.status = CoordinationStatus.IDLE
    
    def initialize(self) -> bool:
        """Initialize task coordinator."""
        self.status = CoordinationStatus.IDLE
        self.logger.info("Task coordinator initialized")
        return True
    
    def start(self) -> bool:
        """Start task coordinator."""
        self.status = CoordinationStatus.COORDINATING
        self.logger.info("Task coordinator started")
        return True
    
    def stop(self) -> bool:
        """Stop task coordinator."""
        self.status = CoordinationStatus.IDLE
        self.logger.info("Task coordinator stopped")
        return True
    
    def get_status(self) -> CoordinationStatus:
        """Get coordinator status."""
        return self.status
    
    def cleanup(self) -> bool:
        """Clean up coordinator resources."""
        self.tasks.clear()
        self.status = CoordinationStatus.IDLE
        self.logger.info("Task coordinator cleaned up")
        return True
    
    def create_task(self, task: Task) -> bool:
        """Create a task."""
        try:
            self.tasks[task.task_id] = task
            self.logger.info(f"Created task: {task.task_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create task {task.task_id}: {e}")
            return False
    
    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign task to agent."""
        try:
            if task_id in self.tasks:
                return self.tasks[task_id].assign_to_agent(agent_id)
            return False
        except Exception as e:
            self.logger.error(f"Failed to assign task {task_id}: {e}")
            return False
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task information."""
        return self.tasks.get(task_id)
    
    def list_tasks(self) -> List[Task]:
        """List all tasks."""
        return list(self.tasks.values())
    
    def get_pending_tasks(self) -> List[Task]:
        """Get pending tasks."""
        return [task for task in self.tasks.values() if task.status == TaskStatus.PENDING]


class ResourceCoordinator(IResourceCoordinator):
    """Resource coordination implementation."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.resources: Dict[str, Resource] = {}
        self.status = CoordinationStatus.IDLE
    
    def initialize(self) -> bool:
        """Initialize resource coordinator."""
        self.status = CoordinationStatus.IDLE
        self.logger.info("Resource coordinator initialized")
        return True
    
    def start(self) -> bool:
        """Start resource coordinator."""
        self.status = CoordinationStatus.COORDINATING
        self.logger.info("Resource coordinator started")
        return True
    
    def stop(self) -> bool:
        """Stop resource coordinator."""
        self.status = CoordinationStatus.IDLE
        self.logger.info("Resource coordinator stopped")
        return True
    
    def get_status(self) -> CoordinationStatus:
        """Get coordinator status."""
        return self.status
    
    def cleanup(self) -> bool:
        """Clean up coordinator resources."""
        self.resources.clear()
        self.status = CoordinationStatus.IDLE
        self.logger.info("Resource coordinator cleaned up")
        return True
    
    def register_resource(self, resource: Resource) -> bool:
        """Register a resource."""
        try:
            self.resources[resource.resource_id] = resource
            self.logger.info(f"Registered resource: {resource.resource_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register resource {resource.resource_id}: {e}")
            return False
    
    def unregister_resource(self, resource_id: str) -> bool:
        """Unregister a resource."""
        try:
            if resource_id in self.resources:
                del self.resources[resource_id]
                self.logger.info(f"Unregistered resource: {resource_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to unregister resource {resource_id}: {e}")
            return False
    
    def allocate_resource(self, resource_id: str, agent_id: str) -> bool:
        """Allocate resource to agent."""
        try:
            if resource_id in self.resources:
                return self.resources[resource_id].allocate(agent_id)
            return False
        except Exception as e:
            self.logger.error(f"Failed to allocate resource {resource_id}: {e}")
            return False
    
    def deallocate_resource(self, resource_id: str) -> bool:
        """Deallocate resource."""
        try:
            if resource_id in self.resources:
                return self.resources[resource_id].deallocate()
            return False
        except Exception as e:
            self.logger.error(f"Failed to deallocate resource {resource_id}: {e}")
            return False
    
    def get_available_resources(self) -> List[Resource]:
        """Get available resources."""
        return [resource for resource in self.resources.values() if resource.is_available()]


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_agent_info(
    agent_id: str,
    agent_name: str,
    agent_type: str,
    capabilities: List[str] = None
) -> AgentInfo:
    """Create agent information."""
    return AgentInfo(
        agent_id=agent_id,
        agent_name=agent_name,
        agent_type=agent_type,
        capabilities=capabilities or []
    )


def create_task(
    task_name: str,
    task_type: str,
    priority: int = 0,
    requirements: List[str] = None
) -> Task:
    """Create a task."""
    return Task(
        task_name=task_name,
        task_type=task_type,
        priority=priority,
        requirements=requirements or []
    )


def create_resource(
    resource_name: str,
    resource_type: str,
    capacity: int = 1
) -> Resource:
    """Create a resource."""
    return Resource(
        resource_name=resource_name,
        resource_type=resource_type,
        capacity=capacity
    )


def create_agent_coordinator() -> AgentCoordinator:
    """Create agent coordinator."""
    return AgentCoordinator()


def create_task_coordinator() -> TaskCoordinator:
    """Create task coordinator."""
    return TaskCoordinator()


def create_resource_coordinator() -> ResourceCoordinator:
    """Create resource coordinator."""
    return ResourceCoordinator()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    print("Core Coordination - Consolidated Coordination System")
    print("=" * 50)
    
    # Create coordinators
    agent_coordinator = create_agent_coordinator()
    task_coordinator = create_task_coordinator()
    resource_coordinator = create_resource_coordinator()
    
    # Initialize coordinators
    agent_coordinator.initialize()
    task_coordinator.initialize()
    resource_coordinator.initialize()
    
    print(f"Agent coordinator status: {agent_coordinator.get_status().value}")
    print(f"Task coordinator status: {task_coordinator.get_status().value}")
    print(f"Resource coordinator status: {resource_coordinator.get_status().value}")
    
    # Create test data
    agent_info = create_agent_info(
        "agent-2",
        "Architecture & Design Specialist",
        "consolidation",
        ["analysis", "consolidation", "architecture"]
    )
    
    task = create_task(
        "Consolidate Core Modules",
        "consolidation",
        priority=1,
        requirements=["analysis", "consolidation"]
    )
    
    resource = create_resource(
        "Development Environment",
        "computing",
        capacity=5
    )
    
    # Register and test
    agent_coordinator.register_agent(agent_info)
    task_coordinator.create_task(task)
    resource_coordinator.register_resource(resource)
    
    print(f"Registered agents: {len(agent_coordinator.list_agents())}")
    print(f"Created tasks: {len(task_coordinator.list_tasks())}")
    print(f"Registered resources: {len(resource_coordinator.get_available_resources())}")
    
    print("\nCore Coordination initialization complete!")


if __name__ == "__main__":
    exit_code = main()
    print()
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    exit(exit_code)
