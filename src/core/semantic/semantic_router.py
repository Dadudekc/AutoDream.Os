import logging
logger = logging.getLogger(__name__)
"""
Semantic Router for intelligent task routing and agent matching.
"""

from __future__ import annotations

from typing import Any

from .status_index import StatusIndex


class SemanticRouter:
    """Routes tasks to appropriate agents using semantic similarity."""

    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        self.status_index = StatusIndex(cfg)

        # Agent specialization mapping
        self.agent_specializations = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "SSOT & System Integration Specialist",
        }

    def route(self, task_text: str, enrich_context: bool = True) -> dict[str, Any]:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.semantic.semantic_router import Semantic_Router

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Semantic_Router(config)

# Execute primary functionality
result = component.process_data(input_data)
logger.info(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    logger.info(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    logger.info(f"Operation failed: {e}")
    # Implement recovery logic

        """Route a task to the most appropriate agent(s)."""
        # Find similar agent statuses/tasks
        similar_statuses = self.status_index.similar(task_text)

        # Determine priority based on task content
        priority = self._determine_priority(task_text)

        # Get agent suggestions based on similarity and specialization
        agent_suggestions = self._get_agent_suggestions(task_text, similar_statuses)

        result = {
            "priority": priority,
            "agent_suggestions": agent_suggestions,
            "task_text": task_text,
        }

        if enrich_context and similar_statuses:
            result["context_hits"] = [
                {"id": hit[0], "score": hit[1], "meta": hit[2]} for hit in similar_statuses[:3]
            ]

        return result

    def _determine_priority(self, task_text: str) -> str:
        """Determine task priority based on content analysis."""
        text_lower = task_text.lower()

        # High priority indicators
        if any(
            word in text_lower
            for word in ["urgent", "critical", "emergency", "fail", "error", "broken"]
        ):
            return "URGENT"

        # Coordination priority indicators
        if any(
            word in text_lower
            for word in ["coordinate", "sync", "align", "consolidate", "integrate"]
        ):
            return "COORDINATION"

        # Default priority
        return "NORMAL"

    def _get_agent_suggestions(
        self, task_text: str, similar_statuses: list
    ) -> list[dict[str, Any]]:
        """Get agent suggestions based on task content and historical performance."""
        suggestions = []

        # Score agents based on task content matching their specializations
        for agent_id, specialization in self.agent_specializations.items():
            # Simple keyword matching for now (can be enhanced with embeddings)
            task_words = set(task_text.lower().split())
            spec_words = set(specialization.lower().split())

            # Calculate overlap score
            overlap = len(task_words.intersection(spec_words))
            total_words = len(task_words.union(spec_words))

            if total_words > 0:
                base_score = overlap / total_words
            else:
                base_score = 0.0

            # Boost score if agent has similar historical tasks
            history_boost = 0.0
            for hit in similar_statuses:
                if hit[2].get("agent_id") == agent_id:
                    history_boost = hit[1] * 0.3  # 30% weight from history
                    break

            final_score = min(1.0, base_score + history_boost)

            if final_score > 0.1:  # Only include relevant matches
                suggestions.append(
                    {
                        "agent": agent_id,
                        "specialization": specialization,
                        "score": final_score,
                        "reason": f"Specialization match ({base_score:.2f}) + history ({history_boost:.2f})",
                    }
                )

        # Sort by score descending
        suggestions.sort(key=lambda x: x["score"], reverse=True)

        return suggestions[:5]  # Return top 5 suggestions
