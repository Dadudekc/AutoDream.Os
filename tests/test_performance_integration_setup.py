#!/usr/bin/env python3
"""Performance integration setup tests."""

import unittest

from core.performance_monitor import PerformanceMonitor
from core.performance_dashboard import PerformanceDashboard
from core.v2_comprehensive_messaging_system import V2ComprehensiveMessagingSystem
from core.api_gateway import APIGateway

CONFIG = {
    "max_metrics_history": 100,
    "snapshot_interval": 60,
    "profiling_enabled": True,
}


def create_env():
    """Create core components for tests."""
    tracker = PerformanceMonitor(CONFIG)
    profiler = PerformanceMonitor(CONFIG)
    messaging = V2ComprehensiveMessagingSystem(CONFIG)
    gateway = APIGateway(CONFIG)
    dashboard = PerformanceDashboard(
        agent_manager=None,
        performance_tracker=tracker,
        config_manager=None,
        message_router=None,
    )
    gateway.set_performance_tracker(tracker)
    dashboard.start()
    gateway.start_gateway()
    return {
        "tracker": tracker,
        "profiler": profiler,
        "messaging": messaging,
        "gateway": gateway,
        "dashboard": dashboard,
    }


def cleanup_env(env):
    """Shutdown components created by ``create_env``."""
    env["dashboard"].cleanup()
    env["gateway"].cleanup()
    env["tracker"].cleanup()
    env["profiler"].cleanup()


class TestPerformanceSetup(unittest.TestCase):
    """Ensure environment boots correctly."""

    def test_environment_setup(self):
        env = create_env()
        self.assertTrue(env["dashboard"].running)
        self.assertTrue(env["gateway"].gateway_active)
        cleanup_env(env)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
