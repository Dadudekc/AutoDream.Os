"""Example MetricSourceAdapter implementation."""

import time
from typing import List

from src.core.health.metrics.adapters import Metric, MetricSourceAdapter


class DummyMetricsAdapter(MetricSourceAdapter):
    """Return a single metric with the current timestamp."""

    def collect(self) -> List[Metric]:
        now = time.time()
        return [Metric(namespace="example", name="dummy", value=1, timestamp=now)]
