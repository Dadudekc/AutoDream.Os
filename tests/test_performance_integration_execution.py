#!/usr/bin/env python3
"""Performance integration execution tests."""

import time
import unittest

from core.performance_monitor import MetricType
from tests.test_performance_integration_setup import create_env, cleanup_env


class TestPerformanceExecution(unittest.TestCase):
    """Run key operations across components."""

    def setUp(self):
        self.env = create_env()

    def tearDown(self):
        cleanup_env(self.env)

    def test_record_metrics(self):
        tracker = self.env["tracker"]
        tracker.record_metric(MetricType.RESPONSE_TIME, 0.5, agent_id="exec")
        metrics = tracker.get_metrics(agent_id="exec")
        self.assertGreater(len(metrics), 0)

    def test_profile_function(self):
        profiler = self.env["profiler"]

        @profiler.profile_function("demo")
        def demo():
            time.sleep(0.01)
            return 42

        self.assertEqual(demo(), 42)
        summary = profiler.get_profiling_summary()
        self.assertIn("demo", summary)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
