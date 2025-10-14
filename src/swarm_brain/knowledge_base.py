#!/usr/bin/env python3
"""
Swarm Knowledge Base
====================

Shared knowledge repository for all agents.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeEntry:
    """Entry in swarm knowledge base."""

    id: str
    title: str
    content: str
    author: str  # Agent who contributed
    category: str  # Category (technical, protocol, learning, decision)
    tags: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict = field(default_factory=dict)


class KnowledgeBase:
    """Centralized knowledge base for swarm."""

    def __init__(self, brain_root: str = "swarm_brain"):
        """
        Initialize knowledge base.

        Args:
            brain_root: Root directory for swarm brain
        """
        self.brain_root = Path(brain_root)
        self.brain_root.mkdir(parents=True, exist_ok=True)

        self.kb_file = self.brain_root / "knowledge_base.json"
        self.shared_learnings_dir = self.brain_root / "shared_learnings"
        self.decisions_dir = self.brain_root / "decisions"
        self.protocols_dir = self.brain_root / "protocols"

        # Create directories
        for dir_path in [
            self.shared_learnings_dir,
            self.decisions_dir,
            self.protocols_dir,
        ]:
            dir_path.mkdir(exist_ok=True)

        # Load knowledge base
        self.kb = self._load_kb()

    def _load_kb(self) -> dict:
        """Load knowledge base."""
        if self.kb_file.exists():
            return json.loads(self.kb_file.read_text(encoding="utf-8"))

        return {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "entries": {},
            "stats": {"total_entries": 0, "contributors": {}},
        }

    def _save_kb(self):
        """Save knowledge base."""
        self.kb["last_updated"] = datetime.now().isoformat()
        self.kb_file.write_text(json.dumps(self.kb, indent=2, ensure_ascii=False), encoding="utf-8")

    def add_entry(self, entry: KnowledgeEntry) -> str:
        """
        Add knowledge entry.

        Args:
            entry: Knowledge entry

        Returns:
            Entry ID
        """
        # Store in knowledge base
        self.kb["entries"][entry.id] = {
            "id": entry.id,
            "title": entry.title,
            "content": entry.content,
            "author": entry.author,
            "category": entry.category,
            "tags": entry.tags,
            "timestamp": entry.timestamp,
            "metadata": entry.metadata,
        }

        # Update stats
        self.kb["stats"]["total_entries"] = len(self.kb["entries"])

        if entry.author not in self.kb["stats"]["contributors"]:
            self.kb["stats"]["contributors"][entry.author] = 0
        self.kb["stats"]["contributors"][entry.author] += 1

        self._save_kb()

        # Save to category-specific file
        self._save_to_category_file(entry)

        logger.info(f"✅ Knowledge entry added: {entry.id} by {entry.author}")
        return entry.id

    def _save_to_category_file(self, entry: KnowledgeEntry):
        """Save entry to category-specific markdown file."""
        category_file = self.shared_learnings_dir / f"{entry.category}.md"

        # Create file if doesn't exist
        if not category_file.exists():
            category_file.write_text(
                f"# Swarm Brain - {entry.category.title()}\n\n", encoding="utf-8"
            )

        # Append entry
        entry_md = f"""## {entry.title}

**Author:** {entry.author}  
**Date:** {entry.timestamp}  
**Tags:** {', '.join(entry.tags)}

{entry.content}

---

"""

        with open(category_file, "a", encoding="utf-8") as f:
            f.write(entry_md)

    def search(self, query: str) -> list[KnowledgeEntry]:
        """
        Search knowledge base.

        Args:
            query: Search query

        Returns:
            Matching entries
        """
        query_lower = query.lower()
        results = []

        for entry_data in self.kb["entries"].values():
            if (
                query_lower in entry_data["title"].lower()
                or query_lower in entry_data["content"].lower()
                or any(query_lower in tag.lower() for tag in entry_data["tags"])
            ):
                results.append(
                    KnowledgeEntry(
                        id=entry_data["id"],
                        title=entry_data["title"],
                        content=entry_data["content"],
                        author=entry_data["author"],
                        category=entry_data["category"],
                        tags=entry_data["tags"],
                        timestamp=entry_data["timestamp"],
                        metadata=entry_data.get("metadata", {}),
                    )
                )

        return results

    def get_by_agent(self, agent_id: str) -> list[KnowledgeEntry]:
        """Get all entries by specific agent."""
        return [
            KnowledgeEntry(**data)
            for data in self.kb["entries"].values()
            if data["author"] == agent_id
        ]

    def get_by_category(self, category: str) -> list[KnowledgeEntry]:
        """Get all entries in category."""
        return [
            KnowledgeEntry(**data)
            for data in self.kb["entries"].values()
            if data["category"] == category
        ]
