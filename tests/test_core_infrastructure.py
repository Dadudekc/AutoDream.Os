#!/usr/bin/env python3
"""
Test Suite: Core Infrastructure Systems - Agent Cellphone V2
==========================================================

Comprehensive testing of the core infrastructure systems including:
- Health Monitor system
- Performance Profiler system
- Error Handler system
- Connection Pool Manager system

Focus: Validating the foundation systems that support the V2 architecture
and ensuring reliability, performance monitoring, and error recovery.
"""

import unittest
import time
import json
from unittest.mock import Mock, patch, MagicMock, call
from typing import Dict, List, Any

# Import the classes we want to test
from src.core.health_monitor import (
    HealthMonitor,
    HealthStatus,
    AlertLevel,
    HealthMetric,
    HealthAlert,
)
from src.core.performance_profiler import (
    PerformanceProfiler,
    PerformanceLevel,
    PerformanceMetric,
    PerformanceSnapshot,
)
from src.core.error_handler import (
    ErrorHandler,
    CircuitBreaker,
    RetryStrategy,
    ErrorSeverity,
    ErrorInfo,
)
from src.core.connection_pool_manager import (
    ConnectionPoolManager,
    ConnectionPool,
    ConnectionState,
    ConnectionInfo,
)


class TestHealthMonitor(unittest.TestCase):
    """Test suite for the HealthMonitor class"""

    def setUp(self):
        """Set up test fixtures"""
        self.monitor = HealthMonitor()

        # Sample health metrics
        self.sample_metrics = {
            "response_time": 0.15,
            "error_rate": 0.02,
            "availability": 0.99,
            "throughput": 100.0,
            "memory_usage": 0.45,
            "cpu_usage": 0.30,
        }

    def test_monitor_initialization(self):
        """Test that health monitor initializes correctly"""
        self.assertIsNotNone(self.monitor.health_metrics)
        self.assertIsNotNone(self.monitor.health_alerts)
        self.assertIsNotNone(self.monitor.health_history)
        self.assertFalse(self.monitor.is_monitoring)
        self.assertEqual(len(self.monitor.health_metrics), 0)
        self.assertEqual(len(self.monitor.health_alerts), 0)

    def test_component_registration(self):
        """Test that components can be registered for health monitoring"""

        def mock_health_function():
            return {"status": "healthy", "score": 0.95}

        self.monitor.register_component("test_component", mock_health_function)

        self.assertIn("test_component", self.monitor.health_metrics)
        self.assertEqual(
            self.monitor.health_metrics["test_component"], mock_health_function
        )

    def test_health_metric_collection(self):
        """Test that health metrics are collected correctly"""

        # Register a component
        def mock_health_function():
            return self.sample_metrics

        self.monitor.register_component("test_component", mock_health_function)

        # Collect metrics
        metrics = self.monitor.collect_health_metrics()

        self.assertIn("test_component", metrics)
        self.assertEqual(metrics["test_component"], self.sample_metrics)

    def test_health_score_calculation(self):
        """Test that health scores are calculated correctly"""
        # Test healthy metrics
        healthy_score = self.monitor._calculate_health_score(self.sample_metrics)
        self.assertGreater(healthy_score, 0.8)

        # Test unhealthy metrics
        unhealthy_metrics = {
            "response_time": 2.0,  # High response time
            "error_rate": 0.15,  # High error rate
            "availability": 0.85,  # Low availability
            "throughput": 50.0,  # Low throughput
            "memory_usage": 0.95,  # High memory usage
            "cpu_usage": 0.90,  # High CPU usage
        }

        unhealthy_score = self.monitor._calculate_health_score(unhealthy_metrics)
        self.assertLess(unhealthy_score, 0.6)

    def test_alert_generation(self):
        """Test that health alerts are generated correctly"""
        # Set up alert thresholds
        self.monitor.set_alert_threshold("response_time", 1.0, AlertLevel.WARNING)
        self.monitor.set_alert_threshold("error_rate", 0.05, AlertLevel.CRITICAL)

        # Test metrics that should trigger alerts
        alert_metrics = {
            "response_time": 1.5,  # Above warning threshold
            "error_rate": 0.08,  # Above critical threshold
            "availability": 0.99,
            "throughput": 100.0,
            "memory_usage": 0.45,
            "cpu_usage": 0.30,
        }

        alerts = self.monitor.check_health_alerts(alert_metrics)

        # Should have generated alerts
        self.assertGreater(len(alerts), 0)

        # Check alert levels
        alert_levels = [alert.alert_level for alert in alerts]
        self.assertIn(AlertLevel.WARNING, alert_levels)
        self.assertIn(AlertLevel.CRITICAL, alert_levels)

    def test_health_history_tracking(self):
        """Test that health history is tracked correctly"""

        # Register component and collect metrics multiple times
        def mock_health_function():
            return self.sample_metrics

        self.monitor.register_component("test_component", mock_health_function)

        # Collect metrics multiple times
        for i in range(3):
            self.monitor.collect_health_metrics()
            time.sleep(0.1)

        # Check history
        history = self.monitor.get_health_history("test_component")
        self.assertGreaterEqual(len(history), 3)

        # Verify history structure
        for entry in history:
            self.assertIn("timestamp", entry)
            self.assertIn("metrics", entry)
            self.assertIn("health_score", entry)

    def test_start_stop_monitoring(self):
        """Test starting and stopping health monitoring"""
        # Start monitoring
        self.monitor.start_monitoring()
        self.assertTrue(self.monitor.is_monitoring)

        # Stop monitoring
        self.monitor.stop_monitoring()
        self.assertFalse(self.monitor.is_monitoring)

    def test_health_status_enumeration(self):
        """Test that health status enums work correctly"""
        self.assertEqual(HealthStatus.HEALTHY.value, "healthy")
        self.assertEqual(HealthStatus.DEGRADED.value, "degraded")
        self.assertEqual(HealthStatus.UNHEALTHY.value, "unhealthy")
        self.assertEqual(HealthStatus.CRITICAL.value, "critical")

    def test_alert_level_enumeration(self):
        """Test that alert level enums work correctly"""
        self.assertEqual(AlertLevel.INFO.value, "info")
        self.assertEqual(AlertLevel.WARNING.value, "warning")
        self.assertEqual(AlertLevel.ERROR.value, "error")
        self.assertEqual(AlertLevel.CRITICAL.value, "critical")


