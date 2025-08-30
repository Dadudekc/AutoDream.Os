"""
🎯 QUALITY REPORTS GENERATOR - REPORTS COMPONENT
Agent-7 - Quality Completion Optimization Manager

Quality report generation for comprehensive analysis results.
Follows V2 coding standards: ≤300 lines per module.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict

from ..tools.coverage_analyzer import TestCoverageAnalyzer
from ..tools.complexity_analyzer import CodeComplexityAnalyzer
from ..tools.dependency_analyzer import DependencyAnalyzer


@dataclass
class QualityReport:
    """Comprehensive quality assessment report."""
    report_id: str
    timestamp: str
    target_directory: str
    overall_quality_score: float
    coverage_metrics: Dict[str, Any]
    complexity_metrics: Dict[str, Any]
    dependency_metrics: Dict[str, Any]
    recommendations: List[str]
    risk_assessment: str
    compliance_status: str


class QualityReportGenerator:
    """Generates comprehensive quality assessment reports."""
    
    def __init__(self):
        """Initialize quality report generator."""
        self.coverage_analyzer = TestCoverageAnalyzer()
        self.complexity_analyzer = CodeComplexityAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        
        self.quality_thresholds = {
            "excellent": 90.0,
            "good": 80.0,
            "acceptable": 70.0,
            "poor": 60.0,
            "critical": 50.0
        }
    
    def generate_quality_report(self, target_directory: str, output_format: str = "json") -> QualityReport:
        """
        Generate comprehensive quality assessment report.
        
        Args:
            target_directory: Path to analyze
            output_format: Output format (json, markdown, html)
            
        Returns:
            QualityReport: Complete quality assessment
        """
        # Generate report ID
        report_id = f"QA_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        timestamp = datetime.now().isoformat()
        
        # Run all quality analyses
        coverage_results = self.coverage_analyzer.analyze_coverage(target_directory)
        complexity_results = self.complexity_analyzer.analyze_complexity(target_directory)
        dependency_results = self.dependency_analyzer.analyze_dependencies(target_directory)
        
        # Calculate overall quality score
        overall_score = self._calculate_overall_quality_score(
            coverage_results, complexity_results, dependency_results
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            coverage_results, complexity_results, dependency_results
        )
        
        # Assess risk level
        risk_assessment = self._assess_risk_level(overall_score)
        
        # Check compliance status
        compliance_status = self._check_compliance_status(
            coverage_results, complexity_results, dependency_results
        )
        
        # Create quality report
        quality_report = QualityReport(
            report_id=report_id,
            timestamp=timestamp,
            target_directory=target_directory,
            overall_quality_score=overall_score,
            coverage_metrics=coverage_results,
            complexity_metrics=complexity_results,
            dependency_metrics=dependency_results,
            recommendations=recommendations,
            risk_assessment=risk_assessment,
            compliance_status=compliance_status
        )
        
        return quality_report
    
    def _calculate_overall_quality_score(
        self, 
        coverage_results: Dict[str, Any], 
        complexity_results: Dict[str, Any], 
        dependency_results: Dict[str, Any]
    ) -> float:
        """Calculate overall quality score from all metrics."""
        # Coverage weight: 40%
        coverage_score = coverage_results.get("overall_coverage", 0.0)
        
        # Complexity weight: 30%
        complexity_score = 100.0 - min(
            complexity_results.get("overall_complexity", 0.0) * 10, 100.0
        )
        
        # Dependency weight: 30%
        dependency_score = 100.0 - min(
            dependency_results.get("overall_dependency_score", 0.0) * 100, 100.0
        )
        
        # Calculate weighted average
        overall_score = (
            coverage_score * 0.4 +
            complexity_score * 0.3 +
            dependency_score * 0.3
        )
        
        return round(overall_score, 2)
    
    def _generate_recommendations(
        self, 
        coverage_results: Dict[str, Any], 
        complexity_results: Dict[str, Any], 
        dependency_results: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable recommendations based on analysis results."""
        recommendations = []
        
        # Coverage recommendations
        coverage = coverage_results.get("overall_coverage", 0.0)
        if coverage < 80.0:
            recommendations.append(f"Increase test coverage from {coverage:.1f}% to at least 80%")
        
        # Complexity recommendations
        avg_complexity = complexity_results.get("average_cyclomatic", 0.0)
        if avg_complexity > 10.0:
            recommendations.append(f"Reduce average cyclomatic complexity from {avg_complexity:.1f} to below 10")
        
        # Dependency recommendations
        circular_deps = dependency_results.get("circular_dependencies_found", 0)
        if circular_deps > 0:
            recommendations.append(f"Eliminate {circular_deps} circular dependency(ies)")
        
        # Add general recommendations
        if not recommendations:
            recommendations.append("Code quality is excellent - maintain current standards")
        
        return recommendations
    
    def _assess_risk_level(self, quality_score: float) -> str:
        """Assess risk level based on quality score."""
        if quality_score >= self.quality_thresholds["excellent"]:
            return "LOW RISK - Excellent code quality"
        elif quality_score >= self.quality_thresholds["good"]:
            return "LOW-MEDIUM RISK - Good code quality"
        elif quality_score >= self.quality_thresholds["acceptable"]:
            return "MEDIUM RISK - Acceptable code quality"
        elif quality_score >= self.quality_thresholds["poor"]:
            return "HIGH RISK - Poor code quality"
        else:
            return "CRITICAL RISK - Critical quality issues detected"
    
    def _check_compliance_status(
        self, 
        coverage_results: Dict[str, Any], 
        complexity_results: Dict[str, Any], 
        dependency_results: Dict[str, Any]
    ) -> str:
        """Check compliance with quality standards."""
        compliance_checks = []
        
        # Coverage compliance
        if coverage_results.get("overall_coverage", 0.0) >= 80.0:
            compliance_checks.append("Coverage: PASS")
        else:
            compliance_checks.append("Coverage: FAIL")
        
        # Complexity compliance
        if complexity_results.get("average_cyclomatic", 0.0) <= 10.0:
            compliance_checks.append("Complexity: PASS")
        else:
            compliance_checks.append("Complexity: FAIL")
        
        # Dependency compliance
        if dependency_results.get("circular_dependencies_found", 0) == 0:
            compliance_checks.append("Dependencies: PASS")
        else:
            compliance_checks.append("Dependencies: FAIL")
        
        # Overall compliance
        pass_count = sum(1 for check in compliance_checks if "PASS" in check)
        total_checks = len(compliance_checks)
        
        if pass_count == total_checks:
            return f"FULLY COMPLIANT ({pass_count}/{total_checks})"
        else:
            return f"PARTIALLY COMPLIANT ({pass_count}/{total_checks})"
    
    def export_report(self, report: QualityReport, output_path: str, format: str = "json") -> bool:
        """
        Export quality report to specified format and path.
        
        Args:
            report: Quality report to export
            output_path: Path to save the report
            format: Export format (json, markdown, html)
            
        Returns:
            bool: True if export successful
        """
        try:
            if format.lower() == "json":
                return self._export_json(report, output_path)
            elif format.lower() == "markdown":
                return self._export_markdown(report, output_path)
            elif format.lower() == "html":
                return self._export_html(report, output_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            print(f"Error exporting report: {e}")
            return False
    
    def _export_json(self, report: QualityReport, output_path: str) -> bool:
        """Export report as JSON."""
        try:
            with open(output_path, 'w') as f:
                json.dump(asdict(report), f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return False
    
    def _export_markdown(self, report: QualityReport, output_path: str) -> bool:
        """Export report as Markdown."""
        try:
            markdown_content = f"""# Quality Assessment Report - {report.report_id}

## Executive Summary
- **Overall Quality Score**: {report.overall_quality_score}/100
- **Risk Assessment**: {report.risk_assessment}
- **Compliance Status**: {report.compliance_status}
- **Analysis Date**: {report.timestamp}

## Coverage Analysis
- **Overall Coverage**: {report.coverage_metrics.get('overall_coverage', 0.0):.1f}%
- **Function Coverage**: {report.coverage_metrics.get('function_coverage', 0.0):.1f}%
- **Class Coverage**: {report.coverage_metrics.get('class_coverage', 0.0):.1f}%

## Complexity Analysis
- **Average Cyclomatic Complexity**: {report.complexity_metrics.get('average_cyclomatic', 0.0):.1f}
- **Max Nesting Depth**: {report.complexity_metrics.get('max_nesting_depth', 0)}
- **Total Functions**: {report.complexity_metrics.get('total_functions', 0)}

## Dependency Analysis
- **Overall Dependency Score**: {report.dependency_metrics.get('overall_dependency_score', 0.0):.2f}
- **Circular Dependencies**: {report.dependency_metrics.get('circular_dependencies_found', 0)}

## Recommendations
{chr(10).join(f"- {rec}" for rec in report.recommendations)}

## Compliance Details
{report.compliance_status}
"""
            
            with open(output_path, 'w') as f:
                f.write(markdown_content)
            return True
        except Exception as e:
            print(f"Error exporting Markdown: {e}")
            return False
    
    def _export_html(self, report: QualityReport, output_path: str) -> bool:
        """Export report as HTML."""
        try:
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Quality Assessment Report - {report.report_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .metric {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007acc; }}
        .score {{ font-size: 24px; font-weight: bold; color: #007acc; }}
        .risk-high {{ color: #d32f2f; }}
        .risk-medium {{ color: #f57c00; }}
        .risk-low {{ color: #388e3c; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Quality Assessment Report</h1>
        <p><strong>Report ID:</strong> {report.report_id}</p>
        <p><strong>Date:</strong> {report.timestamp}</p>
        <p><strong>Target:</strong> {report.target_directory}</p>
    </div>
    
    <div class="metric">
        <h2>Overall Quality Score</h2>
        <div class="score">{report.overall_quality_score}/100</div>
        <p><strong>Risk Level:</strong> <span class="risk-{'high' if 'HIGH' in report.risk_assessment else 'medium' if 'MEDIUM' in report.risk_assessment else 'low'}">{report.risk_assessment}</span></p>
        <p><strong>Compliance:</strong> {report.compliance_status}</p>
    </div>
    
    <div class="metric">
        <h2>Coverage Analysis</h2>
        <p>Overall Coverage: {report.coverage_metrics.get('overall_coverage', 0.0):.1f}%</p>
        <p>Function Coverage: {report.coverage_metrics.get('function_coverage', 0.0):.1f}%</p>
        <p>Class Coverage: {report.coverage_metrics.get('class_coverage', 0.0):.1f}%</p>
    </div>
    
    <div class="metric">
        <h2>Complexity Analysis</h2>
        <p>Average Cyclomatic Complexity: {report.complexity_metrics.get('average_cyclomatic', 0.0):.1f}</p>
        <p>Max Nesting Depth: {report.complexity_metrics.get('max_nesting_depth', 0)}</p>
        <p>Total Functions: {report.complexity_metrics.get('total_functions', 0)}</p>
    </div>
    
    <div class="metric">
        <h2>Dependency Analysis</h2>
        <p>Overall Dependency Score: {report.dependency_metrics.get('overall_dependency_score', 0.0):.2f}</p>
        <p>Circular Dependencies: {report.dependency_metrics.get('circular_dependencies_found', 0)}</p>
    </div>
    
    <div class="metric">
        <h2>Recommendations</h2>
        <ul>
            {chr(10).join(f'<li>{rec}</li>' for rec in report.recommendations)}
        </ul>
    </div>
</body>
</html>"""
            
            with open(output_path, 'w') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error exporting HTML: {e}")
            return False
