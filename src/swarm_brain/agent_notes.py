#!/usr/bin/env python3
"""
Agent Notes System
==================

Personal note-taking system for individual agents.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import json
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class NoteType(str, Enum):
    """Types of notes agents can take."""

    LEARNING = "learning"  # What agent learned
    IMPORTANT = "important"  # Key information to remember
    TODO = "todo"  # Personal todo items
    DECISION = "decision"  # Decisions made
    WORK_LOG = "work_log"  # Session work logs
    COORDINATION = "coordination"  # Inter-agent coordination notes


class AgentNotes:
    """Manages personal notes for an agent."""

    def __init__(self, agent_id: str, workspace_root: str = "agent_workspaces"):
        """
        Initialize agent notes.

        Args:
            agent_id: Agent ID (e.g., "Agent-7")
            workspace_root: Root directory for agent workspaces
        """
        self.agent_id = agent_id
        self.workspace = Path(workspace_root) / agent_id
        self.notes_dir = self.workspace / "notes"
        self.notes_dir.mkdir(parents=True, exist_ok=True)

        # Note files
        self.notes_file = self.notes_dir / "notes.json"
        self.learnings_file = self.notes_dir / "learnings.md"
        self.important_file = self.notes_dir / "important_info.md"
        self.work_log_file = self.notes_dir / "work_log.md"
        self.todos_file = self.notes_dir / "todos.md"

        # Load existing notes
        self.notes = self._load_notes()

    def _load_notes(self) -> dict:
        """Load notes from file."""
        if self.notes_file.exists():
            return json.loads(self.notes_file.read_text(encoding="utf-8"))

        return {
            "agent_id": self.agent_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "notes": [],
        }

    def _save_notes(self):
        """Save notes to file."""
        self.notes["last_updated"] = datetime.now().isoformat()
        self.notes_file.write_text(
            json.dumps(self.notes, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def add_note(
        self, content: str, note_type: NoteType = NoteType.IMPORTANT, tags: list[str] = None
    ) -> str:
        """
        Add a note.

        Args:
            content: Note content
            note_type: Type of note
            tags: Optional tags for categorization

        Returns:
            Note ID
        """
        note_id = f"note-{len(self.notes['notes']) + 1}"

        note = {
            "id": note_id,
            "type": note_type.value,
            "content": content,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat(),
        }

        self.notes["notes"].append(note)
        self._save_notes()

        # Also append to type-specific markdown file
        self._append_to_markdown(note_type, content)

        logger.info(f"✅ Note added: {note_id} ({note_type.value})")
        return note_id

    def _append_to_markdown(self, note_type: NoteType, content: str):
        """Append note to type-specific markdown file."""
        file_map = {
            NoteType.LEARNING: self.learnings_file,
            NoteType.IMPORTANT: self.important_file,
            NoteType.WORK_LOG: self.work_log_file,
            NoteType.TODO: self.todos_file,
        }

        target_file = file_map.get(note_type)
        if not target_file:
            return

        # Create file if doesn't exist
        if not target_file.exists():
            target_file.write_text(
                f"# {self.agent_id} - {note_type.value.title()}\n\n", encoding="utf-8"
            )

        # Append note
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n## {timestamp}\n\n{content}\n\n---\n"

        with open(target_file, "a", encoding="utf-8") as f:
            f.write(entry)

    def get_notes(self, note_type: NoteType | None = None, tags: list[str] = None) -> list[dict]:
        """
        Get notes with optional filtering.

        Args:
            note_type: Filter by type
            tags: Filter by tags

        Returns:
            List of matching notes
        """
        notes = self.notes["notes"]

        if note_type:
            notes = [n for n in notes if n["type"] == note_type.value]

        if tags:
            notes = [n for n in notes if any(tag in n.get("tags", []) for tag in tags)]

        return notes

    def search_notes(self, query: str) -> list[dict]:
        """
        Search notes by content.

        Args:
            query: Search query

        Returns:
            Matching notes
        """
        query_lower = query.lower()
        return [
            n
            for n in self.notes["notes"]
            if query_lower in n["content"].lower() or query_lower in n["type"].lower()
        ]

    def log_work(self, session_summary: str):
        """
        Log work session.

        Args:
            session_summary: Summary of work completed
        """
        self.add_note(session_summary, NoteType.WORK_LOG, tags=["session"])

    def record_learning(self, learning: str):
        """
        Record something learned.

        Args:
            learning: What was learned
        """
        self.add_note(learning, NoteType.LEARNING, tags=["knowledge"])

    def mark_important(self, info: str):
        """
        Mark information as important.

        Args:
            info: Important information
        """
        self.add_note(info, NoteType.IMPORTANT, tags=["critical"])
