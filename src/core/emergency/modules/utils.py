#!/usr/bin/env python3
"""Shared utilities for emergency response modules."""
from pathlib import Path
from typing import Optional

# Base directory points to repository root
BASE_DIR = Path(__file__).resolve().parents[4]
TEMPLATE_DIR = BASE_DIR / "docs" / "templates" / "emergency"


def load_template(name: str, templates_dir: Optional[Path] = None) -> str:
    """Load a documentation template by name."""
    directory = templates_dir or TEMPLATE_DIR
    template_path = directory / f"{name}.md"
    return template_path.read_text(encoding="utf-8")


def ensure_directory(path: Path) -> None:
    """Ensure that a directory exists."""
    path.mkdir(parents=True, exist_ok=True)