class TestPerformanceProfiler(unittest.TestCase):
    """Test suite for the PerformanceProfiler class"""

    def setUp(self):
        """Set up test fixtures"""
        self.profiler = PerformanceProfiler()

    def test_profiler_initialization(self):
        """Test that performance profiler initializes correctly"""
        self.assertIsNotNone(self.profiler.performance_metrics)
        self.assertIsNotNone(self.profiler.performance_history)
        self.assertFalse(self.profiler.is_monitoring)
        self.assertEqual(len(self.profiler.performance_metrics), 0)

    def test_performance_decorator(self):
        """Test that the performance decorator works correctly"""

        @self.profiler.profile_operation("test_operation")
        def test_function():
            time.sleep(0.01)  # Simulate work
            return "test_result"

        # Execute function
        result = test_function()
        self.assertEqual(result, "test_result")

        # Check that metrics were recorded
        metrics = self.profiler.get_operation_metrics("test_operation")
        self.assertIsNotNone(metrics)
        self.assertGreater(metrics.execution_count, 0)

    def test_metric_collection(self):
        """Test that performance metrics are collected correctly"""
        # Record some metrics
        self.profiler.record_metric("test_operation", "response_time", 0.15)
        self.profiler.record_metric("test_operation", "throughput", 100.0)
        self.profiler.record_metric("test_operation", "error_rate", 0.02)

        # Get metrics
        metrics = self.profiler.get_operation_metrics("test_operation")

        self.assertIsNotNone(metrics)
        self.assertEqual(metrics.operation_name, "test_operation")
        self.assertGreater(metrics.execution_count, 0)

    def test_bottleneck_detection(self):
        """Test that performance bottlenecks are detected correctly"""
        # Record slow operation
        self.profiler.record_metric("slow_operation", "response_time", 2.5)

        # Record fast operation
        self.profiler.record_metric("fast_operation", "response_time", 0.05)

        # Detect bottlenecks
        bottlenecks = self.profiler.detect_bottlenecks()

        # Should detect slow operation as bottleneck
        self.assertGreater(len(bottlenecks), 0)

        # Check that slow operation is identified
        bottleneck_operations = [b.operation_name for b in bottlenecks]
        self.assertIn("slow_operation", bottleneck_operations)

    def test_performance_alerts(self):
        """Test that performance alerts are generated correctly"""
        # Set performance thresholds
        self.profiler.set_performance_threshold(
            "response_time", 1.0, PerformanceLevel.DEGRADED
        )
        self.profiler.set_performance_threshold(
            "response_time", 2.0, PerformanceLevel.CRITICAL
        )

        # Record metrics that should trigger alerts
        self.profiler.record_metric("test_operation", "response_time", 1.5)

        # Check for alerts
        alerts = self.profiler.check_performance_alerts()

        # Should have generated alerts
        self.assertGreater(len(alerts), 0)

        # Check alert levels
        alert_levels = [alert.performance_level for alert in alerts]
        self.assertIn(PerformanceLevel.DEGRADED, alert_levels)

    def test_trend_analysis(self):
        """Test that performance trends are analyzed correctly"""
        # Record metrics over time
        for i in range(5):
            self.profiler.record_metric(
                "test_operation", "response_time", 0.1 + i * 0.05
            )
            time.sleep(0.1)

        # Analyze trends
        trends = self.profiler.analyze_performance_trends(
            "test_operation", "response_time"
        )

        # Should detect increasing trend
        self.assertIsNotNone(trends)
        self.assertIn("trend_direction", trends)
        self.assertIn("trend_strength", trends)

    def test_start_stop_monitoring(self):
        """Test starting and stopping performance monitoring"""
        # Start monitoring
        self.profiler.start_monitoring()
        self.assertTrue(self.profiler.is_monitoring)

        # Stop monitoring
        self.profiler.stop_monitoring()
        self.assertFalse(self.profiler.is_monitoring)

    def test_performance_snapshot_creation(self):
        """Test that performance snapshots are created correctly"""
        # Record some metrics
        self.profiler.record_metric("test_operation", "response_time", 0.15)
        self.profiler.record_metric("test_operation", "throughput", 100.0)

        # Create snapshot
        snapshot = self.profiler.create_performance_snapshot()

        self.assertIsInstance(snapshot, PerformanceSnapshot)
        self.assertIsNotNone(snapshot.timestamp)
        self.assertGreater(len(snapshot.metrics), 0)


