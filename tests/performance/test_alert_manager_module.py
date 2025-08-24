from src.core.performance.alerts.manager import AlertManager, AlertSeverity
from src.core.performance.metrics.collector import (
    PerformanceBenchmark,
    BenchmarkType,
    PerformanceLevel,
)


def test_alert_generation_and_handler_trigger():
    manager = AlertManager()
    triggered = []

    def handler(alert):
        triggered.append(alert.alert_id)

    manager.register_alert_handler(AlertSeverity.CRITICAL, handler)

    benchmark = PerformanceBenchmark(
        benchmark_id="b1",
        benchmark_type=BenchmarkType.RESPONSE_TIME,
        test_name="Response",
        start_time="s",
        end_time="e",
        duration=1.0,
        metrics={"average_response_time": 600},
        target_metrics={"target_response_time": 100},
        performance_level=PerformanceLevel.NOT_READY,
        optimization_recommendations=[],
    )

    alerts = manager.check_benchmark_for_alerts(benchmark)
    assert alerts
    assert triggered

