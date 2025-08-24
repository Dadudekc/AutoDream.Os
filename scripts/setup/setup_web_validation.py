#!/usr/bin/env python3
"""Validation helpers for the web development setup."""
from __future__ import annotations

from pathlib import Path
import subprocess
from typing import List


class WebSetupValidator:
    """Run lightweight verification tests."""

    def __init__(self, python_path: Path, project_root: Path) -> None:
        self.python_path = python_path
        self.project_root = project_root

    def run_command(self, command: List[str]) -> bool:
        try:
            print(f"🔄 Running: {' '.join(command)}")
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError as exc:
            print(f"❌ Command failed: {exc}")
            return False

    def run_import_tests(self) -> bool:
        """Verify core frameworks can be imported."""
        test_code = (
            "import flask\n"
            "import fastapi\n"
            "import selenium\n"
            "import pytest\n"
            "print('✅ Core imports succeeded')\n"
        )
        test_file = self.project_root / "test_imports.py"
        test_file.write_text(test_code)
        try:
            return self.run_command([str(self.python_path), str(test_file)])
        finally:
            test_file.unlink(missing_ok=True)
