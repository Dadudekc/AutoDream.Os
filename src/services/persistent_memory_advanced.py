"""Persistent Memory Advanced - Retrieval and organization"""

import logging
from datetime import UTC, datetime

logger = logging.getLogger(__name__)


class MemoryRetrieval:
    """Memory retrieval and search engine."""

    def __init__(self):
        self.search_index: dict[str, list[str]] = {}
        self.memories = {}

    def search_memories(self, query: str, context: dict) -> list[dict]:
        """Search memories based on query and context."""
        try:
            query_lower = query.lower()
            results = []

            for memory_id, memory_data in self.memories.items():
                content = str(memory_data.get("content", "")).lower()
                metadata = memory_data.get("metadata", {})

                if query_lower in content:
                    score = self._calculate_relevance_score(query, memory_data, context)
                    results.append({
                        "memory_id": memory_id,
                        "memory_data": memory_data,
                        "relevance_score": score,
                    })

                tags = metadata.get("tags", [])
                for tag in tags:
                    if query_lower in tag.lower():
                        score = self._calculate_relevance_score(query, memory_data, context)
                        results.append({
                            "memory_id": memory_id,
                            "memory_data": memory_data,
                            "relevance_score": score,
                        })

            results.sort(key=lambda x: x["relevance_score"], reverse=True)
            return results

        except Exception as e:
            logger.error(f"Error searching memories: {e}")
            return []

    def _calculate_relevance_score(self, query: str, memory_data: dict, context: dict) -> float:
        """Calculate relevance score for memory."""
        score = 0.0
        content = str(memory_data.get("content", "")).lower()
        metadata = memory_data.get("metadata", {})

        query_words = query.lower().split()
        content_words = content.split()

        for word in query_words:
            if word in content_words:
                score += 1.0

        priority = metadata.get("priority", "normal")
        if priority == "critical":
            score += 3.0
        elif priority == "high":
            score += 2.0
        elif priority == "normal":
            score += 1.0

        confidence = metadata.get("confidence", 1.0)
        score += confidence

        created_at = metadata.get("created_at")
        if created_at:
            try:
                created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                days_old = (datetime.now(UTC) - created_dt).days
                recency_boost = max(0, 1.0 - (days_old / 365.0))
                score += recency_boost
            except:
                pass

        return score


class MemoryOrganization:
    """Memory organization and categorization system."""

    def __init__(self):
        self.categories: dict[str, list[str]] = {}
        self.hierarchies: dict[str, list[str]] = {}

    def organize_memory(
        self, memory_id: str, categories: list[str], hierarchy: str | None = None
    ) -> bool:
        """Organize memory into categories and hierarchies."""
        try:
            for category in categories:
                if category not in self.categories:
                    self.categories[category] = []
                if memory_id not in self.categories[category]:
                    self.categories[category].append(memory_id)

            if hierarchy:
                if hierarchy not in self.hierarchies:
                    self.hierarchies[hierarchy] = []
                if memory_id not in self.hierarchies[hierarchy]:
                    self.hierarchies[hierarchy].append(memory_id)

            logger.info(f"Organized memory {memory_id} into categories: {categories}")
            return True

        except Exception as e:
            logger.error(f"Error organizing memory {memory_id}: {e}")
            return False

    def get_memories_by_category(self, category: str) -> list[str]:
        """Get memory IDs by category."""
        return self.categories.get(category, [])

    def get_memories_by_hierarchy(self, hierarchy: str) -> list[str]:
        """Get memory IDs by hierarchy."""
        return self.hierarchies.get(hierarchy, [])

