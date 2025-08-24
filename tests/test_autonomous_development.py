"""Orchestrator for autonomous development tests."""

import unittest

from . import (
    test_autonomous_development_core,
    test_autonomous_development_workflow,
    test_autonomous_development_validation,
    test_autonomous_development_integration,
)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for module in [
        test_autonomous_development_core,
        test_autonomous_development_workflow,
        test_autonomous_development_validation,
        test_autonomous_development_integration,
    ]:
        suite.addTests(loader.loadTestsFromModule(module))
    return suite
