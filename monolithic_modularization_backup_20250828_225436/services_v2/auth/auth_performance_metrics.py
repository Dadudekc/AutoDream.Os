"""Metrics utilities for the authentication performance monitor."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import statistics
import time

from .common_performance import PerformanceMetric, PerformanceAlert, record_metric


def collect_performance_metrics(monitor) -> None:
    """Collect current performance metrics from auth service."""
    try:
        if not hasattr(monitor, "auth_service") or not monitor.auth_service:
            return
        metrics = monitor.auth_service.get_performance_metrics()
        # Record key metrics
        if "auth_duration" in metrics:
            record_metric(
                monitor,
                "auth_duration",
                metrics["auth_duration"],
                "seconds",
                {"source": "auth_service", "metric_type": "timing"},
            )
        if "success_rate" in metrics:
            record_metric(
                monitor,
                "success_rate",
                metrics["success_rate"],
                "percentage",
                {"source": "auth_service", "metric_type": "ratio"},
            )
        if "auth_per_second" in metrics:
            record_metric(
                monitor,
                "auth_per_second",
                metrics["auth_per_second"],
                "auths/sec",
                {"source": "auth_service", "metric_type": "throughput"},
            )
        if "total_attempts" in metrics:
            record_metric(
                monitor,
                "total_attempts",
                metrics["total_attempts"],
                "count",
                {"source": "auth_service", "metric_type": "counter"},
            )
        if "uptime_seconds" in metrics:
            record_metric(
                monitor,
                "uptime_seconds",
                metrics["uptime_seconds"],
                "seconds",
                {"source": "auth_service", "metric_type": "uptime"},
            )
    except Exception as e:
        monitor.logger.error(f"Failed to collect performance metrics: {e}")


def calculate_trend(values: List[float]) -> float:
    """Calculate trend slope from values."""
    if len(values) < 2:
        return 0.0
    try:
        n = len(values)
        x_values = list(range(n))
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        if denominator == 0:
            return 0.0
        return numerator / denominator
    except Exception:
        return 0.0


def detect_performance_degradation(
    current_value: float, baseline: Dict[str, Any], metric_name: str
) -> Optional[float]:
    """Detect performance degradation compared to baseline."""
    try:
        baseline_value = baseline.get("value", 0)
        baseline_std = baseline.get("std_dev", 0)
        if baseline_std == 0:
            return None
        z_score = abs(current_value - baseline_value) / baseline_std
        if z_score > 2:
            degradation = ((current_value - baseline_value) / baseline_value) * 100
            return degradation
        return None
    except Exception:
        return None


def analyze_performance(monitor) -> None:
    """Analyze current performance metrics."""
    try:
        for metric_name, metrics in monitor.metrics_history.items():
            if len(metrics) < 2:
                continue
            current_value = metrics[-1].value
            recent_values = [m.value for m in list(metrics)[-10:]]
            if len(recent_values) >= 2:
                trend = calculate_trend(recent_values)
                record_metric(
                    monitor,
                    f"{metric_name}_trend",
                    trend,
                    "slope",
                    {
                        "source": "performance_analyzer",
                        "metric_type": "trend",
                        "base_metric": metric_name,
                    },
                )
            if monitor.baseline_calculated and metric_name in monitor.baselines:
                baseline = monitor.baselines[metric_name]
                degradation = detect_performance_degradation(
                    current_value, baseline, metric_name
                )
                if degradation:
                    record_metric(
                        monitor,
                        f"{metric_name}_degradation",
                        degradation,
                        "percentage",
                        {
                            "source": "performance_analyzer",
                            "metric_type": "degradation",
                            "base_metric": metric_name,
                        },
                    )
    except Exception as e:
        monitor.logger.error(f"Performance analysis failed: {e}")


def calculate_performance_baselines(monitor) -> None:
    """Calculate performance baselines from historical data."""
    try:
        monitor.logger.info("📊 Calculating performance baselines...")
        for metric_name, metrics in monitor.metrics_history.items():
            if len(metrics) < 10:
                continue
            values = [m.value for m in metrics]
            baseline = {
                "value": statistics.mean(values),
                "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
                "min_value": min(values),
                "max_value": max(values),
                "sample_count": len(values),
                "calculated_at": datetime.now(),
            }
            monitor.baselines[metric_name] = baseline
            monitor.logger.info(
                f"✅ Baseline calculated for {metric_name}: {baseline['value']:.3f} ± {baseline['std_dev']:.3f}"
            )
        monitor.baseline_calculated = True
        monitor.logger.info("✅ Performance baselines calculated successfully")
    except Exception as e:
        monitor.logger.error(f"Failed to calculate performance baselines: {e}")


def create_alert(
    monitor, alert_type: str, metric_name: str, current_value: float, threshold: float
) -> None:
    """Create a performance alert."""
    alert_key = f"{alert_type}_{metric_name}"
    current_time = datetime.now()
    if (
        current_time - monitor.last_alert_time[alert_key]
    ).total_seconds() < monitor.config["alert_cooldown"]:
        return
    alert = PerformanceAlert(
        alert_id=f"alert_{int(time.time())}_{alert_type}_{metric_name}",
        timestamp=current_time,
        alert_type=alert_type,
        message=f"Performance {alert_type}: {metric_name} = {current_value:.3f} (threshold: {threshold:.3f})",
        metric_name=metric_name,
        current_value=current_value,
        threshold=threshold,
        severity=3 if alert_type == "warning" else 5,
    )
    monitor.alerts_history.append(alert)
    monitor.alert_counts[alert_key] += 1
    monitor.last_alert_time[alert_key] = current_time
    alert_icon = "⚠️" if alert_type == "warning" else "🚨"
    monitor.logger.warning(f"{alert_icon} {alert.message}")


def check_performance_alerts(monitor) -> None:
    """Check for performance alerts based on thresholds."""
    try:
        for metric_name, thresholds in monitor.performance_thresholds.items():
            if (
                metric_name not in monitor.metrics_history
                or not monitor.metrics_history[metric_name]
            ):
                continue
            current_value = monitor.metrics_history[metric_name][-1].value
            if "warning" in thresholds and current_value > thresholds["warning"]:
                create_alert(
                    monitor,
                    "warning",
                    metric_name,
                    current_value,
                    thresholds["warning"],
                )
            if "critical" in thresholds and current_value > thresholds["critical"]:
                create_alert(
                    monitor,
                    "critical",
                    metric_name,
                    current_value,
                    thresholds["critical"],
                )
    except Exception as e:
        monitor.logger.error(f"Performance alert checking failed: {e}")


def calculate_system_health(monitor) -> str:
    """Calculate overall system health score."""
    try:
        health_score = 100
        if (
            "success_rate" in monitor.metrics_history
            and monitor.metrics_history["success_rate"]
        ):
            current_success = monitor.metrics_history["success_rate"][-1].value
            if current_success < 0.95:
                health_score -= 20
        if (
            "auth_duration" in monitor.metrics_history
            and monitor.metrics_history["auth_duration"]
        ):
            current_duration = monitor.metrics_history["auth_duration"][-1].value
            if current_duration > 1.0:
                health_score -= 15
        recent_alerts = [
            a
            for a in monitor.alerts_history
            if (datetime.now() - a.timestamp).total_seconds() < 300
        ]
        if len(recent_alerts) > 5:
            health_score -= 25
        if health_score >= 90:
            return "excellent"
        if health_score >= 75:
            return "good"
        if health_score >= 60:
            return "fair"
        return "poor"
    except Exception:
        return "unknown"


def calculate_performance_indicators(monitor) -> Dict[str, Any]:
    """Calculate key performance indicators."""
    indicators: Dict[str, Any] = {}
    try:
        if (
            "success_rate" in monitor.metrics_history
            and monitor.metrics_history["success_rate"]
        ):
            success_rates = [m.value for m in monitor.metrics_history["success_rate"]]
            indicators["current_success_rate"] = (
                success_rates[-1] if success_rates else 0
            )
            indicators["avg_success_rate"] = (
                statistics.mean(success_rates) if len(success_rates) > 1 else 0
            )
        if (
            "auth_duration" in monitor.metrics_history
            and monitor.metrics_history["auth_duration"]
        ):
            durations = [m.value for m in monitor.metrics_history["auth_duration"]]
            indicators["current_auth_duration"] = durations[-1] if durations else 0
            indicators["avg_auth_duration"] = (
                statistics.mean(durations) if len(durations) > 1 else 0
            )
            indicators["min_auth_duration"] = min(durations) if durations else 0
            indicators["max_auth_duration"] = max(durations) if durations else 0
        if (
            "auth_per_second" in monitor.metrics_history
            and monitor.metrics_history["auth_per_second"]
        ):
            throughputs = [m.value for m in monitor.metrics_history["auth_per_second"]]
            indicators["current_throughput"] = throughputs[-1] if throughputs else 0
            indicators["avg_throughput"] = (
                statistics.mean(throughputs) if len(throughputs) > 1 else 0
            )
        indicators["system_health"] = calculate_system_health(monitor)
    except Exception as e:
        monitor.logger.error(f"Failed to calculate performance indicators: {e}")
        indicators["error"] = str(e)
    return indicators


__all__ = [
    "PerformanceMetric",
    "PerformanceAlert",
    "collect_performance_metrics",
    "analyze_performance",
    "check_performance_alerts",
    "calculate_performance_baselines",
    "calculate_performance_indicators",
    "record_metric",
]
