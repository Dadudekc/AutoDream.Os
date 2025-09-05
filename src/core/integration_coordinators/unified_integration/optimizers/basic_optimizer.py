"""
Basic Optimizer - V2 Compliant Module
====================================

Handles basic optimization strategies.
Extracted from optimizer.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta

from ..models import (
    IntegrationType, OptimizationLevel, IntegrationMetrics,
    OptimizationConfig, PerformanceReport, OptimizationRecommendation,
    IntegrationModels
)


class BasicOptimizer:
    """
    Handles basic optimization strategies.
    
    Manages basic optimization techniques like caching,
    concurrency control, and simple performance improvements.
    """
    
    def __init__(self):
        """Initialize basic optimizer."""
        self.optimization_history: List[Dict[str, Any]] = []
    
    def optimize_integration(
        self, 
        integration_type: IntegrationType,
        metrics: IntegrationMetrics,
        config: OptimizationConfig
    ) -> List[Dict[str, Any]]:
        """Perform basic optimization."""
        improvements = []
        
        # Enable caching if not already enabled
        if not config.cache_enabled and metrics.average_response_time > 1.0:
            improvements.append({
                'type': 'enable_caching',
                'description': 'Enable caching to improve response time',
                'expected_improvement': 0.3
            })
        
        # Reduce concurrent requests if error rate is high
        if metrics.error_rate > 0.05 and config.max_concurrent_requests > 50:
            improvements.append({
                'type': 'reduce_concurrency',
                'description': 'Reduce concurrent requests to lower error rate',
                'expected_improvement': 0.2
            })
        
        # Increase timeout if response time is high
        if metrics.average_response_time > 2.0 and config.timeout_seconds < 30:
            improvements.append({
                'type': 'increase_timeout',
                'description': 'Increase timeout to handle slow responses',
                'expected_improvement': 0.1
            })
        
        # Enable retries if error rate is moderate
        if metrics.error_rate > 0.02 and config.max_retries < 3:
            improvements.append({
                'type': 'enable_retries',
                'description': 'Enable retries for failed requests',
                'expected_improvement': 0.15
            })
        
        return improvements
    
    def get_optimization_recommendations(
        self, 
        metrics: IntegrationMetrics
    ) -> List[OptimizationRecommendation]:
        """Get optimization recommendations."""
        recommendations = []
        
        # Caching recommendation
        if metrics.average_response_time > 1.0:
            recommendations.append(IntegrationModels.create_optimization_recommendation(
                integration_type=IntegrationType.API,
                optimization_type='enable_caching',
                description='Enable caching to improve response time',
                expected_improvement=0.3,
                priority=1,
                implementation_cost='low'
            ))
        
        # Concurrency recommendation
        if metrics.error_rate > 0.05:
            recommendations.append(IntegrationModels.create_optimization_recommendation(
                integration_type=IntegrationType.API,
                optimization_type='reduce_concurrency',
                description='Reduce concurrent requests to lower error rate',
                expected_improvement=0.2,
                priority=2,
                implementation_cost='low'
            ))
        
        # Timeout recommendation
        if metrics.average_response_time > 2.0:
            recommendations.append(IntegrationModels.create_optimization_recommendation(
                integration_type=IntegrationType.API,
                optimization_type='increase_timeout',
                description='Increase timeout to handle slow responses',
                expected_improvement=0.1,
                priority=3,
                implementation_cost='low'
            ))
        
        return recommendations
    
    def get_optimizer_status(self) -> Dict[str, Any]:
        """Get optimizer status."""
        return {
            'optimization_history_count': len(self.optimization_history),
            'last_optimization': self.optimization_history[-1] if self.optimization_history else None
        }
    
    def _record_optimization(
        self, 
        integration_type: IntegrationType,
        improvements: List[Dict[str, Any]],
        execution_time: float
    ) -> None:
        """Record optimization execution."""
        self.optimization_history.append({
            'timestamp': datetime.now().isoformat(),
            'integration_type': integration_type.value,
            'optimization_level': 'basic',
            'improvements_count': len(improvements),
            'execution_time': execution_time,
            'improvements': improvements
        })
        
        # Keep only last 100 optimizations
        if len(self.optimization_history) > 100:
            self.optimization_history = self.optimization_history[-100:]
    
    def get_optimization_history(
        self, 
        integration_type: Optional[IntegrationType] = None,
        hours: int = 24
    ) -> List[Dict[str, Any]]:
        """Get optimization history."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        history = self.optimization_history
        
        if integration_type:
            history = [
                record for record in history
                if record['integration_type'] == integration_type.value
            ]
        
        # Filter by time
        history = [
            record for record in history
            if datetime.fromisoformat(record['timestamp']) >= cutoff_time
        ]
        
        return history
