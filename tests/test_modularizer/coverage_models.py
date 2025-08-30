#!/usr/bin/env python3
"""
Coverage Models - Data structures for testing coverage analysis.

This module defines the core data models used by the testing coverage analysis system.
V2 COMPLIANT: Focused module under 100 lines
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class CoverageLevel:
    """Coverage level classification for modularized components."""
    level: str
    percentage: float
    description: str
    color: str
    
    def __str__(self) -> str:
        return f"{self.color} {self.level} ({self.percentage:.1f}%)"
    
    def is_excellent(self) -> bool:
        """Check if coverage level is excellent."""
        return self.percentage >= 95.0
    
    def is_good(self) -> bool:
        """Check if coverage level is good."""
        return 85.0 <= self.percentage < 95.0
    
    def is_fair(self) -> bool:
        """Check if coverage level is fair."""
        return 75.0 <= self.percentage < 85.0
    
    def is_poor(self) -> bool:
        """Check if coverage level is poor."""
        return 60.0 <= self.percentage < 75.0
    
    def is_critical(self) -> bool:
        """Check if coverage level is critical."""
        return self.percentage < 60.0


@dataclass
class CoverageMetric:
    """Coverage metric for testing analysis."""
    name: str
    value: float
    target: float
    status: str
    risk_level: str
    
    def __str__(self) -> str:
        return f"{self.name}: {self.value:.1f}% (target: {self.target:.1f}%) - {self.status}"
    
    def is_passing(self) -> bool:
        """Check if metric is passing its target."""
        return self.value >= self.target
    
    def get_gap(self) -> float:
        """Get the gap between current value and target."""
        return max(0, self.target - self.value)
    
    def get_percentage_to_target(self) -> float:
        """Get percentage progress toward target."""
        if self.target == 0:
            return 100.0
        return min(100.0, (self.value / self.target) * 100.0)


@dataclass
class FileStructure:
    """File structure analysis results."""
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    functions: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    branches: List[Dict[str, Any]]
    imports: List[str]
    
    def get_function_count(self) -> int:
        """Get total function count."""
        return len(self.functions)
    
    def get_class_count(self) -> int:
        """Get total class count."""
        return len(self.classes)
    
    def get_code_density(self) -> float:
        """Calculate code density (code lines / total lines)."""
        if self.total_lines == 0:
            return 0.0
        return (self.code_lines / self.total_lines) * 100.0
    
    def get_complexity_score(self) -> float:
        """Calculate complexity score based on functions and classes."""
        return len(self.functions) + len(self.classes) * 2


@dataclass
class CoverageResult:
    """Result of coverage analysis for a specific file."""
    file_path: str
    line_coverage: float
    branch_coverage: float
    function_coverage: float
    class_coverage: float
    uncovered_lines: List[int]
    uncovered_branches: List[str]
    uncovered_functions: List[str]
    uncovered_classes: List[str]
    
    def get_overall_coverage(self) -> float:
        """Calculate overall coverage as average of all metrics."""
        metrics = [
            self.line_coverage,
            self.branch_coverage,
            self.function_coverage,
            self.class_coverage
        ]
        return sum(metrics) / len(metrics)
    
    def get_coverage_gaps(self) -> Dict[str, float]:
        """Get coverage gaps for each metric type."""
        return {
            "line_gap": 100.0 - self.line_coverage,
            "branch_gap": 100.0 - self.branch_coverage,
            "function_gap": 100.0 - self.function_coverage,
            "class_gap": 100.0 - self.class_coverage
        }
    
    def is_well_covered(self) -> bool:
        """Check if file has good overall coverage."""
        return self.get_overall_coverage() >= 80.0


@dataclass
class RiskAssessment:
    """Risk assessment results for coverage analysis."""
    overall_risk: str
    risk_factors: List[str]
    critical_gaps: List[str]
    recommendations: List[str]
    risk_score: float
    
    def __str__(self) -> str:
        return f"Risk Level: {self.overall_risk} (Score: {self.risk_score:.1f})"
    
    def is_high_risk(self) -> bool:
        """Check if overall risk is high."""
        return self.overall_risk in ["HIGH", "CRITICAL"]
    
    def is_medium_risk(self) -> bool:
        """Check if overall risk is medium."""
        return self.overall_risk == "MEDIUM"
    
    def is_low_risk(self) -> bool:
        """Check if overall risk is low."""
        return self.overall_risk == "LOW"
    
    def get_priority_recommendations(self) -> List[str]:
        """Get high-priority recommendations."""
        priority_keywords = ["critical", "high", "immediate", "urgent"]
        return [
            rec for rec in self.recommendations
            if any(keyword in rec.lower() for keyword in priority_keywords)
        ]


@dataclass
class CoverageReport:
    """Complete coverage analysis report."""
    target_file: str
    test_directory: Optional[str]
    overall_coverage: float
    coverage_level: str
    metrics: Dict[str, CoverageMetric]
    risk_assessment: RiskAssessment
    uncovered_areas: List[str]
    recommendations: List[str]
    timestamp: str
    file_structure: Optional[FileStructure] = None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the coverage report."""
        return {
            "target_file": self.target_file,
            "overall_coverage": self.overall_coverage,
            "coverage_level": self.coverage_level,
            "risk_level": self.risk_assessment.overall_risk,
            "total_metrics": len(self.metrics),
            "total_recommendations": len(self.recommendations),
            "timestamp": self.timestamp
        }
    
    def export_summary(self) -> str:
        """Export a human-readable summary."""
        summary = f"""
Coverage Report Summary
======================
File: {self.target_file}
Overall Coverage: {self.overall_coverage:.1f}%
Coverage Level: {self.coverage_level}
Risk Level: {self.risk_assessment.overall_risk}

Key Metrics:
"""
        for name, metric in self.metrics.items():
            summary += f"  {name}: {metric.value:.1f}% (target: {metric.target:.1f}%)\n"
        
        summary += f"\nTop Recommendations:\n"
        for i, rec in enumerate(self.recommendations[:3], 1):
            summary += f"  {i}. {rec}\n"
        
        return summary.strip()
