from pathlib import Path
from typing import Dict, Optional
import logging

        import pyperclip
from .models import CaptureConfig
from __future__ import annotations

"""Data access utilities for response capture."""





def init_file_monitoring(config: CaptureConfig, logger: logging.Logger) -> Dict[str, float]:
    """Discover response files to monitor."""
    watched: Dict[str, float] = {}
    watch_root = Path(config.file_watch_root)
    if watch_root.exists():
        for agent_dir in watch_root.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                response_file = agent_dir / config.file_response_name
                if response_file.exists():
                    watched[str(response_file)] = response_file.stat().st_mtime
                    logger.info("Monitoring response file: %s", response_file)
    else:
        logger.warning("Watch root directory not found: %s", watch_root)
    return watched


def read_response_file(file_path: str) -> str:
    """Read response text from a file."""
    return Path(file_path).read_text(encoding="utf-8").strip()


def clear_response_file(file_path: str, logger: logging.Logger) -> None:
    """Clear a response file after processing."""
    try:
        Path(file_path).write_text("", encoding="utf-8")
        logger.debug("Cleared response file: %s", file_path)
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to clear response file: %s", exc)


def get_clipboard_content(logger: logging.Logger) -> Optional[str]:
    """Return clipboard text if available."""
    try:

        content = pyperclip.paste()
        return content.strip() if content and content.strip() else None
    except ImportError:
        logger.debug("pyperclip not available for clipboard monitoring")
        return None


__all__ = [
    "init_file_monitoring",
    "read_response_file",
    "clear_response_file",
    "get_clipboard_content",
]
