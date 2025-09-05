#!/usr/bin/env python3
"""
Vector Analytics Intelligence Orchestrator
==========================================

Main orchestrator for vector analytics intelligence system.
Coordinates business intelligence, pattern analysis, predictive modeling, and anomaly detection.
V2 COMPLIANT: Focused orchestration under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR ORCHESTRATOR
@license MIT
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from ..vector_analytics_models import (
    AnalyticsInsight, PatternMatch, PredictionResult, VectorAnalyticsConfig,
    AnalyticsMode, IntelligenceLevel
)
from .business_intelligence_engine import BusinessIntelligenceEngine, create_business_intelligence_engine
from .pattern_analysis_engine import PatternAnalysisEngine, create_pattern_analysis_engine
from .predictive_modeling_engine import PredictiveModelingEngine, create_predictive_modeling_engine
from .anomaly_detection_engine import AnomalyDetectionEngine, create_anomaly_detection_engine


class VectorAnalyticsIntelligenceOrchestrator:
    """Main orchestrator for vector analytics intelligence system"""
    
    def __init__(self, config: VectorAnalyticsConfig):
        """Initialize orchestrator with configuration and engines"""
        self.config = config
        self.intelligence_models: Dict[str, Any] = {}
        self.pattern_cache: Dict[str, List[PatternMatch]] = {}
        self.prediction_cache: Dict[str, List[PredictionResult]] = {}
        self.learning_data: Dict[str, List[Any]] = defaultdict(list)
        
        # Initialize engines
        self.business_intelligence_engine = create_business_intelligence_engine(config)
        self.pattern_analysis_engine = create_pattern_analysis_engine(config)
        self.predictive_modeling_engine = create_predictive_modeling_engine(config)
        self.anomaly_detection_engine = create_anomaly_detection_engine(config)
        
        # Initialize intelligence models
        self._initialize_intelligence_models()
    
    def _initialize_intelligence_models(self):
        """Initialize intelligence processing models"""
        self.intelligence_models = {
            'business_intelligence': self.business_intelligence_engine.create_business_intelligence_model(),
            'pattern_analysis': self.pattern_analysis_engine.create_pattern_analysis_model(),
            'predictive_modeling': self.predictive_modeling_engine.create_predictive_modeling_model(),
            'anomaly_detection': self.anomaly_detection_engine.create_anomaly_detection_model()
        }
    
    def process_business_intelligence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process business intelligence analysis"""
        try:
            # Extract metrics for analysis
            metrics = data.get('metrics', {})
            input_metrics = data.get('input_metrics', {})
            output_metrics = data.get('output_metrics', {})
            
            # Perform business intelligence analysis
            trend_analysis = self.business_intelligence_engine.detect_trends(data.get('trend_data', []))
            performance_analysis = self.business_intelligence_engine.analyze_performance(metrics)
            efficiency_analysis = self.business_intelligence_engine.calculate_efficiency(input_metrics, output_metrics)
            
            return {
                'trend_analysis': trend_analysis,
                'performance_analysis': performance_analysis,
                'efficiency_analysis': efficiency_analysis,
                'timestamp': datetime.now()
            }
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now()}
    
    def process_pattern_analysis(self, data: List[Any], pattern_type: str = 'behavioral') -> List[PatternMatch]:
        """Process pattern analysis"""
        try:
            patterns = self.pattern_analysis_engine.detect_patterns(data, pattern_type)
            
            # Cache patterns
            cache_key = f"{pattern_type}_{len(data)}"
            self.pattern_cache[cache_key] = patterns
            
            return patterns
        except Exception as e:
            return []
    
    def process_predictive_modeling(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process predictive modeling"""
        try:
            results = {}
            
            # Time series forecasting
            if 'timeseries_data' in data:
                forecast = self.predictive_modeling_engine.forecast_timeseries(
                    data['timeseries_data'], 
                    data.get('forecast_periods', 5)
                )
                results['timeseries_forecast'] = forecast
            
            # Trend prediction
            if 'trend_data' in data:
                trend_prediction = self.predictive_modeling_engine.predict_trends(data['trend_data'])
                results['trend_prediction'] = trend_prediction
            
            # Behavior prediction
            if 'behavior_data' in data:
                behavior_prediction = self.predictive_modeling_engine.predict_behavior(data['behavior_data'])
                results['behavior_prediction'] = behavior_prediction
            
            # Resource forecasting
            if 'resource_data' in data:
                resource_forecast = self.predictive_modeling_engine.forecast_resources(data['resource_data'])
                results['resource_forecast'] = resource_forecast
            
            return results
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now()}
    
    def process_anomaly_detection(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process anomaly detection"""
        try:
            results = {}
            
            # Statistical anomalies
            if 'statistical_data' in data:
                statistical_anomalies = self.anomaly_detection_engine.detect_statistical_anomalies(
                    data['statistical_data']
                )
                results['statistical_anomalies'] = statistical_anomalies
            
            # Behavioral anomalies
            if 'behavioral_data' in data:
                behavioral_anomalies = self.anomaly_detection_engine.detect_behavioral_anomalies(
                    data['behavioral_data']
                )
                results['behavioral_anomalies'] = behavioral_anomalies
            
            # Performance anomalies
            if 'performance_metrics' in data:
                performance_anomalies = self.anomaly_detection_engine.detect_performance_anomalies(
                    data['performance_metrics']
                )
                results['performance_anomalies'] = performance_anomalies
            
            # Trend anomalies
            if 'trend_data' in data:
                trend_anomalies = self.anomaly_detection_engine.detect_trend_anomalies(
                    data['trend_data']
                )
                results['trend_anomalies'] = trend_anomalies
            
            # Get anomaly summary
            all_anomalies = []
            for anomaly_list in results.values():
                if isinstance(anomaly_list, list):
                    all_anomalies.extend(anomaly_list)
            
            results['anomaly_summary'] = self.anomaly_detection_engine.get_anomaly_summary(all_anomalies)
            
            return results
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now()}
    
    def process_comprehensive_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process comprehensive intelligence analysis"""
        try:
            results = {
                'business_intelligence': self.process_business_intelligence(data),
                'pattern_analysis': {},
                'predictive_modeling': {},
                'anomaly_detection': {},
                'timestamp': datetime.now()
            }
            
            # Pattern analysis for different data types
            if 'behavioral_data' in data:
                results['pattern_analysis']['behavioral_patterns'] = self.process_pattern_analysis(
                    data['behavioral_data'], 'behavioral'
                )
            
            if 'temporal_data' in data:
                results['pattern_analysis']['temporal_patterns'] = self.process_pattern_analysis(
                    data['temporal_data'], 'temporal'
                )
            
            if 'frequency_data' in data:
                results['pattern_analysis']['frequency_patterns'] = self.process_pattern_analysis(
                    data['frequency_data'], 'frequency'
                )
            
            # Predictive modeling
            results['predictive_modeling'] = self.process_predictive_modeling(data)
            
            # Anomaly detection
            results['anomaly_detection'] = self.process_anomaly_detection(data)
            
            return results
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now()}
    
    def get_intelligence_summary(self) -> Dict[str, Any]:
        """Get comprehensive intelligence summary"""
        return {
            'models': list(self.intelligence_models.keys()),
            'pattern_cache_size': len(self.pattern_cache),
            'prediction_cache_size': len(self.prediction_cache),
            'learning_data_size': sum(len(data) for data in self.learning_data.values()),
            'capabilities': [
                model['capabilities'] for model in self.intelligence_models.values()
            ],
            'engine_status': {
                'business_intelligence': 'active',
                'pattern_analysis': 'active',
                'predictive_modeling': 'active',
                'anomaly_detection': 'active'
            }
        }
    
    def clear_caches(self):
        """Clear all caches"""
        self.pattern_cache.clear()
        self.prediction_cache.clear()
        self.learning_data.clear()
    
    def update_learning_data(self, data_type: str, data: List[Any]):
        """Update learning data for continuous improvement"""
        self.learning_data[data_type].extend(data)
        
        # Keep only recent data (last 1000 items per type)
        if len(self.learning_data[data_type]) > 1000:
            self.learning_data[data_type] = self.learning_data[data_type][-1000:]


# Factory function for dependency injection
def create_vector_analytics_intelligence_orchestrator(config: VectorAnalyticsConfig) -> VectorAnalyticsIntelligenceOrchestrator:
    """Factory function to create vector analytics intelligence orchestrator with configuration"""
    return VectorAnalyticsIntelligenceOrchestrator(config)


# Export for DI
__all__ = ['VectorAnalyticsIntelligenceOrchestrator', 'create_vector_analytics_intelligence_orchestrator']
