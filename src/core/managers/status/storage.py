"""Persistence utilities for status data."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Union

from ..status_entities import ComponentHealth
from .tracker import StatusTracker
from .broadcaster import StatusBroadcaster


class StatusStorage:
    """Handle persistence of status information."""

    def __init__(self, tracker: StatusTracker, broadcaster: StatusBroadcaster) -> None:
        self.tracker = tracker
        self.broadcaster = broadcaster

    # ------------------------------------------------------------------
    # In-memory state management
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """Clear all tracked status information."""
        self.tracker.clear()
        self.broadcaster.clear()

    def backup(self) -> Dict[str, Any]:
        """Create an in-memory backup of current status."""
        data = self.tracker.registry.backup()
        data["component_health"] = {
            k: asdict(v) for k, v in self.broadcaster.component_health.items()
        }
        return data

    def restore(self, state: Dict[str, Any]) -> None:
        """Restore status information from backup."""
        self.tracker.registry.restore(state)
        for k, v in state.get("component_health", {}).items():
            self.broadcaster.component_health[k] = ComponentHealth(**v)

    # ------------------------------------------------------------------
    # File persistence helpers
    # ------------------------------------------------------------------
    def save(self, path: Union[str, Path]) -> None:
        """Persist current status to a JSON file."""
        data = self.backup()
        with open(path, "w") as f:
            json.dump(data, f)

    def load(self, path: Union[str, Path]) -> None:
        """Load status information from a JSON file."""
        file_path = Path(path)
        if file_path.exists():
            with open(file_path, "r") as f:
                data = json.load(f)
            self.restore(data)
