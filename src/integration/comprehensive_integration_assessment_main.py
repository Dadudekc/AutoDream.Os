"""
Comprehensive Integration Assessment Main
Main assessment system with comprehensive integration capabilities
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

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


class ComprehensiveIntegrationAssessment:
    """Comprehensive Integration Assessment System"""
    
    def __init__(self):
        self.core = AssessmentCore()
        self.validator = AssessmentValidator()
        self.analyzer = AssessmentAnalyzer()
        self.reporter = AssessmentReporter()
        self.platform_detector = PlatformDetector()
        self.current_platform = self.platform_detector.detect_platform()
    
    def initialize_assessment(self, config: AssessmentConfiguration) -> bool:
        """Initialize assessment with configuration"""
        issues = self.validator.validate_configuration(config)
        if issues:
            print(f"Configuration validation failed: {', '.join(issues)}")
            return False
        
        self.core.configuration = config
        return True
    
    def assess_cross_platform_compatibility(self, component: str) -> IntegrationAssessment:
        """Assess cross-platform compatibility"""
        assessment = self.core.create_assessment(
            area=AssessmentArea.CROSS_PLATFORM,
            component=component,
            priority=Priority.HIGH
        )
        
        # Simulate cross-platform assessment
        score = self._evaluate_cross_platform(component)
        assessment.assessment_score = score
        assessment.status = AssessmentStatus.COMPLETED if score >= 70 else AssessmentStatus.FAILED
        
        if score < 70:
            assessment.issues.append("Cross-platform compatibility issues detected")
            assessment.recommendations.append("Implement platform-specific adaptations")
        
        return assessment
    
    def assess_performance(self, component: str) -> IntegrationAssessment:
        """Assess performance characteristics"""
        assessment = self.core.create_assessment(
            area=AssessmentArea.PERFORMANCE,
            component=component,
            priority=Priority.HIGH
        )
        
        # Simulate performance assessment
        score = self._evaluate_performance(component)
        assessment.assessment_score = score
        assessment.status = AssessmentStatus.COMPLETED if score >= 70 else AssessmentStatus.FAILED
        
        if score < 70:
            assessment.issues.append("Performance bottlenecks detected")
            assessment.recommendations.append("Optimize critical paths and reduce complexity")
        
        return assessment
    
    def assess_repository_automation(self, component: str) -> IntegrationAssessment:
        """Assess repository automation capabilities"""
        assessment = self.core.create_assessment(
            area=AssessmentArea.REPOSITORY_AUTOMATION,
            component=component,
            priority=Priority.MEDIUM
        )
        
        # Simulate repository automation assessment
        score = self._evaluate_repository_automation(component)
        assessment.assessment_score = score
        assessment.status = AssessmentStatus.COMPLETED if score >= 70 else AssessmentStatus.FAILED
        
        if score < 70:
            assessment.issues.append("Automation gaps identified")
            assessment.recommendations.append("Implement automated workflows and CI/CD")
        
        return assessment
    
    def assess_integration_testing(self, component: str) -> IntegrationAssessment:
        """Assess integration testing coverage"""
        assessment = self.core.create_assessment(
            area=AssessmentArea.INTEGRATION_TESTING,
            component=component,
            priority=Priority.CRITICAL
        )
        
        # Simulate integration testing assessment
        score = self._evaluate_integration_testing(component)
        assessment.assessment_score = score
        assessment.status = AssessmentStatus.COMPLETED if score >= 70 else AssessmentStatus.FAILED
        
        if score < 70:
            assessment.issues.append("Insufficient integration test coverage")
            assessment.recommendations.append("Develop comprehensive integration test suite")
        
        return assessment
    
    def _evaluate_cross_platform(self, component: str) -> float:
        """Evaluate cross-platform compatibility"""
        # Simulate cross-platform evaluation
        base_score = 85.0
        platform_bonus = 5.0 if self.current_platform in ['windows', 'linux', 'darwin'] else 0.0
        return min(100.0, base_score + platform_bonus)
    
    def _evaluate_performance(self, component: str) -> float:
        """Evaluate performance characteristics"""
        # Simulate performance evaluation
        base_score = 88.0
        return base_score
    
    def _evaluate_repository_automation(self, component: str) -> float:
        """Evaluate repository automation"""
        # Simulate automation evaluation
        base_score = 82.0
        return base_score
    
    def _evaluate_integration_testing(self, component: str) -> float:
        """Evaluate integration testing"""
        # Simulate testing evaluation
        base_score = 90.0
        return base_score
    
    def run_comprehensive_assessment(self, components: List[str]) -> Dict[str, Any]:
        """Run comprehensive assessment on all components"""
        results = {}
        
        for component in components:
            component_results = {}
            
            # Assess all areas
            for area in AssessmentArea:
                if area == AssessmentArea.CROSS_PLATFORM:
                    assessment = self.assess_cross_platform_compatibility(component)
                elif area == AssessmentArea.PERFORMANCE:
                    assessment = self.assess_performance(component)
                elif area == AssessmentArea.REPOSITORY_AUTOMATION:
                    assessment = self.assess_repository_automation(component)
                elif area == AssessmentArea.INTEGRATION_TESTING:
                    assessment = self.assess_integration_testing(component)
                
                component_results[area.value] = {
                    "score": assessment.assessment_score,
                    "status": assessment.status.value,
                    "issues": assessment.issues,
                    "recommendations": assessment.recommendations
                }
            
            results[component] = component_results
        
        return results
    
    def generate_final_report(self) -> str:
        """Generate final assessment report"""
        if not self.core.metrics:
            self.core.calculate_metrics()
        
        summary = self.reporter.generate_summary_report(self.core.metrics)
        detailed = self.reporter.generate_detailed_report(self.core.assessments)
        
        return summary + "\n" + detailed
    
    def get_assessment_status(self) -> Dict[str, Any]:
        """Get current assessment status"""
        return {
            "total_assessments": len(self.core.assessments),
            "completed_assessments": sum(1 for a in self.core.assessments if a.status == AssessmentStatus.COMPLETED),
            "failed_assessments": sum(1 for a in self.core.assessments if a.status == AssessmentStatus.FAILED),
            "current_platform": self.current_platform,
            "configuration": self.core.configuration.title if self.core.configuration else None
        }


class AssessmentManager:
    """Assessment management system"""
    
    def __init__(self):
        self.assessments: Dict[str, ComprehensiveIntegrationAssessment] = {}
    
    def create_assessment(self, config: AssessmentConfiguration) -> Optional[ComprehensiveIntegrationAssessment]:
        """Create a new assessment"""
        assessment = ComprehensiveIntegrationAssessment()
        if assessment.initialize_assessment(config):
            self.assessments[config.assessment_id] = assessment
            return assessment
        return None
    
    def get_assessment(self, assessment_id: str) -> Optional[ComprehensiveIntegrationAssessment]:
        """Get assessment by ID"""
        return self.assessments.get(assessment_id)
    
    def list_assessments(self) -> List[str]:
        """List all assessment IDs"""
        return list(self.assessments.keys())
    
    def run_all_assessments(self, components: List[str]) -> Dict[str, Dict[str, Any]]:
        """Run all assessments and return results"""
        results = {}
        
        for assessment_id, assessment in self.assessments.items():
            results[assessment_id] = assessment.run_comprehensive_assessment(components)
        
        return results


def create_integration_assessment(
    assessment_id: str,
    title: str,
    description: str,
    target_areas: Optional[List[AssessmentArea]] = None
) -> ComprehensiveIntegrationAssessment:
    """Create an integration assessment"""
    config = create_assessment_configuration(
        assessment_id=assessment_id,
        title=title,
        description=description,
        target_areas=target_areas
    )
    
    assessment = ComprehensiveIntegrationAssessment()
    assessment.initialize_assessment(config)
    return assessment


def run_comprehensive_integration_assessment(components: List[str]) -> Dict[str, Any]:
    """Run comprehensive integration assessment"""
    assessment = create_integration_assessment(
        assessment_id="integration_assessment_001",
        title="Comprehensive Integration Assessment",
        description="Full assessment of integration capabilities",
        target_areas=list(AssessmentArea)
    )
    
    return assessment.run_comprehensive_assessment(components)
