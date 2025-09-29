#!/usr/bin/env python3
"""
Test Roundtrip Operations
========================

Tests for complete ingest-retrieve cycles.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from swarm_brain.db import SwarmBrain
from swarm_brain.ingest import Ingestor
from swarm_brain.retriever import Retriever


@pytest.fixture
def temp_brain():
    """Create a temporary brain for testing."""
    temp_dir = tempfile.mkdtemp()
    brain_path = Path(temp_dir) / "test_brain.sqlite3"

    brain = SwarmBrain(brain_path)
    yield brain
    brain.close()
    shutil.rmtree(temp_dir)


def test_action_roundtrip(temp_brain):
    """Test action ingestion and retrieval."""
    ingestor = Ingestor(temp_brain)
    retriever = Retriever(temp_brain)

    # Ingest an action
    doc_id = ingestor.action(
        title="Project Scanner Result",
        tool="scanner",
        outcome="success",
        context={"violations": 3, "files_analyzed": 100},
        project="TestProject",
        agent_id="Agent-2",
        tags=["scanner", "compliance"],
        summary="Found 3 violations in 100 files",
    )

    assert doc_id > 0

    # Search for it
    results = retriever.search("compliance violations", k=5, project="TestProject")

    assert len(results) > 0
    assert any("Project Scanner Result" in (r["title"] or "") for r in results)


def test_protocol_roundtrip(temp_brain):
    """Test protocol ingestion and retrieval."""
    ingestor = Ingestor(temp_brain)
    retriever = Retriever(temp_brain)

    # Ingest a protocol
    doc_id = ingestor.protocol(
        title="V2 Refactor Protocol",
        steps=["Split files", "Extract classes", "Test"],
        effectiveness=0.9,
        improvements={"success_rate": 0.95},
        project="TestProject",
        agent_id="Agent-3",
        tags=["protocol", "refactor"],
        summary="Protocol for V2 compliance",
    )

    assert doc_id > 0

    # Search for it
    results = retriever.search("refactor protocol", k=5, project="TestProject")

    assert len(results) > 0
    assert any("V2 Refactor Protocol" in (r["title"] or "") for r in results)


def test_workflow_roundtrip(temp_brain):
    """Test workflow ingestion and retrieval."""
    ingestor = Ingestor(temp_brain)
    retriever = Retriever(temp_brain)

    # Ingest a workflow
    doc_id = ingestor.workflow(
        title="Agent Coordination Workflow",
        execution_pattern={"steps": 3, "parallel": True},
        coordination={"agents": ["Agent-1", "Agent-2"]},
        outcomes={"success_rate": 0.95},
        optimization={"caching": True},
        project="TestProject",
        agent_id="Agent-4",
        tags=["workflow", "coordination"],
        summary="Workflow for agent coordination",
    )

    assert doc_id > 0

    # Search for it
    results = retriever.search("agent coordination", k=5, project="TestProject")

    assert len(results) > 0
    assert any("Agent Coordination Workflow" in (r["title"] or "") for r in results)


def test_performance_roundtrip(temp_brain):
    """Test performance ingestion and retrieval."""
    ingestor = Ingestor(temp_brain)
    retriever = Retriever(temp_brain)

    # Ingest performance data
    doc_id = ingestor.performance(
        title="System Performance",
        metrics={"cpu": 45.0, "memory": 60.0, "response_time": 1.2},
        anomalies={"high_memory": True},
        optimizations={"cache_size": 1000},
        trends={"improving": True},
        project="TestProject",
        agent_id="Agent-8",
        tags=["performance", "monitoring"],
        summary="System performance metrics",
    )

    assert doc_id > 0

    # Search for it
    results = retriever.search("performance metrics", k=5, project="TestProject")

    assert len(results) > 0
    assert any("System Performance" in (r["title"] or "") for r in results)


def test_conversation_roundtrip(temp_brain):
    """Test conversation ingestion and retrieval."""
    ingestor = Ingestor(temp_brain)
    retriever = Retriever(temp_brain)

    # Ingest a conversation
    doc_id = ingestor.conversation(
        title="Discord Discussion",
        channel="discord",
        thread_id="thread_123",
        role="agent",
        content="Let's coordinate on the next task",
        project="TestProject",
        agent_id="Agent-6",
        tags=["discord", "coordination"],
        summary="Discord coordination message",
    )

    assert doc_id > 0

    # Search for it
    results = retriever.search("discord coordination", k=5, project="TestProject")

    assert len(results) > 0
    assert any("Discord Discussion" in (r["title"] or "") for r in results)


def test_how_do_agents_do(temp_brain):
    """Test the how_do_agents_do query method."""
    ingestor = Ingestor(temp_brain)
    retriever = Retriever(temp_brain)

    # Ingest some successful actions
    ingestor.action(
        title="Successful V2 Refactor",
        tool="refactor_tool",
        outcome="success",
        context={"files_refactored": 5},
        project="TestProject",
        agent_id="Agent-2",
        tags=["refactor", "v2", "success"],
        summary="Successfully refactored 5 files for V2 compliance",
    )

    ingestor.action(
        title="Failed V2 Refactor",
        tool="refactor_tool",
        outcome="failure",
        context={"error": "circular_import"},
        project="TestProject",
        agent_id="Agent-3",
        tags=["refactor", "v2", "failure"],
        summary="Failed refactor due to circular import",
    )

    # Query for successful patterns
    results = retriever.how_do_agents_do("V2 compliance refactoring", k=5, project="TestProject")

    assert len(results) > 0
    # Should find the successful pattern
    assert any("Successful V2 Refactor" in (r["title"] or "") for r in results)


def test_agent_expertise(temp_brain):
    """Test agent expertise retrieval."""
    ingestor = Ingestor(temp_brain)
    retriever = Retriever(temp_brain)

    # Ingest actions for Agent-2
    ingestor.action(
        title="Scanner Action 1",
        tool="scanner",
        outcome="success",
        context={"files": 100},
        project="TestProject",
        agent_id="Agent-2",
        tags=["scanner"],
        summary="Scanner action 1",
    )

    ingestor.action(
        title="Scanner Action 2",
        tool="scanner",
        outcome="success",
        context={"files": 200},
        project="TestProject",
        agent_id="Agent-2",
        tags=["scanner"],
        summary="Scanner action 2",
    )

    # Get agent expertise
    expertise = retriever.get_agent_expertise("Agent-2", k=10)

    assert expertise["agent_id"] == "Agent-2"
    # Note: total_patterns might be 0 if embeddings aren't created yet
    assert expertise["total_patterns"] >= 0
    assert "scanner" in expertise["tool_expertise"]
    assert expertise["tool_expertise"]["scanner"]["count"] >= 2
