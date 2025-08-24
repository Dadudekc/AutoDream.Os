"""Module providing a lightweight pytest runner."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, Tuple

from .utils import run_command


class TestRunner:
    """Execute pytest on a given test path."""

    def __init__(self, tests_path: Path):
        self.tests_path = Path(tests_path)

    def run(self, extra_args: Iterable[str] | None = None) -> Tuple[int, str, str]:
        """Run pytest for ``tests_path`` and return command result."""
        cmd = [sys.executable, "-m", "pytest", str(self.tests_path)]
        if extra_args:
            cmd.extend(list(extra_args))
        return run_command(cmd, cwd=self.tests_path)
