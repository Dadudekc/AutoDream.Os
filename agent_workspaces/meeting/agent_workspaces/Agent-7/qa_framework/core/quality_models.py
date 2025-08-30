"""
🎯 QUALITY ASSURANCE MODELS - CORE COMPONENT
Agent-7 - Quality Completion Optimization Manager

Data models and structures for quality assurance framework.
Follows V2 coding standards: ≤300 lines per module.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from datetime import datetime


class QualityStatus(Enum):
    """Quality status enumeration."""
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"


class ComplianceLevel(Enum):
    """V2 compliance level enumeration."""
    FULLY_COMPLIANT = "FULLY_COMPLIANT"
    MOSTLY_COMPLIANT = "MOSTLY_COMPLIANT"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    ERROR = "ERROR"


@dataclass
class QualityLevel:
    """Quality level classification for modularized components."""
    level: str
    score: float
    description: str
    color: str
    status: QualityStatus = QualityStatus.FAIR
    
    def __post_init__(self):
        """Set status based on score."""
        if self.score >= 90.0:
            self.status = QualityStatus.EXCELLENT
        elif self.score >= 75.0:
            self.status = QualityStatus.GOOD
        elif self.score >= 60.0:
            self.status = QualityStatus.FAIR
        elif self.score >= 45.0:
            self.status = QualityStatus.POOR
        else:
            self.status = QualityStatus.CRITICAL


@dataclass
class QualityMetric:
    """Individual quality metric for modularization assessment."""
    name: str
    value: Union[float, int, str]
    weight: float
    threshold: Union[float, int]
    status: str = "PASS"
    description: str = ""
    unit: str = ""
    
    def __post_init__(self):
        """Set status based on value and threshold."""
        if isinstance(self.value, (int, float)) and isinstance(self.threshold, (int, float)):
            if self.name.lower().startswith(("reduction", "improvement", "increase")):
                # For metrics where higher is better
                self.status = "PASS" if self.value >= self.threshold else "FAIL"
            else:
                # For metrics where lower is better (complexity, size)
                self.status = "PASS" if self.value <= self.threshold else "FAIL"
        else:
            self.status = "UNKNOWN"


@dataclass
class QualityThresholds:
    """Configurable quality thresholds for assessment."""
    file_size_reduction: float = 30.0  # Minimum 30% reduction
    module_count: int = 5              # Minimum 5 modules
    interface_quality: float = 0.7     # Minimum 0.7 interface quality
    dependency_complexity: float = 0.6 # Maximum 0.6 complexity
    naming_conventions: float = 0.8    # Minimum 0.8 naming score
    documentation: float = 0.7         # Minimum 0.7 documentation score
    code_organization: float = 0.75    # Minimum 0.75 organization score
    test_coverage: float = 80.0       # Minimum 80% test coverage
    max_module_lines: int = 400        # Maximum lines per module (V2 standard)
    
    def get_threshold(self, metric_name: str) -> Union[float, int]:
        """Get threshold value for a specific metric."""
        return getattr(self, metric_name, 0.0)
    
    def update_threshold(self, metric_name: str, value: Union[float, int]) -> None:
        """Update threshold value for a specific metric."""
        if hasattr(self, metric_name):
            setattr(self, metric_name, value)


@dataclass
class QualityAssessment:
    """Complete quality assessment results."""
    target_file: str
    modularized_dir: str
    timestamp: datetime = field(default_factory=datetime.now)
    overall_quality_score: float = 0.0
    quality_level: QualityLevel = None
    compliance_status: ComplianceLevel = ComplianceLevel.NON_COMPLIANT
    metrics: Dict[str, QualityMetric] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def add_metric(self, metric: QualityMetric) -> None:
        """Add a quality metric to the assessment."""
        self.metrics[metric.name] = metric
    
    def get_metric(self, metric_name: str) -> Optional[QualityMetric]:
        """Get a specific quality metric."""
        return self.metrics.get(metric_name)
    
    def add_recommendation(self, recommendation: str) -> None:
        """Add a quality improvement recommendation."""
        self.recommendations.append(recommendation)
    
    def add_issue(self, issue: str) -> None:
        """Add a quality issue."""
        self.issues.append(issue)
    
    def add_warning(self, warning: str) -> None:
        """Add a quality warning."""
        self.warnings.append(warning)
    
    def is_compliant(self) -> bool:
        """Check if the assessment meets compliance requirements."""
        return self.compliance_status in [ComplianceLevel.FULLY_COMPLIANT, ComplianceLevel.MOSTLY_COMPLIANT]
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of all metrics."""
        return {
            "total_metrics": len(self.metrics),
            "passing_metrics": len([m for m in self.metrics.values() if m.status == "PASS"]),
            "failing_metrics": len([m for m in self.metrics.values() if m.status == "FAIL"]),
            "overall_score": self.overall_quality_score,
            "quality_level": self.quality_level.level if self.quality_level else "UNKNOWN",
            "compliance_status": self.compliance_status.value
        }


@dataclass
class QualityReport:
    """Comprehensive quality report with all assessment details."""
    assessment: QualityAssessment
    report_id: str = ""
    generated_at: datetime = field(default_factory=datetime.now)
    report_format: str = "markdown"
    include_details: bool = True
    include_recommendations: bool = True
    include_metrics: bool = True
    
    def __post_init__(self):
        """Generate report ID if not provided."""
        if not self.report_id:
            timestamp = self.generated_at.strftime("%Y%m%d_%H%M%S")
            self.report_id = f"QA_REPORT_{timestamp}"
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the quality report."""
        return {
            "report_id": self.report_id,
            "target_file": self.assessment.target_file,
            "modularized_dir": self.assessment.modularized_dir,
            "overall_score": self.assessment.overall_quality_score,
            "quality_level": self.assessment.quality_level.level if self.assessment.quality_level else "UNKNOWN",
            "compliance_status": self.assessment.compliance_status.value,
            "total_issues": len(self.assessment.issues),
            "total_warnings": len(self.assessment.warnings),
            "total_recommendations": len(self.assessment.recommendations),
            "generated_at": self.generated_at.isoformat()
        }
    
    def export_json(self) -> str:
        """Export report as JSON string."""
        import json
        return json.dumps(self.get_summary(), indent=2, default=str)
    
    def export_markdown(self) -> str:
        """Export report as markdown string."""
        # This will be implemented by the report generator
        return f"# Quality Report: {self.report_id}\n\nGenerated at: {self.generated_at}"
