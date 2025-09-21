"""
Test Suite for Predictive Analytics Engine
==========================================

Comprehensive tests for performance prediction models, capacity planning,
and anomaly detection functionality.
"""

import pytest
from datetime import datetime, timedelta
from analytics.predictive_engine import (
    PerformanceMetrics, PredictionResult, CapacityForecast,
    LoadForecastingModel, CapacityPlanningModel, AnomalyDetectionModel,
    PredictiveAnalyticsEngine
)

# ---------- Test Data ----------

def create_sample_metrics(timestamp: datetime = None, **kwargs) -> PerformanceMetrics:
    """Create sample performance metrics for testing."""
    if timestamp is None:
        timestamp = datetime.now()
    
    defaults = {
        'cpu_usage': 50.0,
        'memory_usage': 60.0,
        'disk_io': 30.0,
        'network_io': 40.0,
        'response_time': 200.0,
        'throughput': 1000.0,
        'error_rate': 0.01,
        'active_connections': 50
    }
    defaults.update(kwargs)
    
    return PerformanceMetrics(
        timestamp=timestamp,
        **defaults
    )

# ---------- Load Forecasting Tests ----------

class TestLoadForecastingModel:
    """Test load forecasting functionality."""
    
    def test_empty_data_prediction(self):
        """Test prediction with no historical data."""
        model = LoadForecastingModel()
        result = model.predict_load(hours_ahead=1)
        
        assert result.metric_name == "system_load"
        assert result.predicted_value == 0.0
        assert result.confidence == 0.0
        assert "Insufficient data" in result.recommendations[0]
    
    def test_insufficient_data_prediction(self):
        """Test prediction with minimal data."""
        model = LoadForecastingModel()
        
        # Add only 2 data points
        model.add_metric(create_sample_metrics(cpu_usage=50.0, memory_usage=60.0))
        model.add_metric(create_sample_metrics(cpu_usage=55.0, memory_usage=65.0))
        
        result = model.predict_load(hours_ahead=1)
        
        assert result.metric_name == "system_load"
        assert result.predicted_value > 0
        assert result.confidence >= 0.0
        assert result.time_horizon == timedelta(hours=1)
    
    def test_trend_calculation(self):
        """Test trend calculation with increasing data."""
        model = LoadForecastingModel(window_size=5)
        
        # Add increasing trend data
        for i in range(5):
            model.add_metric(create_sample_metrics(
                cpu_usage=50.0 + i * 5,
                memory_usage=60.0 + i * 3
            ))
        
        result = model.predict_load(hours_ahead=1)
        
        assert result.trend == "increasing"
        assert result.predicted_value > 0
        assert result.confidence > 0
    
    def test_stable_trend(self):
        """Test stable trend detection."""
        model = LoadForecastingModel(window_size=5)
        
        # Add stable data
        for i in range(5):
            model.add_metric(create_sample_metrics(
                cpu_usage=50.0,
                memory_usage=60.0
            ))
        
        result = model.predict_load(hours_ahead=1)
        
        assert result.trend == "stable"
        assert result.predicted_value > 0
        assert result.confidence > 0
    
    def test_anomaly_detection(self):
        """Test anomaly detection in load data."""
        model = LoadForecastingModel(window_size=5)
        
        # Add normal data
        for i in range(4):
            model.add_metric(create_sample_metrics(
                cpu_usage=50.0,
                memory_usage=60.0
            ))
        
        # Add anomalous data point
        model.add_metric(create_sample_metrics(
            cpu_usage=95.0,  # High anomaly
            memory_usage=60.0
        ))
        
        result = model.predict_load(hours_ahead=1)
        
        assert result.anomaly_score > 0.5  # Should detect high anomaly
        assert "scaling" in " ".join(result.recommendations).lower()
    
    def test_high_load_recommendations(self):
        """Test recommendations for high predicted load."""
        model = LoadForecastingModel(window_size=3)
        
        # Add high load data
        for i in range(3):
            model.add_metric(create_sample_metrics(
                cpu_usage=85.0 + i,
                memory_usage=90.0 + i
            ))
        
        result = model.predict_load(hours_ahead=1)
        
        recommendations = " ".join(result.recommendations)
        assert "scaling" in recommendations.lower()
        assert "80%" in recommendations or "85%" in recommendations

# ---------- Capacity Planning Tests ----------

