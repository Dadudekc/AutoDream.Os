#!/usr/bin/env python3
"""
Vector Analytics Predictive Modeling Engine
===========================================

Predictive modeling engine for vector analytics system.
Handles forecasting, trend prediction, behavior prediction, and resource forecasting.
V2 COMPLIANT: Focused predictive modeling under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR PREDICTIVE MODELING
@license MIT
"""

import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from ..vector_analytics_models import PredictionResult, VectorAnalyticsConfig


class PredictiveModelingEngine:
    """Predictive modeling engine for vector analytics"""
    
    def __init__(self, config: VectorAnalyticsConfig):
        """Initialize predictive modeling engine with configuration"""
        self.config = config
        self.prediction_cache: Dict[str, List[PredictionResult]] = {}
    
    def create_predictive_modeling_model(self) -> Dict[str, Any]:
        """Create predictive modeling processing model"""
        return {
            'model_type': 'predictive_modeling',
            'version': '1.0',
            'capabilities': [
                'time_series_forecasting',
                'trend_prediction',
                'behavior_prediction',
                'resource_forecasting',
                'anomaly_prediction'
            ],
            'algorithms': {
                'forecast_timeseries': self.forecast_timeseries,
                'predict_trends': self.predict_trends,
                'predict_behavior': self.predict_behavior,
                'forecast_resources': self.forecast_resources
            }
        }
    
    def forecast_timeseries(self, data: List[float], periods: int = 5) -> Dict[str, Any]:
        """Forecast time series data"""
        if len(data) < 3:
            return {'forecast': [], 'confidence': 0.0, 'error': 'insufficient_data'}
        
        # Simple linear forecast
        recent_trend = data[-1] - data[-2] if len(data) >= 2 else 0
        forecast = [data[-1] + recent_trend * i for i in range(1, periods + 1)]
        
        # Calculate confidence based on data consistency
        variance = statistics.variance(data) if len(data) > 1 else 0
        mean_val = statistics.mean(data)
        confidence = max(0.1, 1.0 - (variance / max(mean_val, 0.001)))
        
        return {
            'forecast': forecast,
            'confidence': min(confidence, 1.0),
            'trend': recent_trend,
            'last_value': data[-1],
            'periods': periods
        }
    
    def predict_trends(self, data: List[float]) -> Dict[str, Any]:
        """Predict trends in data"""
        if len(data) < 2:
            return {'trend': 'insufficient_data', 'confidence': 0.0}
        
        # Calculate trend direction and strength
        first_half = data[:len(data)//2]
        second_half = data[len(data)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        trend_direction = 'increasing' if second_avg > first_avg else 'decreasing' if second_avg < first_avg else 'stable'
        trend_strength = abs(second_avg - first_avg) / max(first_avg, 0.001)
        
        # Calculate confidence
        variance = statistics.variance(data) if len(data) > 1 else 0
        confidence = max(0.1, 1.0 - (variance / max(statistics.mean(data), 0.001)))
        
        return {
            'trend': trend_direction,
            'strength': min(trend_strength, 1.0),
            'confidence': min(confidence, 1.0),
            'predicted_next': second_avg + (second_avg - first_avg)
        }
    
    def predict_behavior(self, data: List[Any]) -> Dict[str, Any]:
        """Predict behavioral patterns"""
        if not data:
            return {'predicted_behavior': 'unknown', 'confidence': 0.0}
        
        # Simple behavior prediction based on recent patterns
        recent_data = data[-min(10, len(data)):]  # Last 10 items
        
        # Analyze patterns in recent data
        from collections import Counter
        counter = Counter(recent_data)
        most_common = counter.most_common(1)[0] if counter else None
        
        if most_common:
            frequency = most_common[1] / len(recent_data)
            predicted_behavior = most_common[0]
            confidence = frequency
        else:
            predicted_behavior = 'stable'
            confidence = 0.5
        
        return {
            'predicted_behavior': predicted_behavior,
            'confidence': confidence,
            'pattern_frequency': frequency if most_common else 0.0,
            'sample_size': len(recent_data)
        }
    
    def forecast_resources(self, data: Dict[str, float]) -> Dict[str, Any]:
        """Forecast resource requirements"""
        if not data:
            return {'resource_forecast': {}, 'confidence': 0.0}
        
        # Simple resource forecasting based on current usage
        forecast = {}
        total_resources = sum(data.values())
        
        for resource, current_usage in data.items():
            # Simple growth assumption (5% increase)
            growth_rate = 0.05
            forecast[resource] = current_usage * (1 + growth_rate)
        
        # Calculate confidence based on data consistency
        values = list(data.values())
        if len(values) > 1:
            variance = statistics.variance(values)
            mean_val = statistics.mean(values)
            confidence = max(0.1, 1.0 - (variance / max(mean_val, 0.001)))
        else:
            confidence = 0.6
        
        return {
            'resource_forecast': forecast,
            'confidence': min(confidence, 1.0),
            'current_total': total_resources,
            'forecast_total': sum(forecast.values()),
            'growth_rate': 0.05
        }
    
    def predict_anomalies(self, data: List[float], threshold: float = 2.0) -> Dict[str, Any]:
        """Predict potential anomalies"""
        if len(data) < 3:
            return {'anomaly_risk': 'low', 'confidence': 0.0}
        
        # Calculate statistical measures
        mean_val = statistics.mean(data)
        std_val = statistics.stdev(data) if len(data) > 1 else 0
        
        # Check recent values for anomaly risk
        recent_values = data[-min(5, len(data)):]
        anomaly_risk = 'low'
        risk_score = 0.0
        
        for value in recent_values:
            if std_val > 0:
                z_score = abs(value - mean_val) / std_val
                if z_score > threshold:
                    risk_score += z_score / threshold
                    anomaly_risk = 'high' if z_score > threshold * 1.5 else 'medium'
        
        risk_score = min(risk_score / len(recent_values), 1.0)
        
        return {
            'anomaly_risk': anomaly_risk,
            'risk_score': risk_score,
            'confidence': min(risk_score, 1.0),
            'threshold': threshold,
            'recent_values': recent_values
        }
    
    def predict_performance(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Predict performance based on current metrics"""
        if not metrics:
            return {'performance_prediction': 'unknown', 'confidence': 0.0}
        
        # Calculate overall performance score
        performance_scores = []
        for metric, value in metrics.items():
            if metric.endswith('_time') or metric.endswith('_latency'):
                # Lower is better
                score = max(0, 1.0 - (value / 10.0))
            elif metric.endswith('_rate') or metric.endswith('_percentage'):
                # Higher is better
                score = min(1.0, value / 100.0)
            else:
                score = min(1.0, value / 100.0)
            
            performance_scores.append(score)
        
        overall_score = statistics.mean(performance_scores) if performance_scores else 0.0
        
        # Predict future performance
        if overall_score > 0.8:
            prediction = 'excellent'
        elif overall_score > 0.6:
            prediction = 'good'
        elif overall_score > 0.4:
            prediction = 'fair'
        else:
            prediction = 'poor'
        
        return {
            'performance_prediction': prediction,
            'current_score': overall_score,
            'confidence': overall_score,
            'metrics_analyzed': len(metrics)
        }
    
    def get_prediction_summary(self) -> Dict[str, Any]:
        """Get summary of prediction capabilities"""
        return {
            'cached_predictions': len(self.prediction_cache),
            'total_cached_items': sum(len(predictions) for predictions in self.prediction_cache.values()),
            'capabilities': [
                'time_series_forecasting',
                'trend_prediction',
                'behavior_prediction',
                'resource_forecasting',
                'anomaly_prediction',
                'performance_prediction'
            ],
            'model_version': '1.0'
        }


# Factory function for dependency injection
def create_predictive_modeling_engine(config: VectorAnalyticsConfig) -> PredictiveModelingEngine:
    """Factory function to create predictive modeling engine with configuration"""
    return PredictiveModelingEngine(config)


# Export for DI
__all__ = ['PredictiveModelingEngine', 'create_predictive_modeling_engine']
