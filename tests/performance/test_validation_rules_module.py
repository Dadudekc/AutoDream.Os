from src.core.performance.validation.rules import ValidationRules
from src.core.performance.metrics.collector import (
    PerformanceBenchmark,
    BenchmarkType,
    PerformanceLevel,
)


def _make_benchmark(level: PerformanceLevel) -> PerformanceBenchmark:
    return PerformanceBenchmark(
        benchmark_id="b",
        benchmark_type=BenchmarkType.RESPONSE_TIME,
        test_name="test",
        start_time="s",
        end_time="e",
        duration=1.0,
        metrics={"average_response_time": 100},
        target_metrics={"target_response_time": 100},
        performance_level=level,
        optimization_recommendations=[],
    )


def test_classify_performance_level():
    rules = ValidationRules()
    level = rules.classify_performance_level(90, 100, lower_is_better=False)
    assert level == PerformanceLevel.PRODUCTION_READY
    level2 = rules.classify_performance_level(110, 100, lower_is_better=True)
    assert level2 == PerformanceLevel.PRODUCTION_READY


def test_calculate_overall_performance_level():
    rules = ValidationRules()
    b1 = _make_benchmark(PerformanceLevel.ENTERPRISE_READY)
    b2 = _make_benchmark(PerformanceLevel.PRODUCTION_READY)
    overall = rules.calculate_overall_performance_level([b1, b2])
    assert overall == PerformanceLevel.PRODUCTION_READY

