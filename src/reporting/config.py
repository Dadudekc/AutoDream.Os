from src.utils.config_core import get_config

# MIGRATED: This file has been migrated to the centralized configuration system
"""Shared configuration for error report generation."""

from pathlib import Path
from enum import Enum


class ReportFormat(str, Enum):
    """Supported report output formats."""

    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"
    CSV = "csv"
    CONSOLE = "console"


# Default configuration values
DEFAULT_REPORTS_DIR = Path("reports")
DEFAULT_FORMAT = ReportFormat.JSON
INCLUDE_METADATA = get_config('INCLUDE_METADATA', True)
INCLUDE_RECOMMENDATIONS = get_config('INCLUDE_RECOMMENDATIONS', True)

# Template fragments
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head><title>Error Analytics Report</title></head>
<body>{content}</body>
</html>
"""

MARKDOWN_TEMPLATE = """# Error Analytics Report\n\n{content}\n"""
