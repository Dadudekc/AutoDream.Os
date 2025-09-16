"""
Task Context Manager
====================

Task context and search operations for agent vector integration.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
"""

import logging
from typing import Any

from .agent_vector_utils import format_search_result, generate_recommendations
from .vector_database import get_vector_database_service, search_vector_database
from .vector_database.vector_database_models import SearchQuery


class TaskContextManager:
    """Manages task context and search operations."""

    def __init__(self, agent_id: str, config_path: str | None = None):
        """Initialize the task context manager."""
        self.agent_id = agent_id
        self.config_path = config_path
        self.context = {}
service = Task_Context_ManagerService()

# Basic service operation
response = service.handle_request(request_data)
logger.info(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Task_Context_ManagerService)

# Execute service method
result = service.execute_operation(input_data, context)
logger.info(f"Operation result: {result}")

        """Initialize task context manager."""
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)

        # Initialize vector integration
        try:
            self.vector_db = get_vector_database_service()
            self.vector_integration = {"status": "connected", "service": self.vector_db}
        except Exception as e:
            self.logger.warning(f"Vector DB not available: {e}")
            self.vector_integration = {"status": "disconnected", "error": str(e)}

    def get_task_context(self, task_description: str) -> dict[str, Any]:
        """
        Get intelligent context for a task.

        Args:
            task_description: Description of the current task

        Returns:
            Dict containing context, recommendations, and similar solutions
        """
        try:
            if self.vector_integration["status"] != "connected":
                return self._get_fallback_context(task_description)

            # Search for similar tasks and solutions
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
