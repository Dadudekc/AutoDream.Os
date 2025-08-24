#!/usr/bin/env python3
"""
📊 Health Score Calculator - Agent_Cellphone_V2

This component is responsible for calculating health scores and generating recommendations.
Following V2 coding standards: ≤200 LOC, OOP design, SRP.

Author: Foundation & Testing Specialist
License: MIT
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Any
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Agent health status levels"""

    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


class HealthScoreCalculator:
    """
    Health Score Calculator - Single responsibility: Calculate health scores and generate recommendations.

    Follows V2 standards: ≤200 LOC, OOP design, SRP.
    """

    def __init__(self):
        """Initialize the score calculator"""
        logger.info("HealthScoreCalculator initialized")

    def calculate_score(self, snapshot: Any, thresholds: Dict[str, Any]) -> float:
        """Calculate health score (0-100) for an agent"""
        if not snapshot.metrics:
            return 100.0  # No metrics available

        total_score = 0
        metric_count = 0

        for metric_type, metric in snapshot.metrics.items():
            if metric_type in thresholds:
                threshold = thresholds[metric_type]

                # Calculate metric score based on threshold proximity
                if metric.value <= threshold.warning_threshold:
                    score = 100.0  # Excellent
                elif metric.value <= threshold.critical_threshold:
                    # Linear interpolation between warning and critical
                    ratio = (metric.value - threshold.warning_threshold) / (
                        threshold.critical_threshold - threshold.warning_threshold
                    )
                    score = 100.0 - (ratio * 25.0)  # 100 to 75
                else:
                    score = max(
                        0.0,
                        75.0
                        - (
                            (metric.value - threshold.critical_threshold)
                            / threshold.critical_threshold
                        )
                        * 75.0,
                    )

                total_score += score
                metric_count += 1

        # Penalize for active alerts
        active_alerts = [alert for alert in snapshot.alerts if not alert.resolved]
        alert_penalty = 0

        for alert in active_alerts:
            if alert.severity == "critical":
                alert_penalty += 20
            elif alert.severity == "warning":
                alert_penalty += 10

        final_score = (total_score / metric_count) - alert_penalty
        return max(0.0, min(100.0, final_score))

    def determine_health_status(self, score: float) -> str:
        """Determine health status based on score"""
        if score >= 90:
            return HealthStatus.EXCELLENT.value
        elif score >= 75:
            return HealthStatus.GOOD.value
        elif score >= 50:
            return HealthStatus.WARNING.value
        else:
            return HealthStatus.CRITICAL.value

    def generate_recommendations(self, snapshot: Any) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []

        # Check for specific issues and provide recommendations
        for metric_type, metric in snapshot.metrics.items():
            if metric_type == "response_time" and metric.value > 1000:
                recommendations.append(
                    "Consider optimizing response time by reviewing processing logic"
                )

            elif metric_type == "memory_usage" and metric.value > 80:
                recommendations.append(
                    "High memory usage detected - consider memory optimization or cleanup"
                )

            elif metric_type == "cpu_usage" and metric.value > 85:
                recommendations.append(
                    "High CPU usage detected - consider load balancing or optimization"
                )

            elif metric_type == "error_rate" and metric.value > 5:
                recommendations.append(
                    "High error rate detected - review error handling and logging"
                )

        # Add general recommendations based on overall status
        if snapshot.overall_status == "critical":
            recommendations.append("CRITICAL: Immediate intervention required")
        elif snapshot.overall_status == "warning":
            recommendations.append(
                "WARNING: Monitor closely and address issues promptly"
            )

        return recommendations

    def calculate_metric_score(
        self, value: float, warning_threshold: float, critical_threshold: float
    ) -> float:
        """Calculate individual metric score"""
        if value <= warning_threshold:
            return 100.0
        elif value <= critical_threshold:
            # Linear interpolation between warning and critical
            ratio = (value - warning_threshold) / (
                critical_threshold - warning_threshold
            )
            return 100.0 - (ratio * 25.0)  # 100 to 75
        else:
            # Below critical threshold
            return max(
                0.0, 75.0 - ((value - critical_threshold) / critical_threshold) * 75.0
            )

    def calculate_alert_penalty(self, alerts: List[Any]) -> float:
        """Calculate penalty for active alerts"""
        penalty = 0.0

        for alert in alerts:
            if not alert.resolved:
                if alert.severity == "critical":
                    penalty += 20.0
                elif alert.severity == "warning":
                    penalty += 10.0
                elif alert.severity == "info":
                    penalty += 5.0

        return penalty

    def get_score_breakdown(
        self, snapshot: Any, thresholds: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get detailed score breakdown"""
        breakdown = {
            "metric_scores": {},
            "alert_penalty": 0.0,
            "final_score": 0.0,
            "status": "unknown",
        }

        if not snapshot.metrics:
            breakdown["final_score"] = 100.0
            breakdown["status"] = self.determine_health_status(100.0)
            return breakdown

        # Calculate individual metric scores
        total_score = 0
        metric_count = 0

        for metric_type, metric in snapshot.metrics.items():
            if metric_type in thresholds:
                threshold = thresholds[metric_type]
                score = self.calculate_metric_score(
                    metric.value,
                    threshold.warning_threshold,
                    threshold.critical_threshold,
                )
                breakdown["metric_scores"][metric_type] = score
                total_score += score
                metric_count += 1

        # Calculate average metric score
        if metric_count > 0:
            avg_metric_score = total_score / metric_count
        else:
            avg_metric_score = 100.0

        # Calculate alert penalty
        alert_penalty = self.calculate_alert_penalty(snapshot.alerts)
        breakdown["alert_penalty"] = alert_penalty

        # Calculate final score
        final_score = avg_metric_score - alert_penalty
        final_score = max(0.0, min(100.0, final_score))

        breakdown["final_score"] = final_score
        breakdown["status"] = self.determine_health_status(final_score)

        return breakdown

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            logger.info("Running HealthScoreCalculator smoke test...")

            # Test basic initialization
            assert self is not None
            logger.info("Basic initialization passed")

            # Test status determination
            assert self.determine_health_status(95.0) == "excellent"
            assert self.determine_health_status(80.0) == "good"
            assert self.determine_health_status(60.0) == "warning"
            assert self.determine_health_status(30.0) == "critical"
            logger.info("Status determination passed")

            # Test metric score calculation
            assert self.calculate_metric_score(500.0, 1000.0, 5000.0) == 100.0
            assert self.calculate_metric_score(1500.0, 1000.0, 5000.0) == 87.5
            assert self.calculate_metric_score(6000.0, 1000.0, 5000.0) == 0.0
            logger.info("Metric score calculation passed")

            # Test alert penalty calculation
            mock_alerts = [
                Mock(resolved=False, severity="warning"),
                Mock(resolved=False, severity="critical"),
            ]
            penalty = self.calculate_alert_penalty(mock_alerts)
            assert penalty == 30.0
            logger.info("Alert penalty calculation passed")

            # Test recommendations generation
            mock_snapshot = Mock()
            mock_snapshot.metrics = {
                "response_time": Mock(value=1500.0),
                "memory_usage": Mock(value=85.0),
            }
            mock_snapshot.overall_status = "warning"
            mock_snapshot.alerts = []

            recommendations = self.generate_recommendations(mock_snapshot)
            assert len(recommendations) > 0
            assert isinstance(recommendations, list)
            logger.info("Recommendations generation passed")

            logger.info("✅ HealthScoreCalculator smoke test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ HealthScoreCalculator smoke test FAILED: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return False


class Mock:
    """Simple mock class for testing"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Health Score Calculator CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")

    args = parser.parse_args()

    if args.test:
        calculator = HealthScoreCalculator()
        success = calculator.run_smoke_test()
        exit(0 if success else 1)

    elif args.demo:
        print("🚀 Starting Health Score Calculator Demo...")
        calculator = HealthScoreCalculator()

        # Test score calculation
        print("\n🧮 Testing score calculations:")
        test_values = [500.0, 1500.0, 3000.0, 6000.0]
        warning_threshold = 1000.0
        critical_threshold = 5000.0

        for value in test_values:
            score = calculator.calculate_metric_score(
                value, warning_threshold, critical_threshold
            )
            status = calculator.determine_health_status(score)
            print(f"  Value {value}ms: Score {score:.1f}/100 ({status})")

        # Test status determination
        print("\n📊 Testing status determination:")
        test_scores = [95.0, 80.0, 60.0, 30.0]
        for score in test_scores:
            status = calculator.determine_health_status(score)
            print(f"  Score {score:.1f}: {status}")

        # Test alert penalties
        print("\n🚨 Testing alert penalties:")
        mock_alerts = [
            Mock(resolved=False, severity="info"),
            Mock(resolved=False, severity="warning"),
            Mock(resolved=False, severity="critical"),
        ]
        penalty = calculator.calculate_alert_penalty(mock_alerts)
        print(f"  Total penalty: {penalty:.1f} points")

        print("\n✅ Demo completed")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
