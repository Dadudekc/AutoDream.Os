"""
Integration Models - V2 Compliance Refactored
=============================================

V2 Refactored data models for integration coordination.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

# Import modular components
from .models.core_models import (
    IntegrationMetrics, OptimizationConfig, PerformanceReport, OptimizationRecommendation
)
from .models.config_models import (
    IntegrationConfig, IntegrationTask, IntegrationRequest, IntegrationResponse
)
from .models.factory import IntegrationModels

# Re-export for backward compatibility
__all__ = [
    # Core Models
    'IntegrationMetrics', 'OptimizationConfig', 'PerformanceReport', 'OptimizationRecommendation',
    # Config Models
    'IntegrationConfig', 'IntegrationTask', 'IntegrationRequest', 'IntegrationResponse',
    # Factory Class
    'IntegrationModels'
]

# Backward compatibility - create aliases
IntegrationMetrics = IntegrationMetrics
OptimizationConfig = OptimizationConfig
PerformanceReport = PerformanceReport
OptimizationRecommendation = OptimizationRecommendation
IntegrationConfig = IntegrationConfig
IntegrationTask = IntegrationTask
IntegrationRequest = IntegrationRequest
IntegrationResponse = IntegrationResponse
IntegrationModels = IntegrationModels