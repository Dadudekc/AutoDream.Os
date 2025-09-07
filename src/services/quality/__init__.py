from .alerting import QualityAlertManager
from .analysis import QualityTrendAnalyzer
from .assurance_engine import (
from .core_framework import (
from .data_collection import QualityMonitor
from .quality_validator import (

"""
Unified Quality Assurance Framework
==================================

Consolidated quality assurance system for V2 services with testing, validation,
monitoring, and quality metrics.
Follows V2 coding standards: ≤300 lines per module.

This package consolidates functionality from:
- v2_quality_assurance_framework.py (696 lines)

Total consolidation: 696 lines → 400 lines (43% reduction)
"""

# Core Quality Framework
    QualityLevel,
    TestType,
    QualityMetric,
    TestResult,
    QualityReport
)

# Quality Assurance Engine
    V2QualityAssuranceFramework,
    QualityMetricsCollector,
    TestResultManager
)

# Quality Monitoring

# Quality Validation
    QualityValidator,
    QualityGateEnforcer,
    QualityComplianceChecker
)

# Version and compatibility info
__version__ = "2.0.0"
__author__ = "Agent-1 (V2 Standards Compliance)"
__description__ = "Unified Quality Assurance Framework for V2 Services"

# Main framework class for easy access
__all__ = [
    # Core Framework
    "QualityLevel",
    "TestType", 
    "QualityMetric",
    "TestResult",
    "QualityReport",
    
    # Assurance Engine
    "V2QualityAssuranceFramework",
    "QualityMetricsCollector",
    "TestResultManager",
    
    # Quality Monitoring
    "QualityMonitor",
    "QualityAlertManager",
    "QualityTrendAnalyzer",
    
    # Quality Validation
    "QualityValidator",
    "QualityGateEnforcer",
    "QualityComplianceChecker"
]
