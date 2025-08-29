"""Contract parsing utilities for refactoring workflows."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Union


def parse_contract(contract_path: Union[str, Path]) -> Dict[str, Any]:
    """Load contract information from a JSON file.

    Args:
        contract_path: Path to the contract file.

    Returns:
        Parsed contract data as a dictionary.

    Raises:
        FileNotFoundError: If the contract file does not exist.
        ValueError: If the file content is not valid JSON.
    """
    path = Path(contract_path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
