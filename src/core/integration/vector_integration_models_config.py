#!/usr/bin/env python3
"""
Vector Integration Models Config - V2 Compliance Module
======================================================

Configuration classes for vector integration analytics system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import Any, Dict
from dataclasses import dataclass
from .vector_integration_models_core import AnalyticsMode


@dataclass
class IntegrationConfig:
    """Configuration for vector integration analytics."""
    
    # Core settings
    analytics_mode: AnalyticsMode = AnalyticsMode.HYBRID
    monitoring_interval: float = 1.0  # seconds
    data_retention_hours: int = 168  # 1 week
    alert_threshold_multiplier: float = 2.0
    
    # Feature flags
    enable_real_time_monitoring: bool = True
    enable_trend_analysis: bool = True
    enable_forecasting: bool = True
    enable_alerting: bool = True
    enable_recommendations: bool = True
    enable_visualization: bool = False  # Requires matplotlib
    
    # Performance thresholds
    response_time_threshold_ms: float = 100.0
    throughput_threshold_ops_sec: float = 1000.0
    error_rate_threshold_percent: float = 1.0
    memory_usage_threshold_percent: float = 80.0
    cpu_usage_threshold_percent: float = 70.0
    
    # Alert settings
    alert_cooldown_minutes: int = 5
    max_alerts_per_hour: int = 100
    critical_alert_immediate: bool = True
    
    # Forecasting settings
    forecast_horizon_hours: int = 24
    min_data_points_for_forecast: int = 100
    forecast_confidence_threshold: float = 0.7
    
    # Trend analysis settings
    trend_window_hours: int = 4
    min_trend_confidence: float = 0.6
    trend_significance_threshold: float = 0.1
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        if self.monitoring_interval < 0.1:
            raise ValueError("Monitoring interval must be at least 0.1 seconds")
        if self.data_retention_hours < 1:
            raise ValueError("Data retention must be at least 1 hour")
        if not 0.0 <= self.alert_threshold_multiplier <= 10.0:
            raise ValueError("Alert threshold multiplier must be between 0.0 and 10.0")
        if self.response_time_threshold_ms < 1.0:
            raise ValueError("Response time threshold must be at least 1.0 ms")
        if self.throughput_threshold_ops_sec < 1.0:
            raise ValueError("Throughput threshold must be at least 1.0 ops/sec")
        if not 0.0 <= self.error_rate_threshold_percent <= 100.0:
            raise ValueError("Error rate threshold must be between 0.0 and 100.0")
        if not 0.0 <= self.memory_usage_threshold_percent <= 100.0:
            raise ValueError("Memory usage threshold must be between 0.0 and 100.0")
        if not 0.0 <= self.cpu_usage_threshold_percent <= 100.0:
            raise ValueError("CPU usage threshold must be between 0.0 and 100.0")
        if self.alert_cooldown_minutes < 1:
            raise ValueError("Alert cooldown must be at least 1 minute")
        if self.max_alerts_per_hour < 1:
            raise ValueError("Max alerts per hour must be at least 1")
        if self.forecast_horizon_hours < 1:
            raise ValueError("Forecast horizon must be at least 1 hour")
        if self.min_data_points_for_forecast < 10:
            raise ValueError("Min data points for forecast must be at least 10")
        if not 0.0 <= self.forecast_confidence_threshold <= 1.0:
            raise ValueError("Forecast confidence threshold must be between 0.0 and 1.0")
        if self.trend_window_hours < 1:
            raise ValueError("Trend window must be at least 1 hour")
        if not 0.0 <= self.min_trend_confidence <= 1.0:
            raise ValueError("Min trend confidence must be between 0.0 and 1.0")
        if not 0.0 <= self.trend_significance_threshold <= 1.0:
            raise ValueError("Trend significance threshold must be between 0.0 and 1.0")
        return True
