"""Orchestrator for OSRS test modules"""

import sys
import unittest
from pathlib import Path

# Ensure project root is on the path when executed directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def run_osrs_test_suite() -> unittest.result.TestResult:
    """Collect and run OSRS-related test modules"""
    from tests.gaming import (
        test_osrs_game_setup,
        test_osrs_ai_agent,
        test_osrs_scenarios,
        test_osrs_validation,
    )

    suite = unittest.TestSuite()
    for module in (
        test_osrs_game_setup,
        test_osrs_ai_agent,
        test_osrs_scenarios,
        test_osrs_validation,
    ):
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))

    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    result = run_osrs_test_suite()
    sys.exit(0 if result.wasSuccessful() else 1)
