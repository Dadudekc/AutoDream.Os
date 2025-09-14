#!/usr/bin/env python3
"""
Unified Analytics System - V2 Compliant Consolidation
====================================================

Consolidated analytics system providing unified analytics functionality.
V2 COMPLIANT: This module consolidates 38 analytics files into modular components.

Previously monolithic implementation refactored into focused modules:
- models/ (data models and enums)
- interfaces/ (abstract interfaces)
- analytics_orchestrator.py (main coordinator)

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from .analytics_orchestrator import AnalyticsOrchestrator, create_analytics_orchestrator
from .interfaces import AnalyticsEngine, IntelligenceEngine, ProcessingEngine
from .models import (
    AnalyticsData,
    AnalyticsInfo,
    AnalyticsMetrics,
    AnalyticsResult,
    AnalyticsStatus,
    AnalyticsType,
    IntelligenceType,
    ProcessingMode,
)

# Maintain backward compatibility by re-exporting key classes
# This allows existing code to continue working with the new modular system

__all__ = [
    # Main orchestrator
    "AnalyticsOrchestrator",
    "create_analytics_orchestrator",

    # Interfaces
    "AnalyticsEngine",
    "IntelligenceEngine",
    "ProcessingEngine",

    # Models
    "AnalyticsData",
    "AnalyticsInfo",
    "AnalyticsMetrics",
    "AnalyticsResult",

    # Enums
    "AnalyticsStatus",
    "AnalyticsType",
    "IntelligenceType",
    "ProcessingMode",
]
