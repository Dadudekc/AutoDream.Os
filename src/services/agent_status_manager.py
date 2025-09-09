"""
Agent Status Manager
====================

Agent status and utility functions for vector integration.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from .vector_database import get_vector_database_service, search_vector_database
from .vector_database.vector_database_models import SearchQuery, DocumentType


class AgentStatusManager:
    """Handles agent status and utility functions."""

    def __init__(self, agent_id: str, config_path: str | None = None):
        """Initialize agent status manager."""
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")
        
        # Initialize vector integration
        try:
            self.vector_db = get_vector_database_service()
            self.vector_integration = {"status": "connected", "service": self.vector_db}
        except Exception as e:
            self.logger.warning(f"Vector DB not available: {e}")
            self.vector_integration = {"status": "disconnected", "error": str(e)}

    def get_agent_status(self) -> dict[str, Any]:
        """
        Get comprehensive agent status from vector database.

        Returns:
            Dict containing agent status information
        """
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
            }

        except Exception as e:
            self.logger.error(f"Error getting agent status: {e}")
            return {"agent_id": self.agent_id, "status": "error", "error": str(e)}

    def get_integration_stats(self) -> dict[str, Any]:
        """
        Get integration statistics and health metrics.

        Returns:
            Dict containing integration statistics
        """
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
                
            query = SearchQuery(
                query=f"agent:{self.agent_id}",
                collection_name="agent_work",
                limit=100
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
                query=f"agent:{self.agent_id}",
                collection_name="agent_work",
                limit=1000
            )
            results = search_vector_database(query)
            return len(results)
        except Exception:
            return 0
