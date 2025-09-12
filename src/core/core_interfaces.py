#!/usr/bin/env python3
"""
Core Interfaces - Consolidated Interface Definitions
===================================================

Consolidated interface definitions providing unified contracts for:
- Coordinator interfaces
- Message queue interfaces
- Agent interfaces
- System interfaces

This module consolidates interface definitions for better organization and reduced complexity.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Protocol

# ============================================================================
# COORDINATOR INTERFACES
# ============================================================================


class CoordinatorStatus(Enum):
    """Coordinator status enumeration."""

    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class CoordinatorInfo:
    """Coordinator information structure."""

    coordinator_id: str
    coordinator_name: str
    status: CoordinatorStatus = CoordinatorStatus.IDLE
    last_activity: datetime = field(default_factory=datetime.now)
    capabilities: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def is_active(self, timeout_seconds: int = 300) -> bool:
        """Check if coordinator is active."""
        return (datetime.now() - self.last_activity).total_seconds() < timeout_seconds

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "coordinator_id": self.coordinator_id,
            "coordinator_name": self.coordinator_name,
            "status": self.status.value,
            "last_activity": self.last_activity.isoformat(),
            "capabilities": self.capabilities,
            "metadata": self.metadata,
        }


class ICoordinator(ABC):
    """Base coordinator interface."""

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the coordinator."""
        pass

    @abstractmethod
    def start(self) -> bool:
        """Start the coordinator."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Stop the coordinator."""
        pass

    @abstractmethod
    def get_status(self) -> CoordinatorStatus:
        """Get coordinator status."""
        pass

    @abstractmethod
    def get_info(self) -> CoordinatorInfo:
        """Get coordinator information."""
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        """Clean up coordinator resources."""
        pass


class ICoordinatorRegistry(ABC):
    """Coordinator registry interface."""

    @abstractmethod
    def register_coordinator(self, coordinator: ICoordinator) -> bool:
        """Register a coordinator."""
        pass

    @abstractmethod
    def unregister_coordinator(self, coordinator_id: str) -> bool:
        """Unregister a coordinator."""
        pass

    @abstractmethod
    def get_coordinator(self, coordinator_id: str) -> ICoordinator | None:
        """Get a coordinator by ID."""
        pass

    @abstractmethod
    def list_coordinators(self) -> list[ICoordinator]:
        """List all coordinators."""
        pass

    @abstractmethod
    def get_coordinator_stats(self) -> dict:
        """Get coordinator statistics."""
        pass


# ============================================================================
# MESSAGE QUEUE INTERFACES
# ============================================================================


class MessagePriority(Enum):
    """Message priority enumeration."""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class MessageStatus(Enum):
    """Message status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"


@dataclass
class Message:
    """Message data structure."""

    id: str
    content: str
    priority: MessagePriority = MessagePriority.NORMAL
    status: MessageStatus = MessageStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    processed_at: datetime | None = None
    retry_count: int = 0
    max_retries: int = 3
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "metadata": self.metadata,
        }


class IMessageQueue(ABC):
    """Message queue interface."""

    @abstractmethod
    def enqueue(self, message: Message) -> bool:
        """Enqueue a message."""
        pass

    @abstractmethod
    def dequeue(self) -> Message | None:
        """Dequeue a message."""
        pass

    @abstractmethod
    def peek(self) -> Message | None:
        """Peek at the next message without removing it."""
        pass

    @abstractmethod
    def get_queue_size(self) -> int:
        """Get queue size."""
        pass

    @abstractmethod
    def get_queue_status(self) -> dict:
        """Get queue status."""
        pass

    @abstractmethod
    def clear_queue(self) -> bool:
        """Clear the queue."""
        pass


class IMessageProcessor(ABC):
    """Message processor interface."""

    @abstractmethod
    def process_message(self, message: Message) -> bool:
        """Process a message."""
        pass

    @abstractmethod
    def can_process(self, message: Message) -> bool:
        """Check if processor can handle the message."""
        pass

    @abstractmethod
    def get_processor_info(self) -> dict:
        """Get processor information."""
        pass


# ============================================================================
# AGENT INTERFACES
# ============================================================================


class AgentStatus(Enum):
    """Agent status enumeration."""

    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class AgentCapability(Enum):
    """Agent capability enumeration."""

    ANALYSIS = "analysis"
    CONSOLIDATION = "consolidation"
    COORDINATION = "coordination"
    COMMUNICATION = "communication"
    INTEGRATION = "integration"
    MONITORING = "monitoring"
    OPTIMIZATION = "optimization"
    VALIDATION = "validation"


@dataclass
class AgentInfo:
    """Agent information structure."""

    agent_id: str
    agent_name: str
    agent_type: str
    status: AgentStatus = AgentStatus.IDLE
    capabilities: list[AgentCapability] = field(default_factory=list)
    last_seen: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def is_online(self, timeout_seconds: int = 300) -> bool:
        """Check if agent is online."""
        return (datetime.now() - self.last_seen).total_seconds() < timeout_seconds

    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has specific capability."""
        return capability in self.capabilities

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "status": self.status.value,
            "capabilities": [cap.value for cap in self.capabilities],
            "last_seen": self.last_seen.isoformat(),
            "metadata": self.metadata,
        }


class IAgent(ABC):
    """Base agent interface."""

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the agent."""
        pass

    @abstractmethod
    def start(self) -> bool:
        """Start the agent."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Stop the agent."""
        pass

    @abstractmethod
    def get_status(self) -> AgentStatus:
        """Get agent status."""
        pass

    @abstractmethod
    def get_info(self) -> AgentInfo:
        """Get agent information."""
        pass

    @abstractmethod
    def execute_task(self, task: dict) -> dict:
        """Execute a task."""
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        """Clean up agent resources."""
        pass