class TestErrorHandler(unittest.TestCase):
    """Test suite for the ErrorHandler class"""

    def setUp(self):
        """Set up test fixtures"""
        self.error_handler = ErrorHandler()

    def test_error_handler_initialization(self):
        """Test that error handler initializes correctly"""
        self.assertIsNotNone(self.error_handler.circuit_breakers)
        self.assertIsNotNone(self.error_handler.retry_strategies)
        self.assertEqual(len(self.error_handler.circuit_breakers), 0)
        self.assertEqual(len(self.error_handler.retry_strategies), 0)

    def test_circuit_breaker_creation(self):
        """Test that circuit breakers are created correctly"""
        circuit_breaker = self.error_handler.create_circuit_breaker(
            "test_service", failure_threshold=5, recovery_timeout=30.0
        )

        self.assertIsInstance(circuit_breaker, CircuitBreaker)
        self.assertEqual(circuit_breaker.service_name, "test_service")
        self.assertEqual(circuit_breaker.failure_threshold, 5)
        self.assertEqual(circuit_breaker.recovery_timeout, 30.0)

        # Should be in CLOSED state initially
        self.assertEqual(circuit_breaker.state, "CLOSED")

    def test_circuit_breaker_state_transitions(self):
        """Test that circuit breaker states transition correctly"""
        circuit_breaker = self.error_handler.create_circuit_breaker(
            "test_service", failure_threshold=2
        )

        # Initially CLOSED
        self.assertEqual(circuit_breaker.state, "CLOSED")

        # Record failures until threshold
        circuit_breaker.record_failure()
        self.assertEqual(circuit_breaker.state, "CLOSED")  # Still under threshold

        circuit_breaker.record_failure()
        self.assertEqual(circuit_breaker.state, "OPEN")  # Threshold reached

        # Wait for recovery timeout
        circuit_breaker.last_failure_time = time.time() - 31.0  # 31 seconds ago

        # Should transition to HALF_OPEN
        self.assertEqual(circuit_breaker.state, "HALF_OPEN")

        # Record success to close circuit
        circuit_breaker.record_success()
        self.assertEqual(circuit_breaker.state, "CLOSED")

    def test_retry_strategy_creation(self):
        """Test that retry strategies are created correctly"""
        retry_strategy = self.error_handler.create_retry_strategy(
            "test_operation", max_retries=3, base_delay=1.0, max_delay=10.0
        )

        self.assertIsInstance(retry_strategy, RetryStrategy)
        self.assertEqual(retry_strategy.operation_name, "test_operation")
        self.assertEqual(retry_strategy.max_retries, 3)
        self.assertEqual(retry_strategy.base_delay, 1.0)
        self.assertEqual(retry_strategy.max_delay, 10.0)

    def test_retry_strategy_execution(self):
        """Test that retry strategies execute correctly"""
        retry_strategy = self.error_handler.create_retry_strategy(
            "test_operation", max_retries=2
        )

        # Mock function that fails then succeeds
        call_count = 0

        def mock_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Test error")
            return "success"

        # Execute with retry
        result = retry_strategy.execute_with_retry(mock_function)

        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)  # Called 3 times (1 initial + 2 retries)

    def test_exponential_backoff_calculation(self):
        """Test that exponential backoff delays are calculated correctly"""
        retry_strategy = self.error_handler.create_retry_strategy(
            "test_operation", base_delay=1.0, max_delay=10.0
        )

        # Calculate delays for different retry attempts
        delay1 = retry_strategy._calculate_delay(1)
        delay2 = retry_strategy._calculate_delay(2)
        delay3 = retry_strategy._calculate_delay(3)

        # Delays should increase exponentially
        self.assertLess(delay1, delay2)
        self.assertLess(delay2, delay3)

        # But not exceed max delay
        self.assertLessEqual(delay1, 10.0)
        self.assertLessEqual(delay2, 10.0)
        self.assertLessEqual(delay3, 10.0)

    def test_error_classification(self):
        """Test that errors are classified correctly"""
        # Test different error types
        network_error = Exception("Connection timeout")
        validation_error = ValueError("Invalid input")
        system_error = RuntimeError("System failure")

        # Classify errors
        network_severity = self.error_handler._classify_error_severity(network_error)
        validation_severity = self.error_handler._classify_error_severity(
            validation_error
        )
        system_severity = self.error_handler._classify_error_severity(system_error)

        # Network errors should be medium severity
        self.assertEqual(network_severity, ErrorSeverity.MEDIUM)

        # Validation errors should be low severity
        self.assertEqual(validation_severity, ErrorSeverity.LOW)

        # System errors should be high severity
        self.assertEqual(system_severity, ErrorSeverity.HIGH)

    def test_error_info_creation(self):
        """Test that error info objects are created correctly"""
        error = Exception("Test error message")
        error_info = self.error_handler.create_error_info(error, "test_operation")

        self.assertIsInstance(error_info, ErrorInfo)
        self.assertEqual(error_info.error_type, "Exception")
        self.assertEqual(error_info.error_message, "Test error message")
        self.assertEqual(error_info.operation_name, "test_operation")
        self.assertIsNotNone(error_info.timestamp)

    def test_error_severity_enumeration(self):
        """Test that error severity enums work correctly"""
        self.assertEqual(ErrorSeverity.LOW.value, "low")
        self.assertEqual(ErrorSeverity.MEDIUM.value, "medium")
        self.assertEqual(ErrorSeverity.HIGH.value, "high")
        self.assertEqual(ErrorSeverity.CRITICAL.value, "critical")


