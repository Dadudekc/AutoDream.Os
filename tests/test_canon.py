#!/usr/bin/env python3
"""
Test Canonical Text Builders
============================

Tests for canonical text generation functions.
"""


from swarm_brain.canon import (
    canonical_action,
    canonical_conversation,
    canonical_performance,
    canonical_protocol,
    canonical_workflow,
)


def test_canonical_action_simple():
    """Test basic action canonical text generation."""
    text = canonical_action(
        title="Run Scanner",
        outcome="success",
        tool="scanner",
        context={"files": 100, "violations": 5},
        summary="Scanned 100 files, found 5 violations",
        tags=["scanner", "compliance"],
    )

    assert "[ACTION] Run Scanner" in text
    assert "Tool: scanner" in text
    assert "Outcome: success" in text
    assert "scanner" in text
    assert "compliance" in text
    assert "Scanned 100 files" in text


def test_canonical_protocol():
    """Test protocol canonical text generation."""
    text = canonical_protocol(
        title="V2 Refactor Protocol",
        steps=["Split large files", "Extract classes", "Test changes"],
        effectiveness=0.85,
        improvements={"success_rate": 0.9},
        summary="Protocol for V2 compliance refactoring",
        tags=["protocol", "refactor"],
    )

    assert "[PROTOCOL] V2 Refactor Protocol" in text
    assert "Effectiveness: 0.850" in text
    assert "Split large files" in text
    assert "protocol" in text
    assert "refactor" in text


def test_canonical_workflow():
    """Test workflow canonical text generation."""
    text = canonical_workflow(
        title="Agent Coordination Workflow",
        execution_pattern={"steps": 5, "parallel": True},
        coordination={"agents": ["Agent-1", "Agent-2"]},
        outcomes={"success_rate": 0.95},
        optimization={"caching": True},
        summary="Workflow for agent coordination",
        tags=["workflow", "coordination"],
    )

    assert "[WORKFLOW] Agent Coordination Workflow" in text
    assert "Execution Pattern:" in text
    assert "coordination" in text
    assert "workflow" in text
    assert "coordination" in text


def test_canonical_performance():
    """Test performance canonical text generation."""
    text = canonical_performance(
        title="System Performance",
        metrics={"cpu": 45.0, "memory": 60.0},
        anomalies={"high_memory": True},
        optimizations={"cache_size": 1000},
        trends={"improving": True},
        summary="System performance metrics",
        tags=["performance", "monitoring"],
    )

    assert "[PERFORMANCE] System Performance" in text
    assert "cpu" in text
    assert "memory" in text
    assert "performance" in text
    assert "monitoring" in text


def test_canonical_conversation():
    """Test conversation canonical text generation."""
    text = canonical_conversation(
        title="Discord Discussion",
        channel="discord",
        role="agent",
        content="Let's coordinate on the next task",
        summary="Discord coordination message",
        tags=["discord", "coordination"],
    )

    assert "[CONVERSATION] Discord Discussion" in text
    assert "Channel: discord" in text
    assert "Role: agent" in text
    assert "Let's coordinate" in text
    assert "discord" in text
    assert "coordination" in text


def test_canonical_text_truncation():
    """Test that long content is properly truncated."""
    long_content = "A" * 2000  # Very long content

    text = canonical_conversation(
        title="Long Message",
        channel="discord",
        role="agent",
        content=long_content,
        summary="Long message test",
        tags=["test"],
    )

    # Should be truncated
    assert len(text) < len(long_content) + 500  # Some overhead for other fields
    assert "..." in text  # Truncation indicator
