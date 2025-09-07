"""Utilities for cleaning up test artifacts.

This module provides helpers to clear out files generated during test runs. It relies on
directory locations defined in :mod:`tests.testing_config` to maintain a single source of
truth for test artifacts.
"""

from tests.testing_config import COVERAGE_DIR, RESULTS_DIR


def cleanup_artifacts() -> None:
    """Remove files generated during test runs.

    The function iterates over the configured results and coverage directories, deleting
    any files present while leaving directory structures intact.
    """

    for directory in (RESULTS_DIR, COVERAGE_DIR):
        if directory.exists():
            for item in directory.iterdir():
                if item.is_file():
                    item.unlink()


__all__ = ["cleanup_artifacts"]

