"""
Predictive Capacity Forecasting - V2 Compliant
==============================================

Capacity forecasting functionality for predictive analytics.
V2 Compliance: ≤400 lines, ≤10 functions, single responsibility
"""

import math
from datetime import datetime, timedelta
from typing import List

from .predictive_models import (
    CapacityForecast,
    PerformanceMetrics,
    ResourceUtilization,
)


class CapacityForecaster:
    """Capacity forecasting functionality."""
    
    def __init__(self):
        """Initialize capacity forecaster."""
        self.resource_limits = {
            "cpu": 100.0,
            "memory": 100.0,
            "disk": 100.0,
            "network": 100.0
        }
    
    def forecast_capacity(self, resource_type: str, time_horizon: timedelta,
                         metrics_history: List[PerformanceMetrics]) -> CapacityForecast:
        """Forecast capacity for a specific resource type."""
        if not metrics_history:
            return self._create_default_capacity_forecast(resource_type)
        
        # Get recent metrics
        recent_metrics = self._get_recent_metrics(metrics_history, time_horizon)
        
        if len(recent_metrics) < 2:
            return self._create_default_capacity_forecast(resource_type)
        
        # Extract values for the resource type
        values = self._extract_resource_values(recent_metrics, resource_type)
        
        if not values:
            return self._create_default_capacity_forecast(resource_type)
        
        # Calculate forecast
        current_utilization = values[-1]
        predicted_utilization = self._predict_utilization(values)
        
        # Calculate time to limit
        limit = self.resource_limits.get(resource_type, 100.0)
        time_to_limit = self._calculate_time_to_limit(
            current_utilization, predicted_utilization, limit
        )
        
        # Generate scaling recommendation
        scaling_recommendation = self._generate_scaling_recommendation(predicted_utilization)
        
        return CapacityForecast(
            resource_type=resource_type,
            current_utilization=current_utilization,
            predicted_utilization=predicted_utilization,
            time_to_limit=time_to_limit,
            scaling_recommendation=scaling_recommendation,
            forecast_period=time_horizon,
            timestamp=datetime.now()
        )
    
    def get_resource_utilization(self, resource_name: str,
                                metrics_history: List[PerformanceMetrics]) -> ResourceUtilization:
        """Get current resource utilization."""
        if not metrics_history:
            return ResourceUtilization(
                resource_name=resource_name,
                current_usage=0.0,
                efficiency_score=0.0,
                recommendations=["No data available"]
            )
        
        recent_metrics = metrics_history[-10:]  # Last 10 metrics
        
        # Calculate current usage
        current_usage = self._extract_resource_values(recent_metrics, resource_name)[-1]
        
        # Calculate efficiency score
        efficiency_score = self._calculate_efficiency_score(
            self._extract_resource_values(recent_metrics, resource_name)
        )
        
        # Generate recommendations
        recommendations = self._generate_utilization_recommendations(
            resource_name, current_usage, efficiency_score
        )
        
        return ResourceUtilization(
            resource_name=resource_name,
            current_usage=current_usage,
            efficiency_score=efficiency_score,
            recommendations=recommendations
        )
    
    def _get_recent_metrics(self, metrics_history: List[PerformanceMetrics],
                           time_horizon: timedelta) -> List[PerformanceMetrics]:
        """Get metrics from recent time horizon."""
        cutoff_time = datetime.now() - time_horizon
        return [m for m in metrics_history if m.timestamp >= cutoff_time]
    
    def _extract_resource_values(self, metrics: List[PerformanceMetrics],
                               resource_type: str) -> List[float]:
        """Extract values for a specific resource type."""
        if resource_type == "cpu":
            return [m.cpu_usage for m in metrics]
        elif resource_type == "memory":
            return [m.memory_usage for m in metrics]
        elif resource_type == "disk":
            return [m.disk_usage for m in metrics]
        elif resource_type == "network":
            return [m.network_usage for m in metrics]
        else:
            return []
    
    def _predict_utilization(self, values: List[float]) -> float:
        """Predict future utilization based on trend."""
        if len(values) < 2:
            return values[-1] if values else 0.0
        
        # Simple linear trend prediction
        recent_values = values[-5:]  # Use last 5 values
        if len(recent_values) < 2:
            return recent_values[-1]
        
        # Calculate average growth rate
        growth_rates = []
        for i in range(1, len(recent_values)):
            growth_rate = recent_values[i] - recent_values[i-1]
            growth_rates.append(growth_rate)
        
        avg_growth_rate = sum(growth_rates) / len(growth_rates)
        
        # Predict next value
        predicted = recent_values[-1] + avg_growth_rate
        
        return max(0.0, min(100.0, predicted))  # Clamp between 0-100
    
    def _calculate_time_to_limit(self, current: float, predicted: float, limit: float) -> timedelta:
        """Calculate time until resource limit is reached."""
        if predicted <= current or predicted >= limit:
            return timedelta(days=365)  # Far future if no growth or already at limit
        
        # Calculate growth rate
        growth_rate = predicted - current
        
        if growth_rate <= 0:
            return timedelta(days=365)
        
        # Calculate time to reach limit
        time_to_limit = (limit - current) / growth_rate
        
        # Convert to timedelta (assuming growth_rate is per hour)
        return timedelta(hours=time_to_limit)
    
    def _generate_scaling_recommendation(self, utilization_percentage: float) -> str:
        """Generate scaling recommendation based on utilization."""
        if utilization_percentage > 90:
            return "Immediate scaling required"
        elif utilization_percentage > 75:
            return "Consider scaling up soon"
        elif utilization_percentage > 50:
            return "Monitor utilization closely"
        else:
            return "Utilization within normal range"
    
    def _calculate_efficiency_score(self, values: List[float]) -> float:
        """Calculate efficiency score for resource utilization."""
        if not values:
            return 0.0
        
        # Calculate coefficient of variation (lower is better)
        mean_val = sum(values) / len(values)
        if mean_val == 0:
            return 1.0
        
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance)
        
        cv = std_dev / mean_val
        efficiency_score = max(0.0, min(1.0, 1.0 - cv))
        
        return efficiency_score
    
    def _generate_utilization_recommendations(self, resource_name: str, current_usage: float,
                                            efficiency_score: float) -> List[str]:
        """Generate utilization recommendations."""
        recommendations = []
        
        if current_usage > 90:
            recommendations.append(f"High {resource_name} usage - consider optimization")
        elif current_usage > 70:
            recommendations.append(f"Moderate {resource_name} usage - monitor closely")
        
        if efficiency_score < 0.5:
            recommendations.append(f"Low {resource_name} efficiency - investigate variability")
        
        if not recommendations:
            recommendations.append(f"{resource_name} utilization is optimal")
        
        return recommendations
    
    def _create_default_capacity_forecast(self, resource_type: str) -> CapacityForecast:
        """Create default capacity forecast when insufficient data."""
        return CapacityForecast(
            resource_type=resource_type,
            current_utilization=0.0,
            predicted_utilization=0.0,
            time_to_limit=timedelta(days=365),
            scaling_recommendation="Insufficient data for forecasting",
            forecast_period=timedelta(hours=1),
            timestamp=datetime.now()
        )
