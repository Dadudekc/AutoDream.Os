#!/usr/bin/env python3
"""
Validation Utils
================

Common validation utilities and helper functions.
V2 Compliance: ≤100 lines, utility functions, KISS principle.
"""

import json
from pathlib import Path
from typing import Any


def load_json_file(file_path: Path) -> dict[str, Any] | None:
    """Safely load JSON file."""
    try:
        if not file_path.exists():
            return None

        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_json_file(file_path: Path, data: dict[str, Any]) -> bool:
    """Safely save JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False


def check_file_exists(file_path: Path) -> bool:
    """Check if file exists."""
    return file_path.exists()


def validate_required_fields(data: dict[str, Any], required_fields: list[str]) -> bool:
    """Validate that all required fields are present."""
    return all(field in data for field in required_fields)


def get_team_alpha_agents() -> list[str]:
    """Get list of Team Alpha agents."""
    return ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]


def format_validation_summary(passed: int, total: int) -> str:
    """Format validation summary string."""
    return f"{passed}/{total} tests passed"
