"""
Vector Integration Data Models - V2 Compliant Module
===================================================

Data models for vector integration analytics system.
Extracted from vector_integration_models.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .enums import (
    AlertLevel,
    TrendDirection,
    RecommendationCategory,
    RecommendationPriority,
    ImplementationEffort,
)


@dataclass
class PerformanceAlert:
    """Performance alert data structure."""

    alert_id: str
    level: AlertLevel
    message: str
    metric_name: str
    metric_value: float
    threshold: float
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate alert data after initialization."""
        if not self.alert_id or not self.message or not self.metric_name:
            raise ValueError("Alert ID, message, and metric name are required")
        if self.metric_value < 0 or self.threshold < 0:
            raise ValueError("Metric value and threshold must be non-negative")

    def is_critical(self) -> bool:
        """Check if alert is critical."""
        return self.level == AlertLevel.CRITICAL

    def is_resolved(self) -> bool:
        """Check if alert is resolved."""
        return self.resolved


@dataclass
class TrendAnalysis:
    """Trend analysis data structure."""

    analysis_id: str
    metric_name: str
    trend_direction: str  # "increasing", "decreasing", "stable", "volatile"
    trend_strength: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    data_points: int
    time_window: timedelta
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate trend analysis data after initialization."""
        if not 0.0 <= self.trend_strength <= 1.0:
            raise ValueError("Trend strength must be between 0.0 and 1.0")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        if self.data_points <= 0:
            raise ValueError("Data points must be positive")

    def is_significant(self) -> bool:
        """Check if trend is statistically significant."""
        return self.confidence >= 0.7 and self.trend_strength >= 0.5


@dataclass
class PerformanceForecast:
    """Performance forecast data structure."""

    forecast_id: str
    metric_name: str
    predicted_values: List[float]
    forecast_horizon: timedelta
    confidence_interval: tuple  # (lower, upper)
    model_accuracy: float  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(
        default_factory=lambda: datetime.now() + timedelta(hours=24)
    )
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate forecast data after initialization."""
        if not 0.0 <= self.model_accuracy <= 1.0:
            raise ValueError("Model accuracy must be between 0.0 and 1.0")
        if len(self.confidence_interval) != 2:
            raise ValueError("Confidence interval must be a tuple of (lower, upper)")

    def is_expired(self) -> bool:
        """Check if forecast has expired."""
        return datetime.now() > self.expires_at


@dataclass
class OptimizationRecommendation:
    """Optimization recommendation."""

    recommendation_id: str
    category: str  # "performance", "resource", "configuration", "architecture"
    priority: str  # "low", "medium", "high", "critical"
    title: str
    description: str
    expected_impact: str
    implementation_effort: str  # "low", "medium", "high"
    estimated_improvement: float  # percentage improvement expected
    timestamp: datetime = field(default_factory=datetime.now)
    implemented: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate recommendation data after initialization."""
        valid_categories = ["performance", "resource", "configuration", "architecture"]
        if self.category not in valid_categories:
            raise ValueError(f"Category must be one of: {valid_categories}")

        valid_priorities = ["low", "medium", "high", "critical"]
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of: {valid_priorities}")

        valid_efforts = ["low", "medium", "high"]
        if self.implementation_effort not in valid_efforts:
            raise ValueError(f"Implementation effort must be one of: {valid_efforts}")


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure."""

    metric_name: str
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate metrics data after initialization."""
        if not self.metric_name or not self.unit:
            raise ValueError("Metric name and unit are required")

    def is_valid(self) -> bool:
        """Check if metric is valid."""
        return self.value >= 0 and bool(self.metric_name) and bool(self.unit)
