#!/usr/bin/env python3
"""Web dependency installation helpers."""
from __future__ import annotations

from pathlib import Path
import subprocess
from typing import List


class WebDependencyInstaller:
    """Install required packages for web development."""

    def __init__(self, pip_path: Path, python_path: Path, project_root: Path) -> None:
        """
        __init__
        
        Purpose: Automated function documentation
        """
        self.pip_path = pip_path
        self.python_path = python_path
        self.project_root = project_root
        self.requirements_file = project_root / "requirements_web_development.txt"

    def run_command(self, command: List[str]) -> bool:
        """
        run_command
        
        Purpose: Automated function documentation
        """
        try:
            print(f"🔄 Running: {' '.join(command)}")
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError as exc:
            print(f"❌ Command failed: {exc}")
            return False

    def install_core_dependencies(self) -> bool:
        """Install core framework dependencies."""
        core_deps = [
            "flask>=2.3.0",
            "fastapi>=0.104.0",
            "selenium>=4.15.0",
            "pytest>=7.4.0",
        ]
        for dep in core_deps:
            if not self.run_command([str(self.pip_path), "install", dep]):
                return False
        if self.requirements_file.exists():
            self.run_command([str(self.pip_path), "install", "-r", str(self.requirements_file)])
        return True

    def setup_webdriver_managers(self) -> bool:
        """Install webdriver-manager and verify Selenium setup."""
        if not self.run_command([str(self.python_path), "-m", "pip", "install", "webdriver-manager"]):
            return False
        test_code = (
            "from webdriver_manager.chrome import ChromeDriverManager\n"
            "ChromeDriverManager().install()\n"
            "print('✅ webdriver-manager ready')\n"
        )
        test_file = self.project_root / "test_webdriver.py"
        test_file.write_text(test_code)
        try:
            return self.run_command([str(self.python_path), str(test_file)])
        finally:
            test_file.unlink(missing_ok=True)

