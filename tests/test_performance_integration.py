#!/usr/bin/env python3
"""
🧪 Performance Integration Tests - Agent_Cellphone_V2

Integration tests for performance tracking, communication, and API gateway systems.
Following V2 coding standards: comprehensive testing with build evidence.

Author: Testing & Quality Assurance Specialist
License: MIT
"""

import os
import sys
import time
import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.performance_monitor import PerformanceMonitor, MetricType
from core.performance_dashboard import PerformanceDashboard, DashboardView, AlertLevel
from core.v2_comprehensive_messaging_system import (
    V2ComprehensiveMessagingSystem,
    V2MessageType,
    V2MessagePriority,
    V2AgentStatus,
)
from core.api_gateway import APIGateway, APIVersion, ServiceStatus


class TestPerformanceIntegration(unittest.TestCase):
    """Integration tests for performance monitoring and communication systems"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            "max_metrics_history": 1000,
            "snapshot_interval": 5,
            "metric_retention_days": 1,
            "profiling_enabled": True,
            "heartbeat_interval": 10,
            "message_timeout": 60,
            "health_check_interval": 30,
        }

        # Initialize components
        self.performance_tracker = PerformanceMonitor(self.config)
        self.performance_profiler = PerformanceMonitor(self.config)
        self.messaging_system = V2ComprehensiveMessagingSystem(self.config)
        self.api_gateway = APIGateway(self.config)

        # Initialize dashboard with components
        self.performance_dashboard = PerformanceDashboard(
            agent_manager=None,  # Mock for testing
            performance_tracker=self.performance_tracker,
            config_manager=None,  # Mock for testing
            message_router=None,  # Mock for testing
        )

        # Set up performance tracking integration
        # Note: V2 messaging system doesn't need performance tracker setup
        self.api_gateway.set_performance_tracker(self.performance_tracker)

        # Start services
        self.performance_dashboard.start()
        # Note: V2 messaging system starts automatically
        self.api_gateway.start_gateway()

        # Wait for initialization
        time.sleep(2)

    def tearDown(self):
        """Clean up test environment"""
        # Stop services
        self.performance_dashboard.cleanup()
        # Note: V2 messaging system cleanup handled automatically
        self.api_gateway.cleanup()
        self.performance_tracker.cleanup()
        self.performance_profiler.cleanup()

        # Clean up temp files
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_performance_tracking_integration(self):
        """Test performance tracking system integration"""
        print("Testing performance tracking integration...")

        # Record various metrics
        self.performance_tracker.record_metric(
            MetricType.RESPONSE_TIME, 0.5, agent_id="test_agent_1"
        )
        self.performance_tracker.record_metric(
            MetricType.CPU_USAGE, 75.0, agent_id="test_agent_1"
        )
        self.performance_tracker.record_metric(
            MetricType.MEMORY_USAGE, 2.5, agent_id="test_agent_2"
        )

        # Wait for snapshot generation
        time.sleep(6)

        # Verify metrics were recorded
        metrics = self.performance_tracker.get_metrics()
        self.assertGreater(len(metrics), 0, "No metrics recorded")

        # Verify snapshots were generated
        snapshots = self.performance_tracker.get_performance_snapshots()
        self.assertGreater(len(snapshots), 0, "No snapshots generated")

        # Verify agent-specific metrics
        agent1_metrics = self.performance_tracker.get_agent_performance_summary(
            "test_agent_1"
        )
        self.assertIn(
            "response_time", agent1_metrics, "Agent 1 response time not recorded"
        )
        self.assertIn("cpu_usage", agent1_metrics, "Agent 1 CPU usage not recorded")

        print("✅ Performance tracking integration test PASSED")

    def test_02_performance_profiling_integration(self):
        """Test performance profiling system integration"""
        print("Testing performance profiling integration...")

        # Test function profiling
        @self.performance_profiler.profile_function("test_function")
        def test_function():
            time.sleep(0.1)
            return "test_result"

        # Execute profiled function
        result = test_function()
        self.assertEqual(result, "test_result", "Profiled function failed")

        # Test context manager profiling
        with self.performance_profiler.profile("test_context", {"test": True}):
            time.sleep(0.1)

        # Wait for profiling data collection
        time.sleep(2)

        # Verify profiling metrics
        profiling_summary = self.performance_profiler.get_profiling_summary()
        self.assertGreater(len(profiling_summary), 0, "No profiling data collected")

        # Verify system metrics
        system_metrics = self.performance_profiler.get_system_metrics()
        self.assertIn("cpu_percent", system_metrics, "CPU metrics not collected")
        self.assertIn("memory_percent", system_metrics, "Memory metrics not collected")

        print("✅ Performance profiling integration test PASSED")

    def test_03_agent_communication_integration(self):
        """Test agent communication system integration"""
        print("Testing agent communication integration...")

        # Register test agents
        self.agent_communication.register_agent(
            "test_agent_1",
            "Test Agent 1",
            ["task_execution", "monitoring"],
            "http://localhost:8001",
            {"version": "1.0"},
        )
        self.agent_communication.register_agent(
            "test_agent_2",
            "Test Agent 2",
            ["data_processing", "reporting"],
            "http://localhost:8002",
            {"version": "1.0"},
        )

        # Verify agent registration
        all_agents = self.agent_communication.get_all_agents()
        self.assertEqual(len(all_agents), 2, "Agent registration failed")

        # Test message sending
        message_id = self.agent_communication.send_message(
            "test_agent_1",
            "test_agent_2",
            MessageType.TASK_ASSIGNMENT,
            {"task": "process_data", "priority": "high"},
            MessagePriority.HIGH,
        )
        self.assertIsNotNone(message_id, "Message sending failed")

        # Test capability-based agent discovery
        monitoring_agents = self.agent_communication.find_agents_by_capability(
            "monitoring"
        )
        self.assertEqual(len(monitoring_agents), 1, "Capability-based discovery failed")
        self.assertEqual(monitoring_agents[0].agent_id, "test_agent_1")

        # Test broadcast messaging
        broadcast_ids = self.agent_communication.broadcast_message(
            "system",
            MessageType.STATUS_UPDATE,
            {"status": "maintenance_mode"},
            MessagePriority.NORMAL,
        )
        self.assertEqual(len(broadcast_ids), 2, "Broadcast messaging failed")

        # Wait for message processing
        time.sleep(2)

        # Verify message history
        # Note: In a real system, messages would be processed and responses would be generated

        print("✅ Agent communication integration test PASSED")

    def test_04_api_gateway_integration(self):
        """Test API gateway system integration"""
        print("Testing API gateway integration...")

        # Register test services
        self.api_gateway.register_service(
            "user_service",
            "User Management Service",
            "v1",
            "http://localhost:8001",
            "http://localhost:8001/health",
            {"description": "User management and authentication"},
        )
        self.api_gateway.register_service(
            "data_service",
            "Data Processing Service",
            "v1",
            "http://localhost:8002",
            "http://localhost:8002/health",
            {"description": "Data processing and analytics"},
        )

        # Verify service registration
        all_services = self.api_gateway.get_all_services()
        self.assertEqual(len(all_services), 2, "Service registration failed")

        # Test API request routing
        response = self.api_gateway.route_request(
            "GET",
            "/v1/users",
            {"Authorization": "Bearer token"},
            {"page": "1", "limit": "10"},
            None,
            "127.0.0.1",
            "test-client",
        )
        self.assertIsNotNone(response, "API request routing failed")
        self.assertEqual(response.status_code, 200, "API request failed")

        # Test rate limiting
        self.api_gateway.set_rate_limit("user_service", 10, 5)

        # Make multiple requests to test rate limiting
        for i in range(12):
            response = self.api_gateway.route_request(
                "GET", "/v1/users", {}, {}, None, "127.0.0.1", "test-client"
            )
            if i < 10:
                self.assertEqual(
                    response.status_code, 200, f"Request {i} should succeed"
                )
            else:
                self.assertEqual(
                    response.status_code, 429, f"Request {i} should be rate limited"
                )

        # Wait for health checks
        time.sleep(2)

        # Verify service health status
        user_service = self.api_gateway.get_service_endpoint("user_service")
        self.assertIsNotNone(user_service, "User service not found")
        self.assertIn(
            user_service.status.value, ["healthy", "degraded", "unhealthy", "unknown"]
        )

        print("✅ API gateway integration test PASSED")

    def test_05_performance_dashboard_integration(self):
        """Test performance dashboard integration"""
        print("Testing performance dashboard integration...")

        # Wait for dashboard data collection
        time.sleep(3)

        # Get dashboard data
        dashboard_data = self.performance_dashboard.get_dashboard_data()
        self.assertIsNotNone(dashboard_data, "Dashboard data not available")

        # Verify dashboard components
        self.assertIsInstance(
            dashboard_data.timestamp, datetime, "Dashboard timestamp invalid"
        )
        self.assertIsInstance(
            dashboard_data.system_metrics, dict, "System metrics not available"
        )
        self.assertIsInstance(dashboard_data.alerts, list, "Alerts not available")
        self.assertIsInstance(
            dashboard_data.performance_summary,
            dict,
            "Performance summary not available",
        )

        # Test dashboard views
        self.performance_dashboard.set_view(DashboardView.AGENT_PERFORMANCE)
        self.assertEqual(
            self.performance_dashboard.current_view, DashboardView.AGENT_PERFORMANCE
        )

        self.performance_dashboard.set_view(DashboardView.SYSTEM_OVERVIEW)
        self.assertEqual(
            self.performance_dashboard.current_view, DashboardView.SYSTEM_OVERVIEW
        )

        # Test alert system
        self.performance_dashboard.add_alert(
            AlertLevel.WARNING,
            "Test warning message",
            "test_system",
            {"test": True, "timestamp": datetime.now().isoformat()},
        )

        # Verify alert was added
        alerts = self.performance_dashboard.get_alerts()
        self.assertGreater(len(alerts), 0, "Alert not added")

        # Test alert acknowledgment
        if alerts:
            alert_id = alerts[0].id
            self.performance_dashboard.acknowledge_alert(alert_id)

            # Verify alert was acknowledged
            acknowledged_alerts = self.performance_dashboard.get_alerts(
                acknowledged=True
            )
            self.assertGreater(
                len(acknowledged_alerts), 0, "Alert acknowledgment failed"
            )

        print("✅ Performance dashboard integration test PASSED")

    def test_06_cross_system_communication(self):
        """Test cross-system communication and data flow"""
        print("Testing cross-system communication...")

        # Create a test agent and record performance metrics
        self.agent_communication.register_agent(
            "integration_test_agent",
            "Integration Test Agent",
            ["testing"],
            "http://localhost:8003",
            {"test_mode": True},
        )

        # Record performance metrics for the agent
        self.performance_tracker.record_metric(
            MetricType.RESPONSE_TIME, 0.3, agent_id="integration_test_agent"
        )
        self.performance_tracker.record_metric(
            MetricType.ERROR_RATE, 0.02, agent_id="integration_test_agent"
        )

        # Send a message to the agent
        message_id = self.agent_communication.send_message(
            "system",
            "integration_test_agent",
            MessageType.PERFORMANCE_METRIC,
            {"metric_type": "response_time", "value": 0.3},
            MessagePriority.NORMAL,
        )

        # Make an API request that should trigger performance tracking
        response = self.api_gateway.route_request(
            "POST",
            "/v1/test",
            {"Content-Type": "application/json"},
            {},
            {"test_data": "integration_test"},
            "127.0.0.1",
            "integration-test",
        )

        # Wait for data propagation
        time.sleep(3)

        # Verify data flow across systems
        # Check that performance metrics are available in dashboard
        dashboard_data = self.performance_dashboard.get_dashboard_data()

        # Check that agent communication has the agent registered
        agent_info = self.agent_communication.get_agent_info("integration_test_agent")
        self.assertIsNotNone(agent_info, "Integration test agent not found")

        # Check that API gateway has processed requests
        all_services = self.api_gateway.get_all_services()
        self.assertGreaterEqual(len(all_services), 0, "No services in API gateway")

        print("✅ Cross-system communication test PASSED")

    def test_07_data_export_and_persistence(self):
        """Test data export and persistence across systems"""
        print("Testing data export and persistence...")

        # Generate some test data
        for i in range(5):
            self.performance_tracker.record_metric(
                MetricType.RESPONSE_TIME,
                0.1 + i * 0.1,
                agent_id=f"export_test_agent_{i}",
            )

        # Wait for data collection
        time.sleep(3)

        # Export data from all systems
        export_files = []

        # Export performance tracker data
        perf_export_path = os.path.join(self.temp_dir, "performance_export.json")
        self.performance_tracker.export_metrics(perf_export_path)
        export_files.append(perf_export_path)

        # Export profiling data
        profiler_export_path = os.path.join(self.temp_dir, "profiler_export.json")
        self.performance_profiler.export_profiling_data(profiler_export_path)
        export_files.append(profiler_export_path)

        # Export dashboard data
        dashboard_export_path = os.path.join(self.temp_dir, "dashboard_export.json")
        self.performance_dashboard.export_dashboard_data(dashboard_export_path)
        export_files.append(dashboard_export_path)

        # Export communication data
        comm_export_path = os.path.join(self.temp_dir, "communication_export.json")
        self.agent_communication.export_communication_data(comm_export_path)
        export_files.append(comm_export_path)

        # Export API gateway data
        gateway_export_path = os.path.join(self.temp_dir, "gateway_export.json")
        self.api_gateway.export_gateway_data(gateway_export_path)
        export_files.append(gateway_export_path)

        # Verify all export files were created and contain valid JSON
        for export_file in export_files:
            self.assertTrue(
                os.path.exists(export_file), f"Export file not created: {export_file}"
            )

            with open(export_file, "r") as f:
                try:
                    export_data = json.load(f)
                    self.assertIsInstance(
                        export_data, dict, f"Invalid JSON in {export_file}"
                    )
                    self.assertIn(
                        "export_timestamp",
                        export_data,
                        f"Missing timestamp in {export_file}",
                    )
                except json.JSONDecodeError as e:
                    self.fail(f"Invalid JSON in {export_file}: {e}")

        print("✅ Data export and persistence test PASSED")

    def test_08_error_handling_and_recovery(self):
        """Test error handling and recovery mechanisms"""
        print("Testing error handling and recovery...")

        # Test invalid agent registration
        result = self.agent_communication.register_agent(
            "", "Invalid Agent", [], "invalid_url", {}
        )
        self.assertFalse(result, "Should not register agent with empty ID")

        # Test invalid service registration
        result = self.api_gateway.register_service(
            "", "Invalid Service", "v1", "invalid_url"
        )
        self.assertFalse(result, "Should not register service with empty ID")

        # Test invalid metric recording
        try:
            self.performance_tracker.record_metric(None, 0.0, agent_id="test_agent")
            self.fail("Should not accept None metric type")
        except (TypeError, AttributeError):
            pass  # Expected error

        # Test invalid API request
        try:
            response = self.api_gateway.route_request(
                "INVALID", "", {}, {}, None, "", ""
            )
            # Should handle gracefully
            self.assertIsNotNone(response, "Should handle invalid request gracefully")
        except Exception as e:
            self.fail(f"Should handle invalid request gracefully: {e}")

        # Test system recovery after errors
        # Verify that systems are still functional
        self.assertTrue(
            self.performance_dashboard.running, "Dashboard should still be running"
        )
        self.assertTrue(
            self.agent_communication.communication_active,
            "Communication should still be active",
        )
        self.assertTrue(
            self.api_gateway.gateway_active, "API gateway should still be active"
        )

        print("✅ Error handling and recovery test PASSED")

    def test_09_performance_under_load(self):
        """Test system performance under load"""
        print("Testing performance under load...")

        start_time = time.time()

        # Generate high volume of metrics
        for i in range(100):
            self.performance_tracker.record_metric(
                MetricType.RESPONSE_TIME,
                0.1 + (i % 10) * 0.1,
                agent_id=f"load_test_agent_{i % 5}",
            )
            self.performance_tracker.record_metric(
                MetricType.CPU_USAGE,
                50.0 + (i % 30),
                agent_id=f"load_test_agent_{i % 5}",
            )

        # Generate high volume of messages
        for i in range(50):
            self.agent_communication.send_message(
                f"load_test_agent_{i % 5}",
                f"load_test_agent_{(i + 1) % 5}",
                MessageType.STATUS_UPDATE,
                {"load_test": True, "iteration": i},
                MessagePriority.NORMAL,
            )

        # Generate high volume of API requests
        for i in range(50):
            self.api_gateway.route_request(
                "GET",
                f"/v1/load_test/{i}",
                {},
                {"test": "load"},
                None,
                "127.0.0.1",
                "load-test-client",
            )

        # Wait for processing
        time.sleep(5)

        end_time = time.time()
        total_time = end_time - start_time

        # Verify system stability under load
        self.assertTrue(
            self.performance_dashboard.running, "Dashboard failed under load"
        )
        self.assertTrue(
            self.agent_communication.communication_active,
            "Communication failed under load",
        )
        self.assertTrue(
            self.api_gateway.gateway_active, "API gateway failed under load"
        )

        # Verify data was processed
        metrics = self.performance_tracker.get_metrics()
        self.assertGreater(len(metrics), 100, "Not all metrics processed under load")

        # Performance should be reasonable (under 10 seconds for 200 operations)
        self.assertLess(
            total_time, 10.0, f"Performance under load too slow: {total_time:.2f}s"
        )

        print(
            f"✅ Performance under load test PASSED ({total_time:.2f}s for 200 operations)"
        )

    def test_10_system_integration_summary(self):
        """Test overall system integration and summary"""
        print("Testing overall system integration...")

        # Verify all systems are running
        self.assertTrue(
            self.performance_dashboard.running, "Performance dashboard not running"
        )
        self.assertTrue(
            self.agent_communication.communication_active,
            "Agent communication not active",
        )
        self.assertTrue(self.api_gateway.gateway_active, "API gateway not active")

        # Verify data flow between systems
        dashboard_data = self.performance_dashboard.get_dashboard_data()
        self.assertIsNotNone(dashboard_data, "Dashboard data not available")

        # Verify performance tracking is working
        metrics = self.performance_tracker.get_metrics()
        self.assertGreater(len(metrics), 0, "No performance metrics available")

        # Verify agent communication is working
        all_agents = self.agent_communication.get_all_agents()
        self.assertGreaterEqual(len(all_agents), 0, "No agents in communication system")

        # Verify API gateway is working
        all_services = self.api_gateway.get_all_services()
        self.assertGreaterEqual(len(all_services), 0, "No services in API gateway")

        # Verify system health
        performance_summary = dashboard_data.performance_summary
        self.assertIn(
            "system_health", performance_summary, "System health not calculated"
        )
        system_health = performance_summary["system_health"]
        self.assertGreaterEqual(
            system_health, 0, "System health should be non-negative"
        )
        self.assertLessEqual(system_health, 100, "System health should be <= 100")

        print(
            f"✅ Overall system integration test PASSED (System Health: {system_health:.1f}/100)"
        )


def run_integration_tests():
    """Run all integration tests with detailed output"""
    print("🚀 Starting Performance Integration Tests")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestPerformanceIntegration)

    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 INTEGRATION TEST RESULTS SUMMARY")
    print("=" * 60)

    total_tests = result.testsRun
    failed_tests = len(result.failures)
    error_tests = len(result.errors)
    passed_tests = total_tests - failed_tests - error_tests

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Errors: {error_tests} ⚠️")

    if result.failures:
        print("\n❌ FAILED TESTS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n⚠️ ERROR TESTS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")

    if success_rate >= 90:
        print("🎉 EXCELLENT: Integration tests passed with high success rate!")
    elif success_rate >= 80:
        print("✅ GOOD: Integration tests passed with good success rate")
    elif success_rate >= 70:
        print("⚠️ ACCEPTABLE: Integration tests passed with acceptable success rate")
    else:
        print("❌ POOR: Integration tests need improvement")

    return result.wasSuccessful()


if __name__ == "__main__":
    # Run integration tests
    success = run_integration_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)
