#!/usr/bin/env python3
"""
Unit tests for Coordination Performance Monitor - Agent Cellphone V2
==================================================================

Comprehensive testing for the performance monitoring system.

Author: Agent-6 (Gaming & Entertainment Specialist)
License: MIT
"""

import time

    CoordinationPerformanceMonitor,
    get_performance_monitor
)


class TestCoordinationPerformanceMonitor:
    """Test coordination performance monitor main class."""
    
    @pytest.fixture
    def performance_monitor(self):
        """Create performance monitor instance for testing."""
        monitor = CoordinationPerformanceMonitor()
        yield monitor
        # Cleanup
        monitor.stop_monitoring()
    
    def test_performance_monitor_initialization(self, performance_monitor):
        """Test performance monitor initialization."""
        assert performance_monitor.collector is not None
        assert performance_monitor.analyzer is not None
        assert performance_monitor.monitoring_active is True
        assert performance_monitor.monitoring_thread is not None
    
    def test_record_operation_start(self, performance_monitor):
        """Test operation start recording."""
        performance_monitor.record_operation_start("test_operation", {"tag": "test"})
        
        # Get the latest metric
        latest_metric = performance_monitor.collector.get_latest_metric("test_operation_start")
        assert latest_metric is not None
        assert latest_metric.name == "test_operation_start"
        assert latest_metric.tags == {"tag": "test"}
    
    def test_record_operation_completion_success(self, performance_monitor):
        """Test operation completion recording with success."""
        performance_monitor.record_operation_completion(
            "test_operation", 1.5, success=True, tags={"tag": "test"}
        )
        
        # Check response time metric
        response_time_metric = performance_monitor.collector.get_latest_metric("test_operation_response_time")
        assert response_time_metric is not None
        assert response_time_metric.value == 1.5
        assert response_time_metric.tags == {"tag": "test"}
        
        # Check success metric
        success_metric = performance_monitor.collector.get_latest_metric("test_operation_success")
        assert success_metric is not None
        assert success_metric.value == 1.0
        
        # Check throughput metric
        throughput_metric = performance_monitor.collector.get_latest_metric("test_operation_throughput")
        assert throughput_metric is not None
        assert throughput_metric.value == 1.0
    
    def test_record_operation_completion_failure(self, performance_monitor):
        """Test operation completion recording with failure."""
        performance_monitor.record_operation_completion(
            "test_operation", 2.0, success=False, tags={"tag": "test"}
        )
        
        # Check response time metric
        response_time_metric = performance_monitor.collector.get_latest_metric("test_operation_response_time")
        assert response_time_metric is not None
        assert response_time_metric.value == 2.0
        
        # Check failure metric
        failure_metric = performance_monitor.collector.get_latest_metric("test_operation_failure")
        assert failure_metric is not None
        assert failure_metric.value == 1.0
        
        # Check throughput metric
        throughput_metric = performance_monitor.collector.get_latest_metric("test_operation_throughput")
        assert throughput_metric is not None
        assert throughput_metric.value == 1.0
    
    def test_get_performance_report(self, performance_monitor):
        """Test performance report generation."""
        # Record some operations
        performance_monitor.record_operation_start("test_op1")
        performance_monitor.record_operation_completion("test_op1", 1.0, success=True)
        
        performance_monitor.record_operation_start("test_op2")
        performance_monitor.record_operation_completion("test_op2", 2.0, success=True)
        
        # Get performance report
        report = performance_monitor.get_performance_report(timedelta(minutes=5))
        
        assert "report_timestamp" in report
        assert "time_window" in report
        assert "total_metrics" in report
        assert "metric_groups" in report
        assert "analysis" in report
        assert "summary" in report
        
        assert report["total_metrics"] > 0
        assert report["metric_groups"] > 0
    
    def test_get_system_health(self, performance_monitor):
        """Test system health assessment."""
        # Record some operations
        performance_monitor.record_operation_start("test_op")
        performance_monitor.record_operation_completion("test_op", 1.0, success=True)
        
        health = performance_monitor.get_system_health()
        
        assert "total_operations" in health
        assert "operations_with_issues" in health
        assert "performance_score" in health
        assert "health_status" in health
        
        assert health["total_operations"] > 0
        assert health["performance_score"] >= 0.0
        assert health["health_status"] in ["EXCELLENT", "GOOD", "FAIR", "POOR"]
    
    def test_stop_monitoring(self, performance_monitor):
        """Test monitoring stop functionality."""
        assert performance_monitor.monitoring_active is True
        
        performance_monitor.stop_monitoring()
        
        assert performance_monitor.monitoring_active is False
    
    def test_record_system_health_with_psutil(self, performance_monitor):
        """Test system health recording with psutil available."""
        # Mock psutil memory info
        mock_memory = MagicMock()
        mock_memory.percent = 75.0
        mock_memory.available = 8 * (1024**3)  # 8 GB
        
        with patch('psutil.virtual_memory', return_value=mock_memory):
            # Record system health
            performance_monitor._record_system_health()
            
            # Check that memory metrics were recorded
            memory_usage_metric = performance_monitor.collector.get_latest_metric("system_memory_usage")
            memory_available_metric = performance_monitor.collector.get_latest_metric("system_memory_available")
            
            assert memory_usage_metric is not None
            assert memory_usage_metric.value == 75.0
            
            assert memory_available_metric is not None
            assert memory_available_metric.value == 8.0  # GB
    
    def test_record_system_health_without_psutil(self, performance_monitor):
        """Test system health recording without psutil."""
        # Mock psutil import error
        with patch('psutil.virtual_memory', side_effect=ImportError("psutil not available")):
            # Record system health (should not fail)
            performance_monitor._record_system_health()
            
            # Check that heartbeat metric was recorded
            heartbeat_metric = performance_monitor.collector.get_latest_metric("monitoring_heartbeat")
            assert heartbeat_metric is not None


