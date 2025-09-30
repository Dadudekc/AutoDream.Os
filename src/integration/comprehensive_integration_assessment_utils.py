"""
Comprehensive Integration Assessment Utils
Utility functions for integration assessment and validation
"""

import platform
from datetime import datetime
from typing import Any, Dict, List, Optional

from .comprehensive_integration_assessment_core import (
    AssessmentArea,
    AssessmentConfiguration,
    AssessmentMetrics,
    AssessmentStatus,
    IntegrationAssessment,
    Priority
)


class AssessmentValidator:
    """Assessment validation utilities"""
    
    @staticmethod
    def validate_assessment(assessment: IntegrationAssessment) -> List[str]:
        """Validate integration assessment"""
        issues = []
        
        if assessment.assessment_score < 0 or assessment.assessment_score > 100:
            issues.append("Assessment score must be between 0 and 100")
        
        if assessment.estimated_effort < 0:
            issues.append("Estimated effort cannot be negative")
        
        if not assessment.component:
            issues.append("Component must be specified")
        
        if not assessment.area:
            issues.append("Assessment area must be specified")
        
        return issues
    
    @staticmethod
    def validate_configuration(config: AssessmentConfiguration) -> List[str]:
        """Validate assessment configuration"""
        issues = []
        
        if not config.assessment_id:
            issues.append("Assessment ID must be specified")
        
        if not config.title:
            issues.append("Title must be specified")
        
        if not config.description:
            issues.append("Description must be specified")
        
        if not config.target_areas:
            issues.append("Target areas must be specified")
        
        if config.deadline and config.deadline < datetime.now():
            issues.append("Deadline cannot be in the past")
        
        return issues


class AssessmentAnalyzer:
    """Assessment analysis utilities"""
    
    @staticmethod
    def analyze_performance(assessments: List[IntegrationAssessment]) -> Dict[str, Any]:
        """Analyze assessment performance"""
        if not assessments:
            return {"error": "No assessments to analyze"}
        
        total_score = sum(a.assessment_score for a in assessments)
        avg_score = total_score / len(assessments)
        completion_rate = sum(1 for a in assessments if a.status == AssessmentStatus.COMPLETED) / len(assessments)
        
        # Analyze by area
        area_scores = {}
        for area in AssessmentArea:
            area_assessments = [a for a in assessments if a.area == area]
            if area_assessments:
                area_scores[area.value] = sum(a.assessment_score for a in area_assessments) / len(area_assessments)
        
        return {
            "total_assessments": len(assessments),
            "average_score": avg_score,
            "completion_rate": completion_rate,
            "area_scores": area_scores,
            "performance_grade": AssessmentAnalyzer._calculate_grade(avg_score)
        }
    
    @staticmethod
    def _calculate_grade(score: float) -> str:
        """Calculate performance grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    @staticmethod
    def identify_issues(assessments: List[IntegrationAssessment]) -> List[str]:
        """Identify assessment issues"""
        issues = []
        
        # Find low-scoring assessments
        low_score_assessments = [a.component for a in assessments if a.assessment_score < 60]
        if low_score_assessments:
            issues.append(f"Low-scoring components: {', '.join(low_score_assessments)}")
        
        # Find failed assessments
        failed_assessments = [a.component for a in assessments if a.status == AssessmentStatus.FAILED]
        if failed_assessments:
            issues.append(f"Failed assessments: {', '.join(failed_assessments)}")
        
        # Find high-effort assessments
        high_effort_assessments = [a.component for a in assessments if a.estimated_effort > 5]
        if high_effort_assessments:
            issues.append(f"High-effort components: {', '.join(high_effort_assessments)}")
        
        return issues


class AssessmentReporter:
    """Assessment reporting utilities"""
    
    @staticmethod
    def generate_summary_report(metrics: AssessmentMetrics) -> str:
        """Generate summary report"""
        return f"""
Integration Assessment Summary Report
====================================
Total Assessments: {metrics.total_assessments}
Completed: {metrics.completed_assessments}
Failed: {metrics.failed_assessments}
Success Rate: {metrics.success_rate:.1f}%
Average Score: {metrics.average_score:.1f}
Quality Score: {metrics.quality_score:.1f}
Total Effort: {metrics.total_effort} hours
"""
    
    @staticmethod
    def generate_detailed_report(assessments: List[IntegrationAssessment]) -> str:
        """Generate detailed report"""
        report = "Detailed Integration Assessment Report\n"
        report += "=====================================\n\n"
        
        for assessment in assessments:
            report += f"Component: {assessment.component}\n"
            report += f"Area: {assessment.area.value}\n"
            report += f"Score: {assessment.assessment_score:.1f}\n"
            report += f"Status: {assessment.status.value}\n"
            report += f"Priority: {assessment.priority.value}\n"
            report += f"Effort: {assessment.estimated_effort} hours\n"
            
            if assessment.issues:
                report += f"Issues: {', '.join(assessment.issues)}\n"
            
            if assessment.recommendations:
                report += f"Recommendations: {', '.join(assessment.recommendations)}\n"
            
            report += "\n"
        
        return report


class PlatformDetector:
    """Platform detection utilities"""
    
    @staticmethod
    def detect_platform() -> str:
        """Detect current platform"""
        return platform.system().lower()
    
    @staticmethod
    def get_platform_info() -> Dict[str, Any]:
        """Get detailed platform information"""
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }


def create_assessment_configuration(
    assessment_id: str,
    title: str,
    description: str,
    target_areas: Optional[List[AssessmentArea]] = None,
    priority_threshold: Priority = Priority.MEDIUM,
    max_effort_per_assessment: int = 5,
    deadline: Optional[datetime] = None
) -> AssessmentConfiguration:
    """Create assessment configuration"""
    return AssessmentConfiguration(
        assessment_id=assessment_id,
        title=title,
        description=description,
        target_areas=target_areas or list(AssessmentArea),
        priority_threshold=priority_threshold,
        max_effort_per_assessment=max_effort_per_assessment,
        deadline=deadline
    )


def format_assessment_score(score: float) -> str:
    """Format assessment score in human-readable format"""
    if score >= 90:
        return f"{score:.1f} (Excellent)"
    elif score >= 80:
        return f"{score:.1f} (Good)"
    elif score >= 70:
        return f"{score:.1f} (Acceptable)"
    elif score >= 60:
        return f"{score:.1f} (Poor)"
    else:
        return f"{score:.1f} (Critical)"
