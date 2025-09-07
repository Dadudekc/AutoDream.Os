"""Tests for the dashboard demo using AgentStatus enum."""

from examples.quickstart_demo.dashboard_demo import (
    AgentStatus,
    display_dashboard,
    get_agent_status,
)


def test_get_agent_status_mapping() -> None:
    """Agent status mapping uses enum values."""
    status = get_agent_status()
    assert status["Agent-1"] is AgentStatus.ONLINE
    assert status["Agent-2"] is AgentStatus.IDLE
    assert status["Agent-3"] is AgentStatus.OFFLINE


def test_display_dashboard_output(capsys) -> None:
    """Dashboard prints human-readable statuses."""
    display_dashboard()
    captured = capsys.readouterr().out
    assert "Agent-1: online" in captured
    assert "Agent-2: idle" in captured
    assert "Agent-3: offline" in captured

