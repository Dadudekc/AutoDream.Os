#!/usr/bin/env python3
"""Web environment preparation utilities."""
from __future__ import annotations

from pathlib import Path
import platform
import subprocess
from typing import List, Optional, Tuple


class WebEnvironmentSetup:
    """Prepare the Python environment for web development."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.venv_path = project_root / "venv_web_dev"
        self.is_windows = platform.system() == "Windows"
        self.python_executable = "python" if self.is_windows else "python3"

    def run_command(self, command: List[str], cwd: Optional[Path] = None) -> bool:
        """Run a shell command and report success."""
        try:
            print(f"🔄 Running: {' '.join(command)}")
            subprocess.run(command, cwd=cwd or self.project_root, check=True)
            return True
        except subprocess.CalledProcessError as exc:
            print(f"❌ Command failed: {exc}")
            return False

    def check_python_version(self) -> bool:
        """Verify a Python 3 interpreter is available."""
        try:
            result = subprocess.run(
                [self.python_executable, "--version"],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"🐍 Python Version: {result.stdout.strip()}")
            return result.stdout.startswith("Python 3")
        except Exception as exc:  # pragma: no cover - defensive
            print(f"❌ Error checking Python version: {exc}")
            return False

    def create_virtual_environment(self) -> bool:
        """Create a dedicated virtual environment for web development."""
        if self.venv_path.exists():
            print(f"📁 Virtual environment already exists at {self.venv_path}")
            return True
        print(f"🔧 Creating virtual environment at {self.venv_path}")
        return self.run_command([self.python_executable, "-m", "venv", str(self.venv_path)])

    def activate_virtual_environment(self) -> Tuple[Path, Path]:
        """Return paths to python and pip inside the virtual environment."""
        if self.is_windows:
            pip_path = self.venv_path / "Scripts" / "pip.exe"
            python_path = self.venv_path / "Scripts" / "python.exe"
        else:
            pip_path = self.venv_path / "bin" / "pip"
            python_path = self.venv_path / "bin" / "python"
        if not pip_path.exists() or not python_path.exists():
            raise RuntimeError("Virtual environment not properly created")
        self.run_command([str(pip_path), "install", "--upgrade", "pip"])
        return python_path, pip_path
