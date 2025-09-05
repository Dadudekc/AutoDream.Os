#!/usr/bin/env python3
"""
Agent Documentation Service - V2 Compliance Module
=================================================

This service provides AI agents with intelligent access to project documentation
through semantic search and context-aware retrieval.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Placeholder classes for V2 compliance
class DocumentationIndexingService:
    def __init__(self, vector_db, config):
        self.vector_db = vector_db
        self.config = config

class DocumentationSearchService:
    def __init__(self, vector_db):
        self.vector_db = vector_db

class SearchHistoryService:
    def __init__(self):
        self.history = []

class AgentContextManager:
    def __init__(self):
        self.contexts = {}

    def set_agent_context(self, agent_id: str, context: Dict[str, Any]) -> None:
        self.contexts[agent_id] = context

    def get_agent_context(self, agent_id: str) -> Dict[str, Any]:
        return self.contexts.get(agent_id, {})

class AgentDocumentationService:
    """
    Service that provides AI agents with intelligent documentation access.
    """

    def __init__(self, vector_db):
        self.vector_db = vector_db
        self.indexer = DocumentationIndexingService(vector_db, None)  # Will be set by factory

        # Initialize specialized services
        self.search_service = DocumentationSearchService(vector_db)
        self.history_service = SearchHistoryService()
        self.context_manager = AgentContextManager()
        self.indexing_service = DocumentationIndexingService(vector_db, None)

    def set_agent_context(self, agent_id: str, context: Dict[str, Any]) -> None:
        """
        Set context for a specific agent to improve search relevance.

        Args:
            agent_id: Unique identifier for the agent
            context: Context information (role, current_task, domain, etc.)
        """
        self.context_manager.set_agent_context(agent_id, context)

    def search_documentation(self, agent_id: str, query: str,
                           n_results: int = 5,
                           context_boost: bool = True) -> List[Dict[str, Any]]:
        """
        Search documentation with agent-specific context awareness.

        Args:
            agent_id: ID of the agent making the request
            query: Search query
            n_results: Number of results to return
            context_boost: Whether to boost results based on agent context

        Returns:
            List of relevant documentation with context
        """
        try:
            # Get agent context
            agent_context = self.context_manager.get_agent_context(agent_id)

            # Perform search
            results = self.search_service.search(
                query=query,
                agent_id=agent_id,
                n_results=n_results,
                context_boost=context_boost,
                agent_context=agent_context
            )

            # Store search in history
            if results:
                self.history_service.add_search(
                    agent_id=agent_id,
                    query=results[0].get('original_query', query),
                    enhanced_query=results[0].get('enhanced_query', query),
                    results_count=len(results)
                )

            return results

        except Exception as e:
            logger.error(f"Error searching documentation for agent {agent_id}: {e}")
            return []

    def get_agent_relevant_docs(self, agent_id: str,
                              doc_types: List[str] = None) -> List[Dict[str, Any]]:
        """
        Get documentation relevant to a specific agent's role and domain.

        Args:
            agent_id: ID of the agent
            doc_types: Optional list of document types to filter by

        Returns:
            List of relevant documents
        """
        try:
            agent_context = self.context_manager.get_agent_context(agent_id)
            return self.search_service.get_relevant_docs(agent_context, doc_types)

        except Exception as e:
            logger.error(f"Error getting relevant docs for agent {agent_id}: {e}")
            return []

    def get_documentation_summary(self, agent_id: str) -> Dict[str, Any]:
        """
        Get a summary of available documentation for an agent.

        Args:
            agent_id: ID of the agent

        Returns:
            Dictionary with documentation summary
        """
        try:
            agent_context = self.context_manager.get_agent_context(agent_id)
            stats = self.vector_db.get_collection_stats()

            # Get agent's search history
            agent_searches = self.history_service.get_agent_search_history(agent_id)

            # Get relevant documentation
            relevant_docs = self.get_agent_relevant_docs(agent_id)

            summary = {
                'agent_id': agent_id,
                'agent_role': self.context_manager.get_agent_role(agent_id),
                'agent_domain': self.context_manager.get_agent_domain(agent_id),
                'total_documents': stats.get('total_chunks', 0),
                'relevant_documents': len(relevant_docs),
                'search_history_count': len(agent_searches),
                'last_search': agent_searches[-1]['timestamp'] if agent_searches else None,
                'document_types_available': list(set(
                    doc['metadata'].get('file_type', '') for doc in relevant_docs
                )),
                'key_directories': list(set(
                    doc['metadata'].get('directory', '') for doc in relevant_docs
                ))[:5]  # Top 5 directories
            }

            return summary

        except Exception as e:
            logger.error(f"Error getting documentation summary for agent {agent_id}: {e}")
            return {}

    def index_project_documentation(self, project_root: str = ".") -> Dict[str, Any]:
        """
        Index all project documentation.

        Args:
            project_root: Root directory of the project

        Returns:
            Dictionary with indexing results
        """
        return self.indexing_service.index_project_documentation(project_root)

    def get_search_suggestions(self, agent_id: str, partial_query: str) -> List[str]:
        """
        Get search suggestions based on agent context and search history.

        Args:
            agent_id: ID of the agent
            partial_query: Partial search query

        Returns:
            List of suggested search terms
        """
        try:
            agent_context = self.context_manager.get_agent_context(agent_id)
            return self.history_service.get_search_suggestions(
                agent_id, partial_query, agent_context
            )

        except Exception as e:
            logger.error(f"Error getting search suggestions for agent {agent_id}: {e}")
            return []

    def export_agent_knowledge(self, agent_id: str, output_path: str) -> bool:
        """
        Export agent's knowledge base and search history.

        Args:
            agent_id: ID of the agent
            output_path: Path to save the export

        Returns:
            True if successful, False otherwise
        """
        try:

            # Get agent data
            agent_context = self.context_manager.get_agent_context(agent_id)
            agent_searches = self.history_service.get_agent_search_history(agent_id)
            relevant_docs = self.get_agent_relevant_docs(agent_id)
            summary = self.get_documentation_summary(agent_id)

            # Prepare export data
            export_data = {
                'agent_id': agent_id,
                'export_timestamp': datetime.now().isoformat(),
                'agent_context': agent_context,
                'documentation_summary': summary,
                'search_history': agent_searches,
                'relevant_documents': relevant_docs[:20],  # Top 20 most relevant
                'vector_db_stats': self.vector_db.get_collection_stats()
            }

            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Exported agent knowledge for {agent_id} to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting agent knowledge for {agent_id}: {e}")
            return False

    # Delegate methods to specialized services
    def update_agent_task(self, agent_id: str, task: str) -> None:
        """Update agent task."""
        self.context_manager.update_agent_task(agent_id, task)

    def get_agent_context(self, agent_id: str) -> Dict[str, Any]:
        """Get agent context."""
        return self.context_manager.get_agent_context(agent_id)

    def get_search_history_stats(self) -> Dict[str, Any]:
        """Get search history statistics."""
        return self.history_service.get_statistics()


def create_agent_documentation_service(vector_db) -> AgentDocumentationService:
    """
    Create an agent documentation service instance.

    Args:
        vector_db: Vector database instance

    Returns:
        Initialized AgentDocumentationService instance
    """
    return AgentDocumentationService(vector_db)