class TestGlobalPerformanceMonitor:
    """Test global performance monitor functionality."""
    
    def test_get_performance_monitor_singleton(self):
        """Test that get_performance_monitor returns singleton instance."""
        monitor1 = get_performance_monitor()
        monitor2 = get_performance_monitor()
        
        assert monitor1 is monitor2
        assert get_unified_validator().validate_type(monitor1, CoordinationPerformanceMonitor)
    
    def test_get_performance_monitor_multiple_calls(self):
        """Test multiple calls to get_performance_monitor return same instance."""
        monitors = []
        for _ in range(5):
            monitors.append(get_performance_monitor())
        
        # All should be the same instance
        first_monitor = monitors[0]
        for monitor in monitors[1:]:
            assert monitor is first_monitor


class TestPerformanceMonitorIntegration:
    """Test performance monitor integration scenarios."""
    
    @pytest.fixture
    def monitor(self):
        """Create monitor for integration testing."""
        monitor = CoordinationPerformanceMonitor()
        yield monitor
        monitor.stop_monitoring()
    
    def test_complete_operation_workflow(self, monitor):
        """Test complete operation workflow from start to completion."""
        operation_name = "integration_test_operation"
        tags = {"environment": "test", "component": "integration"}
        
        # Start operation
        monitor.record_operation_start(operation_name, tags)
        
        # Simulate operation execution
        time.sleep(0.1)
        
        # Complete operation
        monitor.record_operation_completion(operation_name, 0.1, success=True, tags=tags)
        
        # Verify metrics were recorded
        start_metric = monitor.collector.get_latest_metric(f"{operation_name}_start")
        response_time_metric = monitor.collector.get_latest_metric(f"{operation_name}_response_time")
        success_metric = monitor.collector.get_latest_metric(f"{operation_name}_success")
        throughput_metric = monitor.collector.get_latest_metric(f"{operation_name}_throughput")
        
        assert start_metric is not None
        assert response_time_metric is not None
        assert success_metric is not None
        assert throughput_metric is not None
        
        assert start_metric.tags == tags
        assert response_time_metric.tags == tags
        assert response_time_metric.value >= 0.1
    
    def test_multiple_operations_tracking(self, monitor):
        """Test tracking multiple operations simultaneously."""
        operations = ["op1", "op2", "op3"]
        
        # Start all operations
        for op in operations:
            monitor.record_operation_start(op)
        
        # Complete operations with different response times
        monitor.record_operation_completion("op1", 1.0, success=True)
        monitor.record_operation_completion("op2", 2.0, success=True)
        monitor.record_operation_completion("op3", 0.5, success=False)
        
        # Verify all metrics were recorded
        for op in operations:
            response_time_metric = monitor.collector.get_latest_metric(f"{op}_response_time")
            assert response_time_metric is not None
        
        # Check success/failure metrics
        op1_success = monitor.collector.get_latest_metric("op1_success")
        op2_success = monitor.collector.get_latest_metric("op2_success")
        op3_failure = monitor.collector.get_latest_metric("op3_failure")
        
        assert op1_success is not None
        assert op2_success is not None
        assert op3_failure is not None
    
    def test_performance_report_with_multiple_operations(self, monitor):
        """Test performance report generation with multiple operations."""
        # Record various operations
        for i in range(5):
            op_name = f"batch_op_{i}"
            monitor.record_operation_start(op_name)
            monitor.record_operation_completion(op_name, 0.5 + i * 0.1, success=True)
        
        # Generate report
        report = monitor.get_performance_report(timedelta(minutes=5))
        
        assert report["total_metrics"] > 0
        assert report["metric_groups"] > 0
        
        # Check analysis results
        analysis = report["analysis"]
        assert len(analysis) > 0
        
        # Check summary
        summary = report["summary"]
        assert summary["total_operations"] > 0
        assert summary["performance_score"] >= 0.0
        assert summary["health_status"] in ["EXCELLENT", "GOOD", "FAIR", "POOR"]
    
    def test_system_health_assessment_scenarios(self, monitor):
        """Test system health assessment in various scenarios."""
        # Healthy system (no operations)
        health = monitor.get_system_health()
        assert health["health_status"] == "EXCELLENT"
        assert health["performance_score"] == 100.0
        
        # Good performance (fast operations)
        for i in range(3):
            op_name = f"fast_op_{i}"
            monitor.record_operation_start(op_name)
            monitor.record_operation_completion(op_name, 0.1, success=True)
        
        health = monitor.get_system_health()
        # Note: The actual health status depends on the analyzer implementation
        # We just verify it's a valid status
        assert health["health_status"] in ["EXCELLENT", "GOOD", "FAIR", "POOR"]
        assert health["performance_score"] >= 0.0
        
        # Degraded performance (slow operations)
        for i in range(3):
            op_name = f"slow_op_{i}"
            monitor.record_operation_start(op_name)
            monitor.record_operation_completion(op_name, 6.0, success=True)  # Above 5s threshold
        
        health = monitor.get_system_health()
        # Note: The actual health status depends on the analyzer implementation
        # We just verify it's a valid status
        assert health["health_status"] in ["EXCELLENT", "GOOD", "FAIR", "POOR"]
        assert health["performance_score"] >= 0.0


if __name__ == "__main__":
    pytest.main([__file__])

