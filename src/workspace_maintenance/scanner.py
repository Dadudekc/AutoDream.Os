"""Workspace scanning utilities."""

from pathlib import Path
from typing import List


class WorkspaceScanner:
    """Recursively scan a workspace directory for files."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def scan(self) -> List[Path]:
        """Return a list of all files within the workspace."""
        files: List[Path] = []
        for path in self.root.rglob("*"):
            if path.is_file():
                files.append(path)
        return files
