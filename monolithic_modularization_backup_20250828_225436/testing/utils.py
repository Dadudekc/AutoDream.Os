"""Helper utilities for running shell commands."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable, Tuple, Optional


def run_command(cmd: Iterable[str], timeout: int = 30, cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr).

    Parameters
    ----------
    cmd: Iterable[str]
        Command and arguments to execute.
    timeout: int
        Maximum time in seconds to allow the command to run.
    cwd: Optional[Path]
        Working directory for the command.
    """
    result = subprocess.run(
        list(cmd),
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(cwd) if cwd else None,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()
