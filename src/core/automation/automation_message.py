#!/usr/bin/env python3
"""
Automation Message - Message handling for automation system
==========================================================

Handles automation message creation, processing, and metadata management.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 compliance modularization
License: MIT
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class AutomationMessage:
    """Represents an automation message."""

    def __init__(
        self, file_path: Path, content: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """Initialize automation message."""
        self.file_path = file_path
        self.content = content
        self.metadata = metadata or {}
        self.processed_at = None
        self.processing_result = None

    def mark_processed(self, result: str = "success") -> None:
        """Mark message as processed."""
        self.processed_at = datetime.now()
        self.processing_result = result

    def to_dict(self) -> dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "file_path": str(self.file_path),
            "content": self.content,
            "metadata": self.metadata,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "processing_result": self.processing_result,
        }

    def is_processed(self) -> bool:
        """Check if message is processed."""
        return self.processed_at is not None

    def get_processing_time(self) -> float | None:
        """Get processing time in seconds."""
        if self.processed_at and hasattr(self, "created_at"):
            return (self.processed_at - self.created_at).total_seconds()
        return None

    def update_metadata(self, key: str, value: Any) -> None:
        """Update message metadata."""
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get message metadata."""
        return self.metadata.get(key, default)

    def validate(self) -> bool:
        """Validate message content."""
        if not self.content or not self.content.strip():
            logger.warning("Empty message content")
            return False
        
        if not self.file_path or not self.file_path.exists():
            logger.warning(f"Invalid file path: {self.file_path}")
            return False
        
        return True

    def __str__(self) -> str:
        """String representation."""
        return f"AutomationMessage(file={self.file_path.name}, processed={self.is_processed()})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"AutomationMessage("
            f"file_path={self.file_path}, "
            f"content_length={len(self.content)}, "
            f"processed={self.is_processed()}, "
            f"result={self.processing_result})"
        )
