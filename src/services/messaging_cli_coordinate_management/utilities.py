"""Utility helpers for coordinate management."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

from ..messaging_cli_utils import MessagingCLIUtils


def load_coords_file(
    utils: MessagingCLIUtils, file_path: str
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Load coordinates from ``file_path`` if valid.

    Args:
        utils: Utility instance for file operations.
        file_path: Path to the coordinates JSON file.

    Returns:
        A tuple ``(data, error)`` where ``data`` is the parsed coordinates dict
        if successful, otherwise ``None``. ``error`` contains an error message
        when loading fails.
    """
    if not os.path.exists(file_path):
        return None, f"File {file_path} not found"
    data = utils.read_json(file_path)
    if not data or "agents" not in data:
        return None, "Invalid coordinates file"
    return data, None
