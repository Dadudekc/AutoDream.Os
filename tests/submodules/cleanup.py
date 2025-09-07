"""Utilities for cleaning up test artifacts."""

from ..testing_config import RESULTS_DIR, COVERAGE_DIR


def cleanup_artifacts() -> None:
    """Remove files generated during test runs."""
    for directory in (RESULTS_DIR, COVERAGE_DIR):
        if directory.exists():
            for item in directory.iterdir():
                if item.is_file():
                    item.unlink()
