"""
🎯 QUALITY ASSURANCE FRAMEWORK - CORE MODULE
Agent-7 - Quality Completion Optimization Manager

Core framework components for quality assurance.
Follows V2 coding standards: ≤300 lines per module.
"""

from .quality_models import (
    QualityLevel,
    QualityMetric,
    QualityThresholds,
    QualityAssessment,
    QualityReport
)

from .quality_metrics import (
    QualityMetricsCalculator,
    QualityMetricsCollector
)

from .quality_assessor import (
    QualityAssessor,
    QualityAssessmentEngine
)

__all__ = [
    "QualityLevel",
    "QualityMetric",
    "QualityThresholds", 
    "QualityAssessment",
    "QualityReport",
    "QualityMetricsCalculator",
    "QualityMetricsCollector",
    "QualityAssessor",
    "QualityAssessmentEngine"
]
