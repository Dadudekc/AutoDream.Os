#!/usr/bin/env python3
"""Orchestrator for performance integration tests."""

import sys
import unittest
from importlib import import_module

MODULES = [
    "tests.test_performance_integration_setup",
    "tests.test_performance_integration_execution",
    "tests.test_performance_integration_validation",
    "tests.test_performance_integration_cleanup",
]


def load_suite():
    """Load tests from each module in ``MODULES``."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for name in MODULES:
        module = import_module(name)
        suite.addTests(loader.loadTestsFromModule(module))
    return suite


def run():
    """Run the aggregated integration suite."""
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(load_suite())
    return result.wasSuccessful()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(0 if run() else 1)
