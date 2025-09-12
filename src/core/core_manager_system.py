#!/usr/bin/env python3
"""
Core Manager System - Consolidated Manager Classes
=================================================

Consolidated manager system providing unified management functionality for:
- Agent context management
- Documentation services
- Message queue management
- Metrics management
- Workspace agent registry

This module consolidates manager classes for better organization and reduced complexity.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

# ============================================================================
# AGENT CONTEXT MANAGEMENT
# ============================================================================


class AgentContextManager:
    """Manages agent context and state."""

    def __init__(self, agent_id: str = "agent-2"):
        """Initialize core manager system.

        Args:
            agent_id: Identifier for the managing agent
        """
        self.agent_id = agent_id
        self.status = "initialized"
        self.components = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.context = {}
        self.state_history = []

    def set_context(self, key: str, value: Any) -> bool:
        """Set context value."""
        try:
            self.context[key] = value
            self.state_history.append(
                {
                    "timestamp": datetime.now(),
                    "action": "set_context",
                    "key": key,
                    "value": str(value),
                }
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to set context {key}: {e}")
            return False

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context value."""
        return self.context.get(key, default)

    def clear_context(self) -> bool:
        """Clear all context."""
        try:
            self.context.clear()
            self.state_history.append({"timestamp": datetime.now(), "action": "clear_context"})
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear context: {e}")
            return False

    def get_context_summary(self) -> dict:
        """Get context summary."""
        return {
            "agent_id": self.agent_id,
            "context_keys": list(self.context.keys()),
            "context_size": len(self.context),
            "state_history_size": len(self.state_history),
        }


# ============================================================================
# DOCUMENTATION SERVICES
# ============================================================================


class DocumentationService:
    """Manages documentation services."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.documentation_index = {}
        self.search_history = []

    def index_documentation(self, doc_id: str, content: str, metadata: dict = None) -> bool:
        """Index documentation content."""
        try:
            self.documentation_index[doc_id] = {
                "content": content,
                "metadata": metadata or {},
                "indexed_at": datetime.now(),
            }
            return True
        except Exception as e:
            self.logger.error(f"Failed to index documentation {doc_id}: {e}")
            return False

    def search_documentation(self, query: str) -> list[dict]:
        """Search documentation."""
        try:
            results = []
            for doc_id, doc_data in self.documentation_index.items():
                if query.lower() in doc_data["content"].lower():
                    results.append(
                        {
                            "doc_id": doc_id,
                            "content": doc_data["content"],
                            "metadata": doc_data["metadata"],
                        }
                    )

            self.search_history.append(
                {"timestamp": datetime.now(), "query": query, "results_count": len(results)}
            )

            return results
        except Exception as e:
            self.logger.error(f"Failed to search documentation: {e}")
            return []

    def get_documentation_stats(self) -> dict:
        """Get documentation statistics."""
        return {
            "total_docs": len(self.documentation_index),
            "total_searches": len(self.search_history),
            "avg_results_per_search": sum(h["results_count"] for h in self.search_history)
            / max(len(self.search_history), 1),
        }


# ============================================================================
# MESSAGE QUEUE MANAGEMENT
# ============================================================================


class MessageQueueStatus(Enum):
    """Message queue status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"


