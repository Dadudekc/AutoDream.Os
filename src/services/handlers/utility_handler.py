#!/usr/bin/env python3
"""
Utility Handler - V2 Compliant Module
====================================

Handles utility commands for messaging system.

V2 Compliance: < 300 lines, single responsibility.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Any

from ..vector_database import get_vector_database_service, search_vector_database
from ..vector_database.vector_database_models import SearchQuery

# Coordinate functionality now handled by consolidated messaging service
from .onboarding_handler import OnboardingHandler

logger = logging.getLogger(__name__)


class UtilityHandler:
    """Handles utility commands for messaging system."""

    def __init__(self):

EXAMPLE USAGE:
==============

# Import the service
from src.services.handlers.utility_handler import Utility_HandlerService

# Initialize service
service = Utility_HandlerService()

# Basic service operation
response = service.handle_request(request_data)
logger.info(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Utility_HandlerService)

# Execute service method
result = service.execute_operation(input_data, context)
logger.info(f"Operation result: {result}")

        """Initialize utility handler."""
        self.logger = logger

    def check_status(self, agent_id: str | None = None) -> dict[str, Any]:
        """Check status of agents or specific agent using onboarding handler.

        Args:
            agent_id: Optional specific agent ID to check

        Returns:
            Dict containing status information
        """
        try:
            onboarding_handler = OnboardingHandler()

            if agent_id:
                # Check specific agent status
                status = onboarding_handler.get_onboarding_status(agent_id)
                if status:
                    return {
                        "agent_id": agent_id,
                        "status": status.get("status", "unknown"),
                        "role": status.get("role", "unknown"),
                        "onboarded_at": status.get("onboarded_at"),
                        "workspace_path": status.get("workspace_path"),
                        "capabilities": status.get("capabilities", []),
                        "vector_db_enabled": status.get("vector_db_enabled", False),
                    }
                else:
                    return {
                        "agent_id": agent_id,
                        "status": "not_found",
                        "error": f"Agent {agent_id} not found in system",
                    }
            else:
                # Check overall system status
                onboarded_agents = onboarding_handler.list_onboarded_agents()

                # Get vector database stats
                vector_db = get_vector_database_service()
                db_stats = vector_db.get_stats() if vector_db else None

                return {
                    "total_agents": len(onboarded_agents),
                    "active_agents": len(
                        onboarded_agents
                    ),  # All onboarded agents are considered active
                    "status": "system_active" if onboarded_agents else "no_agents",
                    "onboarded_agents": onboarded_agents,
                    "vector_database": {
                        "status": "connected" if db_stats else "disconnected",
                        "total_documents": db_stats.total_documents if db_stats else 0,
                        "total_collections": db_stats.total_collections if db_stats else 0,
                    },
                }
        except Exception as e:
            self.logger.error(f"Error checking status: {e}")
            return {"error": str(e)}

    def list_agents(self) -> list[dict[str, Any]]:
        """List all available agents from onboarding handler.

        Returns:
            List of agent information dictionaries
        """
        try:
            onboarding_handler = OnboardingHandler()
            onboarded_agents = onboarding_handler.list_onboarded_agents()

            agents = []
            for agent_id in onboarded_agents:
                status = onboarding_handler.get_onboarding_status(agent_id)
                if status:
                    agents.append(
                        {
                            "agent_id": agent_id,
                            "status": status.get("status", "unknown"),
                            "role": status.get("role", "unknown"),
                            "onboarded_at": status.get("onboarded_at"),
                            "capabilities": status.get("capabilities", []),
                            "workspace_path": status.get("workspace_path"),
                        }
                    )

            return agents
        except Exception as e:
            self.logger.error(f"Error listing agents: {e}")
            return []

    def get_coordinates(self, agent_id: str) -> dict[str, Any] | None:
        """Get coordinates for a specific agent from coordinate file.

        Args:
            agent_id: Agent ID to get coordinates for

        Returns:
            Dict containing coordinate information or None
        """
        try:
            coords_data = load_coords_file()
            if not coords_data:
                self.logger.warning("No coordinate data available")
                return None

            agent_coords = coords_data.get(agent_id)
            if agent_coords:
                return {
                    "agent_id": agent_id,
                    "x": agent_coords.get("x", 0),
                    "y": agent_coords.get("y", 0),
                    "description": agent_coords.get("description", f"Coordinates for {agent_id}"),
                    "last_updated": agent_coords.get("last_updated"),
                    "active": agent_coords.get("active", True),
                }

            # Return default coordinates if not found
            self.logger.warning(f"No coordinates found for {agent_id}, using defaults")
            return {
                "agent_id": agent_id,
                "x": 100,
                "y": 100,
                "description": f"Default coordinates for {agent_id}",
                "active": False,
            }
        except Exception as e:
            self.logger.error(f"Error getting coordinates for {agent_id}: {e}")
            return None

    def get_history(self, agent_id: str | None = None) -> list[dict[str, Any]]:
        """Get message history for agents from vector database.

        Args:
            agent_id: Optional specific agent ID

        Returns:
            List of message history entries
        """
        try:
            if not agent_id:
                # Get general system history
                query = SearchQuery(
                    query="message OR status", collection_name="agent_messages", limit=20
                )
            else:
                # Get specific agent history
                query = SearchQuery(
                    query=f"agent:{agent_id}", collection_name="agent_messages", limit=50
                )

            results = search_vector_database(query)

            history = []
            for result in results:
                history.append(
                    {
                        "timestamp": result.document.created_at.isoformat(),
                        "agent_id": result.document.metadata.get("agent_id", "unknown"),
                        "message": (
                            result.document.content[:200] + "..."
                            if len(result.document.content) > 200
                            else result.document.content
                        ),
                        "type": result.document.document_type.value,
                        "similarity_score": result.similarity_score,
                        "source": result.document.metadata.get("source_file", "unknown"),
                    }
                )

            # Sort by timestamp (most recent first)
            history.sort(key=lambda x: x["timestamp"], reverse=True)

            return history

        except Exception as e:
            self.logger.error(f"Error getting history: {e}")
            return []
