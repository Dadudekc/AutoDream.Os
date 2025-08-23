"""
Financial Analytics Package - V2 Compliant Modular Structure

This package contains the refactored financial analytics service components,
each following V2 standards (≤200 LOC) and Single Responsibility Principle.

Components:
- data_models.py: Data classes and structures
- metrics_calculator.py: Core metrics calculation functions
- risk_analyzer.py: Risk analysis and VaR calculations
- data_manager.py: Data persistence and loading
"""

from .data_models import BacktestResult, PerformanceMetrics, RiskAnalysis
from .metrics_calculator import MetricsCalculator
from .risk_analyzer import RiskAnalyzer
from .data_manager import DataManager
from .main_service import FinancialAnalyticsService

__all__ = [
    # Data models
    "BacktestResult",
    "PerformanceMetrics", 
    "RiskAnalysis",
    
    # Core components
    "MetricsCalculator",
    "RiskAnalyzer",
    "DataManager",
    
    # Main service
    "FinancialAnalyticsService",
]

# Backward compatibility - expose main service class directly
from .main_service import FinancialAnalyticsService

