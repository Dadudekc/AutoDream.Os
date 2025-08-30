"""Repository configuration module.

Provides a single source of truth (SSOT) for repository related settings.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class RepoConfig:
    """Configuration for repository operations."""

    root_path: Path = BASE_PATH
    remote: str = "origin"


def get_repo_config() -> RepoConfig:
    """Return default repository configuration.

    This function acts as a SSOT so that all repository modules share the
    same configuration instance.
    """
    return RepoConfig()
