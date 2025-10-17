#!/usr/bin/env python3
"""
Swarm Brain & Notes Tools
==========================

Tools for agent notes and swarm knowledge management.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging
from typing import Any

from ..adapters.base_adapter import IToolAdapter, ToolSpec, ToolResult

logger = logging.getLogger(__name__)


class TakeNoteTool(IToolAdapter):
    """Take personal note."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="brain.note", version="1.0.0", category="brain", 
                       summary="Take personal note", required_params=["agent_id", "content"],
                       optional_params={"note_type": "important"})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute note taking."""
        try:
            if params is None:
                return ToolResult(success=False, output=None, error_message="params required", exit_code=1)
                
            from src.swarm_brain import NoteType, SwarmMemory

            agent_id = params.get("agent_id")
            content = params.get("content")
            note_type = params.get("note_type", "important")

            if not agent_id or not content:
                return ToolResult(success=False, output=None, error_message="agent_id and content required", exit_code=1)

            memory = SwarmMemory(agent_id)

            # Map string to enum
            type_map = {
                "learning": NoteType.LEARNING,
                "important": NoteType.IMPORTANT,
                "todo": NoteType.TODO,
                "decision": NoteType.DECISION,
                "work_log": NoteType.WORK_LOG,
            }

            note_type_enum = type_map.get(note_type, NoteType.IMPORTANT)
            memory.take_note(content, note_type_enum)

            return ToolResult(success=True, output={"message": f"Note added: {note_type}"})

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class ShareLearningTool(IToolAdapter):
    """Share learning with swarm brain."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="brain.share", version="1.0.0", category="brain",
                       summary="Share learning with swarm brain", 
                       required_params=["agent_id", "title", "content"],
                       optional_params={"tags": []})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute learning sharing."""
        try:
            if params is None:
                return ToolResult(success=False, output=None, error_message="params required", exit_code=1)
                
            from src.swarm_brain import SwarmMemory

            agent_id = params.get("agent_id")
            title = params.get("title")
            content = params.get("content")
            tags = params.get("tags", [])

            if not agent_id or not title or not content:
                return ToolResult(success=False, output=None, error_message="agent_id, title, content required", exit_code=1)

            memory = SwarmMemory(agent_id)
            entry_id = memory.share_learning(title, content, tags)

            output = {
                "entry_id": entry_id,
                "message": f"Learning shared: {entry_id}",
            }
            return ToolResult(success=True, output=output)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class SearchKnowledgeTool(IToolAdapter):
    """Search swarm knowledge base."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="brain.search", version="1.0.0", category="brain",
                       summary="Search swarm knowledge base",
                       required_params=["query"],
                       optional_params={"agent_id": "Agent-1"})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute knowledge search."""
        try:
            if params is None:
                return ToolResult(success=False, output=None, error_message="params required", exit_code=1)
                
            from src.swarm_brain import SwarmMemory

            agent_id = params.get("agent_id", "Agent-1")
            query = params.get("query")

            if not query:
                return ToolResult(success=False, output=None, error_message="query required", exit_code=1)

            memory = SwarmMemory(agent_id)
            results = memory.search_swarm_knowledge(query)

            output = {
                "results": [
                    {"title": r.title, "author": r.author, "tags": r.tags} for r in results
                ],
                "count": len(results),
            }
            return ToolResult(success=True, output=output)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class LogSessionTool(IToolAdapter):
    """Log work session to agent notes."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="brain.session", version="1.0.0", category="brain",
                       summary="Log work session to agent notes",
                       required_params=["agent_id", "summary"],
                       optional_params={})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute session logging."""
        try:
            if params is None:
                return ToolResult(success=False, output=None, error_message="params required", exit_code=1)
                
            from src.swarm_brain import SwarmMemory

            agent_id = params.get("agent_id")
            summary = params.get("summary")

            if not agent_id or not summary:
                return ToolResult(success=False, output=None, error_message="agent_id and summary required", exit_code=1)

            memory = SwarmMemory(agent_id)
            memory.log_session(summary)

            return ToolResult(success=True, output={"message": "Session logged"})

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class GetAgentNotesTool(IToolAdapter):
    """Get agent's personal notes."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="brain.get", version="1.0.0", category="brain",
                       summary="Get agent's personal notes",
                       required_params=["agent_id"],
                       optional_params={"note_type": None})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute note retrieval."""
        try:
            if params is None:
                return ToolResult(success=False, output=None, error_message="params required", exit_code=1)
                
            from src.swarm_brain import NoteType, SwarmMemory

            agent_id = params.get("agent_id")
            note_type = params.get("note_type")

            if not agent_id:
                return ToolResult(success=False, output=None, error_message="agent_id required", exit_code=1)

            memory = SwarmMemory(agent_id)

            if note_type:
                type_map = {
                    "learning": NoteType.LEARNING,
                    "important": NoteType.IMPORTANT,
                    "todo": NoteType.TODO,
                }
                notes = memory.get_my_notes(type_map.get(note_type))
            else:
                notes = memory.get_my_notes()

            output = {"notes": notes, "count": len(notes)}
            return ToolResult(success=True, output=output)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)
