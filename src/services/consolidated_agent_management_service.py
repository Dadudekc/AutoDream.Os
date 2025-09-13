#!/usr/bin/env python3
"""
Consolidated Agent Management Service - V2 Compliant Module
==========================================================

Unified agent management service consolidating:
- agent_assignment_manager.py (principle assignments)
- agent_status_manager.py (status tracking)
- agent_vector_integration_core.py (vector integration)
- agent_vector_integration_operations.py (vector operations)
- agent_vector_utils.py (vector utilities)

V2 Compliance: < 400 lines, single responsibility for all agent management operations.

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Phase 2 Consolidation - Chunk 002 (Services)
License: MIT
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from .architectural_models import ArchitecturalPrinciple
from .utils.vector_config_utils import load_simple_config

logger = logging.getLogger(__name__)


class ConsolidatedAgentManagementService:
    """Unified agent management service combining assignment, status, and vector integration."""

    def __init__(
        self,
        agent_id: str = "default",
        config_path: str = "src/config/architectural_assignments.json",
    ):
        """Initialize the consolidated agent management service."""
        self.agent_id = agent_id
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.assignments = self._load_assignments()
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")
        self.config = load_simple_config(agent_id, config_path)

        # Initialize vector integration
        self.vector_integration = self._create_vector_integration()

        self.logger.info(f"ConsolidatedAgentManagementService initialized for {agent_id}")

    def _load_assignments(self) -> dict[str, ArchitecturalPrinciple]:
        """Load agent assignments from configuration."""
        # Default assignments
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

        assignments = default_assignments.copy()

        # Try to load from configuration file
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path) as f:
                    config = json.load(f)
                    # Convert string principles back to enum
                    for agent, principle_str in config.items():
                        principle = ArchitecturalPrinciple(principle_str)
                        assignments[agent] = principle
            except Exception:
                # Use defaults if config loading fails
                pass

        return assignments

    def _create_vector_integration(self) -> dict[str, Any]:
        """Create vector integration with fallback handling."""
        try:
            # Try to import and initialize vector database service
            from .consolidated_vector_service import ConsolidatedVectorService

            vector_service = ConsolidatedVectorService(self.agent_id)
            return {"status": "connected", "service": vector_service}
        except Exception as e:
            self.logger.warning(f"Vector DB not available: {e}")
            return {"status": "disconnected", "error": str(e)}

    def _save_assignments(self) -> None:
        """Save assignments to configuration file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            # Convert enum values to strings for JSON serialization
            config = {agent: principle.value for agent, principle in self.assignments.items()}
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception:
            # Silently fail if saving fails
            pass

    # Assignment Management Methods
    def get_agent_principle(self, agent_id: str) -> ArchitecturalPrinciple | None:
        """Get the architectural principle assigned to an agent."""
        return self.assignments.get(agent_id)

    def assign_principle(self, agent_id: str, principle: ArchitecturalPrinciple) -> None:
        """Assign a principle to an agent."""
        self.assignments[agent_id] = principle
        self._save_assignments()

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

    # Status Management Methods
    def get_agent_status(self) -> dict[str, Any]:
        """Get comprehensive agent status."""
        try:
            # Get recent work count from vector database
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
                "architectural_principle": self.get_agent_principle(self.agent_id),
            }

        except Exception as e:
            self.logger.error(f"Error getting agent status: {e}")
            return {"agent_id": self.agent_id, "status": "error", "error": str(e)}

    def get_integration_stats(self) -> dict[str, Any]:
        """Get integration statistics and health metrics."""
        try:
            # Get actual stats from vector database
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

            # Use consolidated vector service
            results = self.vector_integration["service"].search_documents(
                query=f"agent:{self.agent_id}", limit=100
            )
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

            # Find most recent file modification
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

            stats = self.vector_integration["service"].get_collection_stats()
            return stats.total_documents
        except Exception:
            return 0

    def _get_agent_documents(self) -> int:
        """Get documents specific to this agent."""
        try:
            if self.vector_integration["status"] != "connected":
                return 0

            results = self.vector_integration["service"].search_documents(
                query=f"agent:{self.agent_id}", limit=1000
            )
            return len(results)
        except Exception:
            return 0

    # Vector Integration Methods
    def index_agent_work(self, work_content: str, work_type: str = "general") -> bool:
        """Index agent work content."""
        try:
            if self.vector_integration["status"] != "connected":
                return False

            result = self.vector_integration["service"].index_agent_work(work_content, work_type)
            return result.success
        except Exception as e:
            self.logger.error(f"Error indexing work: {e}")
            return False

    def search_agent_work(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Search agent work using vector database."""
        try:
            if self.vector_integration["status"] != "connected":
                return []

            results = self.vector_integration["service"].search_documents(query=query, limit=limit)

            return [
                {
                    "content": result.document.content,
                    "similarity": result.similarity,
                    "metadata": result.document.metadata,
                    "document_id": result.document.id,
                }
                for result in results
            ]
        except Exception as e:
            self.logger.error(f"Error searching work: {e}")
            return []

    def get_agent_context(self, task_description: str) -> dict[str, Any]:
        """Get task context using vector search."""
        try:
            if self.vector_integration["status"] != "connected":
                return {"context": [], "error": "Vector integration not available"}

            context = self.vector_integration["service"].get_task_context(task_description)
            return context
        except Exception as e:
            self.logger.error(f"Error getting context: {e}")
            return {"context": [], "error": str(e)}

    # Configuration and Utility Methods
    def get_agent_config(self) -> dict[str, Any]:
        """Get agent configuration."""
        return {
            "agent_id": self.agent_id,
            "workspace_path": str(self.workspace_path),
            "architectural_principle": self.get_agent_principle(self.agent_id),
            "vector_integration_status": self.vector_integration["status"],
            "config_loaded": bool(self.config),
        }

    def reload_config(self) -> bool:
        """Reload agent configuration."""
        try:
            self.assignments = self._load_assignments()
            self.config = load_simple_config(self.agent_id, self.config_path)
            self.vector_integration = self._create_vector_integration()
            return True
        except Exception as e:
            self.logger.error(f"Error reloading config: {e}")
            return False

    def get_comprehensive_agent_report(self) -> dict[str, Any]:
        """Get comprehensive agent report."""
        return {
            "agent_id": self.agent_id,
            "status": self.get_agent_status(),
            "integration_stats": self.get_integration_stats(),
            "assignments": self.get_all_assignments(),
            "config": self.get_agent_config(),
            "generated_at": datetime.now().isoformat(),
        }
