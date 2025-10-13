"""
Predictive Modeling Forecasters
================================

Forecasting methods for time-series prediction.

Extracted from: predictive_modeling_engine.py (V2 compliance refactor)
Author: Agent-5 (Business Intelligence Specialist)
Refactored by: Agent-6 (VSCode Forking & Quality Gates)
License: MIT
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class PredictiveModelingForecasters:
    """Implements time-series forecasting methods."""

    def __init__(self, forecast_horizon: int, alpha: float, moving_avg_window: int):
        """
        Initialize forecasting parameters.
        
        Args:
            forecast_horizon: Number of periods to forecast
            alpha: Smoothing factor for exponential smoothing
            moving_avg_window: Window size for moving average
        """
        self.forecast_horizon = forecast_horizon
        self.alpha = alpha
        self.moving_avg_window = moving_avg_window
        self.logger = logger

    def forecast_moving_average(self, data: list[float]) -> dict[str, Any]:
        """
        Forecast using moving average method.
        
        Args:
            data: Historical data
            
        Returns:
            Forecast results
        """
        if len(data) < self.moving_avg_window:
            return {"error": "Insufficient data for moving average"}

        try:
            # Calculate last moving average
            last_window = data[-self.moving_avg_window :]
            last_ma = sum(last_window) / len(last_window)

            # Simple forecast: repeat last MA
            forecast_values = [round(last_ma, 3)] * self.forecast_horizon

            return {
                "status": "complete",
                "method": "moving_average",
                "window_size": self.moving_avg_window,
                "forecast": forecast_values,
                "last_actual": data[-1],
            }

        except Exception as e:
            self.logger.error(f"Error in moving average forecast: {e}")
            return {"status": "error", "error": str(e)}

    def forecast_exponential_smoothing(self, data: list[float]) -> dict[str, Any]:
        """
        Forecast using exponential smoothing method.
        
        Args:
            data: Historical data
            
        Returns:
            Forecast results
        """
        if len(data) < 2:
            return {"error": "Insufficient data for exponential smoothing"}

        try:
            # Calculate smoothed values
            smoothed = [data[0]]  # Initialize with first value

            for i in range(1, len(data)):
                smooth_value = self.alpha * data[i] + (1 - self.alpha) * smoothed[-1]
                smoothed.append(smooth_value)

            # Forecast using last smoothed value
            last_smoothed = smoothed[-1]
            forecast_values = [round(last_smoothed, 3)] * self.forecast_horizon

            return {
                "status": "complete",
                "method": "exponential_smoothing",
                "alpha": self.alpha,
                "forecast": forecast_values,
                "last_smoothed": round(last_smoothed, 3),
                "last_actual": data[-1],
            }

        except Exception as e:
            self.logger.error(f"Error in exponential smoothing: {e}")
            return {"status": "error", "error": str(e)}

    def forecast_linear_trend(self, data: list[float]) -> dict[str, Any]:
        """
        Forecast using linear trend extrapolation.
        
        Args:
            data: Historical data
            
        Returns:
            Forecast results
        """
        if len(data) < 2:
            return {"error": "Insufficient data for linear trend"}

        try:
            # Calculate linear regression coefficients
            n = len(data)
            x_mean = (n - 1) / 2
            y_mean = sum(data) / n

            numerator = sum((i - x_mean) * (data[i] - y_mean) for i in range(n))
            denominator = sum((i - x_mean) ** 2 for i in range(n))

            if denominator == 0:
                slope = 0
                intercept = y_mean
            else:
                slope = numerator / denominator
                intercept = y_mean - slope * x_mean

            # Generate forecast
            forecast_values = []
            for i in range(self.forecast_horizon):
                forecast_point = intercept + slope * (n + i)
                forecast_values.append(round(forecast_point, 3))

            return {
                "status": "complete",
                "method": "linear_trend",
                "slope": round(slope, 6),
                "intercept": round(intercept, 3),
                "forecast": forecast_values,
                "trend_direction": "increasing" if slope > 0 else "decreasing",
            }

        except Exception as e:
            self.logger.error(f"Error in linear trend forecast: {e}")
            return {"status": "error", "error": str(e)}

