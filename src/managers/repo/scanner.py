"""Repository scanning utilities."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Dict, Any


def scan_repository(path: str) -> Dict[str, Any]:
    """Gather basic metrics for a repository located at *path*.

    Metrics include the number of files, total size in bytes and a count of
    file extensions present within the repository.
    """
    repo_path = Path(path)
    files = [p for p in repo_path.rglob("*") if p.is_file()]
    total_size = sum(p.stat().st_size for p in files)
    languages = Counter(p.suffix.lstrip(".") or "no_extension" for p in files)
    return {
        "path": str(repo_path.resolve()),
        "file_count": len(files),
        "total_size": total_size,
        "languages": dict(languages),
    }
