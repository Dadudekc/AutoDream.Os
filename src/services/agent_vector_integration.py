#!/usr/bin/env python3
"""
Agent Vector Integration - Agent Cellphone V2
=============================================

Main orchestrator for agent vector database integration.
V2 Compliance: < 100 lines, facade pattern, single responsibility.

REFACTORED: Split into focused integration classes for V2 compliance
- TaskContextManager: Task context and search operations
- WorkIndexer: Agent work indexing operations
- RecommendationEngine: Recommendation and insight generation
- AgentStatusManager: Agent status and utility functions

Author: Agent-7 (Web Development Specialist)
Mission: V2 Compliance Refactoring
"""

from .agent_status_manager import AgentStatusManager
from .recommendation_engine import RecommendationEngine
from .task_context_manager import TaskContextManager
from .work_indexer import WorkIndexer


class AgentVectorIntegration:
    """
    Main orchestrator for agent vector database integration.

    V2 Compliance: < 100 lines, facade pattern, single responsibility.
    This class orchestrates all integration components.
    """

    def __init__(self, agent_id: str, config_path: str | None = None):
        """
        Initialize agent vector integration orchestrator.

        Args:
            agent_id: Agent identifier
            config_path: Optional path to vector database config
        """
        self.agent_id = agent_id

        # Initialize specialized components
        self.task_context = TaskContextManager(agent_id, config_path)
        self.work_indexer = WorkIndexer(agent_id, config_path)
        self.recommendations = RecommendationEngine(agent_id, config_path)
        self.status_manager = AgentStatusManager(agent_id, config_path)

    def get_task_context(self, task_description: str):
        """Delegate to task context manager."""
        return self.task_context.get_task_context(task_description)

    def index_agent_work(self, file_path: str, work_type: str = "code"):

EXAMPLE USAGE:
==============

# Import the service
from src.services.agent_vector_integration import Agent_Vector_IntegrationService

# Initialize service
service = Agent_Vector_IntegrationService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Agent_Vector_IntegrationService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

        """Delegate to work indexer."""
        return self.work_indexer.index_agent_work(file_path, work_type)

    def index_inbox_messages(self):
        """Delegate to work indexer."""
        return self.work_indexer.index_inbox_messages()

    def get_agent_recommendations(self, context: str):
        """Delegate to recommendation engine."""
        return self.recommendations.get_agent_recommendations(context)

    def get_agent_status(self):
        """Delegate to status manager."""
        return self.status_manager.get_agent_status()

    def get_integration_stats(self):
        """Delegate to status manager."""
        return self.status_manager.get_integration_stats()

    def optimize_workflow(self, workflow_data):
        """Delegate to recommendation engine."""
        return self.recommendations.optimize_workflow(workflow_data)


def create_agent_vector_integration(agent_id: str) -> AgentVectorIntegration:
    """
    Factory function to create agent vector integration.

    Args:
        agent_id: Agent identifier

    Returns:
        AgentVectorIntegration instance
    """
    return AgentVectorIntegration(agent_id)
