"""Backup and export utilities for FSM state definitions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from fsm.states import StateDefinition


def export_state_definitions(states: Dict[str, StateDefinition], format: str = "dict") -> Any:
    """Export state definitions to a dictionary or JSON string."""
    if format.lower() == "dict":
        return {
            name: {
                "name": state.name,
                "description": state.description,
                "entry_actions": state.entry_actions,
                "exit_actions": state.exit_actions,
                "timeout_seconds": state.timeout_seconds,
                "retry_count": state.retry_count,
                "retry_delay": state.retry_delay,
                "required_resources": state.required_resources,
                "dependencies": state.dependencies,
                "metadata": state.metadata,
            }
            for name, state in states.items()
        }
    if format.lower() == "json":
        return json.dumps(export_state_definitions(states, "dict"), indent=2)
    raise ValueError(f"Unsupported export format: {format}")


def backup_state_definitions(states: Dict[str, StateDefinition], path: str) -> Path:
    """Write state definitions to a JSON backup file and return the path."""
    data = export_state_definitions(states, "json")
    backup_path = Path(path)
    backup_path.write_text(data, encoding="utf-8")
    return backup_path
