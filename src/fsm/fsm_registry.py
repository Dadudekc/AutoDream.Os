#!/usr/bin/env python3
"""
FSM Registry - V2 Compliant
===========================

Finite State Machine registry for agent and swarm state management.
Provides canonical state definitions and status file access.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import enum
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# V2 Compliance: File under 400 lines, functions under 30 lines
SPEC_PATH = Path("runtime/fsm/fsm_spec.yaml")


class AgentState(str, enum.Enum):
    """Canonical agent states from FSM specification."""

    ONBOARDING = "ONBOARDING"
    ACTIVE = "ACTIVE"
    CONTRACT_EXECUTION_ACTIVE = "CONTRACT_EXECUTION_ACTIVE"
    SURVEY_MISSION_COMPLETED = "SURVEY_MISSION_COMPLETED"
    PAUSED = "PAUSED"
    ERROR = "ERROR"
    RESET = "RESET"
    SHUTDOWN = "SHUTDOWN"


class SwarmState(str, enum.Enum):
    """Canonical swarm states from FSM specification."""

    IDLE = "IDLE"
    COORDINATING = "COORDINATING"
    BROADCAST = "BROADCAST"
    DEGRADED = "DEGRADED"
    HALT = "HALT"


@dataclass
class StatePointer:
    """Pointer to status file and key for state reading."""

    file: Path
    key: str


# Status file pointers for state reading
STATUS_POINTERS = [
    StatePointer(Path("data/semantic_seed/status"), "fsm_state"),
    StatePointer(Path("agent_workspaces"), "status.json"),
]


def load_json(file_path: Path) -> dict[str, Any]:
    """Load JSON file safely with error handling."""
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_agent_state(agent_id: str) -> str | None:
    """Read agent state from status files with fallback priority."""
    # Priority 1: Workspace status file
    ws_path = Path(f"agent_workspaces/{agent_id}/status.json")
    if ws_path.exists():
        data = load_json(ws_path)
        return data.get("fsm_state")

    # Priority 2: Semantic seed status file
    ss_path = Path(f"data/semantic_seed/status/{agent_id}.json")
    if ss_path.exists():
        data = load_json(ss_path)
        return data.get("fsm_state")

    return None


def read_swarm_state() -> str | None:
    """Read swarm state from coordination file."""
    swarm_path = Path("swarm_coordination/swarm_state.json")
    if swarm_path.exists():
        data = load_json(swarm_path)
        return data.get("swarm_state")
    return None


def get_all_agent_states() -> dict[str, str | None]:
    """Get states for all agents."""
    agent_states = {}

    # Check workspace agents
    workspace_path = Path("agent_workspaces")
    if workspace_path.exists():
        for agent_dir in workspace_path.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                agent_id = agent_dir.name
                agent_states[agent_id] = read_agent_state(agent_id)

    # Check semantic seed agents
    semantic_path = Path("data/semantic_seed/status")
    if semantic_path.exists():
        for status_file in semantic_path.glob("Agent-*.json"):
            agent_id = status_file.stem
            if agent_id not in agent_states:
                agent_states[agent_id] = read_agent_state(agent_id)

    return agent_states


def validate_agent_state(state: str) -> bool:
    """Validate if state is a canonical agent state."""
    try:
        AgentState(state)
        return True
    except ValueError:
        return False


def validate_swarm_state(state: str) -> bool:
    """Validate if state is a canonical swarm state."""
    try:
        SwarmState(state)
        return True
    except ValueError:
        return False


def get_valid_agent_states() -> list[str]:
    """Get list of all valid agent states."""
    return [state.value for state in AgentState]


def get_valid_swarm_states() -> list[str]:
    """Get list of all valid swarm states."""
    return [state.value for state in SwarmState]


def update_agent_state(agent_id: str, new_state: str) -> bool:
    """Update agent state in status file."""
    if not validate_agent_state(new_state):
        return False

    # Try workspace status file first
    ws_path = Path(f"agent_workspaces/{agent_id}/status.json")
    if ws_path.exists():
        try:
            data = load_json(ws_path)
            data["fsm_state"] = new_state
            data["last_transition"] = str(Path.cwd())
            ws_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            return True
        except Exception:
            pass

    # Fallback to semantic seed
    ss_path = Path(f"data/semantic_seed/status/{agent_id}.json")
    try:
        data = load_json(ss_path)
        data["fsm_state"] = new_state
        data["last_transition"] = str(Path.cwd())
        ss_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False


def update_swarm_state(new_state: str) -> bool:
    """Update swarm state in coordination file."""
    if not validate_swarm_state(new_state):
        return False

    swarm_path = Path("swarm_coordination/swarm_state.json")
    try:
        data = load_json(swarm_path) if swarm_path.exists() else {}
        data["swarm_state"] = new_state
        data["last_transition"] = str(Path.cwd())
        swarm_path.parent.mkdir(parents=True, exist_ok=True)
        swarm_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False


def get_state_summary() -> dict[str, Any]:
    """Get comprehensive state summary for all agents and swarm."""
    agent_states = get_all_agent_states()
    swarm_state = read_swarm_state()

    # Count states
    state_counts = {}
    for state in agent_states.values():
        if state:
            state_counts[state] = state_counts.get(state, 0) + 1

    return {
        "agent_states": agent_states,
        "swarm_state": swarm_state,
        "state_counts": state_counts,
        "total_agents": len(agent_states),
        "active_agents": sum(
            1
            for state in agent_states.values()
            if state in [AgentState.ACTIVE.value, AgentState.CONTRACT_EXECUTION_ACTIVE.value]
        ),
    }
