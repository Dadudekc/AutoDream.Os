from __future__ import annotations

import time
from typing import List

from .metrics import TestConfiguration, TestResult
from .utils import calculate_percentile, safe_divide


def calculate_test_results(
    config: TestConfiguration,
    start_time: float,
    end_time: float,
    total_duration: float,
    successful_iterations: int,
    failed_iterations: int,
    timeout_iterations: int,
    durations: List[float],
) -> TestResult:
    """Calculate comprehensive test results."""

    if durations:
        min_duration = min(durations)
        max_duration = max(durations)
        average_duration = sum(durations) / len(durations)
        sorted_durations = sorted(durations)
        p95_duration = calculate_percentile(sorted_durations, 0.95)
        p99_duration = calculate_percentile(sorted_durations, 0.99)
    else:
        min_duration = max_duration = average_duration = p95_duration = p99_duration = 0.0

    total_iterations = successful_iterations + failed_iterations + timeout_iterations
    success_rate = safe_divide(successful_iterations, total_iterations)
    throughput = safe_divide(total_iterations, total_duration)

    return TestResult(
        test_id=config.test_id,
        test_type=config.test_type,
        procedure_id=config.procedure_id,
        start_time=start_time,
        end_time=end_time,
        duration=total_duration,
        iterations=total_iterations,
        successful_iterations=successful_iterations,
        failed_iterations=failed_iterations,
        timeout_iterations=timeout_iterations,
        total_duration=total_duration,
        average_duration=average_duration,
        min_duration=min_duration,
        max_duration=max_duration,
        p95_duration=p95_duration,
        p99_duration=p99_duration,
        success_rate=success_rate,
        throughput=throughput,
    )


def create_error_result(config: TestConfiguration, error_details: str) -> TestResult:
    """Create an error result for failed tests."""

    current_time = time.time()
    return TestResult(
        test_id=config.test_id,
        test_type=config.test_type,
        procedure_id=config.procedure_id,
        start_time=current_time,
        end_time=current_time,
        duration=0.0,
        error_details=error_details,
    )
