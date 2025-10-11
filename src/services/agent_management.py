"""
Unified Agent Management Module
================================

Consolidates agent assignment, status, and task context management.
V2 Compliance: Single module for all agent management operations.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from .agent_vector_utils import format_search_result, generate_recommendations
from .architectural_models import ArchitecturalPrinciple
from .vector_database import get_vector_database_service, search_vector_database
from .vector_database.vector_database_models import SearchQuery


class AgentAssignmentManager:
    """Manages agent-to-principle assignments with persistence."""

    def __init__(self, config_path: str = "src/config/architectural_assignments.json"):
        """Initialize assignment manager."""
        self.config_path = config_path
        self.assignments: dict[str, ArchitecturalPrinciple] = {}
        self._load_assignments()

    def _load_assignments(self) -> None:
        """Load agent assignments from configuration."""
        default_assignments = {
            "Agent-1": ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
            "Agent-2": ArchitecturalPrinciple.OPEN_CLOSED,
            "Agent-3": ArchitecturalPrinciple.LISKOV_SUBSTITUTION,
            "Agent-4": ArchitecturalPrinciple.INTERFACE_SEGREGATION,
            "Agent-5": ArchitecturalPrinciple.DEPENDENCY_INVERSION,
            "Agent-6": ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH,
            "Agent-7": ArchitecturalPrinciple.DONT_REPEAT_YOURSELF,
            "Agent-8": ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
        }

        self.assignments = default_assignments.copy()

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path) as f:
                    config = json.load(f)
                    for agent, principle_str in config.items():
                        principle = ArchitecturalPrinciple(principle_str)
                        self.assignments[agent] = principle
            except Exception:
                pass

    def get_agent_principle(self, agent_id: str) -> ArchitecturalPrinciple | None:
        """Get the architectural principle assigned to an agent."""
        return self.assignments.get(agent_id)

    def assign_principle(self, agent_id: str, principle: ArchitecturalPrinciple) -> None:
        """Assign a principle to an agent."""
        self.assignments[agent_id] = principle
        self._save_assignments()

    def _save_assignments(self) -> None:
        """Save assignments to configuration file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            config = {agent: principle.value for agent, principle in self.assignments.items()}
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass

    def get_all_assignments(self) -> dict[str, ArchitecturalPrinciple]:
        """Get all agent assignments."""
        return self.assignments.copy()

    def get_agents_by_principle(self, principle: ArchitecturalPrinciple) -> list[str]:
        """Get all agents assigned to a specific principle."""
        return [
            agent
            for agent, assigned_principle in self.assignments.items()
            if assigned_principle == principle
        ]


class AgentStatusManager:
    """Handles agent status and utility functions."""

    def __init__(self, agent_id: str, config_path: str | None = None):
        """Initialize agent status manager."""
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")

        try:
            self.vector_db = get_vector_database_service()
            self.vector_integration = {"status": "connected", "service": self.vector_db}
        except Exception as e:
            self.logger.warning(f"Vector DB not available: {e}")
            self.vector_integration = {"status": "disconnected", "error": str(e)}

    def get_agent_status(self) -> dict[str, Any]:
        """Get comprehensive agent status from vector database."""
        try:
            recent_work_count = self._get_recent_work_count()
            pending_tasks_count = self._get_pending_tasks_count()
            last_activity = self._get_last_activity()

            return {
                "agent_id": self.agent_id,
                "status": "active",
                "recent_work_count": recent_work_count,
                "pending_tasks_count": pending_tasks_count,
                "last_activity": last_activity,
                "workspace_path": str(self.workspace_path),
                "vector_db_status": self.vector_integration["status"],
            }

        except Exception as e:
            self.logger.error(f"Error getting agent status: {e}")
            return {"agent_id": self.agent_id, "status": "error", "error": str(e)}

    def get_integration_stats(self) -> dict[str, Any]:
        """Get integration statistics and health metrics."""
        try:
            total_documents = self._get_total_documents()
            agent_documents = self._get_agent_documents()

            return {
                "total_documents": total_documents,
                "agent_documents": agent_documents,
                "integration_status": "healthy",
                "last_sync": datetime.now().isoformat(),
                "vector_db_status": self.vector_integration["status"],
            }

        except Exception as e:
            self.logger.error(f"Error getting integration stats: {e}")
            return {"integration_status": "error", "error": str(e)}

    def _get_recent_work_count(self) -> int:
        """Get count of recent work items."""
        try:
            if self.vector_integration["status"] != "connected":
                return 0

            query = SearchQuery(
                query=f"agent:{self.agent_id}", collection_name="agent_work", limit=100
            )
            results = search_vector_database(query)
            return len(results)
        except Exception:
            return 0

    def _get_pending_tasks_count(self) -> int:
        """Get count of pending tasks."""
        try:
            if not self.workspace_path.exists():
                return 0

            inbox_path = self.workspace_path / "inbox"
            if not inbox_path.exists():
                return 0

            return len(list(inbox_path.glob("*.md")))
        except Exception:
            return 0

    def _get_last_activity(self) -> str:
        """Get last activity timestamp."""
        try:
            if not self.workspace_path.exists():
                return datetime.now().isoformat()

            recent_files = []
            for pattern in ["**/*.py", "**/*.md", "**/*.json"]:
                recent_files.extend(self.workspace_path.glob(pattern))

            if recent_files:
                latest_file = max(recent_files, key=lambda f: f.stat().st_mtime)
                return datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat()

            return datetime.now().isoformat()
        except Exception:
            return datetime.now().isoformat()

    def _get_total_documents(self) -> int:
        """Get total documents in vector database."""
        try:
            if self.vector_integration["status"] != "connected":
                return 0

            stats = self.vector_db.get_stats()
            return stats.total_documents
        except Exception:
            return 0

    def _get_agent_documents(self) -> int:
        """Get documents specific to this agent."""
        try:
            if self.vector_integration["status"] != "connected":
                return 0

            query = SearchQuery(
                query=f"agent:{self.agent_id}", collection_name="agent_work", limit=1000
            )
            results = search_vector_database(query)
            return len(results)
        except Exception:
            return 0


