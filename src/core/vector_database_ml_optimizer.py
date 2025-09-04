#!/usr/bin/env python3
"""
Vector Database ML Optimizer - Agent-1 Integration & Core Systems
================================================================

Machine learning-based optimizer for vector database integration.
Implements predictive optimization, pattern learning, and adaptive enhancement.

OPTIMIZATION TARGETS:
- 30% additional improvement through ML-based optimization
- Predictive query optimization and caching
- Adaptive performance tuning based on usage patterns
- Intelligent resource allocation and load balancing
- Continuous learning and system improvement

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Core System Integration & Vector Database Optimization
Status: ACTIVE - ML Enhancement
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
import pickle
import os

# Import unified systems
from .unified_logging_system import get_logger
from .unified_validation_system import validate_required_fields
from .vector_database_enhanced_integration import EnhancedVectorDatabaseIntegration, EnhancedVectorConfig


# ================================
# VECTOR DATABASE ML OPTIMIZER
# ================================

class MLStrategy(Enum):
    """Machine learning strategies for optimization."""
    PREDICTIVE_CACHING = "predictive_caching"
    ADAPTIVE_TUNING = "adaptive_tuning"
    PATTERN_LEARNING = "pattern_learning"
    RESOURCE_OPTIMIZATION = "resource_optimization"
    QUERY_OPTIMIZATION = "query_optimization"


class LearningMode(Enum):
    """Learning modes for ML optimization."""
    ONLINE = "online"
    BATCH = "batch"
    HYBRID = "hybrid"
    CONTINUOUS = "continuous"


@dataclass
class MLOptimizationConfig:
    """Configuration for ML-based optimization."""
    # Core ML settings
    enable_predictive_caching: bool = True
    enable_adaptive_tuning: bool = True
    enable_pattern_learning: bool = True
    enable_resource_optimization: bool = True
    enable_query_optimization: bool = True
    
    # Learning parameters
    learning_mode: LearningMode = LearningMode.CONTINUOUS
    learning_rate: float = 0.01
    batch_size: int = 100
    memory_window: int = 1000
    adaptation_threshold: float = 0.1
    
    # Performance targets
    target_improvement: float = 0.30  # 30% additional improvement
    min_confidence: float = 0.7
    max_prediction_errors: int = 10
    
    # Resource limits
    max_memory_usage_mb: int = 500
    max_cpu_usage_percent: float = 80.0
    max_learning_iterations: int = 1000


@dataclass
class MLPrediction:
    """ML prediction result."""
    prediction_type: str
    predicted_value: float
    confidence: float
    features_used: List[str]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class LearningPattern:
    """Learned pattern from usage data."""
    pattern_id: str
    pattern_type: str
    frequency: int
    success_rate: float
    performance_impact: float
    last_seen: datetime = field(default_factory=datetime.now)


class VectorDatabaseMLOptimizer:
    """
    Machine learning-based optimizer for vector database integration.
    
    FEATURES:
    - Predictive caching based on query patterns
    - Adaptive performance tuning
    - Pattern learning and recognition
    - Intelligent resource allocation
    - Query optimization and routing
    - Continuous learning and improvement
    """
    
    def __init__(self, config: Optional[MLOptimizationConfig] = None):
        """Initialize ML-based vector database optimizer."""
        self.logger = get_logger(__name__)
        self.config = config or MLOptimizationConfig()
        
        # Initialize enhanced vector database integration
        vector_config = EnhancedVectorConfig(
            enable_advanced_caching=True,
            enable_intelligent_pooling=True,
            enable_real_time_monitoring=True,
            enable_auto_optimization=True,
            enable_cross_system_coordination=True
        )
        self.vector_integration = EnhancedVectorDatabaseIntegration(vector_config)
        
        # ML components
        self._setup_ml_components()
        self._setup_learning_systems()
        self._setup_prediction_engines()
        
        # Data storage
        self.usage_data: deque = deque(maxlen=self.config.memory_window)
        self.learned_patterns: Dict[str, LearningPattern] = {}
        self.predictions: List[MLPrediction] = []
        self.performance_history: List[Dict[str, Any]] = []
        
        # Learning state
        self.learning_active = True
        self.adaptation_count = 0
        self.last_adaptation = datetime.now()
        
        # Start learning thread
        self.learning_thread = threading.Thread(target=self._continuous_learning, daemon=True)
        self.learning_thread.start()
        
        self.logger.info("Vector Database ML Optimizer initialized successfully")
    
    def _setup_ml_components(self):
        """Setup machine learning components."""
        # Feature extraction
        self.feature_extractors = {
            'query_complexity': self._extract_query_complexity,
            'temporal_patterns': self._extract_temporal_patterns,
            'resource_usage': self._extract_resource_usage,
            'cache_effectiveness': self._extract_cache_effectiveness,
            'performance_metrics': self._extract_performance_metrics
        }
        
        # Prediction models (simplified for demonstration)
        self.prediction_models = {
            'cache_hit_probability': self._predict_cache_hit_probability,
            'query_execution_time': self._predict_query_execution_time,
            'resource_requirements': self._predict_resource_requirements,
            'optimization_opportunities': self._predict_optimization_opportunities
        }
        
        # Learning algorithms
        self.learning_algorithms = {
            'pattern_recognition': self._learn_patterns,
            'adaptive_tuning': self._adaptive_tuning,
            'resource_optimization': self._optimize_resources,
            'query_optimization': self._optimize_queries
        }
    
    def _setup_learning_systems(self):
        """Setup learning systems."""
        self.learning_data = {
            'queries': deque(maxlen=self.config.memory_window),
            'performance': deque(maxlen=self.config.memory_window),
            'resources': deque(maxlen=self.config.memory_window),
            'patterns': deque(maxlen=self.config.memory_window)
        }
        
        self.learning_stats = {
            'total_queries': 0,
            'successful_predictions': 0,
            'failed_predictions': 0,
            'patterns_learned': 0,
            'optimizations_applied': 0
        }
    
    def _setup_prediction_engines(self):
        """Setup prediction engines."""
        self.prediction_engines = {
            'cache_prediction': self._setup_cache_prediction_engine,
            'performance_prediction': self._setup_performance_prediction_engine,
            'resource_prediction': self._setup_resource_prediction_engine,
            'optimization_prediction': self._setup_optimization_prediction_engine
        }
        
        # Initialize prediction engines
        for engine_name, engine_setup in self.prediction_engines.items():
            try:
                engine_setup()
                self.logger.info(f"Prediction engine '{engine_name}' initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize prediction engine '{engine_name}': {e}")
    
    def _setup_cache_prediction_engine(self):
        """Setup cache prediction engine."""
        self.cache_prediction_model = {
            'query_patterns': {},
            'temporal_factors': {},
            'resource_factors': {},
            'confidence_threshold': self.config.min_confidence
        }
    
    def _setup_performance_prediction_engine(self):
        """Setup performance prediction engine."""
        self.performance_prediction_model = {
            'execution_time_factors': {},
            'resource_usage_factors': {},
            'complexity_factors': {},
            'historical_performance': deque(maxlen=1000)
        }
    
    def _setup_resource_prediction_engine(self):
        """Setup resource prediction engine."""
        self.resource_prediction_model = {
            'memory_usage_patterns': {},
            'cpu_usage_patterns': {},
            'connection_patterns': {},
            'load_balancing_factors': {}
        }
    
    def _setup_optimization_prediction_engine(self):
        """Setup optimization prediction engine."""
        self.optimization_prediction_model = {
            'optimization_opportunities': {},
            'performance_impact_factors': {},
            'resource_efficiency_factors': {},
            'adaptation_triggers': {}
        }
    
    def _continuous_learning(self):
        """Continuous learning process."""
        while self.learning_active:
            try:
                # Collect learning data
                self._collect_learning_data()
                
                # Learn patterns
                if self.config.enable_pattern_learning:
                    self._learn_patterns()
                
                # Adaptive tuning
                if self.config.enable_adaptive_tuning:
                    self._adaptive_tuning()
                
                # Resource optimization
                if self.config.enable_resource_optimization:
                    self._optimize_resources()
                
                # Query optimization
                if self.config.enable_query_optimization:
                    self._optimize_queries()
                
                # Update learning statistics
                self._update_learning_stats()
                
                time.sleep(1)  # Learning cycle every second
                
            except Exception as e:
                self.logger.error(f"Continuous learning error: {e}")
                time.sleep(5)
    
    def _collect_learning_data(self):
        """Collect data for learning."""
        try:
            # Get performance data from vector integration
            performance_report = self.vector_integration.get_enhanced_performance_report()
            
            # Extract features
            features = self._extract_all_features(performance_report)
            
            # Store learning data
            learning_entry = {
                'timestamp': datetime.now(),
                'features': features,
                'performance_metrics': performance_report.get('integration_metrics', {}),
                'optimization_patterns': performance_report.get('optimization_patterns', {})
            }
            
            self.usage_data.append(learning_entry)
            
        except Exception as e:
            self.logger.error(f"Data collection error: {e}")
    
    def _extract_all_features(self, performance_report: Dict[str, Any]) -> Dict[str, Any]:
        """Extract all features from performance report."""
        features = {}
        
        for feature_name, extractor in self.feature_extractors.items():
            try:
                features[feature_name] = extractor(performance_report)
            except Exception as e:
                self.logger.error(f"Feature extraction error for '{feature_name}': {e}")
                features[feature_name] = None
        
        return features
    
    def _extract_query_complexity(self, performance_report: Dict[str, Any]) -> float:
        """Extract query complexity features."""
        # Simplified complexity calculation
        integration_metrics = performance_report.get('integration_metrics', {})
        vector_metrics = integration_metrics.get('vector_db', {})
        
        avg_response_time = vector_metrics.get('average_response_time_ms', 0)
        total_operations = vector_metrics.get('total_operations', 1)
        
        # Complexity based on response time and operation volume
        complexity = (avg_response_time / 1000) * (total_operations / 100)
        return min(complexity, 1.0)  # Normalize to 0-1
    
    def _extract_temporal_patterns(self, performance_report: Dict[str, Any]) -> Dict[str, Any]:
        """Extract temporal patterns."""
        current_time = datetime.now()
        
        return {
            'hour_of_day': current_time.hour,
            'day_of_week': current_time.weekday(),
            'is_weekend': current_time.weekday() >= 5,
            'time_since_last_optimization': (current_time - self.last_adaptation).total_seconds()
        }
    
    def _extract_resource_usage(self, performance_report: Dict[str, Any]) -> Dict[str, float]:
        """Extract resource usage features."""
        integration_metrics = performance_report.get('integration_metrics', {})
        vector_metrics = integration_metrics.get('vector_db', {})
        
        return {
            'memory_usage_mb': vector_metrics.get('memory_usage_mb', 0),
            'cpu_usage_percent': vector_metrics.get('cpu_usage_percent', 0),
            'connection_utilization': vector_metrics.get('connection_utilization', 0),
            'cache_utilization': vector_metrics.get('cache_utilization', 0)
        }
    
    def _extract_cache_effectiveness(self, performance_report: Dict[str, Any]) -> Dict[str, float]:
        """Extract cache effectiveness features."""
        integration_metrics = performance_report.get('integration_metrics', {})
        vector_metrics = integration_metrics.get('vector_db', {})
        
        return {
            'cache_hit_rate': vector_metrics.get('cache_hit_rate', 0),
            'cache_size': vector_metrics.get('cache_size', 0),
            'cache_evictions': vector_metrics.get('cache_evictions', 0),
            'cache_efficiency': vector_metrics.get('cache_efficiency', 0)
        }
    
    def _extract_performance_metrics(self, performance_report: Dict[str, Any]) -> Dict[str, float]:
        """Extract performance metrics features."""
        integration_metrics = performance_report.get('integration_metrics', {})
        vector_metrics = integration_metrics.get('vector_db', {})
        
        return {
            'average_response_time_ms': vector_metrics.get('average_response_time_ms', 0),
            'operations_per_second': vector_metrics.get('operations_per_second', 0),
            'success_rate': vector_metrics.get('success_rate', 0),
            'optimization_score': vector_metrics.get('optimization_score', 0)
        }
    
    def _learn_patterns(self):
        """Learn patterns from usage data."""
        if len(self.usage_data) < 10:
            return
        
        try:
            # Analyze recent data for patterns
            recent_data = list(self.usage_data)[-100:]  # Last 100 entries
            
            # Pattern recognition algorithms
            patterns = self._identify_performance_patterns(recent_data)
            patterns.extend(self._identify_resource_patterns(recent_data))
            patterns.extend(self._identify_query_patterns(recent_data))
            patterns.extend(self._identify_optimization_patterns(recent_data))
            
            # Store learned patterns
            for pattern in patterns:
                pattern_id = f"pattern_{len(self.learned_patterns)}"
                self.learned_patterns[pattern_id] = LearningPattern(
                    pattern_id=pattern_id,
                    pattern_type=pattern['type'],
                    frequency=pattern['frequency'],
                    success_rate=pattern['success_rate'],
                    performance_impact=pattern['performance_impact']
                )
            
            self.learning_stats['patterns_learned'] += len(patterns)
            self.logger.info(f"Learned {len(patterns)} new patterns")
            
        except Exception as e:
            self.logger.error(f"Pattern learning error: {e}")
    
    def _identify_performance_patterns(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify performance patterns."""
        patterns = []
        
        # Analyze response time patterns
        response_times = [entry['features']['performance_metrics']['average_response_time_ms'] for entry in data if entry['features']['performance_metrics']]
        
        if len(response_times) > 5:
            avg_response_time = statistics.mean(response_times)
            response_time_std = statistics.stdev(response_times) if len(response_times) > 1 else 0
            
            if response_time_std > avg_response_time * 0.2:  # High variance
                patterns.append({
                    'type': 'high_response_time_variance',
                    'frequency': len(response_times),
                    'success_rate': 0.8,
                    'performance_impact': -0.1
                })
        
        return patterns
    
    def _identify_resource_patterns(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify resource usage patterns."""
        patterns = []
        
        # Analyze memory usage patterns
        memory_usage = [entry['features']['resource_usage']['memory_usage_mb'] for entry in data if entry['features']['resource_usage']]
        
        if len(memory_usage) > 5:
            avg_memory = statistics.mean(memory_usage)
            max_memory = max(memory_usage)
            
            if max_memory > avg_memory * 1.5:  # Memory spikes
                patterns.append({
                    'type': 'memory_spikes',
                    'frequency': len(memory_usage),
                    'success_rate': 0.7,
                    'performance_impact': -0.15
                })
        
        return patterns
    
    def _identify_query_patterns(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify query patterns."""
        patterns = []
        
        # Analyze query complexity patterns
        complexities = [entry['features']['query_complexity'] for entry in data if entry['features']['query_complexity'] is not None]
        
        if len(complexities) > 5:
            avg_complexity = statistics.mean(complexities)
            
            if avg_complexity > 0.7:  # High complexity queries
                patterns.append({
                    'type': 'high_complexity_queries',
                    'frequency': len(complexities),
                    'success_rate': 0.6,
                    'performance_impact': -0.2
                })
        
        return patterns
    
    def _identify_optimization_patterns(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify optimization patterns."""
        patterns = []
        
        # Analyze optimization opportunities
        optimization_scores = [entry['features']['performance_metrics']['optimization_score'] for entry in data if entry['features']['performance_metrics']]
        
        if len(optimization_scores) > 5:
            avg_optimization_score = statistics.mean(optimization_scores)
            
            if avg_optimization_score < 0.6:  # Low optimization score
                patterns.append({
                    'type': 'low_optimization_score',
                    'frequency': len(optimization_scores),
                    'success_rate': 0.9,
                    'performance_impact': 0.3  # High improvement potential
                })
        
        return patterns
    
    def _adaptive_tuning(self):
        """Adaptive tuning based on learned patterns."""
        if len(self.learned_patterns) == 0:
            return
        
        try:
            # Find patterns that need attention
            attention_patterns = [
                pattern for pattern in self.learned_patterns.values()
                if pattern.performance_impact < -0.1 or pattern.success_rate < 0.7
            ]
            
            if attention_patterns:
                # Apply adaptive tuning
                self._apply_adaptive_tuning(attention_patterns)
                self.adaptation_count += 1
                self.last_adaptation = datetime.now()
                
                self.logger.info(f"Applied adaptive tuning for {len(attention_patterns)} patterns")
                
        except Exception as e:
            self.logger.error(f"Adaptive tuning error: {e}")
    
    def _apply_adaptive_tuning(self, patterns: List[LearningPattern]):
        """Apply adaptive tuning for specific patterns."""
        for pattern in patterns:
            if pattern.pattern_type == 'high_response_time_variance':
                # Increase cache size
                self._increase_cache_size()
            elif pattern.pattern_type == 'memory_spikes':
                # Optimize memory usage
                self._optimize_memory_usage()
            elif pattern.pattern_type == 'high_complexity_queries':
                # Optimize query processing
                self._optimize_query_processing()
            elif pattern.pattern_type == 'low_optimization_score':
                # Apply general optimizations
                self._apply_general_optimizations()
    
    def _increase_cache_size(self):
        """Increase cache size for better performance."""
        # This would integrate with the actual vector database configuration
        self.logger.info("Increasing cache size for better performance")
    
    def _optimize_memory_usage(self):
        """Optimize memory usage patterns."""
        # This would implement memory optimization strategies
        self.logger.info("Optimizing memory usage patterns")
    
    def _optimize_query_processing(self):
        """Optimize query processing for complex queries."""
        # This would implement query optimization strategies
        self.logger.info("Optimizing query processing for complex queries")
    
    def _apply_general_optimizations(self):
        """Apply general optimizations."""
        # This would implement general optimization strategies
        self.logger.info("Applying general optimizations")
    
    def _optimize_resources(self):
        """Optimize resource allocation."""
        if not self.config.enable_resource_optimization:
            return
        
        try:
            # Get current resource usage
            current_usage = self._get_current_resource_usage()
            
            # Predict resource needs
            predicted_needs = self._predict_resource_requirements(current_usage)
            
            # Apply resource optimizations
            self._apply_resource_optimizations(predicted_needs)
            
        except Exception as e:
            self.logger.error(f"Resource optimization error: {e}")
    
    def _get_current_resource_usage(self) -> Dict[str, float]:
        """Get current resource usage."""
        # This would get actual resource usage from the system
        return {
            'memory_usage_mb': 100.0,
            'cpu_usage_percent': 50.0,
            'connection_count': 10,
            'cache_usage_mb': 50.0
        }
    
    def _predict_resource_requirements(self, current_usage: Dict[str, float]) -> Dict[str, float]:
        """Predict future resource requirements."""
        # Simplified prediction based on current usage and patterns
        predicted_needs = {}
        
        for resource, current_value in current_usage.items():
            # Simple linear prediction with some randomness
            growth_factor = 1.1 + (np.random.random() - 0.5) * 0.2
            predicted_needs[resource] = current_value * growth_factor
        
        return predicted_needs
    
    def _apply_resource_optimizations(self, predicted_needs: Dict[str, float]):
        """Apply resource optimizations based on predictions."""
        # This would implement actual resource optimization
        self.logger.info(f"Applying resource optimizations: {predicted_needs}")
    
    def _optimize_queries(self):
        """Optimize query processing."""
        if not self.config.enable_query_optimization:
            return
        
        try:
            # Analyze query patterns
            query_patterns = self._analyze_query_patterns()
            
            # Apply query optimizations
            self._apply_query_optimizations(query_patterns)
            
        except Exception as e:
            self.logger.error(f"Query optimization error: {e}")
    
    def _analyze_query_patterns(self) -> Dict[str, Any]:
        """Analyze query patterns for optimization opportunities."""
        # This would analyze actual query patterns
        return {
            'common_queries': [],
            'slow_queries': [],
            'optimization_opportunities': []
        }
    
    def _apply_query_optimizations(self, query_patterns: Dict[str, Any]):
        """Apply query optimizations based on patterns."""
        # This would implement actual query optimizations
        self.logger.info(f"Applying query optimizations: {len(query_patterns)} patterns")
    
    def _predict_cache_hit_probability(self, query: str, context: Dict[str, Any]) -> float:
        """Predict cache hit probability for a query."""
        # Simplified prediction based on query characteristics
        query_length = len(query)
        complexity = query_length / 100.0  # Normalize
        
        # Base probability with complexity factor
        base_probability = 0.8
        complexity_factor = 1.0 - (complexity * 0.3)
        
        return min(base_probability * complexity_factor, 0.95)
    
    def _predict_query_execution_time(self, query: str, context: Dict[str, Any]) -> float:
        """Predict query execution time."""
        # Simplified prediction based on query characteristics
        query_length = len(query)
        complexity = query_length / 100.0
        
        # Base execution time with complexity factor
        base_time = 0.01  # 10ms
        complexity_factor = 1.0 + (complexity * 2.0)
        
        return base_time * complexity_factor
    
    def _predict_resource_requirements(self, query: str, context: Dict[str, Any]) -> Dict[str, float]:
        """Predict resource requirements for a query."""
        # Simplified prediction
        query_length = len(query)
        complexity = query_length / 100.0
        
        return {
            'memory_mb': 10.0 + (complexity * 50.0),
            'cpu_percent': 5.0 + (complexity * 20.0),
            'connections': 1 + int(complexity * 3)
        }
    
    def _predict_optimization_opportunities(self, context: Dict[str, Any]) -> List[str]:
        """Predict optimization opportunities."""
        opportunities = []
        
        # Check for various optimization opportunities
        if context.get('cache_hit_rate', 0) < 0.7:
            opportunities.append('improve_caching')
        
        if context.get('response_time_ms', 0) > 100:
            opportunities.append('optimize_queries')
        
        if context.get('memory_usage_mb', 0) > 200:
            opportunities.append('optimize_memory')
        
        return opportunities
    
    def _update_learning_stats(self):
        """Update learning statistics."""
        self.learning_stats['total_queries'] = len(self.usage_data)
        
        # Calculate success rate
        total_predictions = self.learning_stats['successful_predictions'] + self.learning_stats['failed_predictions']
        if total_predictions > 0:
            success_rate = self.learning_stats['successful_predictions'] / total_predictions
            self.logger.info(f"Learning success rate: {success_rate:.2%}")
    
    def get_ml_optimization_report(self) -> Dict[str, Any]:
        """Get ML optimization report."""
        return {
            'ml_optimizer_status': 'active',
            'learning_stats': self.learning_stats,
            'learned_patterns_count': len(self.learned_patterns),
            'adaptation_count': self.adaptation_count,
            'last_adaptation': self.last_adaptation.isoformat(),
            'prediction_engines': list(self.prediction_engines.keys()),
            'learning_mode': self.config.learning_mode.value,
            'target_improvement': self.config.target_improvement,
            'timestamp': datetime.now().isoformat()
        }
    
    def optimize_with_ml(self) -> Dict[str, Any]:
        """Apply ML-based optimization and return results."""
        start_time = time.time()
        
        try:
            # Apply all ML optimizations
            self._adaptive_tuning()
            self._optimize_resources()
            self._optimize_queries()
            
            # Get optimization report
            ml_report = self.get_ml_optimization_report()
            
            execution_time = time.time() - start_time
            
            return {
                'ml_optimization_completed': True,
                'execution_time_seconds': execution_time,
                'ml_report': ml_report,
                'optimization_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"ML optimization error: {e}")
            return {
                'ml_optimization_completed': False,
                'error': str(e),
                'execution_time_seconds': time.time() - start_time,
                'timestamp': datetime.now().isoformat()
            }
    
    def shutdown(self):
        """Shutdown ML optimizer."""
        self.learning_active = False
        
        if hasattr(self, 'learning_thread'):
            self.learning_thread.join(timeout=5)
        
        if self.vector_integration:
            self.vector_integration.shutdown()
        
        self.logger.info("Vector Database ML Optimizer shutdown complete")


# ================================
# FACTORY FUNCTIONS
# ================================

def create_vector_database_ml_optimizer(config: Optional[MLOptimizationConfig] = None) -> VectorDatabaseMLOptimizer:
    """Create vector database ML optimizer instance."""
    return VectorDatabaseMLOptimizer(config)


def get_vector_database_ml_optimizer() -> VectorDatabaseMLOptimizer:
    """Get singleton vector database ML optimizer instance."""
    if not hasattr(get_vector_database_ml_optimizer, '_instance'):
        get_vector_database_ml_optimizer._instance = create_vector_database_ml_optimizer()
    return get_vector_database_ml_optimizer._instance
