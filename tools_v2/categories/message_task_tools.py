#!/usr/bin/env python3
"""
Message-Task Integration Tools
===============================

Tools for autonomous message-to-task loop.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging
from typing import Any

from ..adapters.base_adapter import IToolAdapter, ToolSpec, ToolResult

logger = logging.getLogger(__name__)


class MessageIngestTool(IToolAdapter):
    """Ingest message and create task."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="msgtask.ingest", version="1.0.0", category="message_task",
                       summary="Ingest message and create task",
                       required_params=["content"],
                       optional_params={"message_id": "auto", "author": "Agent", "channel": "cli"})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute message ingestion."""
        try:
            if params is None:
                return ToolResult(success=False, output=None, error_message="params required", exit_code=1)
                
            from src.message_task.messaging_integration import process_message_for_task

            message_id = params.get("message_id", f"msg-{params.get('content', '')[:8]}")
            content = params.get("content")
            author = params.get("author", "Agent")
            channel = params.get("channel", "cli")

            if not content:
                return ToolResult(success=False, output=None, error_message="Content required", exit_code=1)

            task_id = process_message_for_task(message_id, content, author, channel)

            if task_id:
                output = {
                    "task_id": task_id,
                    "message": f"Task created: {task_id}",
                }
                return ToolResult(success=True, output=output)
            else:
                return ToolResult(success=False, output=None, error_message="Failed to create task", exit_code=1)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class TaskParserTool(IToolAdapter):
    """Parse message to extract task info."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="msgtask.parse", version="1.0.0", category="message_task",
                       summary="Parse message to extract task info",
                       required_params=["content"],
                       optional_params={})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute task parsing."""
        try:
            if params is None:
                return ToolResult(success=False, output=None, error_message="params required", exit_code=1)
                
            from src.message_task.parsers.ai_parser import AIParser
            from src.message_task.parsers.fallback_regex import FallbackRegexParser
            from src.message_task.parsers.structured_parser import StructuredParser

            content = params.get("content")
            if not content:
                return ToolResult(success=False, output=None, error_message="Content required", exit_code=1)

            # Try parsers
            for parser_name, parser in [
                ("structured", StructuredParser),
                ("ai", AIParser),
                ("fallback", FallbackRegexParser),
            ]:
                result = parser.parse(content)
                if result:
                    output = {
                        "parser_used": parser_name,
                        "title": result.title,
                        "description": result.description,
                        "priority": result.priority,
                        "assignee": result.assignee,
                    }
                    return ToolResult(success=True, output=output)

            return ToolResult(success=False, output=None, error_message="No parser succeeded", exit_code=1)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class TaskFingerprintTool(IToolAdapter):
    """Generate task fingerprint for deduplication."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="msgtask.fingerprint", version="1.0.0", category="message_task",
                       summary="Generate task fingerprint for deduplication",
                       required_params=[],
                       optional_params={"title": "", "description": "", "priority": "P3", "assignee": None})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        return (True, [])  # All params optional

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute fingerprint generation."""
        try:
            if params is None:
                params = {}
                
            from src.message_task.dedupe import task_fingerprint

            task_dict = {
                "title": params.get("title", ""),
                "description": params.get("description", ""),
                "priority": params.get("priority", "P3"),
                "assignee": params.get("assignee"),
            }

            fingerprint = task_fingerprint(task_dict)

            output = {"fingerprint": fingerprint, "length": len(fingerprint)}
            return ToolResult(success=True, output=output)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)
