from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from ..aggregator import Metric


class MetricAdapter(ABC):
    """Base class for metric source adapters."""

    def __init__(self, interval: float = 1.0) -> None:
        self.interval = interval

    @abstractmethod
    def collect(self) -> Iterable[Metric]:
        """Collect metrics from the underlying source."""
        raise NotImplementedError
