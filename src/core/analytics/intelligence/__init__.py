#!/usr/bin/env python3
"""
Analytics Intelligence Package - KISS Compliant
==============================================

Simple analytics intelligence package.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

# Essential imports only
from .business_intelligence_engine import BusinessIntelligenceEngine
from .pattern_analysis_engine import PatternAnalysisEngine
from .anomaly_detection_engine import AnomalyDetectionEngine

# Simple aliases
AnalyticsIntelligence = BusinessIntelligenceEngine

__version__ = "2.0.0"
__all__ = ["BusinessIntelligenceEngine", "PatternAnalysisEngine", "AnomalyDetectionEngine", "AnalyticsIntelligence"]