"""
Predictive Modeling Metrics
============================

Ensemble forecasting and accuracy metrics for time-series models.

Extracted from: predictive_modeling_engine.py (V2 compliance refactor)
Author: Agent-5 (Business Intelligence Specialist)
Refactored by: Agent-6 (VSCode Forking & Quality Gates)
License: MIT
"""

import logging
import statistics
from typing import Any

logger = logging.getLogger(__name__)


class PredictiveModelingMetrics:
    """Handles forecast ensemble and accuracy calculations."""

    def __init__(self, forecast_horizon: int):
        """
        Initialize metrics calculator.
        
        Args:
            forecast_horizon: Number of periods in forecast
        """
        self.forecast_horizon = forecast_horizon
        self.logger = logger

    def calculate_ensemble(self, methods: dict[str, dict[str, Any]]) -> dict[str, Any]:
        """
        Calculate ensemble forecast by averaging all methods.
        
        Args:
            methods: Dictionary of forecasting method results
            
        Returns:
            Ensemble forecast with confidence metrics
        """
        try:
            # Collect all forecasts
            all_forecasts = []
            for method_name, method_result in methods.items():
                if "forecast" in method_result:
                    all_forecasts.append(method_result["forecast"])

            if not all_forecasts:
                return {"status": "no_forecasts_available"}

            # Calculate average forecast for each horizon point
            ensemble_forecast = []
            for i in range(self.forecast_horizon):
                values_at_i = [f[i] for f in all_forecasts if i < len(f)]
                if values_at_i:
                    avg = sum(values_at_i) / len(values_at_i)
                    ensemble_forecast.append(round(avg, 3))

            # Calculate forecast confidence (inverse of variance)
            confidence = self.calculate_forecast_confidence(all_forecasts)

            return {
                "status": "complete",
                "method": "ensemble",
                "forecast": ensemble_forecast,
                "methods_used": len(all_forecasts),
                "confidence": confidence,
            }

        except Exception as e:
            self.logger.error(f"Error calculating ensemble: {e}")
            return {"status": "error", "error": str(e)}

    def calculate_forecast_confidence(
        self, forecasts: list[list[float]]
    ) -> dict[str, float]:
        """
        Calculate confidence metrics for forecasts.
        
        Args:
            forecasts: List of forecast arrays from different methods
            
        Returns:
            Confidence score and variance metrics
        """
        if not forecasts or len(forecasts) < 2:
            return {"confidence_score": 1.0}

        try:
            variances = [
                statistics.variance([f[i] for f in forecasts if i < len(f)])
                for i in range(self.forecast_horizon)
                if len([f[i] for f in forecasts if i < len(f)]) > 1
            ]

            if variances:
                avg_var = sum(variances) / len(variances)
                return {
                    "confidence_score": round(1.0 / (1.0 + avg_var), 3),
                    "average_variance": round(avg_var, 3),
                }
            return {"confidence_score": 1.0}

        except Exception as e:
            self.logger.error(f"Error calculating confidence: {e}")
            return {"confidence_score": 0.5}

    def calculate_forecast_accuracy(
        self, actual: list[float], predicted: list[float]
    ) -> dict[str, float]:
        """
        Calculate forecast accuracy metrics.
        
        Args:
            actual: Actual values
            predicted: Predicted values
            
        Returns:
            Dictionary of accuracy metrics (MAE, MSE, RMSE, MAPE)
        """
        if not actual or not predicted or len(actual) != len(predicted):
            return {"error": "Invalid data for accuracy calculation"}

        try:
            n = len(actual)

            # Mean Absolute Error (MAE)
            mae = sum(abs(actual[i] - predicted[i]) for i in range(n)) / n

            # Mean Squared Error (MSE)
            mse = sum((actual[i] - predicted[i]) ** 2 for i in range(n)) / n

            # Root Mean Squared Error (RMSE)
            rmse = mse**0.5

            # Mean Absolute Percentage Error (MAPE)
            mape_values = []
            for i in range(n):
                if actual[i] != 0:
                    mape_values.append(abs((actual[i] - predicted[i]) / actual[i]))
            mape = (sum(mape_values) / len(mape_values) * 100) if mape_values else 0

            return {
                "mae": round(mae, 3),
                "mse": round(mse, 3),
                "rmse": round(rmse, 3),
                "mape": round(mape, 2),
            }

        except Exception as e:
            self.logger.error(f"Error calculating accuracy: {e}")
            return {"error": str(e)}


