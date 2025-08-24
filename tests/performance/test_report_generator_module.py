import json

from src.core.performance.reporting.generator import ReportGenerator
from src.core.performance.metrics.collector import (
    PerformanceBenchmark,
    BenchmarkType,
    PerformanceLevel,
)


def test_generate_and_format_report():
    generator = ReportGenerator()
    benchmark = PerformanceBenchmark(
        benchmark_id="b1",
        benchmark_type=BenchmarkType.LATENCY,
        test_name="Latency Test",
        start_time="s",
        end_time="e",
        duration=0.5,
        metrics={"average_latency": 40.0},
        target_metrics={"target_latency": 50.0},
        performance_level=PerformanceLevel.ENTERPRISE_READY,
        optimization_recommendations=[],
    )
    report = generator.generate_performance_report(
        [benchmark], PerformanceLevel.ENTERPRISE_READY, ["All good"]
    )
    json_data = json.loads(generator.format_report_as_json(report))
    assert json_data["overall_performance_level"] == "enterprise_ready"
    text = generator.format_report_as_text(report)
    assert "PERFORMANCE VALIDATION REPORT" in text

