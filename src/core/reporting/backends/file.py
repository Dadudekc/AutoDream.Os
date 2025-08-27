from __future__ import annotations

"""File system backend for persisting reports."""

from pathlib import Path

from .base import ReportBackend


class FileReportBackend(ReportBackend):
    """Stores reports on the local file system."""

    def save(self, path: Path, content: str) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return str(path)
