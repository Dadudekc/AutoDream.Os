"""Text-based dashboard demo for AutoDream OS.

Shows how agent status might be displayed."""

from __future__ import annotations

from typing import Dict


def get_agent_status() -> Dict[str, str]:
    """Return a mapping of agent names to status strings."""
    return {
        "Agent-1": "online",
        "Agent-2": "idle",
        "Agent-3": "offline",
    }


def display_dashboard() -> None:
    """Display a simple dashboard of agent statuses."""
    status = get_agent_status()
    print("Agent Status Dashboard")
    for name, state in status.items():
        print(f"{name}: {state}")


if __name__ == "__main__":
    display_dashboard()