class TestCapacityPlanningModel:
    """Test capacity planning functionality."""
    
    def test_capacity_forecast(self):
        """Test basic capacity forecasting."""
        model = CapacityPlanningModel()
        metrics = create_sample_metrics(cpu_usage=70.0, memory_usage=75.0)
        
        forecasts = model.forecast_capacity(metrics, growth_rate=0.1)
        
        assert len(forecasts) == 4  # CPU, Memory, Disk, Network
        assert all(isinstance(f, CapacityForecast) for f in forecasts)
        
        # Check CPU forecast
        cpu_forecast = next(f for f in forecasts if f.resource_type == "CPU")
        assert cpu_forecast.current_usage == 70.0
        assert cpu_forecast.predicted_usage > 70.0  # Should be higher due to growth
        assert cpu_forecast.confidence > 0
    
    def test_high_usage_forecast(self):
        """Test forecasting with high current usage."""
        model = CapacityPlanningModel()
        metrics = create_sample_metrics(cpu_usage=90.0, memory_usage=85.0)
        
        forecasts = model.forecast_capacity(metrics, growth_rate=0.1)
        
        cpu_forecast = next(f for f in forecasts if f.resource_type == "CPU")
        assert "immediate" in cpu_forecast.scaling_recommendation.lower()
        assert cpu_forecast.confidence > 0.8
    
    def test_low_usage_forecast(self):
        """Test forecasting with low current usage."""
        model = CapacityPlanningModel()
        metrics = create_sample_metrics(cpu_usage=30.0, memory_usage=40.0)
        
        forecasts = model.forecast_capacity(metrics, growth_rate=0.1)
        
        cpu_forecast = next(f for f in forecasts if f.resource_type == "CPU")
        assert "sufficient" in cpu_forecast.scaling_recommendation.lower()
        assert cpu_forecast.confidence > 0.5
    
    def test_time_to_limit_calculation(self):
        """Test time to limit calculation."""
        model = CapacityPlanningModel()
        metrics = create_sample_metrics(cpu_usage=50.0)
        
        forecasts = model.forecast_capacity(metrics, growth_rate=0.2)  # 20% growth
        
        cpu_forecast = next(f for f in forecasts if f.resource_type == "CPU")
        assert cpu_forecast.time_to_limit is not None
        assert cpu_forecast.time_to_limit.total_seconds() > 0

# ---------- Anomaly Detection Tests ----------

class TestAnomalyDetectionModel:
    """Test anomaly detection functionality."""
    
    def test_no_baseline_anomalies(self):
        """Test anomaly detection with no baseline."""
        model = AnomalyDetectionModel()
        metrics = create_sample_metrics()
        
        anomalies = model.detect_anomalies(metrics)
        
        assert len(anomalies) == 0  # No baseline, no anomalies
    
    def test_normal_metrics_no_anomalies(self):
        """Test normal metrics don't trigger anomalies."""
        model = AnomalyDetectionModel()
        
        # Set baseline
        baseline = create_sample_metrics()
        model.detect_anomalies(baseline)
        
        # Add similar metrics
        current = create_sample_metrics(
            cpu_usage=52.0,  # Small change
            memory_usage=61.0
        )
        
        anomalies = model.detect_anomalies(current)
        
        assert len(anomalies) == 0  # Should not detect anomalies
    
    def test_cpu_anomaly_detection(self):
        """Test CPU usage anomaly detection."""
        model = AnomalyDetectionModel(threshold=0.5)  # Lower threshold for easier detection
        
        # Set baseline
        baseline = create_sample_metrics(cpu_usage=50.0)
        model.detect_anomalies(baseline)
        
        # Add high CPU usage
        current = create_sample_metrics(cpu_usage=80.0)  # 60% increase
        
        anomalies = model.detect_anomalies(current)
        
        assert len(anomalies) > 0
        cpu_anomaly = next(a for a in anomalies if "cpu_usage" in a.metric_name)
        assert cpu_anomaly.anomaly_score > 0
        assert "cpu" in " ".join(cpu_anomaly.recommendations).lower()
    
    def test_memory_anomaly_detection(self):
        """Test memory usage anomaly detection."""
        model = AnomalyDetectionModel(threshold=0.4)  # Lower threshold for easier detection
        
        # Set baseline
        baseline = create_sample_metrics(memory_usage=60.0)
        model.detect_anomalies(baseline)
        
        # Add high memory usage
        current = create_sample_metrics(memory_usage=90.0)  # 50% increase
        
        anomalies = model.detect_anomalies(current)
        
        assert len(anomalies) > 0
        memory_anomaly = next(a for a in anomalies if "memory_usage" in a.metric_name)
        assert memory_anomaly.anomaly_score > 0
        assert "memory" in " ".join(memory_anomaly.recommendations).lower()
    
    def test_response_time_anomaly(self):
        """Test response time anomaly detection."""
        model = AnomalyDetectionModel(threshold=1.5)
        
        # Set baseline
        baseline = create_sample_metrics(response_time=200.0)
        model.detect_anomalies(baseline)
        
        # Add high response time
        current = create_sample_metrics(response_time=800.0)  # 4x increase
        
        anomalies = model.detect_anomalies(current)
        
        assert len(anomalies) > 0
        response_anomaly = next(a for a in anomalies if "response_time" in a.metric_name)
        assert response_anomaly.anomaly_score > 0
        assert "response" in " ".join(response_anomaly.recommendations).lower()

