#!/usr/bin/env python3
"""
V3-018: Quality Assurance Core
==============================

Core quality assurance functionality with V2 compliance.
Focuses on essential quality checking and reporting.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class QualityLevel(Enum):
    """Quality levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    CRITICAL = "critical"


class QualityMetric(Enum):
    """Quality metrics."""
    CODE_COVERAGE = "code_coverage"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    RELIABILITY = "reliability"
    USABILITY = "usability"


@dataclass
class QualityCheck:
    """Quality check structure."""
    check_id: str
    name: str
    metric: QualityMetric
    threshold: float
    current_value: float
    level: QualityLevel
    description: str
    recommendations: List[str]
    checked_at: datetime


@dataclass
class QualityReport:
    """Quality report structure."""
    report_id: str
    component_id: str
    component_name: str
    checks: List[QualityCheck]
    overall_score: float
    overall_level: QualityLevel
    generated_at: datetime


@dataclass
class QualityThreshold:
    """Quality threshold configuration."""
    metric: QualityMetric
    excellent: float
    good: float
    acceptable: float
    poor: float


class QualityChecker:
    """Core quality checking functionality."""
    
    def __init__(self):
        self.thresholds = self._initialize_thresholds()
        self.checks = []
        self.reports = []
    
    def _initialize_thresholds(self) -> Dict[QualityMetric, QualityThreshold]:
        """Initialize quality thresholds."""
        return {
            QualityMetric.CODE_COVERAGE: QualityThreshold(
                metric=QualityMetric.CODE_COVERAGE,
                excellent=95.0,
                good=85.0,
                acceptable=70.0,
                poor=50.0
            ),
            QualityMetric.PERFORMANCE: QualityThreshold(
                metric=QualityMetric.PERFORMANCE,
                excellent=90.0,
                good=75.0,
                acceptable=60.0,
                poor=40.0
            ),
            QualityMetric.SECURITY: QualityThreshold(
                metric=QualityMetric.SECURITY,
                excellent=95.0,
                good=85.0,
                acceptable=70.0,
                poor=50.0
            ),
            QualityMetric.MAINTAINABILITY: QualityThreshold(
                metric=QualityMetric.MAINTAINABILITY,
                excellent=90.0,
                good=75.0,
                acceptable=60.0,
                poor=40.0
            ),
            QualityMetric.RELIABILITY: QualityThreshold(
                metric=QualityMetric.RELIABILITY,
                excellent=95.0,
                good=85.0,
                acceptable=70.0,
                poor=50.0
            ),
            QualityMetric.USABILITY: QualityThreshold(
                metric=QualityMetric.USABILITY,
                excellent=90.0,
                good=75.0,
                acceptable=60.0,
                poor=40.0
            )
        }
    
    def check_quality(self, component_id: str, component_name: str, 
                     metrics: Dict[QualityMetric, float]) -> QualityReport:
        """Check quality for a component."""
        checks = []
        
        for metric, value in metrics.items():
            check = self._create_quality_check(component_id, metric, value)
            checks.append(check)
        
        overall_score = sum(check.current_value for check in checks) / len(checks)
        overall_level = self._determine_quality_level(overall_score)
        
        report = QualityReport(
            report_id=f"{component_id}_{int(datetime.now().timestamp())}",
            component_id=component_id,
            component_name=component_name,
            checks=checks,
            overall_score=overall_score,
            overall_level=overall_level,
            generated_at=datetime.now()
        )
        
        self.reports.append(report)
        return report
    
    def _create_quality_check(self, component_id: str, metric: QualityMetric, 
                             value: float) -> QualityCheck:
        """Create quality check for metric."""
        threshold = self.thresholds[metric]
        level = self._determine_quality_level(value)
        
        recommendations = self._generate_recommendations(metric, value, level)
        
        return QualityCheck(
            check_id=f"{component_id}_{metric.value}_{int(datetime.now().timestamp())}",
            name=f"{metric.value.replace('_', ' ').title()} Check",
            metric=metric,
            threshold=threshold.acceptable,
            current_value=value,
            level=level,
            description=f"Quality check for {metric.value}",
            recommendations=recommendations,
            checked_at=datetime.now()
        )
    
    def _determine_quality_level(self, value: float) -> QualityLevel:
        """Determine quality level based on value."""
        if value >= 90:
            return QualityLevel.EXCELLENT
        elif value >= 75:
            return QualityLevel.GOOD
        elif value >= 60:
            return QualityLevel.ACCEPTABLE
        elif value >= 40:
            return QualityLevel.POOR
        else:
            return QualityLevel.CRITICAL
    
    def _generate_recommendations(self, metric: QualityMetric, value: float, 
                                 level: QualityLevel) -> List[str]:
        """Generate recommendations based on metric and level."""
        recommendations = []
        
        if level == QualityLevel.CRITICAL:
            recommendations.append(f"Immediate action required for {metric.value}")
            recommendations.append("Consider refactoring or redesign")
        elif level == QualityLevel.POOR:
            recommendations.append(f"Improve {metric.value} to meet standards")
            recommendations.append("Review implementation approach")
        elif level == QualityLevel.ACCEPTABLE:
            recommendations.append(f"Enhance {metric.value} for better quality")
            recommendations.append("Consider optimization opportunities")
        elif level == QualityLevel.GOOD:
            recommendations.append(f"Maintain current {metric.value} level")
            recommendations.append("Look for minor improvements")
        else:  # EXCELLENT
            recommendations.append(f"Excellent {metric.value} - maintain standards")
            recommendations.append("Consider sharing best practices")
        
        return recommendations
    
    def get_quality_summary(self) -> Dict[str, Any]:
        """Get quality summary across all reports."""
        if not self.reports:
            return {"error": "No quality reports available"}
        
        total_reports = len(self.reports)
        total_checks = sum(len(report.checks) for report in self.reports)
        
        level_counts = {}
        for report in self.reports:
            level = report.overall_level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        average_score = sum(report.overall_score for report in self.reports) / total_reports
        
        return {
            "total_reports": total_reports,
            "total_checks": total_checks,
            "average_score": average_score,
            "quality_levels": level_counts,
            "last_report": max(report.generated_at for report in self.reports).isoformat()
        }
    
    def get_component_quality(self, component_id: str) -> Optional[QualityReport]:
        """Get quality report for specific component."""
        for report in self.reports:
            if report.component_id == component_id:
                return report
        return None
    
    def export_quality_report(self, report_id: str, filepath: str) -> bool:
        """Export quality report to file."""
        try:
            report = None
            for r in self.reports:
                if r.report_id == report_id:
                    report = r
                    break
            
            if not report:
                return False
            
            report_data = {
                "report_id": report.report_id,
                "component_id": report.component_id,
                "component_name": report.component_name,
                "overall_score": report.overall_score,
                "overall_level": report.overall_level.value,
                "generated_at": report.generated_at.isoformat(),
                "checks": [
                    {
                        "check_id": check.check_id,
                        "name": check.name,
                        "metric": check.metric.value,
                        "threshold": check.threshold,
                        "current_value": check.current_value,
                        "level": check.level.value,
                        "description": check.description,
                        "recommendations": check.recommendations,
                        "checked_at": check.checked_at.isoformat()
                    }
                    for check in report.checks
                ]
            }
            
            with open(filepath, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False


def main():
    """Main execution function."""
    print("🔍 V3-018 Quality Assurance Core - Testing...")
    
    # Initialize quality checker
    checker = QualityChecker()
    
    # Test quality checking
    test_metrics = {
        QualityMetric.CODE_COVERAGE: 85.5,
        QualityMetric.PERFORMANCE: 78.2,
        QualityMetric.SECURITY: 92.1,
        QualityMetric.MAINTAINABILITY: 67.8,
        QualityMetric.RELIABILITY: 88.9,
        QualityMetric.USABILITY: 73.4
    }
    
    report = checker.check_quality("test_component", "Test Component", test_metrics)
    
    print(f"\n📊 Quality Report:")
    print(f"   Component: {report.component_name}")
    print(f"   Overall Score: {report.overall_score:.1f}")
    print(f"   Overall Level: {report.overall_level.value}")
    print(f"   Total Checks: {len(report.checks)}")
    
    print(f"\n🔍 Quality Checks:")
    for check in report.checks:
        print(f"   {check.name}: {check.current_value:.1f} ({check.level.value})")
    
    # Get quality summary
    summary = checker.get_quality_summary()
    
    print(f"\n📈 Quality Summary:")
    print(f"   Total Reports: {summary['total_reports']}")
    print(f"   Average Score: {summary['average_score']:.1f}")
    print(f"   Quality Levels: {summary['quality_levels']}")
    
    # Export report
    checker.export_quality_report(report.report_id, "quality_report.json")
    
    print("\n✅ V3-018 Quality Assurance Core completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())

