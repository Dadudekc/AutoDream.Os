"""Orchestrator for OSRS test modules.

This module aggregates OSRS-related tests to allow running them as a single
suite. It imports individual test modules located in ``tests.gaming.osrs`` and
combines them using Python's ``unittest`` framework.
"""

import sys
import unittest
from pathlib import Path

# Ensure project root is on the path when executed directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tests.gaming.osrs import (
    test_osrs_game_setup,
    test_osrs_ai_agent,
    test_osrs_scenarios,
    test_osrs_validation,
)


def load_tests() -> unittest.TestSuite:  # type: ignore[override]
    """Build a test suite containing all OSRS modules."""
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    for module in (
        test_osrs_game_setup,
        test_osrs_ai_agent,
        test_osrs_scenarios,
        test_osrs_validation,
    ):
        suite.addTests(loader.loadTestsFromModule(module))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(load_tests())
