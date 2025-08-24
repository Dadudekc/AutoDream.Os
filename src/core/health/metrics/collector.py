"""Orchestration logic for the metrics collection pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Iterable, List, Mapping, Optional

from .adapters import SystemMetricsAdapter
from .aggregation import MetricAggregator
from .interfaces import Metric, MetricSink, MetricSource
from .sinks import InMemoryMetricSink


class MetricSourceType(Enum):
    """Built in metric source identifiers."""

    SYSTEM = "system"


@dataclass
class MetricCollectionResult:
    """Result returned from a single collection run."""

    success: bool
    metrics: List[Metric]
    collection_time: datetime
    errors: List[str] = field(default_factory=list)


class HealthMetricsCollector:
    """Coordinate metric sources, aggregation and persistence."""

    def __init__(
        self,
        sources: Optional[Mapping[MetricSourceType, MetricSource]] = None,
        sinks: Optional[Iterable[MetricSink]] = None,
    ) -> None:
        self.sources: Dict[MetricSourceType, MetricSource] = (
            dict(sources) if sources is not None else {MetricSourceType.SYSTEM: SystemMetricsAdapter()}
        )
        self.sinks: List[MetricSink] = list(sinks) if sinks is not None else [InMemoryMetricSink()]
        self.aggregator = MetricAggregator()

    def collect_metrics_on_demand(self, source_type: MetricSourceType) -> MetricCollectionResult:
        """Collect metrics from a specific source and persist the aggregated summary."""

        source = self.sources.get(source_type)
        collection_time = datetime.now()
        if source is None:
            return MetricCollectionResult(
                success=False,
                metrics=[],
                collection_time=collection_time,
                errors=[f"No source registered for {source_type.value}"]
            )

        metrics = list(source.collect())
        self.aggregator.add(metrics)
        summary = self.aggregator.summary()
        for sink in self.sinks:
            sink.persist(summary)

        return MetricCollectionResult(success=True, metrics=metrics, collection_time=collection_time)

    def get_metrics_summary(self) -> Dict[str, float]:
        """Return aggregated metrics."""

        return self.aggregator.summary()

    def run_smoke_test(self) -> bool:
        """Basic sanity check used in legacy tests."""

        try:
            result = self.collect_metrics_on_demand(MetricSourceType.SYSTEM)
            summary = self.get_metrics_summary()
            return result.success and bool(summary)
        except Exception:
            return False

    def shutdown(self) -> None:
        """Placeholder for interface compatibility."""

        # No resources to cleanup in current implementation
        return None

