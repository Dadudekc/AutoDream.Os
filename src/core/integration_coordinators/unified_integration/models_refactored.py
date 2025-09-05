"""
Integration Models Refactored - KISS Simplified
===============================================

Refactored data models for integration coordination.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined data modeling.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

# Import all integration models components
from .models_core import (
    IntegrationMetrics, OptimizationConfig, PerformanceReport, OptimizationRecommendation
)
from .models_config import (
    IntegrationConfig, IntegrationTask, IntegrationRequest, IntegrationResponse
)

# Re-export all public components for backward compatibility
__all__ = [
    # Core Models
    'IntegrationMetrics', 'OptimizationConfig', 'PerformanceReport', 'OptimizationRecommendation',
    # Config Models
    'IntegrationConfig', 'IntegrationTask', 'IntegrationRequest', 'IntegrationResponse'
]


class IntegrationModels:
    """Integration models factory and utilities."""
    
    @staticmethod
    def create_integration_metrics(integration_type, **kwargs):
        """Create integration metrics."""
        return IntegrationMetrics(integration_type=integration_type, **kwargs)
    
    @staticmethod
    def create_optimization_config(integration_type, optimization_level, **kwargs):
        """Create optimization config."""
        return OptimizationConfig(
            integration_type=integration_type,
            optimization_level=optimization_level,
            **kwargs
        )
    
    @staticmethod
    def create_performance_report(report_id, integration_type, period_start, period_end, **kwargs):
        """Create performance report."""
        return PerformanceReport(
            report_id=report_id,
            integration_type=integration_type,
            period_start=period_start,
            period_end=period_end,
            **kwargs
        )
    
    @staticmethod
    def create_integration_config(config_id, integration_type, name, description, **kwargs):
        """Create integration config."""
        return IntegrationConfig(
            config_id=config_id,
            integration_type=integration_type,
            name=name,
            description=description,
            **kwargs
        )
    
    @staticmethod
    def create_integration_task(task_id, integration_type, name, description, **kwargs):
        """Create integration task."""
        return IntegrationTask(
            task_id=task_id,
            integration_type=integration_type,
            name=name,
            description=description,
            **kwargs
        )