@dataclass
class MessageQueueEntry:
    """Message queue entry."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message: str = ""
    priority: int = 0
    status: MessageQueueStatus = MessageQueueStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    processed_at: datetime | None = None
    retry_count: int = 0
    max_retries: int = 3
    metadata: dict = field(default_factory=dict)

    def is_expired(self, ttl_seconds: int = 3600) -> bool:
        """Check if entry is expired."""
        return (datetime.now() - self.created_at).total_seconds() > ttl_seconds

    def can_retry(self) -> bool:
        """Check if entry can be retried."""
        return self.retry_count < self.max_retries and self.status == MessageQueueStatus.FAILED

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "message": self.message,
            "priority": self.priority,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "metadata": self.metadata,
        }


class MessageQueueManager:
    """Manages message queue operations."""

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.logger = logging.getLogger(self.__class__.__name__)
        self.queue: list[MessageQueueEntry] = []
        self.statistics = {
            "total_processed": 0,
            "total_failed": 0,
            "total_retries": 0,
            "avg_processing_time": 0.0,
        }

    def enqueue(self, message: str, priority: int = 0, metadata: dict = None) -> str:
        """Enqueue a message."""
        if len(self.queue) >= self.max_size:
            self.logger.warning("Queue is full, removing oldest entry")
            self.queue.pop(0)

        entry = MessageQueueEntry(message=message, priority=priority, metadata=metadata or {})

        # Insert based on priority (higher priority first)
        inserted = False
        for i, existing_entry in enumerate(self.queue):
            if priority > existing_entry.priority:
                self.queue.insert(i, entry)
                inserted = True
                break

        if not inserted:
            self.queue.append(entry)

        self.logger.info(f"Enqueued message with priority {priority}")
        return entry.id

    def dequeue(self) -> MessageQueueEntry | None:
        """Dequeue the highest priority message."""
        if not self.queue:
            return None

        entry = self.queue.pop(0)
        entry.status = MessageQueueStatus.PROCESSING
        entry.processed_at = datetime.now()

        self.logger.info(f"Dequeued message {entry.id}")
        return entry

    def mark_completed(self, entry_id: str) -> bool:
        """Mark an entry as completed."""
        for entry in self.queue:
            if entry.id == entry_id:
                entry.status = MessageQueueStatus.COMPLETED
                self.statistics["total_processed"] += 1
                return True

        self.logger.warning(f"Entry {entry_id} not found")
        return False

    def mark_failed(self, entry_id: str) -> bool:
        """Mark an entry as failed."""
        for entry in self.queue:
            if entry.id == entry_id:
                entry.status = MessageQueueStatus.FAILED
                self.statistics["total_failed"] += 1
                return True

        self.logger.warning(f"Entry {entry_id} not found")
        return False

    def retry_entry(self, entry_id: str) -> bool:
        """Retry a failed entry."""
        for entry in self.queue:
            if entry.id == entry_id and entry.can_retry():
                entry.status = MessageQueueStatus.PENDING
                entry.retry_count += 1
                entry.processed_at = None
                self.statistics["total_retries"] += 1
                return True

        self.logger.warning(f"Entry {entry_id} cannot be retried")
        return False

    def get_queue_status(self) -> dict:
        """Get queue status."""
        status_counts = {}
        for status in MessageQueueStatus:
            status_counts[status.value] = sum(1 for entry in self.queue if entry.status == status)

        return {
            "total_entries": len(self.queue),
            "status_counts": status_counts,
            "statistics": self.statistics,
        }

    def cleanup_expired(self, ttl_seconds: int = 3600) -> int:
        """Clean up expired entries."""
        initial_count = len(self.queue)
        self.queue = [entry for entry in self.queue if not entry.is_expired(ttl_seconds)]
        removed_count = initial_count - len(self.queue)

        if removed_count > 0:
            self.logger.info(f"Cleaned up {removed_count} expired entries")

        return removed_count


# ============================================================================
# METRICS MANAGEMENT
# ============================================================================


@dataclass
class Metric:
    """Metric data structure."""

    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    tags: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "tags": self.tags,
        }


class MetricsManager:
    """Manages system metrics."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.metrics: list[Metric] = []
        self.metric_history: dict[str, list[float]] = {}

    def record_metric(self, name: str, value: float, tags: dict = None) -> bool:
        """Record a metric."""
        try:
            metric = Metric(name=name, value=value, tags=tags or {})
            self.metrics.append(metric)

            if name not in self.metric_history:
                self.metric_history[name] = []
            self.metric_history[name].append(value)

            # Keep only last 1000 values per metric
            if len(self.metric_history[name]) > 1000:
                self.metric_history[name] = self.metric_history[name][-1000:]

            return True
        except Exception as e:
            self.logger.error(f"Failed to record metric {name}: {e}")
            return False

    def get_metric_summary(self, name: str) -> dict:
        """Get metric summary."""
        if name not in self.metric_history:
            return {"error": "Metric not found"}

        values = self.metric_history[name]
        return {
            "name": name,
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "latest": values[-1] if values else None,
        }

    def get_all_metrics(self) -> list[dict]:
        """Get all metrics."""
        return [metric.to_dict() for metric in self.metrics]

    def clear_metrics(self) -> bool:
        """Clear all metrics."""
        try:
            self.metrics.clear()
            self.metric_history.clear()
            self.logger.info("All metrics cleared")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear metrics: {e}")
            return False


# ============================================================================
# WORKSPACE AGENT REGISTRY
# ============================================================================


