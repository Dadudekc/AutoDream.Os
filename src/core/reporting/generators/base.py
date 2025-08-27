"""Base class for unified report generators."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

from ..report_models import ReportConfig, UnifiedReport


class ReportGenerator:
    """Base report generator class."""

    def __init__(self, config: ReportConfig):
        self.config = config
        self.output_dir = Path(config.output_directory)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(f"{__name__}.ReportGenerator")

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a report from data."""
        raise NotImplementedError("Subclasses must implement generate_report")

    def _ensure_output_dir(self) -> None:
        """Ensure the output directory exists."""
        self.output_dir.mkdir(exist_ok=True, parents=True)
