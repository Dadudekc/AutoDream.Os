"""Utility functions for preparing the test environment."""

from tests.testing_config import RESULTS_DIR, COVERAGE_DIR


def prepare_environment() -> None:
    """Ensure that required directories for tests exist."""
    for directory in (RESULTS_DIR, COVERAGE_DIR):
        directory.mkdir(exist_ok=True)
