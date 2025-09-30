"""
Comprehensive Integration Assessment Core
Core classes and data structures for integration assessment
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class AssessmentArea(Enum):
    """Assessment area enumeration"""
    CROSS_PLATFORM = "cross_platform"
    PERFORMANCE = "performance"
    REPOSITORY_AUTOMATION = "repository_automation"
    INTEGRATION_TESTING = "integration_testing"


class Priority(Enum):
    """Priority enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AssessmentStatus(Enum):
    """Assessment status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class IntegrationAssessment:
    """Integration assessment structure"""
    area: AssessmentArea
    component: str
    assessment_score: float
    issues: List[str]
    recommendations: List[str]
    priority: Priority
    estimated_effort: int
    timestamp: str
    status: AssessmentStatus = AssessmentStatus.PENDING


@dataclass
class AssessmentMetrics:
    """Assessment metrics structure"""
    total_assessments: int
    completed_assessments: int
    failed_assessments: int
    average_score: float
    total_effort: int
    success_rate: float
    quality_score: float


@dataclass
class AssessmentConfiguration:
    """Assessment configuration structure"""
    assessment_id: str
    title: str
    description: str
    target_areas: List[AssessmentArea]
    priority_threshold: Priority
    max_effort_per_assessment: int
    deadline: Optional[datetime]


class AssessmentCore:
    """Core assessment management functionality"""
    
    def __init__(self):
        self.assessments: List[IntegrationAssessment] = []
        self.metrics: Optional[AssessmentMetrics] = None
        self.configuration: Optional[AssessmentConfiguration] = None
    
    def create_assessment(
        self,
        area: AssessmentArea,
        component: str,
        priority: Priority = Priority.MEDIUM,
        estimated_effort: int = 1
    ) -> IntegrationAssessment:
        """Create a new integration assessment"""
        assessment = IntegrationAssessment(
            area=area,
            component=component,
            assessment_score=0.0,
            issues=[],
            recommendations=[],
            priority=priority,
            estimated_effort=estimated_effort,
            timestamp=datetime.now().isoformat(),
            status=AssessmentStatus.PENDING
        )
        self.assessments.append(assessment)
        return assessment
    
    def update_assessment(self, assessment: IntegrationAssessment, **kwargs) -> IntegrationAssessment:
        """Update an existing assessment"""
        for key, value in kwargs.items():
            if hasattr(assessment, key):
                setattr(assessment, key, value)
        return assessment
    
    def get_assessment_by_area(self, area: AssessmentArea) -> List[IntegrationAssessment]:
        """Get assessments by area"""
        return [a for a in self.assessments if a.area == area]
    
    def get_assessment_by_component(self, component: str) -> Optional[IntegrationAssessment]:
        """Get assessment by component"""
        for assessment in self.assessments:
            if assessment.component == component:
                return assessment
        return None
    
    def calculate_metrics(self) -> AssessmentMetrics:
        """Calculate assessment metrics"""
        if not self.assessments:
            return AssessmentMetrics(0, 0, 0, 0.0, 0, 0.0, 0.0)
        
        total_assessments = len(self.assessments)
        completed_assessments = sum(1 for a in self.assessments if a.status == AssessmentStatus.COMPLETED)
        failed_assessments = sum(1 for a in self.assessments if a.status == AssessmentStatus.FAILED)
        average_score = sum(a.assessment_score for a in self.assessments) / total_assessments
        total_effort = sum(a.estimated_effort for a in self.assessments)
        success_rate = (completed_assessments / total_assessments) * 100 if total_assessments > 0 else 0.0
        quality_score = average_score * (success_rate / 100)
        
        self.metrics = AssessmentMetrics(
            total_assessments=total_assessments,
            completed_assessments=completed_assessments,
            failed_assessments=failed_assessments,
            average_score=average_score,
            total_effort=total_effort,
            success_rate=success_rate,
            quality_score=quality_score
        )
        return self.metrics
