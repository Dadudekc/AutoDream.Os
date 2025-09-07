from collections import defaultdict
from datetime import datetime

import pytest

from src.services_v2.auth.auth_performance_metrics import (
from src.services_v2.auth.common_performance import (


    PerformanceMetric,
    PerformanceAlert,
    record_metric,
)
    calculate_trend,
    detect_performance_degradation,
)


class DummyMonitor:
    def __init__(self):
        self.metrics_history = defaultdict(list)


def test_record_metric_appends_metric():
    monitor = DummyMonitor()
    record_metric(monitor, "test_metric", 1.5, "units", {"source": "test"})
    assert len(monitor.metrics_history["test_metric"]) == 1
    metric = monitor.metrics_history["test_metric"][0]
    assert isinstance(metric, PerformanceMetric)
    assert metric.value == 1.5
    assert metric.unit == "units"
    assert metric.context["source"] == "test"


def test_performance_alert_dataclass():
    alert = PerformanceAlert(
        alert_id="1",
        timestamp=datetime.now(),
        alert_type="warning",
        message="msg",
        metric_name="m",
        current_value=5.0,
        threshold=10.0,
        severity=2,
    )
    assert alert.alert_type == "warning"
    assert alert.metric_name == "m"


def test_calculate_trend_positive_slope():
    values = [1, 2, 3, 4]
    slope = calculate_trend(values)
    assert slope > 0


def test_detect_performance_degradation_detects_change():
    baseline = {"value": 100.0, "std_dev": 10.0}
    degradation = detect_performance_degradation(130.0, baseline, "metric")
    assert degradation is not None
    assert degradation == pytest.approx(30.0)
