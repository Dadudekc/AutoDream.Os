#!/usr/bin/env python3
"""
Knowledge Database API - Agent Cellphone V2
===========================================

Python API wrapper for the knowledge database system.
Agents can use this to programmatically interact with the knowledge base.

Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""

import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import hashlib
from pathlib import Path

from .knowledge_database import KnowledgeDatabase, KnowledgeEntry


class KnowledgeAPI:
    """Python API for knowledge database operations"""

    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db = KnowledgeDatabase(db_path)
        self.logger = logging.getLogger(f"{__name__}.KnowledgeAPI")

    def add_knowledge(
        self,
        title: str,
        content: str,
        category: str,
        agent_id: str,
        tags: Optional[List[str]] = None,
        source: str = "agent_api",
        confidence: float = 0.8,
        related_entries: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        Add new knowledge entry via API

        Args:
            title: Knowledge entry title
            content: Knowledge content
            category: Knowledge category
            agent_id: ID of the agent adding the knowledge
            tags: Optional list of tags
            source: Knowledge source
            confidence: Confidence level (0.0-1.0)
            related_entries: Optional list of related entry IDs
            metadata: Optional additional metadata

        Returns:
            Entry ID if successful, None otherwise
        """
        try:
            # Generate unique ID
            entry_id = hashlib.sha256(
                f"{title}{content}{agent_id}".encode()
            ).hexdigest()[:16]

            # Set defaults
            tags = tags or []
            related_entries = related_entries or []
            metadata = metadata or {}

            # Add API metadata
            metadata.update(
                {
                    "api_created": True,
                    "api_timestamp": datetime.now().isoformat(),
                    "api_version": "1.0",
                }
            )

            # Create entry
            entry = KnowledgeEntry(
                id=entry_id,
                title=title,
                content=content,
                category=category,
                tags=tags,
                source=source,
                confidence=confidence,
                created_at=datetime.now().timestamp(),
                updated_at=datetime.now().timestamp(),
                agent_id=agent_id,
                related_entries=related_entries,
                metadata=metadata,
            )

            if self.db.store_knowledge(entry):
                self.logger.info(f"Knowledge entry added via API: {entry_id}")
                return entry_id
            else:
                self.logger.error(f"Failed to store knowledge entry via API: {title}")
                return None

        except Exception as e:
            self.logger.error(f"API add_knowledge failed: {e}")
            return None

    def search_knowledge(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search knowledge base via API

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of knowledge entries as dictionaries
        """
        try:
            results = self.db.search_knowledge(query, limit)

            # Convert to API-friendly format
            api_results = []
            for entry, relevance in results:
                api_results.append(
                    {
                        "id": entry.id,
                        "title": entry.title,
                        "content": entry.content,
                        "category": entry.category,
                        "tags": entry.tags,
                        "source": entry.source,
                        "confidence": entry.confidence,
                        "agent_id": entry.agent_id,
                        "relevance_score": relevance,
                        "created_at": entry.created_at,
                        "updated_at": entry.updated_at,
                        "related_entries": entry.related_entries,
                        "metadata": entry.metadata,
                    }
                )

            return api_results

        except Exception as e:
            self.logger.error(f"API search_knowledge failed: {e}")
            return []

    def get_knowledge_by_category(
        self, category: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get knowledge entries by category via API

        Args:
            category: Category to filter by
            limit: Maximum number of results

        Returns:
            List of knowledge entries as dictionaries
        """
        try:
            entries = self.db.get_knowledge_by_category(category, limit)

            # Convert to API-friendly format
            api_results = []
            for entry in entries:
                api_results.append(
                    {
                        "id": entry.id,
                        "title": entry.title,
                        "content": entry.content,
                        "category": entry.category,
                        "tags": entry.tags,
                        "source": entry.source,
                        "confidence": entry.confidence,
                        "agent_id": entry.agent_id,
                        "created_at": entry.created_at,
                        "updated_at": entry.updated_at,
                        "related_entries": entry.related_entries,
                        "metadata": entry.metadata,
                    }
                )

            return api_results

        except Exception as e:
            self.logger.error(f"API get_knowledge_by_category failed: {e}")
            return []

    def get_knowledge_by_agent(
        self, agent_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get knowledge entries by agent via API

        Args:
            agent_id: Agent ID to filter by
            limit: Maximum number of results

        Returns:
            List of knowledge entries as dictionaries
        """
        try:
            entries = self.db.get_knowledge_by_agent(agent_id, limit)

            # Convert to API-friendly format
            api_results = []
            for entry in entries:
                api_results.append(
                    {
                        "id": entry.id,
                        "title": entry.title,
                        "content": entry.content,
                        "category": entry.category,
                        "tags": entry.tags,
                        "source": entry.source,
                        "confidence": entry.confidence,
                        "agent_id": entry.agent_id,
                        "created_at": entry.created_at,
                        "updated_at": entry.updated_at,
                        "related_entries": entry.related_entries,
                        "metadata": entry.metadata,
                    }
                )

            return api_results

        except Exception as e:
            self.logger.error(f"API get_knowledge_by_agent failed: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics via API

        Returns:
            Dictionary containing database statistics
        """
        try:
            return self.db.get_statistics()
        except Exception as e:
            self.logger.error(f"API get_statistics failed: {e}")
            return {}

    def add_learning_experience(
        self,
        agent_id: str,
        task_description: str,
        outcome: str,
        lessons_learned: str,
        success_rate: float = 0.5,
        category: str = "learning_experience",
    ) -> Optional[str]:
        """
        Add a learning experience entry

        Args:
            agent_id: ID of the agent
            task_description: Description of the task performed
            outcome: What happened
            lessons_learned: Key learnings from the experience
            success_rate: Success rate (0.0-1.0)
            category: Knowledge category

        Returns:
            Entry ID if successful, None otherwise
        """
        title = f"Learning Experience: {task_description[:50]}..."
        content = f"""
Task Description: {task_description}

Outcome: {outcome}

Lessons Learned: {lessons_learned}

Success Rate: {success_rate:.2f}
        """.strip()

        tags = ["learning", "experience", "improvement", agent_id]
        metadata = {
            "type": "learning_experience",
            "success_rate": success_rate,
            "task_type": "general",
        }

        return self.add_knowledge(
            title=title,
            content=content,
            category=category,
            agent_id=agent_id,
            tags=tags,
            source="learning_experience",
            confidence=0.9,
            metadata=metadata,
        )

    def add_best_practice(
        self,
        agent_id: str,
        practice_name: str,
        description: str,
        when_to_use: str,
        examples: Optional[List[str]] = None,
        category: str = "best_practices",
    ) -> Optional[str]:
        """
        Add a best practice entry

        Args:
            agent_id: ID of the agent
            practice_name: Name of the best practice
            description: Description of the practice
            when_to_use: When to apply this practice
            examples: Optional list of examples
            category: Knowledge category

        Returns:
            Entry ID if successful, None otherwise
        """
        title = f"Best Practice: {practice_name}"

        examples_text = ""
        if examples:
            examples_text = "\n\nExamples:\n" + "\n".join(
                [f"- {ex}" for ex in examples]
            )

        content = f"""
Practice: {practice_name}

Description: {description}

When to Use: {when_to_use}{examples_text}
        """.strip()

        tags = ["best_practice", "guidelines", "recommendations", agent_id]
        metadata = {
            "type": "best_practice",
            "examples_count": len(examples) if examples else 0,
        }

        return self.add_knowledge(
            title=title,
            content=content,
            category=category,
            agent_id=agent_id,
            tags=tags,
            source="best_practice",
            confidence=0.95,
            metadata=metadata,
        )

    def add_troubleshooting_guide(
        self,
        agent_id: str,
        problem: str,
        solution: str,
        steps: List[str],
        prevention_tips: Optional[List[str]] = None,
        category: str = "troubleshooting",
    ) -> Optional[str]:
        """
        Add a troubleshooting guide entry

        Args:
            agent_id: ID of the agent
            problem: Description of the problem
            solution: General solution approach
            steps: Step-by-step solution
            prevention_tips: Optional tips to prevent the problem
            category: Knowledge category

        Returns:
            Entry ID if successful, None otherwise
        """
        title = f"Troubleshooting: {problem[:50]}..."

        steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])

        prevention_text = ""
        if prevention_tips:
            prevention_text = "\n\nPrevention Tips:\n" + "\n".join(
                [f"- {tip}" for tip in prevention_tips]
            )

        content = f"""
Problem: {problem}

Solution: {solution}

Steps to Resolve:
{steps_text}{prevention_text}
        """.strip()

        tags = ["troubleshooting", "problem_solving", "debugging", agent_id]
        metadata = {
            "type": "troubleshooting_guide",
            "steps_count": len(steps),
            "has_prevention_tips": bool(prevention_tips),
        }

        return self.add_knowledge(
            title=title,
            content=content,
            category=category,
            agent_id=agent_id,
            tags=tags,
            source="troubleshooting",
            confidence=0.9,
            metadata=metadata,
        )

    def get_recommendations(
        self, agent_id: str, context: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get personalized knowledge recommendations for an agent

        Args:
            agent_id: ID of the agent
            context: Context for recommendations
            limit: Maximum number of recommendations

        Returns:
            List of recommended knowledge entries
        """
        try:
            # Search for relevant knowledge based on context
            results = self.search_knowledge(context, limit * 2)

            # Filter and prioritize results
            recommendations = []
            for entry in results:
                # Boost entries from the same agent
                if entry["agent_id"] == agent_id:
                    entry["relevance_score"] *= 1.2

                # Boost recent entries
                age_hours = (datetime.now().timestamp() - entry["updated_at"]) / 3600
                if age_hours < 24:  # Last 24 hours
                    entry["relevance_score"] *= 1.1

                recommendations.append(entry)

            # Sort by relevance and return top results
            recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
            return recommendations[:limit]

        except Exception as e:
            self.logger.error(f"API get_recommendations failed: {e}")
            return []


# Convenience functions for quick access
def quick_add(
    title: str, content: str, category: str, agent_id: str, **kwargs
) -> Optional[str]:
    """Quick function to add knowledge without creating API instance"""
    api = KnowledgeAPI()
    return api.add_knowledge(title, content, category, agent_id, **kwargs)


def quick_search(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Quick function to search knowledge without creating API instance"""
    api = KnowledgeAPI()
    return api.search_knowledge(query, limit)


def quick_stats() -> Dict[str, Any]:
    """Quick function to get stats without creating API instance"""
    api = KnowledgeAPI()
    return api.get_statistics()
