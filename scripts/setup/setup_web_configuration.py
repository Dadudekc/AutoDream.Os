#!/usr/bin/env python3
"""Generate configuration and project structure for web development."""
from __future__ import annotations

from pathlib import Path
import json


class WebConfigurator:
    """Create directories and configuration files."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def create_directory_structure(self) -> None:
        """Create common web development directories."""
        dirs = [
            "src/web/automation",
            "src/web/api",
            "src/web/frontend",
            "src/web/testing",
            "tests/web",
            "web_config",
            "web_logs",
        ]
        for rel_path in dirs:
            path = self.project_root / rel_path
            path.mkdir(parents=True, exist_ok=True)
            print(f"📂 Created: {rel_path}")

    def create_config_files(self) -> None:
        """Create minimal Flask and Selenium configuration files."""
        config_dir = self.project_root / "web_config"
        flask_config = {"development": {"DEBUG": True, "TESTING": False}}
        selenium_config = {
            "browsers": {"chrome": {"headless": False, "window_size": "1920x1080"}}
        }
        (config_dir / "flask_config.json").write_text(json.dumps(flask_config, indent=2))
        (config_dir / "selenium_config.json").write_text(
            json.dumps(selenium_config, indent=2)
        )
        print(f"⚙️  Configuration files created in {config_dir}")
