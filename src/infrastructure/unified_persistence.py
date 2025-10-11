#!/usr/bin/env python3
"""
Unified Persistence Service - V2 Compliance Module
==================================================

Consolidated data persistence system following SOLID principles.
Combines functionality from:
- sqlite_agent_repo.py (agent persistence)
- sqlite_task_repo.py (task persistence)
- __init__.py (module coordination)

SOLID Implementation:
- SRP: Each repository handles one entity type
- OCP: Extensible repository system
- DIP: Dependencies injected via constructor
- ISP: Separate interfaces for different persistence operations

Author: Agent-3 (DevOps Specialist)
Refactored by: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

import logging
from typing import Any

from .persistence.agent_repository import AgentRepository
from .persistence.database_connection import DatabaseConnection
from .persistence.persistence_models import Agent, PersistenceConfig, Task
from .persistence.persistence_statistics import PersistenceStatistics
from .persistence.task_repository import TaskRepository

logger = logging.getLogger(__name__)


class UnifiedPersistenceService:
    """Main unified persistence service interface."""

    def __init__(self, config: PersistenceConfig | None = None):
        """Initialize unified persistence service."""
        self.config = config or PersistenceConfig()

        # Initialize components
        self.db_connection = DatabaseConnection(self.config)
        self.agent_repo = AgentRepository(self.db_connection)
        self.task_repo = TaskRepository(self.db_connection)
        self.stats = PersistenceStatistics(self.db_connection)

    # Agent operations
    def save_agent(self, agent: Agent) -> None:
        """Save an agent."""
        self.agent_repo.save(agent)

    def get_agent(self, agent_id: str) -> Agent | None:
        """Get an agent by ID."""
        return self.agent_repo.get(agent_id)

    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent."""
        return self.agent_repo.delete(agent_id)

    def list_agents(self, limit: int = 1000) -> list[Agent]:
        """List all agents."""
        return list(self.agent_repo.list_all(limit))

    def get_active_agents(self) -> list[Agent]:
        """Get all active agents."""
        return list(self.agent_repo.get_active())

    def get_available_agents(self) -> list[Agent]:
        """Get agents that can accept more tasks."""
        return list(self.agent_repo.get_available())

    def get_agents_by_capability(self, capability: str) -> list[Agent]:
        """Get agents by capability."""
        return list(self.agent_repo.get_by_capability(capability))

    # Task operations
    def save_task(self, task: Task) -> None:
        """Save a task."""
        self.task_repo.save(task)

    def get_task(self, task_id: str) -> Task | None:
        """Get a task by ID."""
        return self.task_repo.get(task_id)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        return self.task_repo.delete(task_id)

    def list_tasks(self, limit: int = 1000) -> list[Task]:
        """List all tasks."""
        return list(self.task_repo.list_all(limit))

    def get_tasks_by_agent(self, agent_id: str, limit: int = 100) -> list[Task]:
        """Get tasks by agent ID."""
        return list(self.task_repo.get_by_agent(agent_id, limit))

    def get_pending_tasks(self, limit: int = 100) -> list[Task]:
        """Get pending tasks."""
        return list(self.task_repo.get_pending(limit))

    # Statistics and maintenance
    def get_database_stats(self) -> dict[str, Any]:
        """Get database statistics."""
        return self.stats.get_database_stats()

    def optimize_database(self) -> bool:
        """Optimize database performance."""
        try:
            # Vacuum database to reclaim space
            self.db_connection.execute_update("VACUUM")

            # Rebuild indexes
            self.db_connection.execute_update("REINDEX")

            logger.info("✅ Database optimization completed")
            return True

        except Exception as e:
            logger.error(f"❌ Database optimization failed: {e}")
            return False

    def backup_database(self, backup_path: str) -> bool:
        """Create a backup of the database."""
        try:
            import shutil
            from pathlib import Path

            source = Path(self.config.db_path)
            destination = Path(backup_path)

            if not source.exists():
                logger.error("❌ Source database does not exist")
                return False

            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

            logger.info(f"✅ Database backed up to {backup_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Database backup failed: {e}")
            return False


def create_persistence_service(db_path: str = "data/unified.db") -> UnifiedPersistenceService:
    """Factory function to create persistence service."""
    config = PersistenceConfig(db_path=db_path)
    return UnifiedPersistenceService(config)


if __name__ == "__main__":
    # Example usage
    service = create_persistence_service()

    # Get database stats
    stats = service.get_database_stats()
    print(f"📊 Database Stats: {stats}")

    # List agents
    agents = service.list_agents(limit=10)
    print(f"📋 Agents: {len(agents)}")

    # List tasks
    tasks = service.list_tasks(limit=10)
    print(f"📋 Tasks: {len(tasks)}")
