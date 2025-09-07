"""Data models and handlers for baseline measurements."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from .constants import DEFAULT_BASELINE_CONFIG


class BaselineType(Enum):
    """Types of performance baselines."""

    PERFORMANCE = "performance"
    QUALITY = "quality"
    EFFICIENCY = "efficiency"
    COMPOSITE = "composite"
    CUSTOM = "custom"


class BaselineStatus(Enum):
    """Baseline status indicators."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    CALIBRATING = "calibrating"
    VALIDATING = "validating"
    ERROR = "error"


@dataclass
class BaselineMetric:
    """Individual baseline metric definition."""

    name: str
    value: float
    unit: str
    min_threshold: Optional[float] = None
    max_threshold: Optional[float] = None
    target_value: Optional[float] = None
    weight: float = 1.0
    description: str = ""


@dataclass
class PerformanceBaseline:
    """Comprehensive performance baseline definition."""

    baseline_id: str
    name: str
    description: str
    baseline_type: BaselineType
    status: BaselineStatus
    version: str
    created_at: datetime
    updated_at: datetime
    metrics: Dict[str, BaselineMetric]
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    confidence_score: float = 1.0
    sample_size: int = 0
    validity_period_days: int = 30


@dataclass
class BaselineComparison:
    """Result of comparing current metrics against a baseline."""

    baseline_id: str
    comparison_timestamp: datetime
    overall_score: float
    metric_comparisons: Dict[str, Dict[str, Any]]
    improvements: List[str]
    regressions: List[str]
    recommendations: List[str]
    confidence_level: str


@dataclass
class BaselineTrend:
    """Trend analysis for baseline metrics over time."""

    metric_name: str
    time_period: str
    trend_direction: str
    trend_strength: float
    data_points: List[Any]
    forecast: Optional[float] = None


class BaselineDataHandler:
    """Manage creation and lifecycle of performance baselines."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.baseline_config: Dict[str, Any] = DEFAULT_BASELINE_CONFIG.copy()
        if config:
            self.baseline_config.update(config)
        self.baselines: List[PerformanceBaseline] = []

    def create_baseline(
        self,
        name: str,
        description: str,
        baseline_type: BaselineType,
        metrics: Dict[str, BaselineMetric],
        version: str = "1.0.0",
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """Create a new performance baseline and return its identifier."""

        baseline_id = (
            f"baseline_{baseline_type.value}_{int(datetime.now().timestamp())}"
        )
        retention = self.baseline_config["baseline_retention_days"]
        baseline = PerformanceBaseline(
            baseline_id=baseline_id,
            name=name,
            description=description,
            baseline_type=baseline_type,
            status=BaselineStatus.ACTIVE,
            version=version,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metrics=metrics,
            context=context or {},
            tags=tags or [],
            confidence_score=1.0,
            sample_size=0,
            validity_period_days=retention,
        )
        self._manage_baseline_limits(baseline_type)
        self.baselines.append(baseline)
        return baseline_id

    def _manage_baseline_limits(self, baseline_type: BaselineType) -> None:
        """Ensure baselines per type do not exceed configuration."""

        type_baselines = [
            b for b in self.baselines if b.baseline_type == baseline_type
        ]  # noqa: E501
        max_baselines = self.baseline_config["max_baselines_per_type"]
        if len(type_baselines) >= max_baselines:
            oldest = min(type_baselines, key=lambda x: x.created_at)
            oldest.status = BaselineStatus.DEPRECATED

    def update_baseline(
        self,
        baseline_id: str,
        updates: Dict[str, Any],
    ) -> bool:
        """Update an existing baseline with provided values."""

        baseline = self.get_baseline(baseline_id)
        if not baseline:
            return False
        for field_name, value in updates.items():
            if hasattr(baseline, field_name):
                setattr(baseline, field_name, value)
        baseline.updated_at = datetime.now()
        return True

    def deprecate_baseline(self, baseline_id: str) -> bool:
        """Mark a baseline as deprecated."""

        baseline = self.get_baseline(baseline_id)
        if not baseline:
            return False
        baseline.status = BaselineStatus.DEPRECATED
        baseline.updated_at = datetime.now()
        return True

    def get_baseline(self, baseline_id: str) -> Optional[PerformanceBaseline]:
        """Retrieve a baseline by its identifier."""

        return next(
            (b for b in self.baselines if b.baseline_id == baseline_id),
            None,
        )

    def get_baselines_by_type(
        self, baseline_type: BaselineType
    ) -> List[PerformanceBaseline]:
        """Return all active baselines of a specific type."""

        return [
            b
            for b in self.baselines
            if (
                b.baseline_type == baseline_type
                and b.status == BaselineStatus.ACTIVE  # noqa: E501
            )
        ]

    def get_active_baselines(self) -> List[PerformanceBaseline]:
        """Return all active baselines."""

        return [b for b in self.baselines if b.status == BaselineStatus.ACTIVE]


__all__ = [
    "BaselineType",
    "BaselineStatus",
    "BaselineMetric",
    "PerformanceBaseline",
    "BaselineComparison",
    "BaselineTrend",
    "BaselineDataHandler",
]
