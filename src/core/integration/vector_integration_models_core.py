#!/usr/bin/env python3
"""
Vector Integration Models Core - V2 Compliance Module
====================================================

Core data models for vector integration analytics system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


class AnalyticsMode(Enum):
    """Analytics modes."""
    REAL_TIME = "real_time"
    BATCH = "batch"
    HYBRID = "hybrid"
    SCHEDULED = "scheduled"


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


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
        if not self.alert_id or not self.message:
            raise ValueError("Alert ID and message are required")
        if not isinstance(self.level, AlertLevel):
            raise ValueError("Alert level must be an AlertLevel enum")


@dataclass  
class TrendAnalysis:
    """Trend analysis result."""
    analysis_id: str
    metric_name: str
    trend_direction: str  # "increasing", "decreasing", "stable"
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
        if self.trend_direction not in ["increasing", "decreasing", "stable"]:
            raise ValueError("Trend direction must be increasing, decreasing, or stable")


@dataclass
class PerformanceForecast:
    """Performance forecast result."""
    forecast_id: str
    metric_name: str
    predicted_values: List[float]
    forecast_horizon: timedelta
    confidence_interval: tuple  # (lower, upper)
    model_accuracy: float
    timestamp: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=24))
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
