#!/usr/bin/env python3
"""
Vector Integration Models Utils - V2 Compliance Module
=====================================================

Utility functions and factory methods for vector integration analytics system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import List
from datetime import timedelta
from .vector_integration_models_core import (
    PerformanceAlert,
    TrendAnalysis,
    PerformanceForecast,
    OptimizationRecommendation,
    AlertLevel
)
from .vector_integration_models_config import IntegrationConfig


# Constants
ALERT_LEVELS = ["info", "warning", "error", "critical"]
TREND_DIRECTIONS = ["increasing", "decreasing", "stable"]
RECOMMENDATION_CATEGORIES = ["performance", "resource", "configuration", "architecture"]
RECOMMENDATION_PRIORITIES = ["low", "medium", "high", "critical"]
IMPLEMENTATION_EFFORTS = ["low", "medium", "high"]


# Validation functions
def validate_performance_alert(alert: PerformanceAlert) -> bool:
    """Validate performance alert."""
    try:
        alert.__post_init__()
        return True
    except ValueError:
        return False


def validate_trend_analysis(trend: TrendAnalysis) -> bool:
    """Validate trend analysis."""
    try:
        trend.__post_init__()
        return True
    except ValueError:
        return False


def validate_performance_forecast(forecast: PerformanceForecast) -> bool:
    """Validate performance forecast."""
    try:
        forecast.__post_init__()
        return True
    except ValueError:
        return False


def validate_optimization_recommendation(recommendation: OptimizationRecommendation) -> bool:
    """Validate optimization recommendation."""
    try:
        recommendation.__post_init__()
        return True
    except ValueError:
        return False


def validate_integration_config(config: IntegrationConfig) -> bool:
    """Validate integration configuration."""
    return config.validate()


# Factory functions
def create_default_config() -> IntegrationConfig:
    """Create default integration analytics configuration."""
    return IntegrationConfig()


def create_performance_alert(alert_id: str, level: AlertLevel, message: str,
                           metric_name: str, metric_value: float, threshold: float) -> PerformanceAlert:
    """Create performance alert with validation."""
    alert = PerformanceAlert(
        alert_id=alert_id,
        level=level,
        message=message,
        metric_name=metric_name,
        metric_value=metric_value,
        threshold=threshold
    )
    if not validate_performance_alert(alert):
        raise ValueError("Invalid performance alert data")
    return alert


def create_trend_analysis(analysis_id: str, metric_name: str, trend_direction: str,
                         trend_strength: float, confidence: float, data_points: int,
                         time_window: timedelta) -> TrendAnalysis:
    """Create trend analysis with validation."""
    trend = TrendAnalysis(
        analysis_id=analysis_id,
        metric_name=metric_name,
        trend_direction=trend_direction,
        trend_strength=trend_strength,
        confidence=confidence,
        data_points=data_points,
        time_window=time_window
    )
    if not validate_trend_analysis(trend):
        raise ValueError("Invalid trend analysis data")
    return trend


def create_performance_forecast(forecast_id: str, metric_name: str, predicted_values: List[float],
                              forecast_horizon: timedelta, confidence_interval: tuple,
                              model_accuracy: float) -> PerformanceForecast:
    """Create performance forecast with validation."""
    forecast = PerformanceForecast(
        forecast_id=forecast_id,
        metric_name=metric_name,
        predicted_values=predicted_values,
        forecast_horizon=forecast_horizon,
        confidence_interval=confidence_interval,
        model_accuracy=model_accuracy
    )
    if not validate_performance_forecast(forecast):
        raise ValueError("Invalid performance forecast data")
    return forecast


def create_optimization_recommendation(recommendation_id: str, category: str, priority: str,
                                     title: str, description: str, expected_impact: str,
                                     implementation_effort: str, estimated_improvement: float) -> OptimizationRecommendation:
    """Create optimization recommendation with validation."""
    recommendation = OptimizationRecommendation(
        recommendation_id=recommendation_id,
        category=category,
        priority=priority,
        title=title,
        description=description,
        expected_impact=expected_impact,
        implementation_effort=implementation_effort,
        estimated_improvement=estimated_improvement
    )
    if not validate_optimization_recommendation(recommendation):
        raise ValueError("Invalid optimization recommendation data")
    return recommendation
