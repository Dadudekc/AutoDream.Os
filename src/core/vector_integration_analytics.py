#!/usr/bin/env python3
"""
Vector Integration Analytics - Agent-1 Integration & Core Systems
================================================================

Advanced analytics system for vector database integration performance.
Provides real-time monitoring, trend analysis, and predictive insights.

ANALYTICS TARGETS:
- Real-time performance monitoring and alerting
- Trend analysis and pattern recognition
- Predictive performance forecasting
- Optimization recommendation engine
- Comprehensive reporting and visualization

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Core System Integration & Vector Database Optimization
Status: ACTIVE - Analytics Enhancement
"""

import asyncio
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
from datetime import datetime, timedelta
import statistics
import numpy as np
from collections import deque, defaultdict
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Import unified systems
from .unified_logging_system import get_logger
from .unified_validation_system import validate_required_fields
from .vector_database_ml_optimizer import VectorDatabaseMLOptimizer, MLOptimizationConfig


# ================================
# VECTOR INTEGRATION ANALYTICS
# ================================

class AnalyticsMode(Enum):
    """Analytics modes."""
    REAL_TIME = "real_time"
    BATCH = "batch"
    HISTORICAL = "historical"
    PREDICTIVE = "predictive"


class AlertLevel(Enum):
    """Alert levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class PerformanceAlert:
    """Performance alert."""
    alert_id: str
    level: AlertLevel
    message: str
    metric_name: str
    current_value: float
    threshold_value: float
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False


@dataclass
class TrendAnalysis:
    """Trend analysis result."""
    metric_name: str
    trend_direction: str  # 'increasing', 'decreasing', 'stable'
    trend_strength: float  # 0-1
    change_percentage: float
    confidence: float
    time_period: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class PerformanceForecast:
    """Performance forecast."""
    metric_name: str
    forecast_values: List[float]
    forecast_timestamps: List[datetime]
    confidence_interval: List[float]
    forecast_horizon_hours: int
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class OptimizationRecommendation:
    """Optimization recommendation."""
    recommendation_id: str
    priority: str  # 'low', 'medium', 'high', 'critical'
    category: str
    description: str
    expected_improvement: float
    implementation_effort: str  # 'low', 'medium', 'high'
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)


class VectorIntegrationAnalytics:
    """
    Advanced analytics system for vector database integration performance.
    
    FEATURES:
    - Real-time performance monitoring and alerting
    - Trend analysis and pattern recognition
    - Predictive performance forecasting
    - Optimization recommendation engine
    - Comprehensive reporting and visualization
    - Historical data analysis and insights
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize vector integration analytics."""
        self.logger = get_logger(__name__)
        self.config = config or {}
        
        # Initialize ML optimizer for analytics
        ml_config = MLOptimizationConfig(
            enable_predictive_caching=True,
            enable_adaptive_tuning=True,
            enable_pattern_learning=True,
            enable_resource_optimization=True,
            enable_query_optimization=True
        )
        self.ml_optimizer = VectorDatabaseMLOptimizer(ml_config)
        
        # Analytics components
        self._setup_analytics_components()
        self._setup_monitoring_systems()
        self._setup_alerting_systems()
        self._setup_forecasting_engines()
        
        # Data storage
        self.performance_data: deque = deque(maxlen=10000)
        self.alerts: List[PerformanceAlert] = []
        self.trend_analyses: List[TrendAnalysis] = []
        self.forecasts: List[PerformanceForecast] = []
        self.recommendations: List[OptimizationRecommendation] = []
        
        # Analytics state
        self.analytics_active = True
        self.monitoring_thread = threading.Thread(target=self._continuous_monitoring, daemon=True)
        self.monitoring_thread.start()
        
        self.logger.info("Vector Integration Analytics initialized successfully")
    
    def _setup_analytics_components(self):
        """Setup analytics components."""
        # Performance metrics
        self.metrics_config = {
            'response_time': {'threshold': 200.0, 'unit': 'ms'},
            'throughput': {'threshold': 100.0, 'unit': 'ops/s'},
            'memory_usage': {'threshold': 500.0, 'unit': 'MB'},
            'cpu_usage': {'threshold': 80.0, 'unit': '%'},
            'cache_hit_rate': {'threshold': 0.7, 'unit': 'ratio'},
            'error_rate': {'threshold': 0.05, 'unit': 'ratio'}
        }
        
        # Alert thresholds
        self.alert_thresholds = {
            'warning': 0.8,  # 80% of critical threshold
            'critical': 1.0,  # 100% of critical threshold
            'emergency': 1.2   # 120% of critical threshold
        }
        
        # Trend analysis parameters
        self.trend_config = {
            'min_data_points': 10,
            'trend_window_hours': 24,
            'confidence_threshold': 0.7
        }
    
    def _setup_monitoring_systems(self):
        """Setup monitoring systems."""
        self.monitoring_systems = {
            'performance_monitor': self._monitor_performance,
            'resource_monitor': self._monitor_resources,
            'error_monitor': self._monitor_errors,
            'capacity_monitor': self._monitor_capacity
        }
    
    def _monitor_performance(self):
        """Monitor performance metrics."""
        try:
            # Get performance data from ML optimizer
            ml_report = self.ml_optimizer.get_ml_optimization_report()
            vector_report = self.ml_optimizer.vector_integration.get_enhanced_performance_report()
            
            # Extract performance metrics
            performance_metrics = {
                'timestamp': datetime.now(),
                'ml_optimizer_status': ml_report.get('ml_optimizer_status', 'unknown'),
                'learning_stats': ml_report.get('learning_stats', {}),
                'patterns_learned': ml_report.get('learned_patterns_count', 0),
                'adaptation_count': ml_report.get('adaptation_count', 0)
            }
            
            return performance_metrics
        except Exception as e:
            self.logger.error(f"Performance monitoring error: {e}")
            return {}
    
    def _monitor_resources(self):
        """Monitor resource usage."""
        try:
            # Get resource usage data
            resource_metrics = {
                'timestamp': datetime.now(),
                'memory_usage_mb': 100.0,  # Placeholder
                'cpu_usage_percent': 50.0,  # Placeholder
                'connection_count': 10,  # Placeholder
                'cache_usage_mb': 50.0  # Placeholder
            }
            
            return resource_metrics
        except Exception as e:
            self.logger.error(f"Resource monitoring error: {e}")
            return {}
    
    def _monitor_errors(self):
        """Monitor error conditions."""
        try:
            # Check for error conditions
            error_metrics = {
                'timestamp': datetime.now(),
                'error_count': 0,  # Placeholder
                'error_rate': 0.0,  # Placeholder
                'last_error': None,  # Placeholder
                'error_types': {}  # Placeholder
            }
            
            return error_metrics
        except Exception as e:
            self.logger.error(f"Error monitoring error: {e}")
            return {}
    
    def _monitor_capacity(self):
        """Monitor system capacity."""
        try:
            # Check capacity metrics
            capacity_metrics = {
                'timestamp': datetime.now(),
                'memory_capacity_mb': 1000.0,  # Placeholder
                'cpu_capacity_percent': 100.0,  # Placeholder
                'connection_capacity': 100,  # Placeholder
                'cache_capacity_mb': 500.0  # Placeholder
            }
            
            return capacity_metrics
        except Exception as e:
            self.logger.error(f"Capacity monitoring error: {e}")
            return {}
    
    def _setup_alerting_systems(self):
        """Setup alerting systems."""
        self.alerting_systems = {
            'threshold_alerts': self._check_threshold_alerts,
            'trend_alerts': self._check_trend_alerts,
            'anomaly_alerts': self._check_anomaly_alerts,
            'capacity_alerts': self._check_capacity_alerts
        }
    
    def _setup_forecasting_engines(self):
        """Setup forecasting engines."""
        self.forecasting_engines = {
            'performance_forecast': self._forecast_performance,
            'resource_forecast': self._forecast_resources,
            'capacity_forecast': self._forecast_capacity,
            'trend_forecast': self._forecast_trends
        }
    
    def _forecast_performance(self):
        """Forecast performance metrics."""
        try:
            # Simple performance forecasting
            forecast = {
                'timestamp': datetime.now(),
                'forecast_horizon_hours': 24,
                'predicted_response_time_ms': 150.0,
                'predicted_throughput_ops_per_sec': 120.0,
                'confidence': 0.8
            }
            return forecast
        except Exception as e:
            self.logger.error(f"Performance forecasting error: {e}")
            return {}
    
    def _forecast_resources(self):
        """Forecast resource requirements."""
        try:
            # Simple resource forecasting
            forecast = {
                'timestamp': datetime.now(),
                'forecast_horizon_hours': 24,
                'predicted_memory_usage_mb': 200.0,
                'predicted_cpu_usage_percent': 60.0,
                'confidence': 0.7
            }
            return forecast
        except Exception as e:
            self.logger.error(f"Resource forecasting error: {e}")
            return {}
    
    def _forecast_capacity(self):
        """Forecast capacity needs."""
        try:
            # Simple capacity forecasting
            forecast = {
                'timestamp': datetime.now(),
                'forecast_horizon_hours': 24,
                'predicted_connection_needs': 15,
                'predicted_cache_needs_mb': 100.0,
                'confidence': 0.6
            }
            return forecast
        except Exception as e:
            self.logger.error(f"Capacity forecasting error: {e}")
            return {}
    
    def _forecast_trends(self):
        """Forecast trend patterns."""
        try:
            # Simple trend forecasting
            forecast = {
                'timestamp': datetime.now(),
                'forecast_horizon_hours': 24,
                'trend_direction': 'stable',
                'trend_strength': 0.5,
                'confidence': 0.6
            }
            return forecast
        except Exception as e:
            self.logger.error(f"Trend forecasting error: {e}")
            return {}
    
    def _continuous_monitoring(self):
        """Continuous monitoring process."""
        while self.analytics_active:
            try:
                # Collect performance data
                self._collect_performance_data()
                
                # Check for alerts
                self._check_all_alerts()
                
                # Analyze trends
                self._analyze_trends()
                
                # Generate forecasts
                self._generate_forecasts()
                
                # Generate recommendations
                self._generate_recommendations()
                
                # Update analytics
                self._update_analytics()
                
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Continuous monitoring error: {e}")
                time.sleep(10)
    
    def _collect_performance_data(self):
        """Collect performance data from ML optimizer."""
        try:
            # Get ML optimization report
            ml_report = self.ml_optimizer.get_ml_optimization_report()
            
            # Get performance data from vector integration
            vector_report = self.ml_optimizer.vector_integration.get_enhanced_performance_report()
            
            # Extract performance metrics
            performance_entry = {
                'timestamp': datetime.now(),
                'response_time_ms': self._extract_metric(vector_report, 'average_response_time_ms'),
                'throughput_ops_per_sec': self._extract_metric(vector_report, 'operations_per_second'),
                'memory_usage_mb': self._extract_metric(vector_report, 'memory_usage_mb'),
                'cpu_usage_percent': self._extract_metric(vector_report, 'cpu_usage_percent'),
                'cache_hit_rate': self._extract_metric(vector_report, 'cache_hit_rate'),
                'error_rate': self._extract_metric(vector_report, 'error_rate'),
                'optimization_score': self._extract_metric(vector_report, 'optimization_score'),
                'ml_learning_rate': ml_report.get('learning_stats', {}).get('total_queries', 0),
                'patterns_learned': ml_report.get('learned_patterns_count', 0)
            }
            
            self.performance_data.append(performance_entry)
            
        except Exception as e:
            self.logger.error(f"Performance data collection error: {e}")
    
    def _extract_metric(self, report: Dict[str, Any], metric_name: str) -> float:
        """Extract metric value from report."""
        try:
            integration_metrics = report.get('integration_metrics', {})
            vector_metrics = integration_metrics.get('vector_db', {})
            return vector_metrics.get(metric_name, 0.0)
        except Exception:
            return 0.0
    
    def _check_all_alerts(self):
        """Check all alerting systems."""
        for alert_system_name, alert_system in self.alerting_systems.items():
            try:
                alerts = alert_system()
                self.alerts.extend(alerts)
            except Exception as e:
                self.logger.error(f"Alert system '{alert_system_name}' error: {e}")
    
    def _check_threshold_alerts(self) -> List[PerformanceAlert]:
        """Check threshold-based alerts."""
        alerts = []
        
        if len(self.performance_data) == 0:
            return alerts
        
        latest_data = self.performance_data[-1]
        
        for metric_name, config in self.metrics_config.items():
            current_value = latest_data.get(metric_name, 0)
            threshold = config['threshold']
            
            # Check alert levels
            if current_value >= threshold * self.alert_thresholds['emergency']:
                level = AlertLevel.EMERGENCY
            elif current_value >= threshold * self.alert_thresholds['critical']:
                level = AlertLevel.CRITICAL
            elif current_value >= threshold * self.alert_thresholds['warning']:
                level = AlertLevel.WARNING
            else:
                continue
            
            alert = PerformanceAlert(
                alert_id=f"threshold_{metric_name}_{int(time.time())}",
                level=level,
                message=f"{metric_name} exceeded {level.value} threshold: {current_value:.2f} {config['unit']}",
                metric_name=metric_name,
                current_value=current_value,
                threshold_value=threshold
            )
            
            alerts.append(alert)
        
        return alerts
    
    def _check_trend_alerts(self) -> List[PerformanceAlert]:
        """Check trend-based alerts."""
        alerts = []
        
        if len(self.performance_data) < self.trend_config['min_data_points']:
            return alerts
        
        # Analyze recent trends
        recent_data = list(self.performance_data)[-self.trend_config['min_data_points']:]
        
        for metric_name in self.metrics_config.keys():
            values = [entry.get(metric_name, 0) for entry in recent_data]
            
            if len(values) < 5:
                continue
            
            # Calculate trend
            trend_direction = self._calculate_trend_direction(values)
            trend_strength = self._calculate_trend_strength(values)
            
            # Check for concerning trends
            if trend_direction == 'increasing' and trend_strength > 0.7:
                alert = PerformanceAlert(
                    alert_id=f"trend_{metric_name}_{int(time.time())}",
                    level=AlertLevel.WARNING,
                    message=f"{metric_name} showing strong increasing trend (strength: {trend_strength:.2f})",
                    metric_name=metric_name,
                    current_value=values[-1],
                    threshold_value=0.0
                )
                alerts.append(alert)
        
        return alerts
    
    def _check_anomaly_alerts(self) -> List[PerformanceAlert]:
        """Check anomaly-based alerts."""
        alerts = []
        
        if len(self.performance_data) < 20:
            return alerts
        
        # Simple anomaly detection using statistical methods
        for metric_name in self.metrics_config.keys():
            values = [entry.get(metric_name, 0) for entry in self.performance_data]
            
            if len(values) < 20:
                continue
            
            # Calculate statistical thresholds
            mean_value = statistics.mean(values)
            std_value = statistics.stdev(values) if len(values) > 1 else 0
            
            if std_value == 0:
                continue
            
            # Check for anomalies (values beyond 2 standard deviations)
            latest_value = values[-1]
            z_score = abs((latest_value - mean_value) / std_value)
            
            if z_score > 2.0:  # Anomaly threshold
                alert = PerformanceAlert(
                    alert_id=f"anomaly_{metric_name}_{int(time.time())}",
                    level=AlertLevel.WARNING,
                    message=f"{metric_name} anomaly detected (z-score: {z_score:.2f})",
                    metric_name=metric_name,
                    current_value=latest_value,
                    threshold_value=mean_value + 2 * std_value
                )
                alerts.append(alert)
        
        return alerts
    
    def _check_capacity_alerts(self) -> List[PerformanceAlert]:
        """Check capacity-based alerts."""
        alerts = []
        
        if len(self.performance_data) == 0:
            return alerts
        
        latest_data = self.performance_data[-1]
        
        # Check memory usage
        memory_usage = latest_data.get('memory_usage_mb', 0)
        if memory_usage > 400:  # 400MB threshold
            alert = PerformanceAlert(
                alert_id=f"capacity_memory_{int(time.time())}",
                level=AlertLevel.WARNING,
                message=f"High memory usage: {memory_usage:.2f} MB",
                metric_name='memory_usage',
                current_value=memory_usage,
                threshold_value=400.0
            )
            alerts.append(alert)
        
        # Check CPU usage
        cpu_usage = latest_data.get('cpu_usage_percent', 0)
        if cpu_usage > 70:  # 70% threshold
            alert = PerformanceAlert(
                alert_id=f"capacity_cpu_{int(time.time())}",
                level=AlertLevel.WARNING,
                message=f"High CPU usage: {cpu_usage:.2f}%",
                metric_name='cpu_usage',
                current_value=cpu_usage,
                threshold_value=70.0
            )
            alerts.append(alert)
        
        return alerts
    
    def _analyze_trends(self):
        """Analyze performance trends."""
        if len(self.performance_data) < self.trend_config['min_data_points']:
            return
        
        try:
            # Analyze trends for each metric
            for metric_name in self.metrics_config.keys():
                trend_analysis = self._analyze_metric_trend(metric_name)
                if trend_analysis:
                    self.trend_analyses.append(trend_analysis)
            
        except Exception as e:
            self.logger.error(f"Trend analysis error: {e}")
    
    def _analyze_metric_trend(self, metric_name: str) -> Optional[TrendAnalysis]:
        """Analyze trend for a specific metric."""
        values = [entry.get(metric_name, 0) for entry in self.performance_data]
        
        if len(values) < self.trend_config['min_data_points']:
            return None
        
        # Calculate trend direction and strength
        trend_direction = self._calculate_trend_direction(values)
        trend_strength = self._calculate_trend_strength(values)
        
        # Calculate change percentage
        if len(values) >= 2:
            change_percentage = ((values[-1] - values[0]) / values[0]) * 100 if values[0] != 0 else 0
        else:
            change_percentage = 0
        
        # Calculate confidence
        confidence = min(trend_strength, 1.0)
        
        return TrendAnalysis(
            metric_name=metric_name,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            change_percentage=change_percentage,
            confidence=confidence,
            time_period=f"{len(values)} data points"
        )
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """Calculate trend direction."""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear regression slope
        x = list(range(len(values)))
        n = len(values)
        
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return 'stable'
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        
        if slope > 0.1:
            return 'increasing'
        elif slope < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def _calculate_trend_strength(self, values: List[float]) -> float:
        """Calculate trend strength (0-1)."""
        if len(values) < 3:
            return 0.0
        
        # Calculate R-squared for trend strength
        x = list(range(len(values)))
        n = len(values)
        
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        sum_y2 = sum(values[i] ** 2 for i in range(n))
        
        if n * sum_x2 - sum_x ** 2 == 0 or n * sum_y2 - sum_y ** 2 == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Calculate R-squared
        y_mean = sum_y / n
        ss_tot = sum((values[i] - y_mean) ** 2 for i in range(n))
        ss_res = sum((values[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
        
        if ss_tot == 0:
            return 0.0
        
        r_squared = 1 - (ss_res / ss_tot)
        return max(0.0, min(1.0, r_squared))
    
    def _generate_forecasts(self):
        """Generate performance forecasts."""
        if len(self.performance_data) < 20:
            return
        
        try:
            # Generate forecasts for key metrics
            forecast_metrics = ['response_time_ms', 'throughput_ops_per_sec', 'memory_usage_mb']
            
            for metric_name in forecast_metrics:
                forecast = self._generate_metric_forecast(metric_name)
                if forecast:
                    self.forecasts.append(forecast)
            
        except Exception as e:
            self.logger.error(f"Forecast generation error: {e}")
    
    def _generate_metric_forecast(self, metric_name: str) -> Optional[PerformanceForecast]:
        """Generate forecast for a specific metric."""
        values = [entry.get(metric_name, 0) for entry in self.performance_data]
        
        if len(values) < 10:
            return None
        
        # Simple linear forecast
        x = list(range(len(values)))
        n = len(values)
        
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return None
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Generate forecast for next 24 hours (assuming 5-second intervals)
        forecast_horizon = 24 * 60 * 60 // 5  # 24 hours in 5-second intervals
        forecast_values = []
        forecast_timestamps = []
        confidence_interval = []
        
        for i in range(1, forecast_horizon + 1):
            forecast_value = slope * (n + i) + intercept
            forecast_values.append(forecast_value)
            forecast_timestamps.append(datetime.now() + timedelta(seconds=i * 5))
            
            # Simple confidence interval (based on historical variance)
            historical_std = statistics.stdev(values) if len(values) > 1 else 0
            confidence_interval.append(historical_std * 1.96)  # 95% confidence
        
        return PerformanceForecast(
            metric_name=metric_name,
            forecast_values=forecast_values,
            forecast_timestamps=forecast_timestamps,
            confidence_interval=confidence_interval,
            forecast_horizon_hours=24
        )
    
    def _generate_recommendations(self):
        """Generate optimization recommendations."""
        try:
            # Analyze current performance and generate recommendations
            recommendations = []
            
            if len(self.performance_data) == 0:
                return
            
            latest_data = self.performance_data[-1]
            
            # Response time recommendations
            response_time = latest_data.get('response_time_ms', 0)
            if response_time > 150:
                recommendations.append(OptimizationRecommendation(
                    recommendation_id=f"response_time_{int(time.time())}",
                    priority='high',
                    category='performance',
                    description=f"Response time is {response_time:.2f}ms, consider query optimization",
                    expected_improvement=0.2,
                    implementation_effort='medium',
                    confidence=0.8
                ))
            
            # Memory usage recommendations
            memory_usage = latest_data.get('memory_usage_mb', 0)
            if memory_usage > 300:
                recommendations.append(OptimizationRecommendation(
                    recommendation_id=f"memory_usage_{int(time.time())}",
                    priority='medium',
                    category='resources',
                    description=f"Memory usage is {memory_usage:.2f}MB, consider memory optimization",
                    expected_improvement=0.15,
                    implementation_effort='low',
                    confidence=0.7
                ))
            
            # Cache hit rate recommendations
            cache_hit_rate = latest_data.get('cache_hit_rate', 0)
            if cache_hit_rate < 0.6:
                recommendations.append(OptimizationRecommendation(
                    recommendation_id=f"cache_optimization_{int(time.time())}",
                    priority='high',
                    category='caching',
                    description=f"Cache hit rate is {cache_hit_rate:.2%}, consider cache optimization",
                    expected_improvement=0.25,
                    implementation_effort='medium',
                    confidence=0.9
                ))
            
            self.recommendations.extend(recommendations)
            
        except Exception as e:
            self.logger.error(f"Recommendation generation error: {e}")
    
    def _update_analytics(self):
        """Update analytics and clean up old data."""
        # Keep only recent alerts (last 1000)
        if len(self.alerts) > 1000:
            self.alerts = self.alerts[-1000:]
        
        # Keep only recent trend analyses (last 100)
        if len(self.trend_analyses) > 100:
            self.trend_analyses = self.trend_analyses[-100:]
        
        # Keep only recent forecasts (last 50)
        if len(self.forecasts) > 50:
            self.forecasts = self.forecasts[-50:]
        
        # Keep only recent recommendations (last 200)
        if len(self.recommendations) > 200:
            self.recommendations = self.recommendations[-200:]
    
    def get_analytics_report(self) -> Dict[str, Any]:
        """Get comprehensive analytics report."""
        return {
            'analytics_status': 'active',
            'performance_data_points': len(self.performance_data),
            'active_alerts': len([a for a in self.alerts if not a.resolved]),
            'total_alerts': len(self.alerts),
            'trend_analyses': len(self.trend_analyses),
            'forecasts': len(self.forecasts),
            'recommendations': len(self.recommendations),
            'latest_performance': self.performance_data[-1] if self.performance_data else {},
            'recent_alerts': [a.__dict__ for a in self.alerts[-10:]],
            'recent_trends': [t.__dict__ for t in self.trend_analyses[-5:]],
            'recent_recommendations': [r.__dict__ for r in self.recommendations[-10:]],
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_performance_dashboard(self) -> Dict[str, Any]:
        """Generate performance dashboard data."""
        if len(self.performance_data) < 2:
            return {'error': 'Insufficient data for dashboard'}
        
        # Prepare data for visualization
        timestamps = [entry['timestamp'] for entry in self.performance_data]
        
        dashboard_data = {
            'timestamps': [ts.isoformat() for ts in timestamps],
            'metrics': {}
        }
        
        # Extract metrics for visualization
        for metric_name in self.metrics_config.keys():
            values = [entry.get(metric_name, 0) for entry in self.performance_data]
            dashboard_data['metrics'][metric_name] = {
                'values': values,
                'current': values[-1] if values else 0,
                'average': statistics.mean(values) if values else 0,
                'min': min(values) if values else 0,
                'max': max(values) if values else 0,
                'trend': self._calculate_trend_direction(values)
            }
        
        return dashboard_data
    
    def shutdown(self):
        """Shutdown analytics system."""
        self.analytics_active = False
        
        if hasattr(self, 'monitoring_thread'):
            self.monitoring_thread.join(timeout=5)
        
        if self.ml_optimizer:
            self.ml_optimizer.shutdown()
        
        self.logger.info("Vector Integration Analytics shutdown complete")


# ================================
# FACTORY FUNCTIONS
# ================================

def create_vector_integration_analytics(config: Optional[Dict[str, Any]] = None) -> VectorIntegrationAnalytics:
    """Create vector integration analytics instance."""
    return VectorIntegrationAnalytics(config)


def get_vector_integration_analytics() -> VectorIntegrationAnalytics:
    """Get singleton vector integration analytics instance."""
    if not hasattr(get_vector_integration_analytics, '_instance'):
        get_vector_integration_analytics._instance = create_vector_integration_analytics()
    return get_vector_integration_analytics._instance
