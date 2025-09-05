"""
Integration Models - KISS Simplified (V2 Refactored)
====================================================

V2 Refactored data models for integration coordination.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined data modeling.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

# V2 Refactored - Backward Compatibility Wrapper
from .models_refactored import *

# Maintain backward compatibility
__all__ = [
    # Core Models
    'IntegrationMetrics', 'OptimizationConfig', 'PerformanceReport', 'OptimizationRecommendation',
    # Config Models
    'IntegrationConfig', 'IntegrationTask', 'IntegrationRequest', 'IntegrationResponse',
    # Factory Class
    'IntegrationModels'
]