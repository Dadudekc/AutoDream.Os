"""Utility for managing status report files."""

from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional


@dataclass
class StatusReportWriter:
    """Handle creation and cleanup of status report files."""

    _file: Optional[tempfile._TemporaryFileWrapper] = None
    path: Optional[Path] = None

    def initialize(self) -> None:
        """Allocate a temporary file for status reporting."""
        self._file = tempfile.NamedTemporaryFile(
            prefix="status_manager_", suffix=".json", delete=False, mode="w"
        )
        self.path = Path(self._file.name)

    def finalize(self, summary: Dict[str, Any]) -> None:
        """Write summary data and close the report file."""
        if self._file:
            json.dump(summary, self._file)
            self._file.close()
            self._file = None