class TaskContextManager:
    """Manages task context and search operations."""

    def __init__(self, agent_id: str, config_path: str | None = None):
        """Initialize task context manager."""
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)

        try:
            self.vector_db = get_vector_database_service()
            self.vector_integration = {"status": "connected", "service": self.vector_db}
        except Exception as e:
            self.logger.warning(f"Vector DB not available: {e}")
            self.vector_integration = {"status": "disconnected", "error": str(e)}

    def get_task_context(self, task_description: str) -> dict[str, Any]:
        """Get intelligent context for a task."""
        try:
            if self.vector_integration["status"] != "connected":
                return self._get_fallback_context(task_description)

            similar_tasks = self._search_similar_tasks(task_description)
            related_messages = self._search_related_messages(task_description)
            devlog_insights = self._search_devlog_insights(task_description)

            return {
                "task_description": task_description,
                "similar_tasks": [format_search_result(r) for r in similar_tasks],
                "related_messages": [format_search_result(r) for r in related_messages],
                "devlog_insights": [format_search_result(r) for r in devlog_insights],
                "recommendations": generate_recommendations(similar_tasks),
                "context_loaded": True,
                "search_results_count": len(similar_tasks)
                + len(related_messages)
                + len(devlog_insights),
            }

        except Exception as e:
            self.logger.error(f"Error getting task context: {e}")
            return {
                "task_description": task_description,
                "error": str(e),
                "context_loaded": False,
            }

    def _search_similar_tasks(self, task_description: str) -> list[Any]:
        """Search for similar tasks in agent work."""
        try:
            query = SearchQuery(query=task_description, collection_name="agent_work", limit=5)
            return search_vector_database(query)
        except Exception as e:
            self.logger.error(f"Error searching similar tasks: {e}")
            return []

    def _search_related_messages(self, task_description: str) -> list[Any]:
        """Search for related messages in agent inbox."""
        try:
            query = SearchQuery(query=task_description, collection_name="agent_messages", limit=3)
            return search_vector_database(query)
        except Exception as e:
            self.logger.error(f"Error searching related messages: {e}")
            return []

    def _search_devlog_insights(self, task_description: str) -> list[Any]:
        """Search for devlog insights related to the task."""
        try:
            query = SearchQuery(
                query=f"devlog {task_description}", collection_name="agent_work", limit=3
            )
            return search_vector_database(query)
        except Exception as e:
            self.logger.error(f"Error searching devlog insights: {e}")
            return []

    def _get_fallback_context(self, task_description: str) -> dict[str, Any]:
        """Get fallback context when vector DB is unavailable."""
        return {
            "task_description": task_description,
            "similar_tasks": [],
            "related_messages": [],
            "devlog_insights": [],
            "recommendations": ["Proceed with standard approach - vector DB unavailable"],
            "context_loaded": False,
            "fallback_mode": True,
        }
