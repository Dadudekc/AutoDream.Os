from __future__ import annotations

"""Metric source adapters.

These adapters provide a small interface for fetching metrics from different
sources. They are intentionally light weight so they can be tested in
isolation and composed by higher level components.
"""

from abc import ABC, abstractmethod
from typing import List

import psutil
import time

from .interfaces import Metric, MetricSource


class MetricSourceAdapter(MetricSource, ABC):
    """Base class for metric source adapters."""

    def __init__(self, interval: float = 1.0) -> None:
        self.interval = interval

    @abstractmethod
    def collect(self) -> List[Metric]:
        """Collect metrics from the underlying source.

        Returns:
            List[Metric]: Collected metrics.
        """
        raise NotImplementedError("collect must be implemented by subclasses")


class SystemMetricsAdapter(MetricSourceAdapter):
    """Collect a handful of system level metrics using ``psutil``."""

    def collect(self) -> List[Metric]:
        now = time.time()
        cpu = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory().percent
        return [
            Metric("system", "cpu_percent", cpu, now),
            Metric("system", "memory_percent", memory, now),
        ]
