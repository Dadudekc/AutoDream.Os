#!/usr/bin/env python3
"""
Refactoring Integration Package - Agent-5
========================================

This package provides a modular integration system for coordinating
refactoring metrics, dashboard, and baseline systems.

Components:
- models: Data structures and enums for integration
- session_service: Session lifecycle management
- analysis_service: Analysis and reporting
- refactoring_metrics_integration: Main integration orchestration

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .models import (
    PerformanceStatus,
    AlertSeverity,
    IntegrationConfiguration,
    SessionContext,
    SessionAnalysis,
    PerformanceAnalysis,
    BaselineComparison,
    ExecutiveSummary,
    PerformanceMetrics,
    ExportData,
    FinalReport,
    SystemStatus
)

from .session_service import SessionManagementService
from .analysis_service import AnalysisService
from .refactoring_metrics_integration import RefactoringMetricsIntegration

__all__ = [
    # Models
    'PerformanceStatus',
    'AlertSeverity',
    'IntegrationConfiguration',
    'SessionContext',
    'SessionAnalysis',
    'PerformanceAnalysis',
    'BaselineComparison',
    'ExecutiveSummary',
    'PerformanceMetrics',
    'ExportData',
    'FinalReport',
    'SystemStatus',
    
    # Services
    'SessionManagementService',
    'AnalysisService',
    
    # Main Integration
    'RefactoringMetricsIntegration'
]

__version__ = "2.0.0"
__author__ = "V2 SWARM CAPTAIN"
__status__ = "REFACTORED AND MODULARIZED"
