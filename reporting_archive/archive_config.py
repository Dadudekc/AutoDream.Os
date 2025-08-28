"""Configuration for the reporting archive utilities."""

from pathlib import Path

# Root directory for generated archive reports
REPORTS_DIR: Path = Path("scanner_reports")
REPORTS_DIR.mkdir(exist_ok=True)

# Default encoding used for reading and writing files
ENCODING: str = "utf-8"
