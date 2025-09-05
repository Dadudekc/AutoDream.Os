"""
Vector Integration Config Models - V2 Compliant Module
=====================================================

Configuration models for vector integration analytics system.
Extracted from vector_integration_models.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .enums import AnalyticsMode


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
        try:
            # Validate core settings
            if self.monitoring_interval <= 0:
                raise ValueError("Monitoring interval must be positive")
            if self.data_retention_hours <= 0:
                raise ValueError("Data retention hours must be positive")
            if self.alert_threshold_multiplier <= 0:
                raise ValueError("Alert threshold multiplier must be positive")
            
            # Validate thresholds
            if not 0 <= self.response_time_threshold_ms <= 10000:
                raise ValueError("Response time threshold must be between 0 and 10000 ms")
            if not 0 <= self.throughput_threshold_ops_sec <= 100000:
                raise ValueError("Throughput threshold must be between 0 and 100000 ops/sec")
            if not 0 <= self.error_rate_threshold_percent <= 100:
                raise ValueError("Error rate threshold must be between 0 and 100%")
            if not 0 <= self.memory_usage_threshold_percent <= 100:
                raise ValueError("Memory usage threshold must be between 0 and 100%")
            if not 0 <= self.cpu_usage_threshold_percent <= 100:
                raise ValueError("CPU usage threshold must be between 0 and 100%")
            
            # Validate alert settings
            if self.alert_cooldown_minutes < 0:
                raise ValueError("Alert cooldown must be non-negative")
            if self.max_alerts_per_hour <= 0:
                raise ValueError("Max alerts per hour must be positive")
            
            # Validate forecasting settings
            if self.forecast_horizon_hours <= 0:
                raise ValueError("Forecast horizon must be positive")
            if self.min_data_points_for_forecast <= 0:
                raise ValueError("Min data points for forecast must be positive")
            if not 0 <= self.forecast_confidence_threshold <= 1:
                raise ValueError("Forecast confidence threshold must be between 0 and 1")
            
            # Validate trend analysis settings
            if self.trend_window_hours <= 0:
                raise ValueError("Trend window must be positive")
            if not 0 <= self.min_trend_confidence <= 1:
                raise ValueError("Min trend confidence must be between 0 and 1")
            if not 0 <= self.trend_significance_threshold <= 1:
                raise ValueError("Trend significance threshold must be between 0 and 1")
            
            return True
            
        except ValueError:
            return False
    
    def get_performance_thresholds(self) -> Dict[str, float]:
        """Get performance thresholds as dictionary."""
        return {
            'response_time_ms': self.response_time_threshold_ms,
            'throughput_ops_sec': self.throughput_threshold_ops_sec,
            'error_rate_percent': self.error_rate_threshold_percent,
            'memory_usage_percent': self.memory_usage_threshold_percent,
            'cpu_usage_percent': self.cpu_usage_threshold_percent
        }
    
    def get_alert_settings(self) -> Dict[str, Any]:
        """Get alert settings as dictionary."""
        return {
            'cooldown_minutes': self.alert_cooldown_minutes,
            'max_alerts_per_hour': self.max_alerts_per_hour,
            'critical_immediate': self.critical_alert_immediate,
            'threshold_multiplier': self.alert_threshold_multiplier
        }
    
    def get_forecasting_settings(self) -> Dict[str, Any]:
        """Get forecasting settings as dictionary."""
        return {
            'horizon_hours': self.forecast_horizon_hours,
            'min_data_points': self.min_data_points_for_forecast,
            'confidence_threshold': self.forecast_confidence_threshold
        }
    
    def get_trend_analysis_settings(self) -> Dict[str, Any]:
        """Get trend analysis settings as dictionary."""
        return {
            'window_hours': self.trend_window_hours,
            'min_confidence': self.min_trend_confidence,
            'significance_threshold': self.trend_significance_threshold
        }
    
    def get_feature_flags(self) -> Dict[str, bool]:
        """Get feature flags as dictionary."""
        return {
            'real_time_monitoring': self.enable_real_time_monitoring,
            'trend_analysis': self.enable_trend_analysis,
            'forecasting': self.enable_forecasting,
            'alerting': self.enable_alerting,
            'recommendations': self.enable_recommendations,
            'visualization': self.enable_visualization
        }
    
    def update_threshold(self, metric_name: str, value: float) -> bool:
        """Update performance threshold."""
        threshold_map = {
            'response_time': 'response_time_threshold_ms',
            'throughput': 'throughput_threshold_ops_sec',
            'error_rate': 'error_rate_threshold_percent',
            'memory_usage': 'memory_usage_threshold_percent',
            'cpu_usage': 'cpu_usage_threshold_percent'
        }
        
        if metric_name in threshold_map:
            setattr(self, threshold_map[metric_name], value)
            return self.validate()
        return False
