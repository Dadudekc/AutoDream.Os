#!/usr/bin/env python3
"""
Message-Task Integration Tests
===============================

Tests for message-to-task pipeline.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import pytest

from src.message_task.dedupe import normalize_priority, task_fingerprint
from src.message_task.fsm_bridge import (
    TaskEvent,
    TaskState,
    can_transition,
    transition_on_create,
)
from src.message_task.parsers.ai_parser import AIParser
from src.message_task.parsers.fallback_regex import FallbackRegexParser
from src.message_task.parsers.structured_parser import StructuredParser
from src.message_task.schemas import InboundMessage


class TestStructuredParser:
    """Test structured message parser."""

    def test_parse_full_format(self):
        """Test parsing complete structured format."""
        content = """
TASK: Implement error handling
DESC: Add try-catch blocks to all API calls
PRIORITY: P1
ASSIGNEE: Agent-2
"""
        result = StructuredParser.parse(content)
        assert result is not None
        assert result.title == "Implement error handling"
        assert "try-catch" in result.description
        assert result.priority == "P1"
        assert result.assignee == "Agent-2"

    def test_parse_minimal_format(self):
        """Test parsing minimal structured format."""
        content = "TASK: Fix bug in login"
        result = StructuredParser.parse(content)
        assert result is not None
        assert result.title == "Fix bug in login"
        assert result.priority == "P3"  # default

    def test_parse_with_tags(self):
        """Test parsing with tags."""
        content = """
TASK: Update documentation
TAGS: docs, urgent, v2
"""
        result = StructuredParser.parse(content)
        assert result is not None
        assert "docs" in result.tags
        assert "urgent" in result.tags


class TestAIParser:
    """Test AI-powered parser."""

    def test_parse_natural_language(self):
        """Test parsing natural language."""
        content = "Please implement the new dashboard feature as soon as possible"
        result = AIParser.parse(content)
        assert result is not None
        assert "dashboard" in result.title.lower()
        assert result.priority == "P0"  # detected "as soon as possible"

    def test_parse_with_assignee(self):
        """Test extracting assignee."""
        content = "Fix the bug and assign to @Agent-3"
        result = AIParser.parse(content)
        assert result is not None
        assert result.assignee == "Agent-3"

    def test_parse_priority_detection(self):
        """Test priority detection."""
        content = "This is a low priority enhancement"
        result = AIParser.parse(content)
        assert result is not None
        assert result.priority == "P3"


class TestFallbackParser:
    """Test fallback regex parser."""

    def test_parse_todo_format(self):
        """Test parsing TODO format."""
        content = "todo: Review pull request"
        result = FallbackRegexParser.parse(content)
        assert result is not None
        assert "Review pull request" in result.title

    def test_parse_fix_format(self):
        """Test parsing FIX format."""
        content = "fix: Memory leak in worker thread"
        result = FallbackRegexParser.parse(content)
        assert result is not None
        assert "Memory leak" in result.title

    def test_parse_fallback_to_first_line(self):
        """Test ultimate fallback."""
        content = "Just a random message\nWith multiple lines"
        result = FallbackRegexParser.parse(content)
        assert result is not None
        assert result.title == "Just a random message"


class TestDeduplication:
    """Test task deduplication."""

    def test_fingerprint_identical(self):
        """Test identical tasks produce same fingerprint."""
        task1 = {
            "title": "Fix bug",
            "description": "Memory leak",
            "priority": "P1",
        }
        task2 = {
            "title": "Fix bug",
            "description": "Memory leak",
            "priority": "P1",
        }
        fp1 = task_fingerprint(task1)
        fp2 = task_fingerprint(task2)
        assert fp1 == fp2

    def test_fingerprint_different(self):
        """Test different tasks produce different fingerprints."""
        task1 = {"title": "Fix bug A", "description": ""}
        task2 = {"title": "Fix bug B", "description": ""}
        fp1 = task_fingerprint(task1)
        fp2 = task_fingerprint(task2)
        assert fp1 != fp2

    def test_priority_normalization(self):
        """Test priority normalization."""
        assert normalize_priority("URGENT") == "P0"
        assert normalize_priority("high") == "P1"
        assert normalize_priority("P2") == "P2"
        assert normalize_priority("unknown") == "P3"


class TestFSMBridge:
    """Test FSM state management."""

    def test_initial_state(self):
        """Test initial state creation."""
        state, event = transition_on_create()
        assert state == TaskState.TODO
        assert event == TaskEvent.CREATE

    def test_valid_transitions(self):
        """Test valid state transitions."""
        assert can_transition(TaskState.TODO, TaskState.DOING)
        assert can_transition(TaskState.DOING, TaskState.DONE)
        assert can_transition(TaskState.DOING, TaskState.BLOCKED)
        assert can_transition(TaskState.BLOCKED, TaskState.DOING)

    def test_invalid_transitions(self):
        """Test invalid state transitions."""
        assert not can_transition(TaskState.DONE, TaskState.TODO)
        assert not can_transition(TaskState.TODO, TaskState.DONE)


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_message_to_task_structured(self):
        """Test complete flow with structured message."""
        msg = InboundMessage(
            id="msg-001",
            channel="discord",
            author="Captain",
            content="TASK: Deploy to production\nPRIORITY: P0",
        )

        # Parse
        parsed = StructuredParser.parse(msg.content)
        assert parsed is not None

        # Fingerprint
        fp = task_fingerprint(parsed.to_dict())
        assert len(fp) == 40  # SHA-1 hex

    def test_parser_cascade(self):
        """Test parser cascade fallback."""
        messages = [
            "TASK: Structured format",  # Structured
            "Please fix the bug",  # AI
            "todo: fallback format",  # Fallback
        ]

        parsers = [StructuredParser, AIParser, FallbackRegexParser]

        for content in messages:
            parsed = None
            for parser in parsers:
                parsed = parser.parse(content)
                if parsed:
                    break
            assert parsed is not None, f"Failed to parse: {content}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
