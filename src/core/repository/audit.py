"""Repository auditing utilities."""
from __future__ import annotations

import subprocess
from typing import Dict, List

from config.repo_config import RepoConfig, get_repo_config


def audit_repository(config: RepoConfig | None = None) -> Dict[str, List[str]]:
    """Audit repository for local changes.

    Returns a dictionary with lists of modified and untracked files.
    """
    cfg = config or get_repo_config()
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=cfg.root_path,
        check=False,
        capture_output=True,
        text=True,
    )
    modified: List[str] = []
    untracked: List[str] = []
    for line in result.stdout.splitlines():
        status, file = line[:2], line[3:]
        if status == "??":
            untracked.append(file)
        elif file:
            modified.append(file)
    return {"modified": modified, "untracked": untracked}
