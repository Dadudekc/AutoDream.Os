#!/usr/bin/env python3
"""
Risk Assessor - Risk assessment and analysis for coverage gaps.

This module handles risk assessment, uncovered area identification, and risk scoring.
"""

from typing import Dict, List, Any
from .coverage_models import CoverageMetric, RiskAssessment


class RiskAssessor:
    """Handles risk assessment and uncovered area identification."""
    
    def __init__(self):
        self.risk_thresholds = {
            "high_risk": 60.0,
            "medium_risk": 75.0,
            "low_risk": 85.0,
            "safe": 95.0
        }
    
    def assess_coverage_risk(self, metrics: Dict[str, CoverageMetric],
                           overall_coverage: float) -> RiskAssessment:
        """Assess overall risk based on coverage metrics."""
        critical_issues = []
        warnings = []
        suggestions = []
        
        # Analyze each metric for issues
        for metric_name, metric in metrics.items():
            if metric.risk_level == "CRITICAL":
                critical_issues.append(f"{metric.name}: {metric.value:.1f}% (target: {metric.target:.1f}%)")
            elif metric.risk_level == "HIGH":
                warnings.append(f"{metric.name}: {metric.value:.1f}% (target: {metric.target:.1f}%)")
            elif metric.risk_level == "MEDIUM":
                suggestions.append(f"Consider improving {metric.name}: {metric.value:.1f}%")
        
        # Overall coverage risk
        if overall_coverage < self.risk_thresholds["high_risk"]:
            critical_issues.append(f"Overall coverage {overall_coverage:.1f}% is critically low")
        elif overall_coverage < self.risk_thresholds["medium_risk"]:
            warnings.append(f"Overall coverage {overall_coverage:.1f}% needs improvement")
        elif overall_coverage < self.risk_thresholds["low_risk"]:
            suggestions.append(f"Overall coverage {overall_coverage:.1f}% could be improved")
        
        # Determine overall risk level
        if critical_issues:
            risk_level = "CRITICAL"
        elif warnings:
            risk_level = "HIGH"
        elif suggestions:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Calculate risk score (0-100, higher = more risky)
        risk_score = self._calculate_risk_score(metrics, overall_coverage)
        
        return RiskAssessment(
            risk_level=risk_level,
            risk_score=risk_score,
            critical_issues=critical_issues,
            warnings=warnings,
            suggestions=suggestions
        )
    
    def identify_uncovered_areas(self, target_file: str,
                               file_structure: Any,
                               coverage_data: Dict[str, Any]) -> List[str]:
        """Identify specific uncovered areas in the code."""
        uncovered_areas = []
        
        # Check for uncovered functions
        if hasattr(file_structure, 'functions'):
            covered_functions = coverage_data.get("functions", [])
            for func in file_structure.functions:
                if func not in covered_functions:
                    uncovered_areas.append(f"Function '{func}' is not covered by tests")
        
        # Check for uncovered classes
        if hasattr(file_structure, 'classes'):
            covered_classes = coverage_data.get("classes", [])
            for cls in file_structure.classes:
                if cls not in covered_classes:
                    uncovered_areas.append(f"Class '{cls}' is not covered by tests")
        
        # Check for uncovered lines (simplified)
        if hasattr(file_structure, 'total_lines') and file_structure.total_lines > 0:
            line_coverage = coverage_data.get("line_coverage", 0.0)
            if line_coverage < 100.0:
                uncovered_areas.append(f"Line coverage is {line_coverage:.1f}% - some lines are not tested")
        
        # Check for uncovered branches (simplified)
        branch_coverage = coverage_data.get("branch_coverage", 0.0)
        if branch_coverage < 100.0:
            uncovered_areas.append(f"Branch coverage is {branch_coverage:.1f}% - some code paths are not tested")
        
        return uncovered_areas
    
    def _calculate_risk_score(self, metrics: Dict[str, CoverageMetric],
                            overall_coverage: float) -> float:
        """Calculate a numerical risk score from 0-100."""
        if not metrics:
            return 100.0  # Maximum risk if no metrics
        
        # Calculate weighted risk based on individual metrics
        total_weight = 0.0
        weighted_risk = 0.0
        
        for metric_name, metric in metrics.items():
            # Weight different metrics
            if metric_name == "line_coverage":
                weight = 0.3
            elif metric_name == "function_coverage":
                weight = 0.3
            elif metric_name == "class_coverage":
                weight = 0.2
            elif metric_name == "branch_coverage":
                weight = 0.2
            else:
                weight = 0.1
            
            # Calculate risk for this metric (0-100)
            if metric.value >= metric.target:
                metric_risk = 0.0  # No risk if target met
            else:
                gap = metric.target - metric.value
                max_gap = metric.target  # Maximum possible gap
                metric_risk = (gap / max_gap) * 100.0
            
            weighted_risk += metric_risk * weight
            total_weight += weight
        
        # Add overall coverage risk
        if overall_coverage < 100.0:
            overall_risk = (100.0 - overall_coverage) * 0.5  # Reduce impact of overall coverage
            weighted_risk += overall_risk * 0.2
            total_weight += 0.2
        
        if total_weight == 0.0:
            return 100.0
        
        return min(100.0, weighted_risk / total_weight)
