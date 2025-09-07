"""Centralized configuration for tests.

This module defines directory locations used during testing to store intermediate artifacts.
By keeping these paths here, we maintain a single source of truth for test configuration.
"""

from pathlib import Path


BASE_TEST_DIR: Path = Path(__file__).resolve().parent
RESULTS_DIR: Path = BASE_TEST_DIR / "results"
COVERAGE_DIR: Path = BASE_TEST_DIR / "coverage"


__all__ = ["BASE_TEST_DIR", "RESULTS_DIR", "COVERAGE_DIR"]

