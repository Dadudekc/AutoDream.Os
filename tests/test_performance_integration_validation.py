#!/usr/bin/env python3
"""Performance integration validation tests."""

import json
import os
import tempfile
import unittest

from core.performance_dashboard import DashboardView
from core.performance_monitor import MetricType
from tests.test_performance_integration_setup import create_env, cleanup_env


class TestPerformanceValidation(unittest.TestCase):
    """Validate data produced by operations."""

    def setUp(self):
        self.env = create_env()

    def tearDown(self):
        cleanup_env(self.env)

    def test_dashboard_view_and_metrics(self):
        tracker = self.env["tracker"]
        tracker.record_metric(MetricType.RESPONSE_TIME, 0.2, agent_id="val")
        dashboard = self.env["dashboard"]
        dashboard.set_view(DashboardView.SYSTEM_OVERVIEW)
        self.assertEqual(dashboard.current_view, DashboardView.SYSTEM_OVERVIEW)
        data = dashboard.get_dashboard_data()
        self.assertIsNotNone(data)

    def test_export_metrics(self):
        tracker = self.env["tracker"]
        tracker.record_metric(MetricType.CPU_USAGE, 10.0, agent_id="val")
        tmp = tempfile.NamedTemporaryFile(delete=False)
        try:
            tracker.export_metrics(tmp.name)
            with open(tmp.name, "r", encoding="utf-8") as f:
                export = json.load(f)
            self.assertIn("export_timestamp", export)
        finally:
            tmp.close()
            os.unlink(tmp.name)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
