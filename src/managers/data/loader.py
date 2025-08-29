"""Utility functions for loading data from various sources."""

from pathlib import Path
from typing import Any, Optional, Tuple

import json
import pandas as pd


def detect_file_type(file_path: Path) -> str:
    """Detect the file type based on the extension.

    Returns a simple string identifier such as "csv", "json", "excel", or
    "text". Unknown extensions default to "text".
    """
    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix == ".json":
        return "json"
    if suffix in {".xlsx", ".xls"}:
        return "excel"
    if suffix in {".txt", ".md", ".py", ".js", ".html"}:
        return "text"
    return "text"


def load_file(file_path: str, data_type: Optional[str] = None) -> Tuple[Optional[Any], Optional[str]]:
    """Load data from a file path.

    Args:
        file_path: Path to the file on disk.
        data_type: Optional explicit data type string. If omitted, the type is
            detected from the file extension.

    Returns:
        Tuple of loaded data and the resolved data type string. If loading
        fails, both values will be ``None``.
    """
    path = Path(file_path)
    if not path.exists():
        return None, None

    if data_type is None:
        data_type = detect_file_type(path)

    try:
        if data_type == "csv":
            data = pd.read_csv(path)
        elif data_type == "json":
            with open(path, "r") as f:
                data = json.load(f)
        elif data_type == "excel":
            data = pd.read_excel(path)
        elif data_type == "text":
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
        else:
            return None, data_type
    except Exception:
        return None, None

    return data, data_type
