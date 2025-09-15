#!/usr/bin/env python3
"""
Coordinate Loader - Load and validate agent coordinates from JSON files
=====================================================================

Loads agent coordinates from JSON files with comprehensive validation.
Provides type-safe coordinate access and validation reporting.

Author: Agent-8 (Operations & Swarm Coordinator)
License: MIT
"""

from __future__ import annotations

import builtins
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

COORD_MIN = -10_000
COORD_MAX = 10_000


@dataclass(frozen=True)
class AgentCoords:
    agent_id: str
    x: int
    y: int
    raw: Any

    @property
    def tuple(self) -> builtins.tuple[int, int]:
        return (self.x, self.y)


@dataclass(frozen=True)
class ValidationIssue:
    agent_id: str
    level: str  # "ERROR" | "WARN"
    message: str


@dataclass
class ValidationReport:
    ok: list[str]
    issues: list[ValidationIssue]

    def is_all_ok(self) -> bool:
        return len(self.issues) == 0

    def to_lines(self) -> list[str]:
        lines: list[str] = []
        for a in self.ok:
            lines.append(f"OK    : {a}")
        for i in self.issues:
            lines.append(f"{i.level:<5}: {i.agent_id} -> {i.message}")
        return lines


class CoordinateLoader:
    """
    Loads and validates agent coordinates from a JSON SSOT.

    Expected JSON shape (excerpt):
    {
      "agents": {
        "Agent-1": {"chat_input_coordinates": [-1269, 481], "active": true, ...},
        "Agent-2": {"chat_input_coordinates": [-308, 480], "active": true, ...}
      }
    }
    """

    def __init__(self, path: str | Path | None = None):
        if path is None:
            # Try default locations
            cursor_file = Path("cursor_agent_coords.json")
            config_file = Path("config/coordinates.json")

            if cursor_file.exists():
                self.path = cursor_file
            elif config_file.exists():
                self.path = config_file
            else:
                raise FileNotFoundError("No coordinate file found in default locations")
        else:
            self.path = Path(path)

        self._data: dict[str, Any] = {}
        self._coords_cache: dict[str, AgentCoords] = {}

    # ---------- Load ----------
    def load(self) -> None:
        if not self.path.exists():
            raise FileNotFoundError(f"Coordinate file not found: {self.path}")
        self._data = json.loads(self.path.read_text(encoding="utf-8"))
        self._coords_cache.clear()

    # ---------- Access ----------
    def get_agent_ids(self) -> list[str]:
        return list((self._data.get("agents") or {}).keys())

    def get_coords(self, agent_id: str) -> AgentCoords:
        if agent_id in self._coords_cache:
            return self._coords_cache[agent_id]

        agents = self._data.get("agents") or {}
        entry = agents.get(agent_id)
        if not entry:
            raise KeyError(f"Agent not found in coordinate file: {agent_id}")

        coords = entry.get("chat_input_coordinates")
        if not isinstance(coords, (list, tuple)) or len(coords) != 2:
            raise ValueError(f"Malformed coordinates for {agent_id}: {coords}")

        try:
            x = int(coords[0])
            y = int(coords[1])
        except (TypeError, ValueError) as e:
            raise ValueError(f"Non-numeric coordinates for {agent_id}: {coords}") from e

        ac = AgentCoords(agent_id=agent_id, x=x, y=y, raw=entry)
        self._coords_cache[agent_id] = ac
        return ac

    # ---------- Validation ----------
    def validate_agent(self, agent_id: str) -> ValidationReport:
        ok: list[str] = []
        issues: list[ValidationIssue] = []

        try:
            ac = self.get_coords(agent_id)
        except Exception as e:
            issues.append(ValidationIssue(agent_id, "ERROR", str(e)))
            return ValidationReport(ok=[], issues=issues)

        # Default (0,0) detector
        if ac.x == 0 and ac.y == 0:
            issues.append(ValidationIssue(agent_id, "WARN", "Default (0,0) likely unconfigured"))

        # Range checks
        if not (COORD_MIN <= ac.x <= COORD_MAX):
            issues.append(ValidationIssue(agent_id, "ERROR", f"x out of range {ac.x}"))
        if not (COORD_MIN <= ac.y <= COORD_MAX):
            issues.append(ValidationIssue(agent_id, "ERROR", f"y out of range {ac.y}"))

        if len(issues) == 0:
            ok.append(agent_id)

        return ValidationReport(ok=ok, issues=issues)

    def validate_all(self) -> ValidationReport:
        ok: list[str] = []
        issues: list[ValidationIssue] = []
        for aid in self.get_agent_ids():
            r = self.validate_agent(aid)
            ok.extend(r.ok)
            issues.extend(r.issues)
        return ValidationReport(ok=ok, issues=issues)

    # ---------- Legacy compatibility methods ----------
    def get_chat_coordinates(self, agent_id: str) -> tuple[int, int] | None:
        """Legacy compatibility method."""
        try:
            return self.get_coords(agent_id).tuple
        except Exception:
            return None

    def get_all_agents(self) -> list[str]:
        """Legacy compatibility method."""
        return self.get_agent_ids()

    def is_agent_active(self, agent_id: str) -> bool:
        """Legacy compatibility method."""
        report = self.validate_agent(agent_id)
        return report.is_all_ok()

    def get_valid_agents(self) -> list[str]:
        """Legacy compatibility method."""
        report = self.validate_all()
        return report.ok

    def get_validation_report(self) -> dict[str, Any]:
        """Legacy compatibility method."""
        report = self.validate_all()
        return {
            "total_agents": len(self.get_agent_ids()),
            "valid_agents": report.ok,
            "invalid_agents": [i.agent_id for i in report.issues],
            "validation_errors": {i.agent_id: i.message for i in report.issues},
        }


# ---------- Legacy compatibility functions ----------
def load_coordinates_from_json() -> dict[str, list[int]]:
    """Legacy compatibility function."""
    try:
        loader = CoordinateLoader()
        loader.load()
        coords = {}
        for agent_id in loader.get_agent_ids():
            try:
                ac = loader.get_coords(agent_id)
                coords[agent_id] = [ac.x, ac.y]
            except Exception:
                coords[agent_id] = [0, 0]
        return coords
    except Exception as e:
        logger.warning(f"Failed to load coordinates: {e}")
        return {}


def get_agent_coordinates(agent_id: str) -> list[int] | None:
    """Legacy compatibility function."""
    try:
        loader = CoordinateLoader()
        loader.load()
        ac = loader.get_coords(agent_id)
        return [ac.x, ac.y]
    except Exception:
        return None


def get_coordinate_loader():
    """Get the coordinate loader instance."""
    return CoordinateLoader()
