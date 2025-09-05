"""
Vector Integration Analytics - V2 Compliant Modular Architecture
==============================================================

Modular vector integration analytics system with clean separation of concerns.
Each module handles a specific aspect of analytics processing.

V2 Compliance: < 300 lines per module, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from .analytics_engine import VectorIntegrationAnalyticsEngine
from .trend_analyzer import TrendAnalyzer
from .forecast_generator import ForecastGenerator
from .recommendation_engine import RecommendationEngine

__all__ = [
    'VectorIntegrationAnalyticsEngine',
    'TrendAnalyzer',
    'ForecastGenerator',
    'RecommendationEngine'
]
