#!/usr/bin/env python3
"""Validate agent workspaces against coordinate SSOT."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Set


def load_ssot_agents(coord_file: Path) -> Set[str]:
    """Return agent IDs defined in the SSOT coordinate file."""
    data = json.loads(coord_file.read_text(encoding="utf-8"))
    return set(data.get("agents", {}).keys())


def list_workspace_agents(workspaces_dir: Path) -> Set[str]:
    """Return agent IDs present in agent_workspaces directory."""
    return {
        p.name
        for p in workspaces_dir.iterdir()
        if p.is_dir() and p.name.startswith("Agent-")
    }


def find_coordinate_entries(workspaces_dir: Path) -> Dict[str, str]:
    """Find files in workspaces that contain hard-coded coordinates."""
    pattern = re.compile(r"\(-?\d+\s*,\s*-?\d+\)")
    offenders: Dict[str, str] = {}
    for path in workspaces_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "coordinates" in text and pattern.search(text):
                offenders[str(path)] = path.name
    return offenders


def validate_workspaces(
    workspaces_dir: Path = Path("agent_workspaces"),
    coord_file: Path = Path("cursor_agent_coords.json"),
) -> bool:
    """Validate workspace directories against coordinate SSOT."""
    agents_in_ssot = load_ssot_agents(coord_file)
    agents_in_ws = list_workspace_agents(workspaces_dir)

    missing = agents_in_ssot - agents_in_ws
    extra = agents_in_ws - agents_in_ssot
    offenders = find_coordinate_entries(workspaces_dir)

    if missing or offenders:
        if missing:
            print(f"Agents missing workspace directories: {sorted(missing)}")
        if offenders:
            print("Coordinate entries found in workspaces:")
            for file in offenders:
                print(f" - {file}")
        return False
    if extra:
        print(f"Extra workspace directories without SSOT entry: {sorted(extra)}")
    return True


if __name__ == "__main__":
    if not validate_workspaces():
        raise SystemExit(1)
    print("All workspaces match coordinate SSOT.")

