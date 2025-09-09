"""
Forecast Generator - V2 Compliant Module
=======================================

Handles performance forecasting and prediction for vector integration.
Extracted from vector_integration_analytics_engine.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import logging
import statistics
from datetime import datetime, timedelta
from typing import Any

from ..vector_integration_models import (
    PerformanceForecast,
    PerformanceMetrics,
    create_performance_forecast,
)


class ForecastGenerator:
    """Generator for performance forecasting and prediction.

    Provides forecasting capabilities using various statistical methods.
    """

    def __init__(self, config):
        """Initialize forecast generator."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.forecast_cache: dict[str, PerformanceForecast] = {}

    def generate_forecast(
        self, metrics_data: list[PerformanceMetrics], metric_name: str
    ) -> PerformanceForecast | None:
        """Generate performance forecast for metric."""
        try:
            # Filter and prepare data
            metric_values = [m.value for m in metrics_data if m.metric_name == metric_name]

            if len(metric_values) < self.config.min_data_points_for_forecast:
                return None

            # Generate forecast
            forecast_values, confidence_interval, model_accuracy = self._generate_simple_forecast(
                metric_values
            )

            # Create forecast
            forecast_id = f"forecast_{metric_name}_{int(datetime.now().timestamp())}"
            forecast_horizon = timedelta(hours=self.config.forecast_horizon_hours)

            forecast = create_performance_forecast(
                forecast_id=forecast_id,
                metric_name=metric_name,
                predicted_values=forecast_values,
                forecast_horizon=forecast_horizon,
                confidence_interval=confidence_interval,
                model_accuracy=model_accuracy,
            )

            # Cache the result
            self.forecast_cache[metric_name] = forecast

            self.logger.debug(
                f"Forecast generated for {metric_name} with accuracy {model_accuracy:.2f}"
            )
            return forecast

        except Exception as e:
            self.logger.error(f"Error generating forecast for {metric_name}: {e}")
            return None

    def _generate_simple_forecast(
        self, values: list[float]
    ) -> tuple[list[float], tuple[float, float], float]:
        """Generate simple linear forecast."""
        if len(values) < 10:
            # Not enough data for reliable forecast
            last_value = values[-1] if values else 0.0
            forecast_values = [last_value] * 24  # 24 hour forecast
            confidence_interval = (last_value * 0.9, last_value * 1.1)
            model_accuracy = 0.5
            return forecast_values, confidence_interval, model_accuracy

        # Calculate simple linear trend
        recent_window = min(len(values), 50)  # Use last 50 points
        recent_values = values[-recent_window:]

        # Calculate trend
        x_values = list(range(len(recent_values)))
        mean_x = statistics.mean(x_values)
        mean_y = statistics.mean(recent_values)

        # Simple linear regression
        numerator = sum(
            (x - mean_x) * (y - mean_y) for x, y in zip(x_values, recent_values, strict=False)
        )
        denominator = sum((x - mean_x) ** 2 for x in x_values)

        if denominator == 0:
            # No trend, use last value
            last_value = recent_values[-1]
            forecast_values = [last_value] * 24
            confidence_interval = (last_value * 0.9, last_value * 1.1)
            model_accuracy = 0.6
            return forecast_values, confidence_interval, model_accuracy

        slope = numerator / denominator
        intercept = mean_y - slope * mean_x

        # Generate forecast values
        forecast_hours = 24
        forecast_values = []
        for i in range(forecast_hours):
            x = len(recent_values) + i
            predicted_value = slope * x + intercept
            forecast_values.append(max(0, predicted_value))  # Ensure non-negative

        # Calculate confidence interval
        residuals = [
            y - (slope * x + intercept) for x, y in zip(x_values, recent_values, strict=False)
        ]
        residual_std = statistics.stdev(residuals) if len(residuals) > 1 else 0

        # 95% confidence interval
        margin_of_error = 1.96 * residual_std
        last_forecast = forecast_values[-1]
        confidence_interval = (
            max(0, last_forecast - margin_of_error),
            last_forecast + margin_of_error,
        )

        # Calculate model accuracy (R-squared)
        ss_res = sum(r**2 for r in residuals)
        ss_tot = sum((y - mean_y) ** 2 for y in recent_values)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        model_accuracy = max(0, min(1, r_squared))

        return forecast_values, confidence_interval, model_accuracy

    def generate_multi_metric_forecast(
        self, metrics_data: list[PerformanceMetrics]
    ) -> dict[str, PerformanceForecast]:
        """Generate forecasts for multiple metrics."""
        forecasts = {}

        # Group metrics by name
        metrics_by_name = {}
        for metric in metrics_data:
            if metric.metric_name not in metrics_by_name:
                metrics_by_name[metric.metric_name] = []
            metrics_by_name[metric.metric_name].append(metric)

        # Generate forecast for each metric
        for metric_name, metric_list in metrics_by_name.items():
            forecast = self.generate_forecast(metric_list, metric_name)
            if forecast:
                forecasts[metric_name] = forecast

        return forecasts

    def validate_forecast_accuracy(
        self, forecast: PerformanceForecast, actual_values: list[float]
    ) -> float:
        """Validate forecast accuracy against actual values."""
        if not actual_values or len(actual_values) == 0:
            return 0.0

        predicted_values = forecast.predicted_values
        min_length = min(len(predicted_values), len(actual_values))

        if min_length == 0:
            return 0.0

        # Calculate mean absolute percentage error (MAPE)
        errors = []
        for i in range(min_length):
            if actual_values[i] != 0:
                error = abs(predicted_values[i] - actual_values[i]) / actual_values[i]
                errors.append(error)

        if not errors:
            return 0.0

        mape = statistics.mean(errors)
        accuracy = max(0, 1 - mape)  # Convert MAPE to accuracy
        return min(1.0, accuracy)

    def get_forecast_summary(self, forecasts: dict[str, PerformanceForecast]) -> dict[str, Any]:
        """Get summary of all forecasts."""
        summary = {
            "total_forecasts": len(forecasts),
            "metrics": {},
            "overall_accuracy": 0.0,
        }

        if not forecasts:
            return summary

        accuracies = []
        for metric_name, forecast in forecasts.items():
            metric_summary = {
                "forecast_id": forecast.forecast_id,
                "predicted_values_count": len(forecast.predicted_values),
                "model_accuracy": forecast.model_accuracy,
                "confidence_interval": forecast.confidence_interval,
                "forecast_horizon_hours": (forecast.forecast_horizon.total_seconds() / 3600),
            }
            summary["metrics"][metric_name] = metric_summary
            accuracies.append(forecast.model_accuracy)

        summary["overall_accuracy"] = statistics.mean(accuracies) if accuracies else 0.0
        return summary

    def get_cached_forecasts(self) -> dict[str, PerformanceForecast]:
        """Get cached forecasts."""
        return dict(self.forecast_cache)

    def clear_forecast_cache(self):
        """Clear forecast cache."""
        self.forecast_cache.clear()
        self.logger.info("Forecast cache cleared")
