"""
🎯 MODULARIZATION QUALITY ASSURANCE FRAMEWORK
Agent-7 - Quality Completion Optimization Manager
Contract: MODULAR-009 - Modularization Quality Assurance Framework

Main framework interface providing access to all quality assurance components.
Follows V2 coding standards: ≤300 lines per module.
"""

from .core.quality_models import (
    QualityLevel,
    QualityMetric,
    QualityThresholds,
    QualityAssessment,
    QualityReport
)

from .core.quality_metrics import (
    QualityMetricsCalculator,
    QualityMetricsCollector
)

from .core.quality_assessor import (
    QualityAssessor,
    QualityAssessmentEngine
)

from .protocols.testing_protocols import (
    TestingProtocols,
    TestCoverageRequirements,
    TestQualityStandards
)

from .protocols.validation_protocols import (
    ValidationProtocols,
    ValidationProcesses,
    QualityGates
)

from .protocols.compliance_protocols import (
    ComplianceProtocols,
    V2ComplianceChecker,
    StandardsValidator
)

from .tools.coverage_analyzer import TestCoverageAnalyzer
from .tools.complexity_analyzer import CodeComplexityAnalyzer
from .tools.dependency_analyzer import DependencyAnalyzer

from .reports.quality_reports import QualityReportGenerator
from .reports.compliance_reports import ComplianceReportGenerator

# Main framework class for easy access
class ModularizationQualityAssuranceFramework:
    """
    Main quality assurance framework for modularized components.
    
    This framework provides:
    - Comprehensive quality metrics calculation
    - Testing protocols and standards
    - Validation processes and quality gates
    - V2 compliance checking
    - Quality reporting and analysis
    """
    
    def __init__(self):
        """Initialize the quality assurance framework."""
        self.quality_assessor = QualityAssessmentEngine()
        self.testing_protocols = TestingProtocols()
        self.validation_protocols = ValidationProtocols()
        self.compliance_protocols = ComplianceProtocols()
        self.coverage_analyzer = TestCoverageAnalyzer()
        self.complexity_analyzer = CodeComplexityAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        self.report_generator = QualityReportGenerator()
        self.compliance_reporter = ComplianceReportGenerator()
    
    def assess_modularization_quality(self, target_file: str, modularized_dir: str) -> QualityReport:
        """
        Assess the quality of modularized components.
        
        Args:
            target_file: Path to the original monolithic file
            modularized_dir: Path to the modularized components directory
            
        Returns:
            QualityReport: Comprehensive quality assessment report
        """
        return self.quality_assessor.assess_modularization_quality(target_file, modularized_dir)
    
    def validate_v2_compliance(self, modularized_dir: str) -> dict:
        """
        Validate V2 compliance of modularized components.
        
        Args:
            modularized_dir: Path to the modularized components directory
            
        Returns:
            dict: V2 compliance validation results
        """
        return self.compliance_protocols.validate_v2_compliance(modularized_dir)
    
    def run_quality_tests(self, modularized_dir: str) -> dict:
        """
        Run comprehensive quality tests on modularized components.
        
        Args:
            modularized_dir: Path to the modularized components directory
            
        Returns:
            dict: Quality test results and metrics
        """
        return self.testing_protocols.run_quality_tests(modularized_dir)
    
    def generate_quality_report(self, assessment: QualityAssessment) -> str:
        """
        Generate a comprehensive quality report.
        
        Args:
            assessment: Quality assessment results
            
        Returns:
            str: Formatted quality report
        """
        return self.report_generator.generate_report(assessment)
    
    def generate_compliance_report(self, compliance_results: dict) -> str:
        """
        Generate a V2 compliance report.
        
        Args:
            compliance_results: V2 compliance validation results
            
        Returns:
            str: Formatted compliance report
        """
        return self.compliance_reporter.generate_report(compliance_results)

# Convenience function for quick quality assessment
def assess_modularization_quality(target_file: str, modularized_dir: str) -> QualityReport:
    """
    Convenience function for quick quality assessment.
    
    Args:
        target_file: Path to the original monolithic file
        modularized_dir: Path to the modularized components directory
        
    Returns:
        QualityReport: Quality assessment report
    """
    framework = ModularizationQualityAssuranceFramework()
    return framework.assess_modularization_quality(target_file, modularized_dir)

# Version and compatibility info
__version__ = "1.0.0"
__author__ = "Agent-7 (Quality Completion Optimization Manager)"
__description__ = "Modularization Quality Assurance Framework for V2 Compliance"

# Main exports
__all__ = [
    # Core Framework
    "ModularizationQualityAssuranceFramework",
    "assess_modularization_quality",
    
    # Core Components
    "QualityLevel",
    "QualityMetric", 
    "QualityThresholds",
    "QualityAssessment",
    "QualityReport",
    "QualityMetricsCalculator",
    "QualityMetricsCollector",
    "QualityAssessor",
    "QualityAssessmentEngine",
    
    # Protocols
    "TestingProtocols",
    "TestCoverageRequirements", 
    "TestQualityStandards",
    "ValidationProtocols",
    "ValidationProcesses",
    "QualityGates",
    "ComplianceProtocols",
    "V2ComplianceChecker",
    "StandardsValidator",
    
    # Tools
    "TestCoverageAnalyzer",
    "CodeComplexityAnalyzer",
    "DependencyAnalyzer",
    
    # Reporting
    "QualityReportGenerator",
    "ComplianceReportGenerator"
]
