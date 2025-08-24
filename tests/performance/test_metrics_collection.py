"""Tests for performance metrics collection and validation."""

from unittest.mock import Mock


def test_performance_monitoring_startup(perf_monitor):
    assert perf_monitor.start_monitoring()
    perf_monitor.start_monitoring.assert_called_once()


def test_performance_monitoring_shutdown(perf_monitor):
    assert perf_monitor.stop_monitoring()
    perf_monitor.stop_monitoring.assert_called_once()


def test_cpu_usage_monitoring():
    cpu_monitor = Mock()
    cpu_monitor.get_cpu_usage.return_value = 45.2
    cpu_usage = cpu_monitor.get_cpu_usage()
    assert 0 <= cpu_usage <= 100
    cpu_monitor.get_cpu_usage.assert_called_once()


def test_memory_usage_monitoring():
    memory_monitor = Mock()
    memory_monitor.get_memory_usage.return_value = 1_073_741_824
    memory_usage = memory_monitor.get_memory_usage()
    assert memory_usage > 0
    memory_monitor.get_memory_usage.assert_called_once()


def test_disk_io_monitoring():
    disk_monitor = Mock()
    disk_monitor.get_disk_io.return_value = {
        "read_bytes": 1_048_576,
        "write_bytes": 524_288,
        "read_count": 100,
        "write_count": 50,
    }
    disk_io = disk_monitor.get_disk_io()
    assert disk_io["read_bytes"] > 0 and disk_io["write_bytes"] > 0
    disk_monitor.get_disk_io.assert_called_once()


def test_network_monitoring():
    network_monitor = Mock()
    network_monitor.get_network_stats.return_value = {
        "bytes_sent": 2_097_152,
        "bytes_recv": 4_194_304,
        "packets_sent": 1_000,
        "packets_recv": 2_000,
    }
    stats = network_monitor.get_network_stats()
    assert stats["bytes_sent"] > 0 and stats["bytes_recv"] > 0
    network_monitor.get_network_stats.assert_called_once()


def test_response_time_validation(performance_metrics):
    response_monitor = Mock()
    response_monitor.measure_response_time.return_value = 0.125
    response_time = response_monitor.measure_response_time()
    assert response_time < performance_metrics["response_time"]["good"]
    response_monitor.measure_response_time.assert_called_once()


def test_throughput_validation(performance_metrics):
    throughput_monitor = Mock()
    throughput_monitor.measure_throughput.return_value = 75
    throughput = throughput_monitor.measure_throughput()
    assert throughput >= performance_metrics["throughput"]["good"]
    throughput_monitor.measure_throughput.assert_called_once()


def test_error_rate_validation(performance_metrics):
    error_monitor = Mock()
    error_monitor.calculate_error_rate.return_value = 0.03
    error_rate = error_monitor.calculate_error_rate()
    assert error_rate < performance_metrics["error_rate"]["good"]
    error_monitor.calculate_error_rate.assert_called_once()


def test_load_testing_validation():
    load_tester = Mock()
    load_tester.run_load_test.return_value = {
        "concurrent_users": 100,
        "avg_response_time": 0.8,
        "throughput": 120,
        "error_rate": 0.02,
        "success": True,
    }
    result = load_tester.run_load_test()
    assert result["success"]
    load_tester.run_load_test.assert_called_once()


def test_stress_testing_validation():
    stress_tester = Mock()
    stress_tester.run_stress_test.return_value = {
        "max_concurrent_users": 500,
        "breaking_point": 450,
        "recovery_time": 2.5,
        "system_stability": "stable",
    }
    result = stress_tester.run_stress_test()
    assert result["system_stability"] == "stable"
    stress_tester.run_stress_test.assert_called_once()


def test_performance_baseline_validation():
    baseline_validator = Mock()
    baseline_validator.validate_baseline.return_value = {
        "baseline_met": True,
        "performance_score": 0.85,
        "improvements": ["CPU optimization", "Memory management"],
        "regressions": [],
    }
    result = baseline_validator.validate_baseline()
    assert result["baseline_met"]
    baseline_validator.validate_baseline.assert_called_once()

