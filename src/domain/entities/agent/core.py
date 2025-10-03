#!/usr/bin/env python3
"""
Agent Core - Clean OOP Design
============================

Core Agent entity following clean object-oriented principles.
Single responsibility: Represent an agent with essential functionality.

Author: Agent-1 (Integration Specialist)
License: MIT
"""

import logging
from datetime import datetime
from typing import List, Optional
import uuid

from .enums import AgentStatus, AgentType, AgentCapability
from .metrics import AgentMetrics
from .configuration import AgentConfiguration

logger = logging.getLogger(__name__)


class Agent:
    """Core Agent entity with clean separation of concerns."""
    
    def __init__(self,
                 name: str,
                 agent_type: AgentType,
                 capabilities: List[AgentCapability] = None,
                 configuration: Optional[AgentConfiguration] = None):
        """Initialize agent with clean dependencies."""
        self._id = str(uuid.uuid4())
        self._name = name
        self._agent_type = agent_type
        self._capabilities = capabilities or []
        self._status = AgentStatus.INACTIVE
        self._created_at = datetime.now()
        
        # Dependency injection for clean design
        self._configuration = configuration or AgentConfiguration(
            name=name,
            agent_type=agent_type.value,
            capabilities=self._capabilities
        )
        self._metrics = AgentMetrics()
    
    # Properties with clean encapsulation
    @property
    def id(self) -> str:
        """Get agent ID."""
        return self._id
    
    @property
    def name(self) -> str:
        """Get agent name."""
        return self._name
    
    @property
    def agent_type(self) -> AgentType:
        """Get agent type."""
        return self._agent_type
    
    @property
    def status(self) -> AgentStatus:
        """Get agent status."""
        return self._status
    
    @property
    def capabilities(self) -> List[AgentCapability]:
        """Get agent capabilities."""
        return self._capabilities.copy()
    
    @property
    def configuration(self) -> AgentConfiguration:
        """Get agent configuration."""
        return self._configuration
    
    @property
    def metrics(self) -> AgentMetrics:
        """Get agent metrics."""
        return self._metrics
    
    @property
    def created_at(self) -> datetime:
        """Get creation timestamp."""
        return self._created_at
    
    # Status management with clean state transitions
    def activate(self):
        """Activate the agent."""
        if self._status == AgentStatus.INACTIVE:
            self._status = AgentStatus.ACTIVE
            self._metrics.update_activity()
            logger.info(f"Agent {self._name} activated")
    
    def deactivate(self):
        """Deactivate the agent."""
        if self._status == AgentStatus.ACTIVE:
            self._status = AgentStatus.INACTIVE
            self._metrics.update_activity()
            logger.info(f"Agent {self._name} deactivated")
    
    def set_busy(self):
        """Set agent to busy status."""
        if self._status == AgentStatus.ACTIVE:
            self._status = AgentStatus.BUSY
            self._metrics.update_activity()
    
    def set_error(self, error_message: str = ""):
        """Set agent to error status."""
        self._status = AgentStatus.ERROR
        self._metrics.last_error = datetime.now()
        self._metrics.update_activity()
        logger.error(f"Agent {self._name} error: {error_message}")
    
    def set_offline(self):
        """Set agent to offline status."""
        self._status = AgentStatus.OFFLINE
        self._metrics.update_activity()
        logger.info(f"Agent {self._name} went offline")
    
    # Capability management with clean interface
    def add_capability(self, capability: AgentCapability):
        """Add capability to agent."""
        if capability not in self._capabilities:
            self._capabilities.append(capability)
            self._configuration.add_capability(capability)
            logger.info(f"Added capability {capability.value} to agent {self._name}")
    
    def remove_capability(self, capability: AgentCapability):
        """Remove capability from agent."""
        if capability in self._capabilities:
            self._capabilities.remove(capability)
            self._configuration.remove_capability(capability)
            logger.info(f"Removed capability {capability.value} from agent {self._name}")
    
    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has specific capability."""
        return capability in self._capabilities
    
    # Task execution with clean metrics tracking
    def execute_task(self, task_name: str, success: bool, response_time: float):
        """Execute a task and update metrics."""
        self._metrics.record_task_completion(success, response_time)
        logger.info(f"Agent {self._name} executed task {task_name}: {'success' if success else 'failed'}")
    
    def send_message(self):
        """Record message sent."""
        self._metrics.record_message(sent=True)
    
    def receive_message(self):
        """Record message received."""
        self._metrics.record_message(sent=False)
    
    def execute_command(self, command: str):
        """Execute a command."""
        if self._configuration.is_command_allowed(command):
            self._metrics.record_command()
            logger.info(f"Agent {self._name} executed command: {command}")
            return True
        else:
            logger.warning(f"Agent {self._name} blocked command: {command}")
            return False
    
    # Health and status checks with clean interface
    def is_healthy(self) -> bool:
        """Check if agent is healthy."""
        return (
            self._status in [AgentStatus.ACTIVE, AgentStatus.BUSY] and
            self._metrics.get_success_rate() > 80.0 and
            self._metrics.uptime_percentage > 95.0
        )
    
    def get_status_summary(self) -> dict:
        """Get comprehensive status summary."""
        return {
            'id': self._id,
            'name': self._name,
            'type': self._agent_type.value,
            'status': self._status.value,
            'capabilities': [cap.value for cap in self._capabilities],
            'is_healthy': self.is_healthy(),
            'success_rate': self._metrics.get_success_rate(),
            'uptime_hours': self._metrics.get_uptime_hours(),
            'tasks_completed': self._metrics.tasks_completed,
            'tasks_failed': self._metrics.tasks_failed,
            'created_at': self._created_at.isoformat(),
            'last_activity': self._metrics.last_activity.isoformat()
        }