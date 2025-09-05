#!/usr/bin/env python3
"""
Vector Analytics Intelligence Package
====================================

Modular vector analytics intelligence system.
V2 COMPLIANT: Clean, focused, modular architecture.

@version 1.0.0 - V2 COMPLIANCE MODULAR PACKAGE
@license MIT
"""

# Import main orchestrator
from .vector_analytics_intelligence_orchestrator import (
    VectorAnalyticsIntelligenceOrchestrator,
    create_vector_analytics_intelligence_orchestrator
)

# Import individual engines
from .business_intelligence_engine import (
    BusinessIntelligenceEngine,
    create_business_intelligence_engine
)

from .pattern_analysis_engine import (
    PatternAnalysisEngine,
    create_pattern_analysis_engine
)

from .predictive_modeling_engine import (
    PredictiveModelingEngine,
    create_predictive_modeling_engine
)

from .anomaly_detection_engine import (
    AnomalyDetectionEngine,
    create_anomaly_detection_engine
)

# Export all public interfaces
__all__ = [
    # Main orchestrator
    'VectorAnalyticsIntelligenceOrchestrator',
    'create_vector_analytics_intelligence_orchestrator',
    
    # Individual engines
    'BusinessIntelligenceEngine',
    'create_business_intelligence_engine',
    'PatternAnalysisEngine',
    'create_pattern_analysis_engine',
    'PredictiveModelingEngine',
    'create_predictive_modeling_engine',
    'AnomalyDetectionEngine',
    'create_anomaly_detection_engine'
]
