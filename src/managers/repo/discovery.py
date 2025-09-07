"""Repository discovery helpers."""

from __future__ import annotations

from pathlib import Path
from typing import List


def discover_repositories(root: str) -> List[str]:
    """Return a list of git repository paths under *root*.

    The function searches recursively for directories containing a ``.git``
    folder and returns the parent directory of each match.
    """
    base = Path(root)
    repositories: List[str] = []
    for git_dir in base.rglob(".git"):
        if git_dir.is_dir():
            repositories.append(str(git_dir.parent.resolve()))
    return repositories
