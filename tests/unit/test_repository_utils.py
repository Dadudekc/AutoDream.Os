"""Tests for repository utility modules."""
from __future__ import annotations

from pathlib import Path

from config.repo_config import get_repo_config
from src.core.repository import access, audit, sync


def test_is_repository() -> None:
    cfg = get_repo_config()
    assert access.is_repository(cfg.root_path)


def test_list_files_excludes_git_dir() -> None:
    cfg = get_repo_config()
    files = access.list_files(cfg)
    assert all(".git" not in p.parts for p in files)


def test_sync_get_status() -> None:
    status = sync.get_status()
    assert isinstance(status, str)


def test_audit_repository_returns_dict() -> None:
    result = audit.audit_repository()
    assert set(result.keys()) == {"modified", "untracked"}