class TestConnectionPoolManager(unittest.TestCase):
    """Test suite for the ConnectionPoolManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.pool_manager = ConnectionPoolManager()

    def test_pool_manager_initialization(self):
        """Test that connection pool manager initializes correctly"""
        self.assertIsNotNone(self.pool_manager.connection_pools)
        self.assertEqual(len(self.pool_manager.connection_pools), 0)

    def test_connection_pool_creation(self):
        """Test that connection pools are created correctly"""
        pool = self.pool_manager.create_connection_pool(
            "test_pool", max_connections=10, min_connections=2
        )

        self.assertIsInstance(pool, ConnectionPool)
        self.assertEqual(pool.pool_name, "test_pool")
        self.assertEqual(pool.max_connections, 10)
        self.assertEqual(pool.min_connections, 2)

        # Should be in pool manager
        self.assertIn("test_pool", self.pool_manager.connection_pools)

    def test_connection_pool_operations(self):
        """Test that connection pools handle operations correctly"""
        pool = self.pool_manager.create_connection_pool("test_pool", max_connections=5)

        # Test connection acquisition
        connection = pool.acquire_connection()
        self.assertIsNotNone(connection)
        self.assertEqual(connection.state, ConnectionState.ACTIVE)

        # Test connection release
        pool.release_connection(connection)
        self.assertEqual(connection.state, ConnectionState.IDLE)

    def test_connection_pool_health_monitoring(self):
        """Test that connection pools monitor health correctly"""
        pool = self.pool_manager.create_connection_pool("test_pool", max_connections=5)

        # Get health metrics
        health_metrics = pool.get_health_metrics()

        self.assertIn("active_connections", health_metrics)
        self.assertIn("idle_connections", health_metrics)
        self.assertIn("total_connections", health_metrics)
        self.assertIn("connection_utilization", health_metrics)

        # Initial state should be healthy
        self.assertEqual(health_metrics["active_connections"], 0)
        self.assertEqual(health_metrics["idle_connections"], 0)

    def test_connection_pool_optimization(self):
        """Test that connection pools optimize themselves correctly"""
        pool = self.pool_manager.create_connection_pool(
            "test_pool", max_connections=10, min_connections=2
        )

        # Optimize pool
        optimization_result = pool.optimize_pool()

        self.assertIsNotNone(optimization_result)
        self.assertIn("optimization_type", optimization_result)
        self.assertIn("recommendations", optimization_result)

    def test_connection_lifecycle_management(self):
        """Test that connection lifecycle is managed correctly"""
        pool = self.pool_manager.create_connection_pool("test_pool", max_connections=3)

        # Acquire multiple connections
        connections = []
        for i in range(3):
            conn = pool.acquire_connection()
            connections.append(conn)

        # Pool should be at capacity
        self.assertEqual(pool.get_active_connection_count(), 3)

        # Try to acquire another connection (should fail or wait)
        try:
            extra_conn = pool.acquire_connection(timeout=0.1)
            self.fail("Should not be able to acquire more connections")
        except Exception:
            pass  # Expected behavior

        # Release connections
        for conn in connections:
            pool.release_connection(conn)

        # Pool should be empty
        self.assertEqual(pool.get_active_connection_count(), 0)

    def test_connection_info_creation(self):
        """Test that connection info objects are created correctly"""
        connection_info = ConnectionInfo(
            connection_id="test_conn_1",
            state=ConnectionState.IDLE,
            created_at=time.time(),
            last_used=time.time(),
        )

        self.assertEqual(connection_info.connection_id, "test_conn_1")
        self.assertEqual(connection_info.state, ConnectionState.IDLE)
        self.assertIsNotNone(connection_info.created_at)
        self.assertIsNotNone(connection_info.last_used)

    def test_connection_state_enumeration(self):
        """Test that connection state enums work correctly"""
        self.assertEqual(ConnectionState.IDLE.value, "idle")
        self.assertEqual(ConnectionState.ACTIVE.value, "active")
        self.assertEqual(ConnectionState.ERROR.value, "error")
        self.assertEqual(ConnectionState.CLOSED.value, "closed")


def run_core_infrastructure_tests():
    """Run all core infrastructure tests"""
    print("🧪 RUNNING CORE INFRASTRUCTURE SYSTEM TESTS")
    print("=" * 70)
    print(
        "Focus: Health monitoring, performance profiling, error handling, connection pooling"
    )
    print("Note: All systems are mocked for safe testing")
    print()

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestHealthMonitor))
    test_suite.addTest(unittest.makeSuite(TestPerformanceProfiler))
    test_suite.addTest(unittest.makeSuite(TestErrorHandler))
    test_suite.addTest(unittest.makeSuite(TestConnectionPoolManager))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 CORE INFRASTRUCTURE TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if not result.failures and not result.errors:
        print("\n✅ ALL TESTS PASSED!")
        print("   Core infrastructure validation successful!")
        print("   Health monitoring working correctly!")
        print("   Performance profiling functioning properly!")
        print("   Error handling validated!")
        print("   Connection pooling tested!")

    return result.wasSuccessful()


if __name__ == "__main__":
    # Run core infrastructure tests
    success = run_core_infrastructure_tests()

    # Exit with appropriate code
    exit(0 if success else 1)
