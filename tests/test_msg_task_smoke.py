#!/usr/bin/env python3
"""
Message-Task Integration Smoke Tests
=====================================

Quick validation tests for message-task loop.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import pytest

pytestmark = pytest.mark.smoke


@pytest.mark.smoke
def test_structured_parser_basic():
    """Smoke test: Structured parser works."""
    from src.message_task.parsers.structured_parser import StructuredParser

    content = "TASK: Test task\nPRIORITY: P1"
    result = StructuredParser.parse(content)

    assert result is not None
    assert result.title == "Test task"
    assert result.priority == "P1"


@pytest.mark.smoke
def test_ai_parser_basic():
    """Smoke test: AI parser works."""
    from src.message_task.parsers.ai_parser import AIParser

    content = "Please fix the urgent bug in authentication"
    result = AIParser.parse(content)

    assert result is not None
    assert "authentication" in result.title.lower()


@pytest.mark.smoke
def test_fallback_parser_basic():
    """Smoke test: Fallback parser works."""
    from src.message_task.parsers.fallback_regex import FallbackRegexParser

    content = "todo: implement feature X"
    result = FallbackRegexParser.parse(content)

    assert result is not None
    assert "feature X" in result.title


@pytest.mark.smoke
def test_fingerprint_deduplication():
    """Smoke test: Fingerprint deduplication works."""
    from src.message_task.dedupe import task_fingerprint

    task1 = {"title": "Fix bug", "description": "Memory leak", "priority": "P1"}
    task2 = {"title": "Fix bug", "description": "Memory leak", "priority": "P1"}

    fp1 = task_fingerprint(task1)
    fp2 = task_fingerprint(task2)

    assert fp1 == fp2
    assert len(fp1) == 40  # SHA-1 hex


@pytest.mark.smoke
def test_fsm_state_transitions():
    """Smoke test: FSM state management works."""
    from src.message_task.fsm_bridge import (
        TaskState,
        can_transition,
        initial_state,
    )

    assert initial_state() == TaskState.TODO
    assert can_transition(TaskState.TODO, TaskState.DOING)
    assert not can_transition(TaskState.DONE, TaskState.TODO)


@pytest.mark.smoke
def test_ingest_structured_message():
    """Smoke test: Full ingest pipeline for structured message."""
    from src.message_task.parsers.structured_parser import StructuredParser
    from src.message_task.schemas import InboundMessage

    msg = InboundMessage(
        id="smoke-001",
        channel="cli",
        author="captain",
        content="TASK: Add LOC guard\nPRIORITY: P2\nASSIGNEE: Agent-2",
    )

    parsed = StructuredParser.parse(msg.content)

    assert parsed is not None
    assert parsed.title == "Add LOC guard"
    assert parsed.priority == "P2"
    assert parsed.assignee == "Agent-2"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "smoke"])
