"""
Integration Optimizer - V2 Compliant Module
===========================================

Main optimizer for integration coordination.
Coordinates all optimizer components and provides unified interface.

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
from .basic_optimizer import BasicOptimizer
from .advanced_optimizer import AdvancedOptimizer
from .maximum_optimizer import MaximumOptimizer


class IntegrationOptimizer:
    """
    Main optimizer for integration coordination.
    
    Coordinates basic, advanced, and maximum optimization
    strategies for integration performance.
    """
    
    def __init__(self):
        """Initialize integration optimizer."""
        self.optimization_configs: Dict[IntegrationType, OptimizationConfig] = {}
        self.optimization_handlers: Dict[IntegrationType, Callable] = {}
        self.optimization_history: List[Dict[str, Any]] = []
        
        # Initialize component optimizers
        self.basic_optimizer = BasicOptimizer()
        self.advanced_optimizer = AdvancedOptimizer()
        self.maximum_optimizer = MaximumOptimizer()
    
    def register_optimization_config(self, config: OptimizationConfig) -> None:
        """Register optimization configuration."""
        self.optimization_configs[config.integration_type] = config
    
    def register_optimization_handler(
        self, 
        integration_type: IntegrationType, 
        handler: Callable
    ) -> None:
        """Register optimization handler."""
        self.optimization_handlers[integration_type] = handler
        self.maximum_optimizer.register_optimization_handler(integration_type, handler)
    
    def optimize_integration(
        self, 
        integration_type: IntegrationType,
        metrics: IntegrationMetrics
    ) -> Dict[str, Any]:
        """Optimize specific integration."""
        config = self.optimization_configs.get(integration_type)
        if not config:
            return {
                'success': False,
                'message': f'No configuration found for {integration_type.value}',
                'improvements': []
            }
        
        start_time = time.time()
        
        try:
            # Choose optimization level
            if config.optimization_level == OptimizationLevel.BASIC:
                improvements = self.basic_optimizer.optimize_integration(integration_type, metrics, config)
            elif config.optimization_level == OptimizationLevel.ADVANCED:
                improvements = self.advanced_optimizer.optimize_integration(integration_type, metrics, config)
            elif config.optimization_level == OptimizationLevel.MAXIMUM:
                improvements = self.maximum_optimizer.optimize_integration(integration_type, metrics, config)
            else:
                improvements = []
            
            execution_time = (time.time() - start_time) * 1000
            self._record_optimization(integration_type, improvements, execution_time)
            
            return {
                'success': True,
                'message': f'Optimization completed for {integration_type.value}',
                'improvements': improvements,
                'execution_time': execution_time
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                'success': False,
                'message': f'Optimization failed: {str(e)}',
                'improvements': []
            }
    
    def get_optimization_recommendations(
        self, 
        metrics: IntegrationMetrics
    ) -> List[OptimizationRecommendation]:
        """Get optimization recommendations."""
        recommendations = []
        
        # Get recommendations from all optimizers
        recommendations.extend(self.basic_optimizer.get_optimization_recommendations(metrics))
        recommendations.extend(self.advanced_optimizer.get_optimization_recommendations(metrics))
        recommendations.extend(self.maximum_optimizer.get_optimization_recommendations(metrics))
        
        return recommendations
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """Get optimization system status."""
        return {
            'registered_configs': len(self.optimization_configs),
            'registered_handlers': len(self.optimization_handlers),
            'optimization_history_count': len(self.optimization_history),
            'last_optimization': self.optimization_history[-1] if self.optimization_history else None,
            'component_status': {
                'basic_optimizer': self.basic_optimizer.get_optimizer_status(),
                'advanced_optimizer': self.advanced_optimizer.get_optimizer_status(),
                'maximum_optimizer': self.maximum_optimizer.get_optimizer_status()
            }
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
    
    def clear_optimization_history(self, days_to_keep: int = 7) -> int:
        """Clear old optimization history."""
        cutoff_time = datetime.now() - timedelta(days=days_to_keep)
        
        old_count = len(self.optimization_history)
        self.optimization_history = [
            record for record in self.optimization_history
            if datetime.fromisoformat(record['timestamp']) >= cutoff_time
        ]
        
        return old_count - len(self.optimization_history)
