#!/usr/bin/env python3
"""
Agent Vector Integration - Agent Cellphone V2
=============================================

Seamless integration between agents and vector database for intelligent workflows.
Provides simple, agent-friendly interface for vector database operations.

V2 Compliance: < 300 lines, single responsibility, agent integration.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from typing import Optional, Dict, Any, List
from ..core.unified_import_system import logging


class AgentVectorIntegration:
    """
    Seamless vector database integration for agent workflows.

    Provides intelligent context, recommendations, and knowledge management
    for agent cycles and task execution.
    """

    def __init__(self, agent_id: str, config_path: Optional[str] = None):
        """
        Initialize agent vector integration.

        Args:
            agent_id: Agent identifier
            config_path: Optional path to vector database config
        """
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)

        # Load configuration
        self.config = load_vector_database_config(config_path)

        # Initialize vector integration
        self.vector_integration = VectorMessagingIntegration(self.config)

        # Agent workspace path
        self.workspace_path = get_unified_utility().Path(f"agent_workspaces/{agent_id}")

        self.get_logger(__name__).info(f"Vector integration initialized for {agent_id}")

    def get_task_context(self, task_description: str) -> Dict[str, Any]:
        """
        Get intelligent context for a task.

        Args:
            task_description: Description of the current task

        Returns:
            Dict containing context, recommendations, and similar solutions
        """
        try:
            # Search for similar tasks and solutions
            similar_tasks = self.vector_integration.search_all(
                query_text=task_description, agent_id=self.agent_id, limit=5
            )

            # Get related messages
            related_messages = self.vector_integration.search_messages(
                query_text=task_description, agent_id=self.agent_id, limit=3
            )

            # Get devlog insights
            devlog_insights = self.vector_integration.search_devlogs(
                query_text=task_description, agent_id=self.agent_id, limit=3
            )

            return {
                "task_description": task_description,
                "similar_tasks": [self._format_search_result(r) for r in similar_tasks],
                "related_messages": [
                    self._format_search_result(r) for r in related_messages
                ],
                "devlog_insights": [
                    self._format_search_result(r) for r in devlog_insights
                ],
                "recommendations": self._generate_recommendations(similar_tasks),
                "context_loaded": True,
            }

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting task context: {e}")
            return {
                "task_description": task_description,
                "error": str(e),
                "context_loaded": False,
            }

    def index_agent_work(self, file_path: str, work_type: str = "code") -> bool:
        """
        Index agent's completed work to vector database.

        Args:
            file_path: Path to the file to index
            work_type: Type of work (code, documentation, test, etc.)

        Returns:
            True if successfully indexed
        """
        try:
            file_path = get_unified_utility().Path(file_path)
            if not file_path.exists():
                self.get_logger(__name__).error(f"File not found: {file_path}")
                return False

            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Determine document type
            if file_path.suffix in [".py", ".js", ".ts"]:
                doc_type = DocumentType.CODE
            elif file_path.suffix in [".md", ".txt"]:
                doc_type = DocumentType.DOCUMENTATION
            else:
                doc_type = DocumentType.DOCUMENTATION

            # Create document

            doc = VectorDocument(
                content=content,
                document_type=doc_type,
                source_file=str(file_path),
                agent_id=self.agent_id,
                tags=[work_type, file_path.suffix[1:], "agent_work"],
            )

            # Add to database
            success = self.vector_integration.vector_db.add_document(doc)

            if success:
                self.get_logger(__name__).info(f"Indexed {work_type} work: {file_path}")
                return True
            else:
                self.get_logger(__name__).error(f"Failed to index work: {file_path}")
                return False

        except Exception as e:
            self.get_logger(__name__).error(f"Error indexing agent work: {e}")
            return False

    def index_inbox_messages(self) -> int:
        """
        Index agent's inbox messages for intelligent search.

        Returns:
            Number of messages indexed
        """
        try:
            inbox_path = self.workspace_path / "inbox"
            if not inbox_path.exists():
                self.get_logger(__name__).warning(f"Inbox not found: {inbox_path}")
                return 0

            indexed_count = self.vector_integration.index_inbox_files(
                self.agent_id, str(inbox_path)
            )

            self.get_logger(__name__).info(
                f"Indexed {indexed_count} inbox messages for {self.agent_id}"
            )
            return indexed_count

        except Exception as e:
            self.get_logger(__name__).error(f"Error indexing inbox messages: {e}")
            return 0

    def get_success_patterns(self, task_type: str) -> List[Dict[str, Any]]:
        """
        Get success patterns for a specific task type.

        Args:
            task_type: Type of task (syntax_fix, refactoring, etc.)

        Returns:
            List of success patterns and recommendations
        """
        try:
            # Search for successful completions of similar tasks
            success_results = self.vector_integration.search_all(
                query_text=f"successful {task_type} completion",
                agent_id=self.agent_id,
                limit=5,
            )

            patterns = []
            for result in success_results:
                if result.similarity_score > 0.7:  # High similarity
                    patterns.append(
                        {
                            "task_type": task_type,
                            "similarity": result.similarity_score,
                            "content": result.document.content[:200] + "...",
                            "source": result.document.source_file,
                            "tags": result.document.tags,
                        }
                    )

            return patterns

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting success patterns: {e}")
            return []

    def get_agent_insights(self) -> Dict[str, Any]:
        """
        Get comprehensive insights about the agent's work patterns.

        Returns:
            Dict containing agent insights and recommendations
        """
        try:
            # Get agent's work history
            work_history = self.vector_integration.search_all(
                query_text=f"agent {self.agent_id} work completion",
                agent_id=self.agent_id,
                limit=10,
            )

            # Get communication patterns
            comm_patterns = self.vector_integration.search_messages(
                query_text=f"agent {self.agent_id} communication",
                agent_id=self.agent_id,
                limit=5,
            )

            # Calculate insights
            total_work = len(work_history)
            high_similarity_work = len(
                [w for w in work_history if w.similarity_score > 0.8]
            )

            return {
                "agent_id": self.agent_id,
                "total_work_items": total_work,
                "high_quality_work": high_similarity_work,
                "work_quality_score": high_similarity_work / max(total_work, 1),
                "recent_work": [
                    self._format_search_result(w) for w in work_history[:3]
                ],
                "communication_patterns": [
                    self._format_search_result(c) for c in comm_patterns
                ],
                "recommendations": self._generate_agent_recommendations(work_history),
            }

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting agent insights: {e}")
            return {"agent_id": self.agent_id, "error": str(e)}

    def _format_search_result(self, result) -> Dict[str, Any]:
        """Format search result for agent consumption."""
        return {
            "similarity": result.similarity_score,
            "content": (
                result.document.content[:150] + "..."
                if len(result.document.content) > 150
                else result.document.content
            ),
            "type": result.document.document_type.value,
            "source": result.document.source_file,
            "tags": result.document.tags,
        }

    def _generate_recommendations(self, similar_tasks) -> List[str]:
        """Generate recommendations based on similar tasks."""
        recommendations = []

        if similar_tasks:
            # Extract common patterns
            tags = []
            for task in similar_tasks:
                if get_unified_validator().validate_hasattr(task, "document") and task.document.tags:
                    tags.extend(task.document.tags)

            if tags:

                common_tags = Counter(tags).most_common(3)
                for tag, count in common_tags:
                    recommendations.append(
                        f"Consider using {tag} approach (used in {count} similar tasks)"
                    )

        if not get_unified_validator().validate_required(recommendations):
            recommendations.append(
                "No specific patterns found - proceed with standard approach"
            )

        return recommendations

    def _generate_agent_recommendations(self, work_history) -> List[str]:
        """Generate agent-specific recommendations."""
        recommendations = []

        if work_history:
            avg_similarity = sum(w.similarity_score for w in work_history) / len(
                work_history
            )

            if avg_similarity > 0.8:
                recommendations.append(
                    "Excellent work quality - maintain current approach"
                )
            elif avg_similarity > 0.6:
                recommendations.append(
                    "Good work quality - consider improving consistency"
                )
            else:
                recommendations.append(
                    "Focus on improving work quality and consistency"
                )

        return recommendations


def create_agent_vector_integration(agent_id: str) -> AgentVectorIntegration:
    """
    Factory function to create agent vector integration.

    Args:
        agent_id: Agent identifier

    Returns:
        AgentVectorIntegration instance
    """
    return AgentVectorIntegration(agent_id)

