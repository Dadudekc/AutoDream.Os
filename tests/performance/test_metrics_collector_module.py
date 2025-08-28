import pytest

from src.core.performance.metrics.collector import (
    MetricsCollector,
    PerformanceBenchmark,
    BenchmarkType,
    PerformanceLevel,
)


def test_collect_response_time_metrics():
    collector = MetricsCollector()
    metrics = collector.collect_response_time_metrics([100, 120, 140])
    assert metrics["average_response_time"] == pytest.approx(120)
    assert metrics["min_response_time"] == 100
    assert metrics["max_response_time"] == 140


def test_collect_throughput_metrics():
    collector = MetricsCollector()
    metrics = collector.collect_throughput_metrics(operations_count=20, duration=4)
    assert metrics["throughput_ops_per_sec"] == pytest.approx(5.0)


def test_store_and_retrieve_benchmark():
    collector = MetricsCollector()
    benchmark = PerformanceBenchmark(
        benchmark_id="b1",
        benchmark_type=BenchmarkType.THROUGHPUT,
        test_name="dummy",
        start_time="s",
        end_time="e",
        duration=1.0,
        metrics={"throughput_ops_per_sec": 5.0},
        target_metrics={"target_throughput": 5.0},
        performance_level=PerformanceLevel.PRODUCTION_READY,
        optimization_recommendations=[],
    )
    assert collector.store_benchmark(benchmark)
    assert collector.get_benchmark("b1") is benchmark


def test_collect_reliability_metrics():
    collector = MetricsCollector()
    metrics = collector.collect_reliability_metrics(
        total_operations=100, failed_operations=5, duration=50
    )
    assert metrics["success_rate_percent"] == pytest.approx(95.0)
    assert metrics["failure_rate_percent"] == pytest.approx(5.0)
    assert metrics["mean_time_between_failures"] == pytest.approx(10.0)


def test_collect_latency_metrics():
    collector = MetricsCollector()
    latencies = [10, 20, 30, 40, 50]
    metrics = collector.collect_latency_metrics(latencies)
    assert metrics["average_latency"] == pytest.approx(30)
    assert metrics["p95_latency"] == 50
    assert metrics["p99_latency"] == 50

