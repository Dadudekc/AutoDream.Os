"""
Vector Integration Helper Functions
===================================
Utility functions for vector integration service formatting and recommendations.
Extracted for V2 compliance.

Author: Agent-5 (extracted from Agent-1's vector_integration_unified.py)
License: MIT
"""

import logging
from collections import Counter
from typing import Any

logger = logging.getLogger(__name__)


def format_search_result(result: Any) -> dict[str, Any]:
    """Format search result for agent consumption.

    Args:
        result: Search result object

    Returns:
        Formatted result dictionary
    """
    try:
        return {
            "similarity": getattr(result, "similarity_score", 0.0),
            "content": (
                result.document.content[:150] + "..."
                if len(result.document.content) > 150
                else result.document.content
            ),
            "type": result.document.document_type.value,
            "source": getattr(result.document, "source_file", "unknown"),
            "tags": getattr(result.document, "tags", []),
        }
    except Exception as e:
        logger.error(f"Failed to format search result: {e}")
        return {"error": str(e)}


def generate_recommendations(similar_tasks: list[Any]) -> list[str]:
    """Generate recommendations based on similar tasks.

    Args:
        similar_tasks: List of similar task results

    Returns:
        List of recommendation strings
    """
    recommendations = []
    if similar_tasks:
        tags = []
        for task in similar_tasks:
            if hasattr(task, "document") and hasattr(task.document, "tags"):
                tags.extend(task.document.tags)

        if tags:
            common_tags = Counter(tags).most_common(3)
            for tag, count in common_tags:
                recommendations.append(
                    f"Consider using {tag} approach (used in {count} similar tasks)"
                )

    if not recommendations:
        recommendations.append("No specific patterns found - proceed with standard approach")

    return recommendations


def generate_agent_recommendations(work_history: list[Any]) -> list[str]:
    """Generate agent-specific recommendations.

    Args:
        work_history: List of work history items

    Returns:
        List of recommendation strings
    """
    recommendations = []
    if work_history:
        avg_similarity = sum(getattr(w, "similarity_score", 0.0) for w in work_history) / len(
            work_history
        )

        if avg_similarity > 0.8:
            recommendations.append("Excellent work quality - maintain current approach")
        elif avg_similarity > 0.6:
            recommendations.append("Good work quality - consider improving consistency")
        else:
            recommendations.append("Focus on improving work quality and consistency")

    return recommendations
