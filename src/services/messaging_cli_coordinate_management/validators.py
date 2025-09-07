"""Validation helpers for coordinate management."""

from __future__ import annotations

from typing import Tuple


def parse_coord_string(coord_string: str) -> Tuple[str, int, int]:
    """Parse and validate a coordinate string.

    Args:
        coord_string: Comma-separated string ``agent_id,x,y``.

    Returns:
        A tuple of ``(agent_id, x, y)``.

    Raises:
        ValueError: If the string is not in the expected format or contains non-integer values.
    """
    parts = coord_string.split(",")
    if len(parts) != 3:
        raise ValueError("Invalid format. Use: agent_id,x,y")
    agent_id, x_str, y_str = parts
    try:
        x, y = int(x_str), int(y_str)
    except ValueError as exc:  # pragma: no cover - defensive
        raise ValueError("Coordinates must be integers") from exc
    return agent_id, x, y
