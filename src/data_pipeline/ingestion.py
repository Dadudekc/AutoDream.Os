from pathlib import Path
from typing import Dict
import hashlib
import re
import sys

    from typing import Protocol
from .data_config import RESPONSE_PATTERNS
from __future__ import annotations

"""Data ingestion utilities for capturing agent responses."""




if sys.version_info >= (3, 8):
else:
    Protocol = object  # type: ignore[misc,assignment]


class AnalyticsInterface(Protocol):
    """Protocol describing analytics dependency."""

    def analyze_and_generate_tasks(
        self, response_id: int, content: str, response_type: str, agent_id: str
    ) -> None:
        """Analyze content and optionally generate follow up tasks."""


class DatabaseInterface(Protocol):
    """Protocol describing storage dependency."""

    def insert_response(
        self,
        agent_id: str,
        response_file: str,
        response_content: str,
        response_hash: str,
        response_type: str,
        file_size: int,
    ) -> int:
        """Persist a captured response and return its identifier."""


class ResponseCapture:
    """Capture agent responses and trigger analytics."""

    def __init__(
        self, db: DatabaseInterface, analytics: AnalyticsInterface, response_patterns: Dict[str, str] | None = None
    ) -> None:
        self.db = db
        self.analytics = analytics
        self.response_patterns = response_patterns or RESPONSE_PATTERNS

    def classify_response(self, file_path: Path, content: str) -> str:
        """Classify the response based on filename and content."""
        filename = file_path.name.lower()
        for response_type, pattern in self.response_patterns.items():
            if re.search(pattern, filename):
                return response_type
        if "def " in content or "class " in content:
            return "code_file"
        if re.search(r"\b(error|exception)\b", content, re.IGNORECASE):
            return "error_report"
        if re.search(r"\b(analysis|report)\b", content, re.IGNORECASE):
            return "analysis_report"
        if re.search(r"\b(task|todo)\b", content, re.IGNORECASE):
            return "task_update"
        return "unknown"

    def capture_response(self, agent_id: str, response_file_path: str) -> bool:
        """Capture a response file and trigger analytics."""
        try:
            file_path = Path(response_file_path)
            if not file_path.exists():
                return False
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            response_type = self.classify_response(file_path, content)
            response_id = self.db.insert_response(
                agent_id,
                str(file_path),
                content,
                content_hash,
                response_type,
                file_path.stat().st_size,
            )
            if response_id:
                self.analytics.analyze_and_generate_tasks(
                    response_id, content, response_type, agent_id
                )
                return True
            return False
        except Exception as e:  # pragma: no cover - defensive programming
            print(f"❌ Error capturing response: {e}", file=sys.stderr)
            return False
