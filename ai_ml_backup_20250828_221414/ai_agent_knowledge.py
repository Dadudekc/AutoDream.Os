from typing import Dict, Iterable, List, Optional

from __future__ import annotations
from dataclasses import dataclass


"""Knowledge management utilities for the AI agent learner."""



@dataclass
class KnowledgeItem:
    """Simple container for a piece of knowledge."""

    topic: str
    content: str


class KnowledgeBase:
    """In-memory store of :class:`KnowledgeItem` objects."""

    def __init__(self) -> None:
        self._items: Dict[str, KnowledgeItem] = {}

    # CRUD operations -----------------------------------------------------
    def add(self, topic: str, content: str) -> KnowledgeItem:
        item = KnowledgeItem(topic, content)
        self._items[topic] = item
        return item

    def get(self, topic: str) -> Optional[KnowledgeItem]:
        return self._items.get(topic)

    def remove(self, topic: str) -> None:
        self._items.pop(topic, None)

    # Search utilities ----------------------------------------------------
    def search(self, keyword: str) -> List[KnowledgeItem]:
        keyword = keyword.lower()
        return [
            item for item in self._items.values() if keyword in item.content.lower()
        ]

    def topics(self) -> Iterable[str]:
        """Iterate over available knowledge topics."""

        return self._items.keys()


__all__ = ["KnowledgeItem", "KnowledgeBase"]
