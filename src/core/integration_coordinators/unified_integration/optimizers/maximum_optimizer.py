"""Maximum optimizer providing advanced optimization techniques."""

from typing import Any, Callable, Dict, List

from ..models import (
    IntegrationType, IntegrationMetrics,
    OptimizationConfig, PerformanceReport, OptimizationRecommendation,
    IntegrationModels
)
from .advanced_optimizer import AdvancedOptimizer
from .base_optimization_history import BaseOptimizationHistory


class MaximumOptimizer(BaseOptimizationHistory):
    """Handles maximum optimization strategies and custom optimizations."""

    def __init__(self) -> None:
        super().__init__()
        self.advanced_optimizer = AdvancedOptimizer()
        self.optimization_handlers: Dict[IntegrationType, Callable] = {}
    
    def register_optimization_handler(
        self, 
        integration_type: IntegrationType, 
        handler: Callable
    ) -> None:
        """Register optimization handler."""
        self.optimization_handlers[integration_type] = handler
    
    def optimize_integration(
        self, 
        integration_type: IntegrationType,
        metrics: IntegrationMetrics,
        config: OptimizationConfig
    ) -> List[Dict[str, Any]]:
        """Perform maximum optimization."""
        improvements = self.advanced_optimizer.optimize_integration(integration_type, metrics, config)
        
        # Custom optimization handler
        if integration_type in self.optimization_handlers:
            try:
                custom_improvements = self.optimization_handlers[integration_type](metrics, config)
                improvements.extend(custom_improvements)
            except Exception:
                pass  # Continue with standard optimizations
        
        # Circuit breaker pattern
        if metrics.error_rate > 0.1:
            improvements.append({
                'type': 'circuit_breaker',
                'description': 'Implement circuit breaker pattern',
                'expected_improvement': 0.7
            })
        
        # Asynchronous processing
        if metrics.average_response_time > 2.0:
            improvements.append({
                'type': 'async_processing',
                'description': 'Implement asynchronous processing',
                'expected_improvement': 0.8
            })
        
        # Database connection pooling
        if metrics.average_response_time > 1.0:
            improvements.append({
                'type': 'db_connection_pooling',
                'description': 'Implement database connection pooling',
                'expected_improvement': 0.6
            })
        
        return improvements
    
    def get_optimization_recommendations(
        self, 
        metrics: IntegrationMetrics
    ) -> List[OptimizationRecommendation]:
        """Get optimization recommendations."""
        recommendations = self.advanced_optimizer.get_optimization_recommendations(metrics)
        
        # Circuit breaker recommendation
        if metrics.error_rate > 0.1:
            recommendations.append(IntegrationModels.create_optimization_recommendation(
                integration_type=IntegrationType.API,
                optimization_type='circuit_breaker',
                description='Implement circuit breaker pattern',
                expected_improvement=0.7,
                priority=1,
                implementation_cost='high'
            ))
        
        # Asynchronous processing recommendation
        if metrics.average_response_time > 2.0:
            recommendations.append(IntegrationModels.create_optimization_recommendation(
                integration_type=IntegrationType.API,
                optimization_type='async_processing',
                description='Implement asynchronous processing',
                expected_improvement=0.8,
                priority=1,
                implementation_cost='high'
            ))
        
        # Parallel processing recommendation
        if metrics.throughput < 10.0:
            recommendations.append(IntegrationModels.create_optimization_recommendation(
                integration_type=IntegrationType.API,
                optimization_type='parallel_processing',
                description='Increase throughput with parallel processing',
                expected_improvement=0.6,
                priority=3,
                implementation_cost='high'
            ))
        
        return recommendations
    
    def get_optimizer_status(self) -> Dict[str, Any]:
        """Get optimizer status."""
        return {
            'optimization_history_count': len(self.optimization_history),
            'last_optimization': self.optimization_history[-1] if self.optimization_history else None,
            'registered_handlers': len(self.optimization_handlers),
            'advanced_optimizer_status': self.advanced_optimizer.get_optimizer_status()
        }

    def _record_optimization(
        self,
        integration_type: IntegrationType,
        improvements: List[Dict[str, Any]],
        execution_time: float,
    ) -> None:
        """Record optimization execution with level metadata."""
        super()._record_optimization(
            integration_type,
            improvements,
            execution_time,
            extra_fields={'optimization_level': 'maximum'},
        )
