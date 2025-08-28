"""Utilities for importing analysis data from files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .archive_config import ENCODING


def load_project_data(file_path: Path) -> Dict[str, Any]:
    """Load project analysis data from a JSON file.

    Parameters
    ----------
    file_path:
        Path to the JSON file containing project analysis output.

    Returns
    -------
    Dict[str, Any]
        Parsed data from the file.
    """
    with open(file_path, "r", encoding=ENCODING) as f:
        return json.load(f)
