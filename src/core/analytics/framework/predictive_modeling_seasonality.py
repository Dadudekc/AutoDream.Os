"""
Predictive Modeling Seasonality
================================

Seasonal pattern detection for time-series data.

Extracted from: predictive_modeling_engine.py (V2 compliance refactor)
Author: Agent-5 (Business Intelligence Specialist)
Refactored by: Agent-6 (VSCode Forking & Quality Gates)
License: MIT
"""

import logging
import statistics
from typing import Any

logger = logging.getLogger(__name__)


class PredictiveModelingSeasonality:
    """Handles seasonal pattern detection and analysis."""

    def __init__(self):
        """Initialize seasonality detector."""
        self.logger = logger

    def detect_seasonality(
        self, data: list[float], period: int = 7
    ) -> dict[str, Any]:
        """
        Detect seasonal patterns in data.
        
        Args:
            data: Historical time series data
            period: Expected seasonal period (e.g., 7 for weekly)
            
        Returns:
            Seasonality analysis results
        """
        if len(data) < 2 * period:
            return {"error": "Insufficient data for seasonality detection"}

        try:
            # Calculate average for each position in the period
            seasonal_components = []
            for i in range(period):
                values_at_position = [data[j] for j in range(i, len(data), period)]
                if values_at_position:
                    avg = sum(values_at_position) / len(values_at_position)
                    seasonal_components.append(round(avg, 3))

            # Calculate seasonal strength (variance of seasonal components)
            overall_mean = sum(data) / len(data)
            seasonal_variance = sum(
                (comp - overall_mean) ** 2 for comp in seasonal_components
            ) / len(seasonal_components)

            # Data variance
            data_variance = statistics.variance(data)

            # Seasonal strength: ratio of seasonal variance to total variance
            seasonal_strength = (
                seasonal_variance / data_variance if data_variance > 0 else 0
            )

            return {
                "status": "complete",
                "period": period,
                "seasonal_components": seasonal_components,
                "seasonal_strength": round(seasonal_strength, 3),
                "has_seasonality": seasonal_strength > 0.1,
            }

        except Exception as e:
            self.logger.error(f"Error detecting seasonality: {e}")
            return {"status": "error", "error": str(e)}

