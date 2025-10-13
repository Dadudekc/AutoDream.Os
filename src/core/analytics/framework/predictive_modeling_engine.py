"""
Module: Predictive Modeling Engine
Responsibilities: Advanced forecasting models coordination

Implements time-series forecasting using statistical methods:
- Moving average forecasting
- Exponential smoothing
- Linear trend extrapolation
- Seasonal decomposition

Refactored into modular components for V2 compliance:
- predictive_modeling_forecasters.py: Forecasting methods
- predictive_modeling_metrics.py: Ensemble and accuracy
- predictive_modeling_seasonality.py: Seasonal detection

Author: Agent-5 (Business Intelligence Specialist)
Refactored by: Agent-6 (VSCode Forking & Quality Gates)
License: MIT
"""

import logging
from datetime import datetime
from typing import Any

from .predictive_modeling_forecasters import PredictiveModelingForecasters
from .predictive_modeling_metrics import PredictiveModelingMetrics
from .predictive_modeling_seasonality import PredictiveModelingSeasonality

logger = logging.getLogger(__name__)


class PredictiveModelingEngine:
    """
    Implements time-series and forecasting models.
    
    Coordinates forecasting methods, ensemble calculations,
    and seasonal pattern detection without external dependencies.
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """
        Initialize forecasting models.
        
        Args:
            config: Optional configuration with:
                   - forecast_horizon: int (default 5)
                   - alpha: float for exponential smoothing (default 0.3)
                   - moving_avg_window: int (default 3)
        """
        self.config = config or {}
        self.logger = logger
        self.forecast_horizon = self.config.get("forecast_horizon", 5)
        self.alpha = self.config.get("alpha", 0.3)
        self.moving_avg_window = self.config.get("moving_avg_window", 3)

        # Initialize component modules
        self.forecasters = PredictiveModelingForecasters(
            self.forecast_horizon, self.alpha, self.moving_avg_window
        )
        self.metrics = PredictiveModelingMetrics(self.forecast_horizon)
        self.seasonality = PredictiveModelingSeasonality()

    def forecast(self, data: Any) -> dict[str, Any]:
        """
        Generate forecast based on historical data.
        
        Args:
            data: Historical time series data (list of numbers)
            
        Returns:
            Dictionary containing forecasts from multiple methods
        """
        try:
            if not data:
                return {"error": "No data provided"}

            if not isinstance(data, list):
                return {"error": "Data must be a list"}

            # Convert to numeric if possible
            numeric_data = self._convert_to_numeric(data)

            if not numeric_data or len(numeric_data) < 2:
                return {"error": "Insufficient numeric data for forecasting"}

            forecasts = {
                "timestamp": datetime.now().isoformat(),
                "historical_data_points": len(numeric_data),
                "forecast_horizon": self.forecast_horizon,
                "methods": {},
            }

            # Apply multiple forecasting methods via forecasters module
            forecasts["methods"]["moving_average"] = (
                self.forecasters.forecast_moving_average(numeric_data)
            )
            forecasts["methods"]["exponential_smoothing"] = (
                self.forecasters.forecast_exponential_smoothing(numeric_data)
            )
            forecasts["methods"]["linear_trend"] = (
                self.forecasters.forecast_linear_trend(numeric_data)
            )

            # Calculate ensemble forecast via metrics module
            forecasts["ensemble"] = self.metrics.calculate_ensemble(
                forecasts["methods"]
            )

            return forecasts

        except Exception as e:
            self.logger.error(f"Error generating forecast: {e}")
            return {"error": str(e)}

    def _convert_to_numeric(self, data: Any) -> list[float]:
        """Convert data to numeric list."""
        if not isinstance(data, list):
            return []
        numeric_data = []
        for item in data:
            if isinstance(item, (int, float)):
                numeric_data.append(float(item))
            elif (
                isinstance(item, dict)
                and "value" in item
                and isinstance(item["value"], (int, float))
            ):
                numeric_data.append(float(item["value"]))
        return numeric_data

    # Delegate to component modules
    def forecast_moving_average(self, data: list[float]) -> dict[str, Any]:
        """Delegate to forecasters module."""
        return self.forecasters.forecast_moving_average(data)

    def forecast_exponential_smoothing(self, data: list[float]) -> dict[str, Any]:
        """Delegate to forecasters module."""
        return self.forecasters.forecast_exponential_smoothing(data)

    def forecast_linear_trend(self, data: list[float]) -> dict[str, Any]:
        """Delegate to forecasters module."""
        return self.forecasters.forecast_linear_trend(data)

    def detect_seasonality(
        self, data: list[float], period: int = 7
    ) -> dict[str, Any]:
        """Delegate to seasonality module."""
        return self.seasonality.detect_seasonality(data, period)

    def calculate_forecast_accuracy(
        self, actual: list[float], predicted: list[float]
    ) -> dict[str, float]:
        """Delegate to metrics module."""
        return self.metrics.calculate_forecast_accuracy(actual, predicted)
