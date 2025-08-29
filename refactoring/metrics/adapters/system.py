from __future__ import annotations

import time
import psutil

from .base import MetricAdapter
from ..aggregator import Metric


class SystemMetricsAdapter(MetricAdapter):
    """Collect a handful of system level metrics using ``psutil``."""

    def collect(self):
        now = time.time()
        cpu = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory().percent
        return [
            Metric("system", "cpu_percent", cpu, now),
            Metric("system", "memory_percent", memory, now),
        ]
