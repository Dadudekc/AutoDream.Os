"""Cross-Platform Environment Core - Basic environment operations"""

import logging
import os
import platform
from pathlib import Path

logger = logging.getLogger(__name__)


class CrossPlatformEnvironment:
    """Cross-platform environment management utilities."""

    def __init__(self):
        self.platform = platform.system()
        self.is_windows = self.platform == "Windows"
        self.is_linux = self.platform == "Linux"
        self.is_macos = self.platform == "Darwin"

    def get_env_var(self, name: str, default: str | None = None) -> str | None:
        """Get environment variable with platform-specific handling."""
        value = os.environ.get(name, default)

        if value is None and self.is_windows:
            value = os.environ.get(name.upper(), default)
        elif value is None and not self.is_windows:
            value = os.environ.get(name.lower(), default)

        return value

    def set_env_var(self, name: str, value: str, overwrite: bool = True):
        """Set environment variable."""
        if overwrite or name not in os.environ:
            os.environ[name] = value
            logger.info(f"Set environment variable: {name}")

    def get_path_env(self) -> list:
        """Get PATH environment variable as list."""
        path_var = self.get_env_var("PATH", "")
        separator = ";" if self.is_windows else ":"
        return [p for p in path_var.split(separator) if p]

    def add_to_path(self, path: str | Path):
        """Add path to PATH environment variable."""
        path_str = str(path)
        current_path = self.get_path_env()

        if path_str not in current_path:
            separator = ";" if self.is_windows else ":"
            new_path = separator.join([path_str] + current_path)
            self.set_env_var("PATH", new_path)
            logger.info(f"Added to PATH: {path_str}")

    def get_python_path(self) -> Path:
        """Get Python executable path."""
        return Path(sys.executable) if hasattr(sys, 'executable') else Path("python")

    def get_python_version(self) -> str:
        """Get Python version string."""
        return platform.python_version()

