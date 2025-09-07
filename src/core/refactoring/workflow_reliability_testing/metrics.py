from typing import Dict, List

from .config import (
from .utils import get_logger
from __future__ import annotations

"""Analysis helpers for workflow reliability testing."""



    ReliabilityTest,
    ReliabilityTestSuite,
    TestResult,
)

logger = get_logger(__name__)


def calculate_test_suite_scores(
    test_suite: ReliabilityTestSuite, tests: Dict[str, ReliabilityTest]
) -> ReliabilityTestSuite:
    """Calculate overall reliability and performance scores for a suite."""
    if not test_suite.test_results:
        return test_suite

    total_weight = 0.0
    weighted_reliability = 0.0

    for result in test_suite.test_results:
        test = tests.get(result.test_id)
        if test:
            weight = test.weight
            total_weight += weight
            weighted_reliability += result.reliability_score * weight

    if total_weight:
        test_suite.overall_reliability = weighted_reliability / total_weight

    performance_scores = [
        r.performance_metrics.get("performance_score", r.reliability_score)
        for r in test_suite.test_results
    ]
    if performance_scores:
        test_suite.performance_score = sum(performance_scores) / len(performance_scores)
        test_suite.stability_score = test_suite.performance_score

    return test_suite


def generate_test_recommendations(test_suite: ReliabilityTestSuite) -> List[str]:
    """Create human-readable recommendations from test results."""
    recommendations: List[str] = []
    for result in test_suite.test_results:
        if result.result != TestResult.PASSED:
            recommendations.append(
                f"Investigate {result.test_name} ({result.result.value})"
            )
    if not recommendations:
        recommendations.append(
            "All reliability tests passed. Maintain current configurations."
        )
    return recommendations


def get_reliability_trends(history: List[float]) -> Dict[str, float]:
    """Compute basic trend information for reliability history."""
    if not history:
        return {
            "current_reliability": 0.0,
            "average_reliability": 0.0,
            "reliability_trend": "stable",
        }

    current = history[-1]
    average = sum(history) / len(history)
    trend = "improving" if current >= average else "declining"
    return {
        "current_reliability": current,
        "average_reliability": average,
        "reliability_trend": trend,
    }
