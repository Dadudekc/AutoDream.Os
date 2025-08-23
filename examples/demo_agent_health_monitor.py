"""
Comprehensive Demo for Agent Health Monitoring System

This demo showcases the complete agent health monitoring system including:
- Core health monitoring functionality
- Web interface integration
- Real-time health updates
- Alert management
- Health metrics visualization

Author: Agent-1
License: MIT
"""

import asyncio
import json
import logging
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentHealthMonitorDemo:
    """
    Comprehensive demo for the agent health monitoring system

    Tests all major components and features:
    1. Core health monitoring
    2. Health metrics collection
    3. Alert generation and management
    4. Web interface functionality
    5. Real-time updates
    6. Health scoring and recommendations
    7. Integration with core systems
    """

    def __init__(self):
        """Initialize the demo system"""
        self.demo_active = False
        self.health_monitor = None
        self.web_interface = None
        self.demo_thread = None

        # Demo configuration
        self.demo_agents = [
            "agent_001",
            "agent_002",
            "agent_003",
            "agent_004",
            "agent_005",
        ]

        # Demo metrics patterns
        self.metric_patterns = {
            "agent_001": {
                "response_time": 500,
                "memory_usage": 75,
                "cpu_usage": 60,
                "error_rate": 2,
            },
            "agent_002": {
                "response_time": 1200,
                "memory_usage": 85,
                "cpu_usage": 90,
                "error_rate": 8,
            },
            "agent_003": {
                "response_time": 300,
                "memory_usage": 45,
                "cpu_usage": 30,
                "error_rate": 1,
            },
            "agent_004": {
                "response_time": 8000,
                "memory_usage": 95,
                "cpu_usage": 98,
                "error_rate": 25,
            },
            "agent_005": {
                "response_time": 200,
                "memory_usage": 25,
                "cpu_usage": 20,
                "error_rate": 0,
            },
        }

        logger.info("AgentHealthMonitorDemo initialized")

    def run_comprehensive_demo(self):
        """Run the complete health monitoring demo"""
        logger.info("🚀 Starting Comprehensive Agent Health Monitor Demo...")

        try:
            # Test 1: Core health monitoring functionality
            self._test_core_health_monitoring()

            # Test 2: Health metrics collection and analysis
            self._test_health_metrics_collection()

            # Test 3: Alert generation and management
            self._test_alert_management()

            # Test 4: Health scoring and recommendations
            self._test_health_scoring()

            # Test 5: Real-time monitoring and updates
            self._test_real_time_monitoring()

            # Test 6: Web interface integration
            self._test_web_interface()

            # Test 7: Performance under load
            self._test_performance_under_load()

            # Test 8: Integration with core systems
            self._test_core_system_integration()

            logger.info("✅ All demo tests completed successfully!")

        except Exception as e:
            logger.error(f"❌ Demo test failed: {e}")
            raise

    def _test_core_health_monitoring(self):
        """Test core health monitoring functionality"""
        logger.info("🧪 Testing core health monitoring functionality...")

        try:
            # Import and initialize health monitor
            from src.core.agent_health_monitor import AgentHealthMonitor

            self.health_monitor = AgentHealthMonitor()

            # Test basic initialization
            assert self.health_monitor is not None
            assert hasattr(self.health_monitor, "start")
            assert hasattr(self.health_monitor, "stop")
            assert hasattr(self.health_monitor, "record_health_metric")

            # Test smoke test
            success = self.health_monitor.run_smoke_test()
            assert success, "Health monitor smoke test failed"

            logger.info("✅ Core health monitoring functionality test PASSED")

        except Exception as e:
            logger.error(f"❌ Core health monitoring test failed: {e}")
            raise

    def _test_health_metrics_collection(self):
        """Test health metrics collection and storage"""
        logger.info("📊 Testing health metrics collection...")

        try:
            # Record various health metrics
            for agent_id in self.demo_agents:
                patterns = self.metric_patterns[agent_id]

                # Record response time
                self.health_monitor.record_health_metric(
                    agent_id, "response_time", patterns["response_time"], "ms"
                )

                # Record memory usage
                self.health_monitor.record_health_metric(
                    agent_id, "memory_usage", patterns["memory_usage"], "%"
                )

                # Record CPU usage
                self.health_monitor.record_health_metric(
                    agent_id, "cpu_usage", patterns["cpu_usage"], "%"
                )

                # Record error rate
                self.health_monitor.record_health_metric(
                    agent_id, "error_rate", patterns["error_rate"], "%"
                )

            # Verify metrics were recorded
            all_health = self.health_monitor.get_all_agent_health()
            assert len(all_health) == len(
                self.demo_agents
            ), "Not all agents have health data"

            for agent_id in self.demo_agents:
                health = self.health_monitor.get_agent_health(agent_id)
                assert health is not None, f"Health data missing for {agent_id}"
                assert len(health.metrics) >= 4, f"Insufficient metrics for {agent_id}"

            logger.info("✅ Health metrics collection test PASSED")

        except Exception as e:
            logger.error(f"❌ Health metrics collection test failed: {e}")
            raise

    def _test_alert_management(self):
        """Test alert generation and management"""
        logger.info("🚨 Testing alert management...")

        try:
            # Start monitoring to generate alerts
            self.health_monitor.start()
            time.sleep(2)  # Allow monitoring to process metrics

            # Check for generated alerts
            alerts = self.health_monitor.get_health_alerts()
            assert len(alerts) > 0, "No alerts were generated from critical metrics"

            # Test alert filtering
            critical_alerts = self.health_monitor.get_health_alerts(severity="critical")
            warning_alerts = self.health_monitor.get_health_alerts(severity="warning")

            # Test alert acknowledgment
            if alerts:
                first_alert = alerts[0]
                self.health_monitor.acknowledge_alert(first_alert.alert_id)

                # Verify acknowledgment
                updated_alerts = self.health_monitor.get_health_alerts()
                acknowledged_alert = next(
                    (a for a in updated_alerts if a.alert_id == first_alert.alert_id),
                    None,
                )
                assert (
                    acknowledged_alert is not None
                ), "Alert not found after acknowledgment"
                assert (
                    acknowledged_alert.acknowledged
                ), "Alert not marked as acknowledged"

            # Test alert resolution
            if alerts:
                first_alert = alerts[0]
                self.health_monitor.resolve_alert(first_alert.alert_id)

                # Verify resolution
                updated_alerts = self.health_monitor.get_health_alerts()
                resolved_alert = next(
                    (a for a in updated_alerts if a.alert_id == first_alert.alert_id),
                    None,
                )
                assert resolved_alert is not None, "Alert not found after resolution"
                assert resolved_alert.resolved, "Alert not marked as resolved"

            logger.info("✅ Alert management test PASSED")

        except Exception as e:
            logger.error(f"❌ Alert management test failed: {e}")
            raise

    def _test_health_scoring(self):
        """Test health scoring and recommendation generation"""
        logger.info("📈 Testing health scoring and recommendations...")

        try:
            # Get health summary
            summary = self.health_monitor.get_health_summary()
            assert "total_agents" in summary, "Health summary missing total_agents"
            assert (
                "average_health_score" in summary
            ), "Health summary missing average_health_score"
            assert (
                "status_distribution" in summary
            ), "Health summary missing status_distribution"

            # Verify health scores are calculated
            for agent_id in self.demo_agents:
                health = self.health_monitor.get_agent_health(agent_id)
                assert health.health_score >= 0, f"Invalid health score for {agent_id}"
                assert (
                    health.health_score <= 100
                ), f"Invalid health score for {agent_id}"

                # Check for recommendations
                assert hasattr(
                    health, "recommendations"
                ), f"Health snapshot missing recommendations for {agent_id}"
                assert isinstance(
                    health.recommendations, list
                ), f"Recommendations not a list for {agent_id}"

            # Verify status distribution
            status_dist = summary["status_distribution"]
            assert isinstance(status_dist, dict), "Status distribution not a dictionary"

            logger.info("✅ Health scoring test PASSED")

        except Exception as e:
            logger.error(f"❌ Health scoring test failed: {e}")
            raise

    def _test_real_time_monitoring(self):
        """Test real-time monitoring capabilities"""
        logger.info("⏱️ Testing real-time monitoring...")

        try:
            # Test health update callbacks
            callback_called = False
            callback_data = None

            def health_callback(health_data, alerts):
                nonlocal callback_called, callback_data
                callback_called = True
                callback_data = {"health_data": health_data, "alerts": alerts}

            # Subscribe to health updates
            self.health_monitor.subscribe_to_health_updates(health_callback)

            # Record a new metric to trigger callback
            self.health_monitor.record_health_metric(
                "test_agent", "response_time", 1500.0, "ms"
            )

            # Wait for callback
            time.sleep(3)

            # Verify callback was called
            assert callback_called, "Health update callback was not called"
            assert callback_data is not None, "Callback data is None"

            # Unsubscribe
            self.health_monitor.unsubscribe_from_health_updates(health_callback)

            logger.info("✅ Real-time monitoring test PASSED")

        except Exception as e:
            logger.error(f"❌ Real-time monitoring test failed: {e}")
            raise

    def _test_web_interface(self):
        """Test web interface functionality"""
        logger.info("🌐 Testing web interface...")

        try:
            # Import web interface
            from src.web.health_monitor_web import HealthMonitorWebInterface

            # Initialize web interface
            self.web_interface = HealthMonitorWebInterface(
                health_monitor=self.health_monitor, config={"debug": False}
            )

            # Test basic initialization
            assert self.web_interface is not None
            assert hasattr(self.web_interface, "app")
            assert hasattr(self.web_interface, "socketio")

            # Test smoke test
            success = self.web_interface.run_smoke_test()
            assert success, "Web interface smoke test failed"

            # Test route setup
            routes = [rule.rule for rule in self.web_interface.app.url_map.iter_rules()]
            expected_routes = [
                "/",
                "/api/health/summary",
                "/api/health/agents",
                "/api/health/alerts",
            ]

            for route in expected_routes:
                assert route in routes, f"Route {route} not found"

            logger.info("✅ Web interface test PASSED")

        except Exception as e:
            logger.error(f"❌ Web interface test failed: {e}")
            raise

    def _test_performance_under_load(self):
        """Test performance under load"""
        logger.info("⚡ Testing performance under load...")

        try:
            # Record many metrics rapidly
            start_time = time.time()

            for i in range(100):
                agent_id = f"load_test_agent_{i % 10}"
                metric_type = "response_time"
                value = 100 + (i % 1000)

                self.health_monitor.record_health_metric(
                    agent_id, metric_type, value, "ms"
                )

            end_time = time.time()
            duration = end_time - start_time

            # Verify performance (should complete in reasonable time)
            assert duration < 5.0, f"Performance test took too long: {duration:.2f}s"

            # Verify all metrics were recorded
            all_health = self.health_monitor.get_all_agent_health()
            load_test_agents = [f"load_test_agent_{i}" for i in range(10)]

            for agent_id in load_test_agents:
                health = self.health_monitor.get_agent_health(agent_id)
                assert (
                    health is not None
                ), f"Load test agent {agent_id} missing health data"

            logger.info(f"✅ Performance test PASSED (100 metrics in {duration:.2f}s)")

        except Exception as e:
            logger.error(f"❌ Performance test failed: {e}")
            raise

    def _test_core_system_integration(self):
        """Test integration with core agent management systems"""
        logger.info("🔗 Testing core system integration...")

        try:
            # Test threshold management
            from src.core.agent_health_monitor import HealthMetricType

            # Set custom threshold
            self.health_monitor.set_health_threshold(
                HealthMetricType.RESPONSE_TIME,
                warning_threshold=800.0,
                critical_threshold=3000.0,
                unit="ms",
                description="Custom response time threshold",
            )

            # Verify threshold was set
            thresholds = self.health_monitor.thresholds
            assert (
                HealthMetricType.RESPONSE_TIME in thresholds
            ), "Custom threshold not set"

            custom_threshold = thresholds[HealthMetricType.RESPONSE_TIME]
            assert (
                custom_threshold.warning_threshold == 800.0
            ), "Warning threshold not set correctly"
            assert (
                custom_threshold.critical_threshold == 3000.0
            ), "Critical threshold not set correctly"

            # Test health summary integration
            summary = self.health_monitor.get_health_summary()
            assert "monitoring_active" in summary, "Summary missing monitoring status"
            assert "last_update" in summary, "Summary missing last update timestamp"

            logger.info("✅ Core system integration test PASSED")

        except Exception as e:
            logger.error(f"❌ Core system integration test failed: {e}")
            raise

    def run_demo_scenario(self):
        """Run a realistic demo scenario"""
        logger.info("🎭 Running realistic demo scenario...")

        try:
            # Start monitoring
            self.health_monitor.start()

            # Simulate agent health degradation
            logger.info("📉 Simulating agent health degradation...")

            # Agent 002 gets worse
            for i in range(5):
                self.health_monitor.record_health_metric(
                    "agent_002",
                    "response_time",
                    2000 + (i * 500),  # Increasing response time
                    "ms",
                )
                self.health_monitor.record_health_metric(
                    "agent_002",
                    "memory_usage",
                    90 + (i * 2),  # Increasing memory usage
                    "%",
                )
                time.sleep(1)

            # Agent 004 recovers
            logger.info("📈 Simulating agent recovery...")
            for i in range(5):
                self.health_monitor.record_health_metric(
                    "agent_004",
                    "response_time",
                    8000 - (i * 1500),  # Decreasing response time
                    "ms",
                )
                self.health_monitor.record_health_metric(
                    "agent_004",
                    "memory_usage",
                    95 - (i * 10),  # Decreasing memory usage
                    "%",
                )
                time.sleep(1)

            # Show final status
            logger.info("📊 Final health status:")
            summary = self.health_monitor.get_health_summary()
            for key, value in summary.items():
                logger.info(f"  {key}: {value}")

            # Show active alerts
            alerts = self.health_monitor.get_health_alerts()
            logger.info(f"🚨 Active alerts: {len(alerts)}")
            for alert in alerts[:3]:  # Show first 3 alerts
                logger.info(f"  {alert.severity.value.upper()}: {alert.message}")

            logger.info("✅ Demo scenario completed successfully!")

        except Exception as e:
            logger.error(f"❌ Demo scenario failed: {e}")
            raise

    def cleanup(self):
        """Cleanup demo resources"""
        try:
            if self.health_monitor:
                self.health_monitor.stop()
                self.health_monitor.shutdown()

            if self.web_interface:
                self.web_interface.shutdown()

            logger.info("🧹 Demo cleanup completed")

        except Exception as e:
            logger.error(f"❌ Demo cleanup failed: {e}")


def main():
    """Main demo function"""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Health Monitor Demo")
    parser.add_argument(
        "--scenario", action="store_true", help="Run realistic demo scenario"
    )
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")

    args = parser.parse_args()

    demo = AgentHealthMonitorDemo()

    try:
        if args.scenario:
            # Run realistic scenario
            demo.run_demo_scenario()
        elif args.quick:
            # Run quick tests
            demo._test_core_health_monitoring()
            demo._test_health_metrics_collection()
            demo._test_alert_management()
        else:
            # Run comprehensive demo
            demo.run_comprehensive_demo()

        print("\n🎉 Demo completed successfully!")

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        exit(1)

    finally:
        demo.cleanup()


if __name__ == "__main__":
    main()
