#!/usr/bin/env python3
"""
Swarm Memory System
===================

Unified memory system combining agent notes and shared knowledge.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from .agent_notes import AgentNotes, NoteType
from .knowledge_base import KnowledgeBase, KnowledgeEntry

logger = logging.getLogger(__name__)


class SwarmMemory:
    """Unified memory system for agents and swarm."""

    def __init__(
        self,
        agent_id: str,
        workspace_root: str = "agent_workspaces",
        brain_root: str = "swarm_brain",
    ):
        """
        Initialize swarm memory.

        Args:
            agent_id: Agent ID
            workspace_root: Agent workspaces root
            brain_root: Swarm brain root
        """
        self.agent_id = agent_id
        self.agent_notes = AgentNotes(agent_id, workspace_root)
        self.knowledge_base = KnowledgeBase(brain_root)

    def take_note(self, content: str, note_type: NoteType = NoteType.IMPORTANT):
        """
        Take personal note.

        Args:
            content: Note content
            note_type: Type of note
        """
        note_id = self.agent_notes.add_note(content, note_type)
        logger.info(f"📝 {self.agent_id} took note: {note_id}")

    def share_learning(self, title: str, content: str, tags: list[str] = None) -> str:
        """
        Share learning with entire swarm.

        Args:
            title: Learning title
            content: Learning content
            tags: Tags for categorization

        Returns:
            Knowledge entry ID
        """
        entry = KnowledgeEntry(
            id=f"kb-{len(self.knowledge_base.kb['entries']) + 1}",
            title=title,
            content=content,
            author=self.agent_id,
            category="learning",
            tags=tags or [],
        )

        entry_id = self.knowledge_base.add_entry(entry)
        logger.info(f"🧠 {self.agent_id} shared learning: {entry_id}")
        return entry_id

    def record_decision(self, title: str, decision: str, rationale: str):
        """
        Record important decision for swarm.

        Args:
            title: Decision title
            decision: What was decided
            rationale: Why this decision
        """
        content = f"""**Decision:** {decision}

**Rationale:** {rationale}
"""

        entry = KnowledgeEntry(
            id=f"dec-{len(self.knowledge_base.kb['entries']) + 1}",
            title=title,
            content=content,
            author=self.agent_id,
            category="decision",
            tags=["decision", "architecture"],
        )

        self.knowledge_base.add_entry(entry)
        logger.info(f"🎯 {self.agent_id} recorded decision: {title}")

    def log_session(self, summary: str):
        """
        Log work session.

        Args:
            summary: Session summary
        """
        self.agent_notes.log_work(summary)
        logger.info(f"📋 {self.agent_id} logged session")

    def search_swarm_knowledge(self, query: str) -> list[KnowledgeEntry]:
        """
        Search swarm's shared knowledge.

        Args:
            query: Search query

        Returns:
            Matching entries
        """
        return self.knowledge_base.search(query)

    def get_my_notes(self, note_type: NoteType | None = None) -> list[dict]:
        """
        Get my personal notes.

        Args:
            note_type: Optional filter by type

        Returns:
            List of notes
        """
        return self.agent_notes.get_notes(note_type)

    def get_my_learnings(self) -> list[dict]:
        """Get my learning notes."""
        return self.get_my_notes(NoteType.LEARNING)

    def update_status_with_notes(self, status_file: str):
        """
        Update status.json with notes section.

        Args:
            status_file: Path to status.json
        """
        status_path = Path(status_file)
        if not status_path.exists():
            return

        # Load status
        status = json.loads(status_path.read_text(encoding="utf-8"))

        # Add notes section
        status["agent_notes"] = {
            "notes_dir": str(self.agent_notes.notes_dir),
            "total_notes": len(self.agent_notes.notes["notes"]),
            "recent_notes": self.agent_notes.notes["notes"][-5:],  # Last 5
            "learnings_count": len(self.agent_notes.get_notes(NoteType.LEARNING)),
            "important_count": len(self.agent_notes.get_notes(NoteType.IMPORTANT)),
            "last_updated": datetime.now().isoformat(),
        }

        # Save updated status
        status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")

        logger.info("✅ Status updated with notes section")
