"""
Agent Vector Utilities
=====================

Utility functions for vector database operations and search result formatting.
"""

from typing import Any


def format_search_result(result: Any) -> str:
    """
    Format a vector search result for display.

    Args:
        result: Search result object

    Returns:
        Formatted string representation
    """
    try:
        if hasattr(result, "document") and hasattr(result, "similarity_score"):
            content = (
                result.document.content[:200] + "..."
                if len(result.document.content) > 200
                else result.document.content
            )
            return f"Score: {result.similarity_score:.3f} | {content}"
        return str(result)
    except Exception:
        return str(result)


def generate_recommendations(results: list[Any]) -> list[str]:
    """
    Generate recommendations based on search results.

    Args:
        results: List of search results

    Returns:
        List of recommendation strings
    """
    recommendations = []

    if not results:
        recommendations.append("No relevant information found")
        return recommendations

    # Generate recommendations based on top results
    for i, result in enumerate(results[:5], 1):
        try:
            if hasattr(result, "document"):
                rec = f"{i}. {result.document.content[:100]}..."
                recommendations.append(rec)
        except Exception:
            continue

    return recommendations
