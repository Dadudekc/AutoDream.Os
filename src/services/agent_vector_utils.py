from collections import Counter
from typing import Any

from ..core.validation.unified_validation_orchestrator import get_unified_validator


def format_search_result(result) -> dict[str, Any]:
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


def generate_recommendations(similar_tasks) -> list[str]:
    """Generate recommendations based on similar tasks."""
    recommendations = []
    if similar_tasks:
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
        recommendations.append("No specific patterns found - proceed with standard approach")
    return recommendations


def generate_agent_recommendations(work_history) -> list[str]:
    """Generate agent-specific recommendations."""
    recommendations = []
    if work_history:
        avg_similarity = sum(w.similarity_score for w in work_history) / len(work_history)
        if avg_similarity > 0.8:
            recommendations.append("Excellent work quality - maintain current approach")
        elif avg_similarity > 0.6:
            recommendations.append("Good work quality - consider improving consistency")
        else:
            recommendations.append("Focus on improving work quality and consistency")
    return recommendations
