#!/usr/bin/env python3
"""
Machine Learning Engine - V2 Compliant
======================================

Machine learning engine for predictive analytics and business intelligence.
V2 COMPLIANT: Under 400 lines, single responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import math
import statistics
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class MLModel:
    """Machine learning model definition."""
    model_id: str
    model_type: str
    accuracy: float
    last_trained: datetime
    parameters: Dict[str, Any]
    training_data_size: int


@dataclass
class PredictionResult:
    """Prediction result."""
    model_id: str
    prediction: Any
    confidence: float
    timestamp: datetime
    input_features: Dict[str, Any]


class SimpleLinearRegression:
    """Simple linear regression implementation."""
    
    def __init__(self):
        self.slope = 0.0
        self.intercept = 0.0
        self.trained = False
        self.r_squared = 0.0
    
    def fit(self, X: List[float], y: List[float]) -> None:
        """Fit the linear regression model."""
        if len(X) != len(y) or len(X) < 2:
            raise ValueError("Invalid training data")
        
        n = len(X)
        sum_x = sum(X)
        sum_y = sum(y)
        sum_xy = sum(x * y for x, y in zip(X, y))
        sum_x2 = sum(x * x for x in X)
        
        # Calculate slope and intercept
        self.slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        self.intercept = (sum_y - self.slope * sum_x) / n
        
        # Calculate R-squared
        y_mean = sum_y / n
        ss_tot = sum((y_val - y_mean) ** 2 for y_val in y)
        ss_res = sum((y_val - (self.slope * x + self.intercept)) ** 2 for x, y_val in zip(X, y))
        self.r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        self.trained = True
        logger.debug(f"Linear regression trained: slope={self.slope:.3f}, intercept={self.intercept:.3f}, R²={self.r_squared:.3f}")
    
    def predict(self, X: List[float]) -> List[float]:
        """Make predictions."""
        if not self.trained:
            raise ValueError("Model not trained")
        
        return [self.slope * x + self.intercept for x in X]
    
    def get_accuracy(self) -> float:
        """Get model accuracy (R-squared)."""
        return self.r_squared


class TimeSeriesPredictor:
    """Time series prediction using moving averages and trend analysis."""
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.data_points = deque(maxlen=window_size * 2)
        self.trend = 0.0
        self.seasonality = []
        self.trained = False
    
    def add_data_point(self, timestamp: datetime, value: float) -> None:
        """Add a data point to the time series."""
        self.data_points.append((timestamp, value))
        if len(self.data_points) >= self.window_size:
            self._update_trend()
            self._update_seasonality()
            self.trained = True
    
    def _update_trend(self) -> None:
        """Update trend calculation."""
        if len(self.data_points) < 2:
            return
        
        # Simple linear trend calculation
        recent_points = list(self.data_points)[-self.window_size:]
        if len(recent_points) >= 2:
            x_values = [(point[0] - recent_points[0][0]).total_seconds() for point in recent_points]
            y_values = [point[1] for point in recent_points]
            
            if len(set(x_values)) > 1:  # Ensure we have variation in x
                n = len(x_values)
                sum_x = sum(x_values)
                sum_y = sum(y_values)
                sum_xy = sum(x * y for x, y in zip(x_values, y_values))
                sum_x2 = sum(x * x for x in x_values)
                
                self.trend = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    
    def _update_seasonality(self) -> None:
        """Update seasonality patterns."""
        if len(self.data_points) < self.window_size:
            return
        
        # Simple seasonality detection (hourly patterns)
        hourly_values = {}
        for timestamp, value in self.data_points:
            hour = timestamp.hour
            if hour not in hourly_values:
                hourly_values[hour] = []
            hourly_values[hour].append(value)
        
        self.seasonality = {}
        for hour, values in hourly_values.items():
            if values:
                self.seasonality[hour] = statistics.mean(values)
    
    def predict_next(self, steps: int = 1) -> List[Tuple[datetime, float]]:
        """Predict next values in the time series."""
        if not self.trained or not self.data_points:
            return []
        
        predictions = []
        last_timestamp, last_value = self.data_points[-1]
        
        for i in range(1, steps + 1):
            # Calculate next timestamp
            next_timestamp = last_timestamp + timedelta(hours=i)
            
            # Base prediction from trend
            trend_prediction = last_value + (self.trend * i * 3600)  # Convert trend to per-hour
            
            # Add seasonality if available
            hour = next_timestamp.hour
            if hour in self.seasonality:
                seasonal_adjustment = self.seasonality[hour] - statistics.mean(list(self.seasonality.values()))
                trend_prediction += seasonal_adjustment * 0.3  # Weight seasonality
            
            predictions.append((next_timestamp, trend_prediction))
        
        return predictions
    
    def get_accuracy(self) -> float:
        """Get prediction accuracy based on recent performance."""
        if len(self.data_points) < 5:
            return 0.0
        
        # Simple accuracy calculation based on trend consistency
        recent_points = list(self.data_points)[-5:]
        if len(recent_points) < 2:
            return 0.0
        
        # Calculate how well the trend fits recent data
        x_values = [(point[0] - recent_points[0][0]).total_seconds() for point in recent_points]
        y_values = [point[1] for point in recent_points]
        
        predicted_values = [self.trend * x + recent_points[0][1] for x in x_values]
        mse = sum((actual - pred) ** 2 for actual, pred in zip(y_values, predicted_values)) / len(y_values)
        
        # Convert MSE to accuracy percentage (simplified)
        variance = statistics.variance(y_values) if len(y_values) > 1 else 1.0
        accuracy = max(0.0, 1.0 - (mse / variance))
        
        return min(1.0, accuracy)


class AnomalyDetector:
    """Anomaly detection using statistical methods."""
    
    def __init__(self, threshold_multiplier: float = 2.0):
        self.threshold_multiplier = threshold_multiplier
        self.data_points = deque(maxlen=100)
        self.mean = 0.0
        self.std_dev = 0.0
        self.trained = False
    
    def add_data_point(self, value: float) -> None:
        """Add a data point for anomaly detection."""
        self.data_points.append(value)
        if len(self.data_points) >= 10:
            self._update_statistics()
            self.trained = True
    
    def _update_statistics(self) -> None:
        """Update mean and standard deviation."""
        if len(self.data_points) < 2:
            return
        
        self.mean = statistics.mean(self.data_points)
        self.std_dev = statistics.stdev(self.data_points) if len(self.data_points) > 1 else 0.0
    
    def detect_anomaly(self, value: float) -> Tuple[bool, float]:
        """Detect if a value is an anomaly."""
        if not self.trained:
            return False, 0.0
        
        if self.std_dev == 0:
            return False, 0.0
        
        z_score = abs(value - self.mean) / self.std_dev
        is_anomaly = z_score > self.threshold_multiplier
        
        return is_anomaly, z_score
    
    def get_anomaly_threshold(self) -> Tuple[float, float]:
        """Get anomaly detection thresholds."""
        if not self.trained:
            return 0.0, 0.0
        
        lower_threshold = self.mean - (self.threshold_multiplier * self.std_dev)
        upper_threshold = self.mean + (self.threshold_multiplier * self.std_dev)
        
        return lower_threshold, upper_threshold


class MachineLearningEngine:
    """Main machine learning engine for business intelligence."""
    
    def __init__(self):
        self.models = {}
        self.time_series_predictors = {}
        self.anomaly_detectors = {}
        self.ml_stats = {
            'models_trained': 0,
            'predictions_made': 0,
            'anomalies_detected': 0,
            'accuracy_improvements': 0
        }
    
    def train_linear_regression(self, model_id: str, X: List[float], y: List[float]) -> MLModel:
        """Train a linear regression model."""
        model = SimpleLinearRegression()
        model.fit(X, y)
        
        ml_model = MLModel(
            model_id=model_id,
            model_type="linear_regression",
            accuracy=model.get_accuracy(),
            last_trained=datetime.now(),
            parameters={"slope": model.slope, "intercept": model.intercept},
            training_data_size=len(X)
        )
        
        self.models[model_id] = ml_model
        self.ml_stats['models_trained'] += 1
        
        logger.info(f"Linear regression model {model_id} trained with accuracy {ml_model.accuracy:.3f}")
        return ml_model
    
    def predict_with_model(self, model_id: str, X: List[float]) -> PredictionResult:
        """Make predictions with a trained model."""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model_info = self.models[model_id]
        
        # For now, use simple linear prediction
        # In a real implementation, this would use the actual trained model
        if model_info.model_type == "linear_regression":
            slope = model_info.parameters.get("slope", 0.0)
            intercept = model_info.parameters.get("intercept", 0.0)
            predictions = [slope * x + intercept for x in X]
        else:
            predictions = [0.0] * len(X)
        
        self.ml_stats['predictions_made'] += 1
        
        return PredictionResult(
            model_id=model_id,
            prediction=predictions,
            confidence=model_info.accuracy,
            timestamp=datetime.now(),
            input_features={"X": X}
        )
    
    def setup_time_series_prediction(self, series_id: str, window_size: int = 10) -> None:
        """Set up time series prediction for a data series."""
        self.time_series_predictors[series_id] = TimeSeriesPredictor(window_size)
        logger.debug(f"Time series predictor set up for {series_id}")
    
    def add_time_series_data(self, series_id: str, timestamp: datetime, value: float) -> None:
        """Add data to a time series."""
        if series_id in self.time_series_predictors:
            self.time_series_predictors[series_id].add_data_point(timestamp, value)
    
    def predict_time_series(self, series_id: str, steps: int = 1) -> List[Tuple[datetime, float]]:
        """Predict future values in a time series."""
        if series_id not in self.time_series_predictors:
            raise ValueError(f"Time series {series_id} not found")
        
        return self.time_series_predictors[series_id].predict_next(steps)
    
    def setup_anomaly_detection(self, detector_id: str, threshold_multiplier: float = 2.0) -> None:
        """Set up anomaly detection for a data stream."""
        self.anomaly_detectors[detector_id] = AnomalyDetector(threshold_multiplier)
        logger.debug(f"Anomaly detector set up for {detector_id}")
    
    def detect_anomaly(self, detector_id: str, value: float) -> Tuple[bool, float]:
        """Detect anomaly in a data stream."""
        if detector_id not in self.anomaly_detectors:
            raise ValueError(f"Anomaly detector {detector_id} not found")
        
        detector = self.anomaly_detectors[detector_id]
        detector.add_data_point(value)
        is_anomaly, z_score = detector.detect_anomaly(value)
        
        if is_anomaly:
            self.ml_stats['anomalies_detected'] += 1
        
        return is_anomaly, z_score
    
    def get_ml_stats(self) -> Dict[str, Any]:
        """Get machine learning statistics."""
        return {
            'total_models': len(self.models),
            'time_series_predictors': len(self.time_series_predictors),
            'anomaly_detectors': len(self.anomaly_detectors),
            'models_trained': self.ml_stats['models_trained'],
            'predictions_made': self.ml_stats['predictions_made'],
            'anomalies_detected': self.ml_stats['anomalies_detected'],
            'accuracy_improvements': self.ml_stats['accuracy_improvements']
        }


# Global ML engine instance
_global_ml_engine = None


def get_machine_learning_engine() -> MachineLearningEngine:
    """Get global machine learning engine."""
    global _global_ml_engine
    if _global_ml_engine is None:
        _global_ml_engine = MachineLearningEngine()
    return _global_ml_engine


if __name__ == "__main__":
    # Example usage
    ml_engine = get_machine_learning_engine()
    
    # Train a linear regression model
    X = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    model = ml_engine.train_linear_regression("test_model", X, y)
    print(f"Model trained: {model}")
    
    # Make predictions
    predictions = ml_engine.predict_with_model("test_model", [6, 7, 8])
    print(f"Predictions: {predictions}")
    
    # Set up time series prediction
    ml_engine.setup_time_series_prediction("sales_data")
    now = datetime.now()
    for i in range(20):
        ml_engine.add_time_series_data("sales_data", now + timedelta(hours=i), 100 + i * 2 + (i % 3) * 5)
    
    # Predict future values
    future_predictions = ml_engine.predict_time_series("sales_data", 3)
    print(f"Future predictions: {future_predictions}")
    
    # Set up anomaly detection
    ml_engine.setup_anomaly_detection("performance_metrics")
    for value in [10, 12, 11, 13, 10, 11, 12, 50, 11, 12]:  # 50 is an anomaly
        is_anomaly, z_score = ml_engine.detect_anomaly("performance_metrics", value)
        print(f"Value {value}: Anomaly={is_anomaly}, Z-score={z_score:.2f}")
    
    # Get ML stats
    stats = ml_engine.get_ml_stats()
    print(f"ML Stats: {stats}")
