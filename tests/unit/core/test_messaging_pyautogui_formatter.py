"""
Unit tests for format_c2a_message (Lean Excellence Framework)
Tests the compact C2A message formatter per STANDARDS.md
"""

import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.core.messaging_pyautogui import format_c2a_message


def test_format_c2a_message_happy_path():
    """Test format_c2a_message with standard inputs (happy path)."""

    # Test with minimal fields (default priority)
    result = format_c2a_message(
        recipient="Agent-1",
        content="Please review the consolidated files."
    )
    
    assert "[C2A] Agent-1" in result
    assert "Please review the consolidated files." in result
    assert "\n\n" in result  # Ensure proper spacing


def test_format_c2a_message_with_priority_normal():
    """Test format_c2a_message with normal priority (should be compact)."""
    result = format_c2a_message(
        recipient="Agent-2",
        content="Task assigned.",
        priority="normal"
    )
    
    # Normal priority should NOT show in header (lean format)
    assert result == "[C2A] Agent-2\n\nTask assigned."
    assert "normal" not in result.lower() or "NORMAL" not in result


def test_format_c2a_message_with_priority_urgent():
    """Test format_c2a_message with urgent priority (should show in header)."""
    result = format_c2a_message(
        recipient="Agent-3",
        content="Critical bug fix required immediately!",
        priority="urgent"
    )
    
    # Urgent priority SHOULD show in header
    assert "[C2A] Agent-3 | URGENT" in result
    assert "Critical bug fix required immediately!" in result


def test_format_c2a_message_with_priority_high():
    """Test format_c2a_message with high priority (should show in header)."""
    result = format_c2a_message(
        recipient="Agent-5",
        content="Please prioritize this task.",
        priority="high"
    )
    
    # High priority SHOULD show in header
    assert "[C2A] Agent-5 | HIGH" in result
    assert "Please prioritize this task." in result


def test_format_c2a_message_with_priority_low():
    """Test format_c2a_message with low priority (should be compact)."""
    result = format_c2a_message(
        recipient="Agent-7",
        content="When you have time, review docs.",
        priority="low"
    )
    
    # Low priority should NOT show in header (lean format)
    assert result == "[C2A] Agent-7\n\nWhen you have time, review docs."
    assert "LOW" not in result


def test_format_c2a_message_missing_priority():
    """Test format_c2a_message with None priority (should default to normal)."""
    result = format_c2a_message(
        recipient="Agent-8",
        content="Standard message.",
        priority=None
    )
    
    # None priority should default to normal (compact format)
    assert result == "[C2A] Agent-8\n\nStandard message."


def test_format_c2a_message_empty_content():
    """Test format_c2a_message with empty content."""
    result = format_c2a_message(
        recipient="Agent-4",
        content=""
    )
    
    # Should still format properly with empty content
    assert result == "[C2A] Agent-4\n\n"


def test_format_c2a_message_multiline_content():
    """Test format_c2a_message with multiline content."""
    content = """Line 1: Task description
Line 2: Additional details
Line 3: Next steps"""

    result = format_c2a_message(
        recipient="Agent-6",
        content=content,
        priority="high"
    )
    
    assert "[C2A] Agent-6 | HIGH" in result
    assert "Line 1: Task description" in result
    assert "Line 2: Additional details" in result
    assert "Line 3: Next steps" in result


def test_format_c2a_message_lean_vs_verbose():
    """Test that lean format is actually more compact than old verbose format."""
    # Lean format
    lean_result = format_c2a_message(
        recipient="Agent-1",
        content="Test message",
        priority="normal"
    )
    
    # Old verbose format for comparison
    old_verbose = f"[C2A] CAPTAIN → Agent-1\nPriority: normal\n\nTest message"
    
    # Lean format should be shorter
    assert len(lean_result) < len(old_verbose)
    assert "CAPTAIN →" not in lean_result
    assert "Priority:" not in lean_result


def test_format_c2a_message_all_agent_ids():
    """Test format_c2a_message works with all 8 agent IDs."""
    agent_ids = [f"Agent-{i}" for i in range(1, 9)]
    
    for agent_id in agent_ids:
        result = format_c2a_message(
            recipient=agent_id,
            content=f"Test message for {agent_id}"
        )
        
        assert f"[C2A] {agent_id}" in result
        assert f"Test message for {agent_id}" in result


def test_format_c2a_message_preserves_content_formatting():
    """Test that formatter preserves content formatting (code blocks, etc)."""
    content = """Please run:
```bash
python tools/test_script.py
```

Then review the output."""

    result = format_c2a_message(
        recipient="Agent-2",
        content=content
    )
    
    # Content should be preserved exactly
    assert "```bash" in result
    assert "python tools/test_script.py" in result
    assert "```" in result
    assert "Then review the output." in result

