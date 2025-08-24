import uuid
from unittest.mock import MagicMock, patch

from src.core.performance_validation_system_backup import PerformanceValidationSystem
from src.core.performance.metrics.collector import (
    PerformanceBenchmark,
    BenchmarkType,
    PerformanceLevel,
)


def _make_benchmark(b_type: BenchmarkType) -> PerformanceBenchmark:
    return PerformanceBenchmark(
        benchmark_id=str(uuid.uuid4()),
        benchmark_type=b_type,
        test_name=f"{b_type.value} benchmark",
        start_time="s",
        end_time="e",
        duration=0.1,
        metrics={},
        target_metrics={},
        performance_level=PerformanceLevel.PRODUCTION_READY,
        optimization_recommendations=[],
    )


def test_run_comprehensive_benchmark_with_mocked_benchmarks():
    system = PerformanceValidationSystem(
        MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )

    with patch.object(system, "_run_response_time_benchmark", return_value=_make_benchmark(BenchmarkType.RESPONSE_TIME)), \
         patch.object(system, "_run_throughput_benchmark", return_value=_make_benchmark(BenchmarkType.THROUGHPUT)), \
         patch.object(system, "_run_scalability_benchmark", return_value=_make_benchmark(BenchmarkType.SCALABILITY)), \
         patch.object(system, "_run_reliability_benchmark", return_value=_make_benchmark(BenchmarkType.RELIABILITY)), \
         patch.object(system, "_run_latency_benchmark", return_value=_make_benchmark(BenchmarkType.LATENCY)), \
         patch.object(system.validation_rules, "generate_optimization_recommendations", return_value=[]), \
         patch.object(system.alert_manager, "check_benchmark_for_alerts", return_value=[]):
        benchmark_id = system.run_comprehensive_benchmark()

    assert benchmark_id
    assert len(system.report_generator.reports) == 1

