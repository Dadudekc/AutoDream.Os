"""
Comprehensive Integration Assessment System
Advanced integration assessment for Team Beta mission areas
Refactored into modular components for V2 compliance
"""

# Import all components from refactored modules
from .comprehensive_integration_assessment_core import (
    AssessmentArea,
    AssessmentConfiguration,
    AssessmentCore,
    AssessmentMetrics,
    AssessmentStatus,
    IntegrationAssessment,
    Priority
)
from .comprehensive_integration_assessment_utils import (
    AssessmentAnalyzer,
    AssessmentReporter,
    AssessmentValidator,
    PlatformDetector,
    create_assessment_configuration,
    format_assessment_score
)
from .comprehensive_integration_assessment_main import (
    ComprehensiveIntegrationAssessment,
    AssessmentManager,
    create_integration_assessment,
    run_comprehensive_integration_assessment
)

# Re-export main classes for backward compatibility
__all__ = [
    'AssessmentArea',
    'Priority',
    'AssessmentStatus',
    'IntegrationAssessment',
    'AssessmentConfiguration',
    'AssessmentMetrics',
    'AssessmentCore',
    'AssessmentValidator',
    'AssessmentAnalyzer',
    'AssessmentReporter',
    'PlatformDetector',
    'ComprehensiveIntegrationAssessment',
    'AssessmentManager',
    'create_assessment_configuration',
    'create_integration_assessment',
    'run_comprehensive_integration_assessment',
    'format_assessment_score'
]
