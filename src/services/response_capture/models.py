"""Data models for the response capture service."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

from config.config import (
    FILE_WATCH_ROOT,
    FILE_RESPONSE_NAME,
    CLIPBOARD_POLL_MS,
    OCR_LANG,
    OCR_PSM,
)


class CaptureStrategy(str, Enum):
    """Available response capture strategies."""

    FILE = "file"
    CLIPBOARD = "clipboard"
    OCR = "ocr"
    HYBRID = "hybrid"


class CaptureStatus(str, Enum):
    """Capture operation status."""

    IDLE = "idle"
    MONITORING = "monitoring"
    CAPTURING = "capturing"
    ERROR = "error"


@dataclass
class CaptureConfig:
    """Configuration options for response capture."""

    strategy: CaptureStrategy
    file_watch_root: str = FILE_WATCH_ROOT
    file_response_name: str = FILE_RESPONSE_NAME
    clipboard_poll_ms: int = CLIPBOARD_POLL_MS
    ocr_tesseract_cmd: Optional[str] = None
    ocr_lang: str = OCR_LANG
    ocr_psm: int = OCR_PSM


@dataclass
class CapturedResponse:
    """Captured response data."""

    agent_id: str
    content: str
    source: str
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None


__all__ = [
    "CaptureStrategy",
    "CaptureStatus",
    "CaptureConfig",
    "CapturedResponse",
]
