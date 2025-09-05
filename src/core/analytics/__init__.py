#!/usr/bin/env python3
"""
Analytics Package - KISS Compliant
==================================

Simple analytics package with essential functionality only.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

# Essential imports only
from .vector_analytics_orchestrator import VectorAnalyticsOrchestrator

# Simple aliases
VectorAnalytics = VectorAnalyticsOrchestrator

__version__ = "2.0.0"
__all__ = ["VectorAnalyticsOrchestrator", "VectorAnalytics"]