# ---------- Main Engine Tests ----------

class TestPredictiveAnalyticsEngine:
    """Test main predictive analytics engine."""
    
    def test_engine_initialization(self):
        """Test engine initialization."""
        engine = PredictiveAnalyticsEngine()
        
        assert engine.load_forecaster is not None
        assert engine.capacity_planner is not None
        assert engine.anomaly_detector is not None
        assert len(engine.prediction_history) == 0
    
    def test_comprehensive_analysis(self):
        """Test comprehensive performance analysis."""
        engine = PredictiveAnalyticsEngine()
        metrics = create_sample_metrics(
            cpu_usage=70.0,
            memory_usage=75.0,
            response_time=300.0,
            error_rate=0.02
        )
        
        analysis = engine.analyze_performance(metrics)
        
        # Check structure
        assert "timestamp" in analysis
        assert "current_metrics" in analysis
        assert "predictions" in analysis
        assert "overall_health" in analysis
        
        # Check predictions
        predictions = analysis["predictions"]
        assert "load_forecast" in predictions
        assert "capacity_forecasts" in predictions
        assert "anomalies" in predictions
        
        # Check health score
        health = analysis["overall_health"]
        assert "score" in health
        assert "status" in health
        assert "components" in health
        assert 0 <= health["score"] <= 100
    
    def test_prediction_history(self):
        """Test prediction history tracking."""
        engine = PredictiveAnalyticsEngine()
        
        # Add multiple analyses
        for i in range(5):
            metrics = create_sample_metrics(cpu_usage=50.0 + i)
            engine.analyze_performance(metrics)
        
        history = engine.get_prediction_history(limit=3)
        
        assert len(history) == 3
        assert all("timestamp" in h for h in history)
        assert all("overall_health" in h for h in history)
    
    def test_health_score_calculation(self):
        """Test overall health score calculation."""
        engine = PredictiveAnalyticsEngine()
        
        # Test excellent health
        good_metrics = create_sample_metrics(
            cpu_usage=30.0,
            memory_usage=40.0,
            response_time=100.0,
            error_rate=0.001
        )
        
        analysis = engine.analyze_performance(good_metrics)
        health = analysis["overall_health"]
        
        assert health["score"] > 70  # Adjusted for realistic health calculation
        assert health["status"] in ["excellent", "good"]
        
        # Test poor health
        bad_metrics = create_sample_metrics(
            cpu_usage=95.0,
            memory_usage=90.0,
            response_time=2000.0,
            error_rate=0.1
        )
        
        analysis = engine.analyze_performance(bad_metrics)
        health = analysis["overall_health"]
        
        assert health["score"] < 50
        assert health["status"] in ["fair", "poor"]
    
    def test_analysis_save(self, tmp_path):
        """Test saving analysis to file."""
        engine = PredictiveAnalyticsEngine()
        metrics = create_sample_metrics()
        
        engine.analyze_performance(metrics)
        
        filepath = tmp_path / "test_analysis.json"
        engine.save_analysis(str(filepath))
        
        assert filepath.exists()
        
        # Verify file content
        import json
        with open(filepath) as f:
            data = json.load(f)
        
        assert "timestamp" in data
        assert "overall_health" in data

# ---------- Integration Tests ----------

class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_end_to_end_prediction_workflow(self):
        """Test complete prediction workflow."""
        engine = PredictiveAnalyticsEngine()
        
        # Simulate time series data
        timestamps = [
            datetime.now() - timedelta(hours=4),
            datetime.now() - timedelta(hours=3),
            datetime.now() - timedelta(hours=2),
            datetime.now() - timedelta(hours=1),
            datetime.now()
        ]
        
        cpu_values = [50.0, 55.0, 60.0, 65.0, 70.0]  # Increasing trend
        memory_values = [60.0, 62.0, 64.0, 66.0, 68.0]  # Increasing trend
        
        # Add historical data
        for i, timestamp in enumerate(timestamps[:-1]):
            metrics = create_sample_metrics(
                timestamp=timestamp,
                cpu_usage=cpu_values[i],
                memory_usage=memory_values[i]
            )
            engine.analyze_performance(metrics)
        
        # Analyze current state
        current_metrics = create_sample_metrics(
            timestamp=timestamps[-1],
            cpu_usage=cpu_values[-1],
            memory_usage=memory_values[-1]
        )
        
        analysis = engine.analyze_performance(current_metrics)
        
        # Verify predictions
        load_forecast = analysis["predictions"]["load_forecast"]
        assert load_forecast["trend"] == "increasing"
        assert load_forecast["confidence"] > 0
        
        # Verify capacity forecasts
        capacity_forecasts = analysis["predictions"]["capacity_forecasts"]
        assert len(capacity_forecasts) == 4
        
        # Verify health score
        health = analysis["overall_health"]
        assert 0 <= health["score"] <= 100
        assert health["status"] in ["excellent", "good", "fair", "poor"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