class IAgentRegistry(ABC):
    """Agent registry interface."""

    @abstractmethod
    def register_agent(self, agent: IAgent) -> bool:
        """Register an agent."""
        pass

    @abstractmethod
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        pass

    @abstractmethod
    def get_agent(self, agent_id: str) -> IAgent | None:
        """Get an agent by ID."""
        pass

    @abstractmethod
    def list_agents(self) -> list[IAgent]:
        """List all agents."""
        pass

    @abstractmethod
    def get_agents_by_capability(self, capability: AgentCapability) -> list[IAgent]:
        """Get agents by capability."""
        pass

    @abstractmethod
    def get_agent_stats(self) -> dict:
        """Get agent statistics."""
        pass


# ============================================================================
# SYSTEM INTERFACES
# ============================================================================


class SystemStatus(Enum):
    """System status enumeration."""

    HEALTHY = "healthy"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    MAINTENANCE = "maintenance"


@dataclass
class SystemInfo:
    """System information structure."""

    system_id: str
    system_name: str
    status: SystemStatus = SystemStatus.HEALTHY
    version: str = "1.0.0"
    uptime: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def get_uptime_seconds(self) -> float:
        """Get uptime in seconds."""
        return (datetime.now() - self.uptime).total_seconds()

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "system_id": self.system_id,
            "system_name": self.system_name,
            "status": self.status.value,
            "version": self.version,
            "uptime": self.uptime.isoformat(),
            "uptime_seconds": self.get_uptime_seconds(),
            "metadata": self.metadata,
        }


class ISystem(ABC):
    """Base system interface."""

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the system."""
        pass

    @abstractmethod
    def start(self) -> bool:
        """Start the system."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Stop the system."""
        pass

    @abstractmethod
    def get_status(self) -> SystemStatus:
        """Get system status."""
        pass

    @abstractmethod
    def get_info(self) -> SystemInfo:
        """Get system information."""
        pass

    @abstractmethod
    def health_check(self) -> dict:
        """Perform health check."""
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        """Clean up system resources."""
        pass


class ISystemMonitor(ABC):
    """System monitor interface."""

    @abstractmethod
    def start_monitoring(self) -> bool:
        """Start monitoring."""
        pass

    @abstractmethod
    def stop_monitoring(self) -> bool:
        """Stop monitoring."""
        pass

    @abstractmethod
    def get_metrics(self) -> dict:
        """Get system metrics."""
        pass

    @abstractmethod
    def get_alerts(self) -> list[dict]:
        """Get system alerts."""
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if system is healthy."""
        pass


# ============================================================================
# PROTOCOL DEFINITIONS
# ============================================================================


class IMessageDelivery(Protocol):
    """Message delivery protocol."""

    def send_message(self, message: Message) -> bool:
        """Send a message."""
        ...


class IOnboardingService(Protocol):
    """Onboarding service protocol."""

    def generate_onboarding_message(self, agent_id: str, phase: str) -> str:
        """Generate onboarding message."""
        ...


class IValidationService(Protocol):
    """Validation service protocol."""

    def validate(self, data: Any) -> bool:
        """Validate data."""
        ...

    def get_validation_errors(self) -> list[str]:
        """Get validation errors."""
        ...


class ILoggingService(Protocol):
    """Logging service protocol."""

    def log(self, level: str, message: str, **kwargs) -> None:
        """Log a message."""
        ...

    def get_logs(self, level: str = None) -> list[dict]:
        """Get logs."""
        ...


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def create_coordinator_info(
    coordinator_id: str, coordinator_name: str, capabilities: list[str] = None
) -> CoordinatorInfo:
    """Create coordinator information."""
    return CoordinatorInfo(
        coordinator_id=coordinator_id,
        coordinator_name=coordinator_name,
        capabilities=capabilities or [],
    )


def create_message(
    content: str, priority: MessagePriority = MessagePriority.NORMAL, metadata: dict = None
) -> Message:
    """Create a message."""
    import uuid

    return Message(
        id=str(uuid.uuid4()), content=content, priority=priority, metadata=metadata or {}
    )


def create_agent_info(
    agent_id: str, agent_name: str, agent_type: str, capabilities: list[AgentCapability] = None
) -> AgentInfo:
    """Create agent information."""
    return AgentInfo(
        agent_id=agent_id,
        agent_name=agent_name,
        agent_type=agent_type,
        capabilities=capabilities or [],
    )


def create_system_info(system_id: str, system_name: str, version: str = "1.0.0") -> SystemInfo:
    """Create system information."""
    return SystemInfo(system_id=system_id, system_name=system_name, version=version)


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def main():
    """Main execution function."""
    print("Core Interfaces - Consolidated Interface Definitions")
    print("=" * 50)

    # Create coordinator info
    coordinator_info = create_coordinator_info(
        "coord-1", "Consolidation Coordinator", ["consolidation", "coordination"]
    )
    print(f"Coordinator info created: {coordinator_info.to_dict()}")

    # Create message
    message = create_message(
        "Test consolidation message", MessagePriority.HIGH, {"phase": "consolidation"}
    )
    print(f"Message created: {message.to_dict()}")

    # Create agent info
    agent_info = create_agent_info(
        "agent-2",
        "Architecture & Design Specialist",
        "consolidation",
        [AgentCapability.ANALYSIS, AgentCapability.CONSOLIDATION],
    )
    print(f"Agent info created: {agent_info.to_dict()}")

    # Create system info
    system_info = create_system_info("core-system", "Core Unified System", "2.0.0")
    print(f"System info created: {system_info.to_dict()}")

    print("\nCore Interfaces initialization complete!")


if __name__ == "__main__":
    exit_code = main()
    print()
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    exit(exit_code)
