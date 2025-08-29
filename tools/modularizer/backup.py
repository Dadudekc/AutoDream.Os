"""Backup handling utilities."""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


def create_backup(src: Path = Path("src"), prefix: str = "monolithic_modularization_backup_") -> Path:
    """Create a timestamped backup of ``src``.

    Parameters
    ----------
    src:
        Source directory to back up. Defaults to ``src`` in the current working
        directory.
    prefix:
        Prefix for the backup directory name.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"{prefix}{timestamp}")
    if src.exists():
        shutil.copytree(src, backup_dir)
    return backup_dir
