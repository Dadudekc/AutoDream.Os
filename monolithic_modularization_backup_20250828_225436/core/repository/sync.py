"""Repository synchronization utilities."""
from __future__ import annotations

import subprocess
from typing import Optional

from config.repo_config import RepoConfig, get_repo_config


def fetch(config: RepoConfig | None = None) -> subprocess.CompletedProcess[str]:
    """Fetch updates from the remote without merging."""
    cfg = config or get_repo_config()
    return subprocess.run(
        ["git", "fetch", cfg.remote],
        cwd=cfg.root_path,
        check=False,
        capture_output=True,
        text=True,
    )


def get_status(config: RepoConfig | None = None) -> str:
    """Return short repository status."""
    cfg = config or get_repo_config()
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=cfg.root_path,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()
