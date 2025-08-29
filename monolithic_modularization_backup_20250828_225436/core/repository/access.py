"""Repository access utilities."""
from __future__ import annotations

from pathlib import Path
from typing import List

from config.repo_config import RepoConfig, get_repo_config


def is_repository(path: Path) -> bool:
    """Return True if *path* points to a git repository."""
    return (path / ".git").exists()


def list_files(config: RepoConfig | None = None) -> List[Path]:
    """List all files in the repository defined by *config*.

    Parameters
    ----------
    config:
        Repository configuration. If not provided, the default configuration
        is used.
    """
    cfg = config or get_repo_config()
    root = cfg.root_path
    return [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