@dataclass
class AgentInfo:
    """Agent information structure."""

    agent_id: str
    agent_name: str
    agent_type: str
    status: str = "unknown"
    last_seen: datetime = field(default_factory=datetime.now)
    capabilities: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def is_online(self, timeout_seconds: int = 300) -> bool:
        """Check if agent is online."""
        return (datetime.now() - self.last_seen).total_seconds() < timeout_seconds

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "status": self.status,
            "last_seen": self.last_seen.isoformat(),
            "capabilities": self.capabilities,
            "metadata": self.metadata,
        }


class WorkspaceAgentRegistry:
    """Manages workspace agent registry."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.agents: dict[str, AgentInfo] = {}

    def register_agent(self, agent_info: AgentInfo) -> bool:
        """Register an agent."""
        try:
            self.agents[agent_info.agent_id] = agent_info
            self.logger.info(f"Registered agent {agent_info.agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent_info.agent_id}: {e}")
            return False

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        try:
            if agent_id in self.agents:
                del self.agents[agent_id]
                self.logger.info(f"Unregistered agent {agent_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to unregister agent {agent_id}: {e}")
            return False

    def update_agent_status(self, agent_id: str, status: str) -> bool:
        """Update agent status."""
        try:
            if agent_id in self.agents:
                self.agents[agent_id].status = status
                self.agents[agent_id].last_seen = datetime.now()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update agent status {agent_id}: {e}")
            return False

    def get_agent(self, agent_id: str) -> AgentInfo | None:
        """Get agent information."""
        return self.agents.get(agent_id)

    def get_all_agents(self) -> list[AgentInfo]:
        """Get all agents."""
        return list(self.agents.values())

    def get_online_agents(self) -> list[AgentInfo]:
        """Get online agents."""
        return [agent for agent in self.agents.values() if agent.is_online()]

    def get_agents_by_type(self, agent_type: str) -> list[AgentInfo]:
        """Get agents by type."""
        return [agent for agent in self.agents.values() if agent.agent_type == agent_type]

    def get_registry_stats(self) -> dict:
        """Get registry statistics."""
        total_agents = len(self.agents)
        online_agents = len(self.get_online_agents())

        type_counts = {}
        for agent in self.agents.values():
            type_counts[agent.agent_type] = type_counts.get(agent.agent_type, 0) + 1

        return {
            "total_agents": total_agents,
            "online_agents": online_agents,
            "offline_agents": total_agents - online_agents,
            "type_counts": type_counts,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def create_agent_context_manager(agent_id: str = "agent-2") -> AgentContextManager:
    """Create an agent context manager."""
    return AgentContextManager(agent_id)


def create_documentation_service() -> DocumentationService:
    """Create a documentation service."""
    return DocumentationService()


def create_message_queue_manager(max_size: int = 1000) -> MessageQueueManager:
    """Create a message queue manager."""
    return MessageQueueManager(max_size)


def create_metrics_manager() -> MetricsManager:
    """Create a metrics manager."""
    return MetricsManager()


def create_workspace_agent_registry() -> WorkspaceAgentRegistry:
    """Create a workspace agent registry."""
    return WorkspaceAgentRegistry()


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def main():
    """Main execution function."""
    print("Core Manager System - Consolidated Manager Classes")
    print("=" * 50)

    # Create agent context manager
    context_manager = create_agent_context_manager("agent-2")
    context_manager.set_context("phase", "consolidation")
    print(f"Agent context manager created: {context_manager.get_context_summary()}")

    # Create documentation service
    doc_service = create_documentation_service()
    doc_service.index_documentation("consolidation_plan", "Chunk 001 consolidation plan")
    print(f"Documentation service created: {doc_service.get_documentation_stats()}")

    # Create message queue manager
    queue_manager = create_message_queue_manager()
    queue_manager.enqueue("Test message", priority=1)
    print(f"Message queue manager created: {queue_manager.get_queue_status()}")

    # Create metrics manager
    metrics_manager = create_metrics_manager()
    metrics_manager.record_metric("consolidation_progress", 25.0)
    print(
        f"Metrics manager created: {metrics_manager.get_metric_summary('consolidation_progress')}"
    )

    # Create workspace agent registry
    agent_registry = create_workspace_agent_registry()
    agent_info = AgentInfo(
        agent_id="agent-2",
        agent_name="Architecture & Design Specialist",
        agent_type="consolidation",
        capabilities=["analysis", "consolidation", "architecture"],
    )
    agent_registry.register_agent(agent_info)
    print(f"Workspace agent registry created: {agent_registry.get_registry_stats()}")

    print("\nCore Manager System initialization complete!")

    return 0  # Success exit code


if __name__ == "__main__":
    exit_code = main()
    print()
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    exit(exit_code)
