"""Code generation helpers."""
from __future__ import annotations

from pathlib import Path


def write_file(path: Path, content: str) -> None:
    """Write ``content`` to ``path`` ensuring parent directories exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
