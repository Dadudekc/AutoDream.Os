#!/usr/bin/env python3
"""
Cross-Platform Path Utilities
==============================

This module provides cross-platform path utilities for the Agent Cellphone V2 system,
ensuring consistent file and directory handling across Windows and Linux platforms.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import logging
import os
import platform
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CrossPlatformPaths:
    """Cross-platform path management utilities."""

    def __init__(self):
        self.platform = platform.system()
        self.is_windows = self.platform == "Windows"
        self.is_linux = self.platform == "Linux"
        self.is_macos = self.platform == "Darwin"

    def normalize_path(self, path: str | Path) -> Path:
        """Normalize path for current platform."""
        if isinstance(path, str):
            path = Path(path)

        # Resolve relative paths and symlinks
        try:
            return path.resolve()
        except (OSError, RuntimeError):
            # If resolve fails, return absolute path
            return path.absolute()

    def join_paths(self, *paths: str | Path) -> Path:
        """Join paths in a cross-platform way."""
        result = Path(paths[0]) if paths else Path(".")

        for path in paths[1:]:
            result = result / path

        return self.normalize_path(result)

    def get_home_dir(self) -> Path:
        """Get user home directory."""
        return Path.home()

    def get_temp_dir(self) -> Path:
        """Get system temporary directory."""
        return Path(os.environ.get("TMPDIR", os.environ.get("TEMP", "/tmp")))

    def get_config_dir(self) -> Path:
        """Get application configuration directory."""
        if self.is_windows:
            # Windows: Use AppData/Roaming
            config_dir = self.get_home_dir() / "AppData" / "Roaming" / "AgentCellphoneV2"
        elif self.is_macos:
            # macOS: Use ~/Library/Application Support
            config_dir = (
                self.get_home_dir() / "Library" / "Application Support" / "AgentCellphoneV2"
            )
        else:
            # Linux: Use ~/.config
            config_dir = self.get_home_dir() / ".config" / "agent-cellphone-v2"

        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def get_data_dir(self) -> Path:
        """Get application data directory."""
        if self.is_windows:
            # Windows: Use AppData/Local
            data_dir = self.get_home_dir() / "AppData" / "Local" / "AgentCellphoneV2"
        elif self.is_macos:
            # macOS: Use ~/Library/Application Support
            data_dir = self.get_home_dir() / "Library" / "Application Support" / "AgentCellphoneV2"
        else:
            # Linux: Use ~/.local/share
            data_dir = self.get_home_dir() / ".local" / "share" / "agent-cellphone-v2"

        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    def get_log_dir(self) -> Path:
        """Get application log directory."""
        if self.is_windows:
            # Windows: Use AppData/Local/Logs
            log_dir = self.get_home_dir() / "AppData" / "Local" / "AgentCellphoneV2" / "Logs"
        elif self.is_macos:
            # macOS: Use ~/Library/Logs
            log_dir = self.get_home_dir() / "Library" / "Logs" / "AgentCellphoneV2"
        else:
            # Linux: Use ~/.local/log
            log_dir = self.get_home_dir() / ".local" / "log" / "agent-cellphone-v2"

        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    def get_cache_dir(self) -> Path:
        """Get application cache directory."""
        if self.is_windows:
            # Windows: Use AppData/Local/Cache
            cache_dir = self.get_home_dir() / "AppData" / "Local" / "AgentCellphoneV2" / "Cache"
        elif self.is_macos:
            # macOS: Use ~/Library/Caches
            cache_dir = self.get_home_dir() / "Library" / "Caches" / "AgentCellphoneV2"
        else:
            # Linux: Use ~/.cache
            cache_dir = self.get_home_dir() / ".cache" / "agent-cellphone-v2"

        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def ensure_dir(self, path: str | Path) -> Path:
        """Ensure directory exists, creating if necessary."""
        path = self.normalize_path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def safe_remove(self, path: str | Path) -> bool:
        """Safely remove file or directory."""
        try:
            path = self.normalize_path(path)
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                import shutil

                shutil.rmtree(path)
            return True
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not remove {path}: {e}")
            return False

    def get_relative_path(self, path: str | Path, base: str | Path) -> Path:
        """Get relative path from base."""
        path = self.normalize_path(path)
        base = self.normalize_path(base)

        try:
            return path.relative_to(base)
        except ValueError:
            # If not relative, return absolute path
            return path

    def is_same_path(self, path1: str | Path, path2: str | Path) -> bool:
        """Check if two paths refer to the same location."""
        try:
            return self.normalize_path(path1).samefile(self.normalize_path(path2))
        except (OSError, FileNotFoundError):
            return str(self.normalize_path(path1)) == str(self.normalize_path(path2))

    def get_file_size(self, path: str | Path) -> int:
        """Get file size in bytes."""
        path = self.normalize_path(path)
        if path.is_file():
            return path.stat().st_size
        return 0

    def get_directory_size(self, path: str | Path) -> int:
        """Get directory size in bytes."""
        path = self.normalize_path(path)
        total_size = 0

        if path.is_dir():
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size

        return total_size

    def list_files(self, path: str | Path, pattern: str = "*") -> list[Path]:
        """List files matching pattern."""
        path = self.normalize_path(path)
        if path.is_dir():
            return list(path.glob(pattern))
        return []

    def get_platform_info(self) -> dict:
        """Get platform-specific path information."""
        return {
            "platform": self.platform,
            "is_windows": self.is_windows,
            "is_linux": self.is_linux,
            "is_macos": self.is_macos,
            "home_dir": str(self.get_home_dir()),
            "temp_dir": str(self.get_temp_dir()),
            "config_dir": str(self.get_config_dir()),
            "data_dir": str(self.get_data_dir()),
            "log_dir": str(self.get_log_dir()),
            "cache_dir": str(self.get_cache_dir()),
            "path_separator": os.sep,
            "line_separator": os.linesep,
        }


# Global instance for easy access
path_manager = CrossPlatformPaths()


# Convenience functions
def normalize_path(path: str | Path) -> Path:
    """Normalize path for current platform."""
    return path_manager.normalize_path(path)


def join_paths(*paths: str | Path) -> Path:
    """Join paths in a cross-platform way."""
    return path_manager.join_paths(*paths)


def get_config_dir() -> Path:
    """Get application configuration directory."""
    return path_manager.get_config_dir()


def get_data_dir() -> Path:
    """Get application data directory."""
    return path_manager.get_data_dir()


def get_log_dir() -> Path:
    """Get application log directory."""
    return path_manager.get_log_dir()


def get_cache_dir() -> Path:
    """Get application cache directory."""
    return path_manager.get_cache_dir()


def ensure_dir(path: str | Path) -> Path:
    """Ensure directory exists, creating if necessary."""
    return path_manager.ensure_dir(path)


def safe_remove(path: str | Path) -> bool:
    """Safely remove file or directory."""
    return path_manager.safe_remove(path)


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def is_linux() -> bool:
    """Check if running on Linux."""
    return platform.system() == "Linux"


def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"
