"""
Predictive System Health Assessment - V2 Compliant
==================================================

System health assessment functionality for predictive analytics.
V2 Compliance: ≤400 lines, ≤10 functions, single responsibility
"""

import statistics
from datetime import datetime

from .predictive_models import PerformanceMetrics, SystemHealth


class SystemHealthAssessor:
    """System health assessment functionality."""

    def __init__(self):
        """Initialize system health assessor."""
        self.health_thresholds = {
            "cpu": 80.0,
            "memory": 85.0,
            "response_time": 1000.0,  # milliseconds
            "disk": 90.0,
        }

    def assess_system_health(self, metrics_history: list[PerformanceMetrics]) -> SystemHealth:
        """Assess overall system health."""
        if not metrics_history:
            return self._create_default_health_assessment()

        recent_metrics = metrics_history[-20:]  # Last 20 metrics

        # Calculate health score
        health_score = self._calculate_health_score(recent_metrics)

        # Identify health issues
        issues = self._identify_health_issues(recent_metrics)

        # Generate recommendations
        recommendations = self._generate_health_recommendations(health_score, issues)

        # Determine overall status
        status = self._determine_health_status(health_score)

        return SystemHealth(
            overall_score=health_score,
            status=status,
            issues=issues,
            recommendations=recommendations,
            assessed_at=datetime.now(),
            metrics_analyzed=len(recent_metrics),
        )

    def _calculate_health_score(self, metrics: list[PerformanceMetrics]) -> float:
        """Calculate overall health score from metrics."""
        if not metrics:
            return 0.0

        scores = []

        # CPU health score
        cpu_values = [m.cpu_usage for m in metrics]
        cpu_score = self._calculate_metric_health_score(cpu_values, self.health_thresholds["cpu"])
        scores.append(cpu_score)

        # Memory health score
        memory_values = [m.memory_usage for m in metrics]
        memory_score = self._calculate_metric_health_score(
            memory_values, self.health_thresholds["memory"]
        )
        scores.append(memory_score)

        # Response time health score
        response_values = [m.response_time for m in metrics]
        response_score = self._calculate_response_time_health_score(response_values)
        scores.append(response_score)

        # Disk health score
        disk_values = [m.disk_usage for m in metrics]
        disk_score = self._calculate_metric_health_score(
            disk_values, self.health_thresholds["disk"]
        )
        scores.append(disk_score)

        # Calculate weighted average
        return sum(scores) / len(scores)

    def _calculate_metric_health_score(self, values: list[float], threshold: float) -> float:
        """Calculate health score for a metric based on threshold."""
        if not values:
            return 0.0

        # Calculate average utilization
        avg_utilization = statistics.mean(values)

        # Calculate score based on threshold
        if avg_utilization <= threshold * 0.5:
            return 1.0  # Excellent
        elif avg_utilization <= threshold * 0.7:
            return 0.8  # Good
        elif avg_utilization <= threshold:
            return 0.6  # Fair
        elif avg_utilization <= threshold * 1.2:
            return 0.4  # Poor
        else:
            return 0.2  # Critical

    def _calculate_response_time_health_score(self, values: list[float]) -> float:
        """Calculate health score for response time."""
        if not values:
            return 0.0

        avg_response_time = statistics.mean(values)
        threshold = self.health_thresholds["response_time"]

        # Response time is inverse - lower is better
        if avg_response_time <= threshold * 0.5:
            return 1.0  # Excellent
        elif avg_response_time <= threshold * 0.7:
            return 0.8  # Good
        elif avg_response_time <= threshold:
            return 0.6  # Fair
        elif avg_response_time <= threshold * 1.5:
            return 0.4  # Poor
        else:
            return 0.2  # Critical

    def _identify_health_issues(self, metrics: list[PerformanceMetrics]) -> list[str]:
        """Identify specific health issues."""
        issues = []

        if not metrics:
            return ["No metrics available for analysis"]

        # Check CPU issues
        cpu_values = [m.cpu_usage for m in metrics]
        avg_cpu = statistics.mean(cpu_values)
        if avg_cpu > self.health_thresholds["cpu"]:
            issues.append(f"High CPU usage: {avg_cpu:.1f}%")

        # Check memory issues
        memory_values = [m.memory_usage for m in metrics]
        avg_memory = statistics.mean(memory_values)
        if avg_memory > self.health_thresholds["memory"]:
            issues.append(f"High memory usage: {avg_memory:.1f}%")

        # Check response time issues
        response_values = [m.response_time for m in metrics]
        avg_response = statistics.mean(response_values)
        if avg_response > self.health_thresholds["response_time"]:
            issues.append(f"High response time: {avg_response:.1f}ms")

        # Check disk issues
        disk_values = [m.disk_usage for m in metrics]
        avg_disk = statistics.mean(disk_values)
        if avg_disk > self.health_thresholds["disk"]:
            issues.append(f"High disk usage: {avg_disk:.1f}%")

        # Check for variability issues
        if len(cpu_values) > 1:
            cpu_cv = statistics.stdev(cpu_values) / statistics.mean(cpu_values)
            if cpu_cv > 0.3:
                issues.append("High CPU variability")

        if not issues:
            issues.append("No significant issues detected")

        return issues

    def _generate_health_recommendations(self, health_score: float, issues: list[str]) -> list[str]:
        """Generate health recommendations."""
        recommendations = []

        if health_score >= 0.8:
            recommendations.append("System health is excellent")
        elif health_score >= 0.6:
            recommendations.append("System health is good")
        elif health_score >= 0.4:
            recommendations.append("System health needs attention")
        else:
            recommendations.append("System health requires immediate attention")

        # Add specific recommendations based on issues
        for issue in issues:
            if "CPU" in issue:
                recommendations.append("Consider CPU optimization or scaling")
            elif "memory" in issue:
                recommendations.append("Consider memory optimization or scaling")
            elif "response time" in issue:
                recommendations.append("Consider performance optimization")
            elif "disk" in issue:
                recommendations.append("Consider disk cleanup or expansion")
            elif "variability" in issue:
                recommendations.append("Investigate resource variability causes")

        return recommendations

    def _determine_health_status(self, health_score: float) -> str:
        """Determine overall health status."""
        if health_score >= 0.8:
            return "excellent"
        elif health_score >= 0.6:
            return "good"
        elif health_score >= 0.4:
            return "fair"
        elif health_score >= 0.2:
            return "poor"
        else:
            return "critical"

    def _create_default_health_assessment(self) -> SystemHealth:
        """Create default health assessment when no data available."""
        return SystemHealth(
            overall_score=0.0,
            status="unknown",
            issues=["No metrics available"],
            recommendations=["Collect performance metrics for health assessment"],
            assessed_at=datetime.now(),
            metrics_analyzed=0,
        )
