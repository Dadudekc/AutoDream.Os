"""Centralized configuration constants for the project."""

from __future__ import annotations

# Default paths and filenames for response capture
FILE_WATCH_ROOT: str = "agent_workspaces"
FILE_RESPONSE_NAME: str = "response.txt"

# Response capture timing
CLIPBOARD_POLL_MS: int = 500

# Optical character recognition defaults
OCR_LANG: str = "eng"
OCR_PSM: int = 6

__all__ = [
    "FILE_WATCH_ROOT",
    "FILE_RESPONSE_NAME",
    "CLIPBOARD_POLL_MS",
    "OCR_LANG",
    "OCR_PSM",
]
