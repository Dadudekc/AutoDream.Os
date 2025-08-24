#!/usr/bin/env python3
"""Performance integration cleanup tests."""

import unittest

from tests.test_performance_integration_setup import create_env, cleanup_env


class TestPerformanceCleanup(unittest.TestCase):
    """Verify resources are released properly."""

    def test_cleanup(self):
        env = create_env()
        cleanup_env(env)
        self.assertFalse(env["dashboard"].running)
        self.assertFalse(env["gateway"].gateway_active)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
