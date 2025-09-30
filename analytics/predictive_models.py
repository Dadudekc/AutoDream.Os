#!/usr/bin/env python3
"""
Predictive Analytics Models
===========================

Data models for predictive analytics engine.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


@dataclass
class PerformanceMetrics:
    """System performance metrics for prediction models."""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_io: float
    network_io: float
    response_time: float
    throughput: float
    error_rate: float
    active_connections: int


@dataclass
class PredictionResult:
    """Result of a predictive analysis."""
    metric_name: str
    predicted_value: float
    confidence: float
    time_horizon: timedelta
    trend: str  # "increasing", "decreasing", "stable"
    anomaly_score: float
    recommendations: List[str] = field(default_factory=list)


@dataclass
class CapacityForecast:
    """Capacity planning forecast."""
    resource_type: str
    current_usage: float
    predicted_usage: float
    capacity_limit: float
    utilization_percentage: float
    time_to_limit: timedelta
    scaling_recommendation: str


@dataclass
class AnomalyDetection:
    """Anomaly detection result."""
    metric_name: str
    anomaly_score: float
    severity: str  # "low", "medium", "high", "critical"
    detected_at: datetime
    description: str
    suggested_action: str


@dataclass
class PredictiveModel:
    """Predictive model configuration."""
    model_name: str
    model_type: str
    accuracy: float
    training_data_size: int
    last_trained: datetime
    parameters: Dict[str, Any]


@dataclass
class ForecastPeriod:
    """Forecast time period."""
    start_time: datetime
    end_time: datetime
    interval: timedelta
    data_points: List[PerformanceMetrics]


@dataclass
class SystemHealth:
    """System health assessment."""
    overall_health: str  # "healthy", "warning", "critical"
    health_score: float
    issues: List[str]
    recommendations: List[str]
    last_updated: datetime


@dataclass
class ResourceUtilization:
    """Resource utilization metrics."""
    resource_name: str
    current_utilization: float
    peak_utilization: float
    average_utilization: float
    utilization_trend: str
    efficiency_score: float
