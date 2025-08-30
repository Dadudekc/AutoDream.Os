"""
Core Analyzer - Main coverage analysis orchestration.

This module orchestrates the coverage analysis process using the modular components.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from .coverage_models import CoverageResult, CoverageLevel
from .coverage_calculator import CoverageCalculator
from .risk_assessor import RiskAssessor
from .recommendations_engine import RecommendationsEngine


class CoreCoverageAnalyzer:
    """
    Core coverage analyzer that orchestrates the modular analysis components.
    
    This class coordinates the analysis process using specialized modules for:
    - Coverage calculations
    - Risk assessment
    - Recommendations generation
    """
    
    def __init__(self):
        self.calculator = CoverageCalculator()
        self.risk_assessor = RiskAssessor()
        self.recommendations_engine = RecommendationsEngine()
        self.coverage_levels = self._initialize_coverage_levels()
    
    def _initialize_coverage_levels(self) -> Dict[str, CoverageLevel]:
        """Initialize coverage level classifications."""
        return {
            "excellent": CoverageLevel("EXCELLENT", 95.0, "Outstanding test coverage", "🟢"),
            "good": CoverageLevel("GOOD", 85.0, "Good test coverage", "🟡"),
            "fair": CoverageLevel("FAIR", 75.0, "Acceptable test coverage", "🟠"),
            "poor": CoverageLevel("POOR", 60.0, "Below acceptable coverage", "🔴"),
            "critical": CoverageLevel("CRITICAL", 45.0, "Critical coverage gaps", "⚫")
        }
    
    def analyze_test_coverage(self, target_file: str, test_directory: str = None) -> CoverageResult:
        """
        Analyze test coverage for a modularized component.
        
        Args:
            target_file: Path to the file being analyzed
            test_directory: Optional directory containing tests
            
        Returns:
            CoverageResult with complete analysis
        """
        try:
            # Step 1: Analyze file structure
            file_structure = self.calculator.analyze_file_structure(target_file)
            
            # Step 2: Run coverage analysis (simulated for now)
            coverage_data = self._run_coverage_analysis(target_file, test_directory)
            
            # Step 3: Calculate coverage metrics
            metrics = self.calculator.calculate_coverage_metrics(file_structure, coverage_data)
            
            # Step 4: Calculate overall coverage
            overall_coverage = self.calculator.calculate_overall_coverage(metrics)
            
            # Step 5: Assess risk
            risk_assessment = self.risk_assessor.assess_coverage_risk(metrics, overall_coverage)
            
            # Step 6: Identify uncovered areas
            uncovered_areas = self.risk_assessor.identify_uncovered_areas(
                target_file, file_structure, coverage_data
            )
            
            # Step 7: Generate recommendations
            recommendations = self.recommendations_engine.generate_coverage_recommendations(
                metrics, uncovered_areas
            )
            
            # Step 8: Create result
            result = CoverageResult(
                file_path=target_file,
                timestamp=datetime.now().isoformat(),
                overall_coverage=overall_coverage,
                line_coverage=metrics.get("line_coverage", {}).value if metrics.get("line_coverage") else 0.0,
                branch_coverage=metrics.get("branch_coverage", {}).value if metrics.get("branch_coverage") else 0.0,
                function_coverage=metrics.get("function_coverage", {}).value if metrics.get("function_coverage") else 0.0,
                class_coverage=metrics.get("class_coverage", {}).value if metrics.get("class_coverage") else 0.0,
                risk_level=risk_assessment.risk_level,
                recommendations=recommendations,
                uncovered_areas=uncovered_areas
            )
            
            return result
            
        except Exception as e:
            # Return error result
            return CoverageResult(
                file_path=target_file,
                timestamp=datetime.now().isoformat(),
                overall_coverage=0.0,
                line_coverage=0.0,
                branch_coverage=0.0,
                function_coverage=0.0,
                class_coverage=0.0,
                risk_level="ERROR",
                recommendations=[f"Analysis failed: {str(e)}"],
                uncovered_areas=[]
            )
    
    def _run_coverage_analysis(self, target_file: str, test_directory: str = None) -> Dict[str, Any]:
        """
        Run coverage analysis tools (simulated for now).
        
        In a real implementation, this would integrate with pytest-cov, coverage.py, etc.
        """
        # Simulated coverage data - replace with actual tool integration
        return {
            "line_coverage": 85.0,  # Simulated line coverage
            "branch_coverage": 80.0,  # Simulated branch coverage
            "functions": ["test_function1", "test_function2"],  # Simulated covered functions
            "classes": ["TestClass1"],  # Simulated covered classes
            "uncovered_lines": [10, 15, 20],  # Simulated uncovered line numbers
            "uncovered_branches": ["if x > 0", "except ValueError"]  # Simulated uncovered branches
        }
    
    def determine_coverage_level(self, coverage: float) -> CoverageLevel:
        """Determine coverage level based on percentage."""
        if coverage >= 95.0:
            return self.coverage_levels["excellent"]
        elif coverage >= 85.0:
            return self.coverage_levels["good"]
        elif coverage >= 75.0:
            return self.coverage_levels["fair"]
        elif coverage >= 60.0:
            return self.coverage_levels["poor"]
        else:
            return self.coverage_levels["critical"]
    
    def generate_summary_report(self, result: CoverageResult) -> Dict[str, Any]:
        """Generate a summary report from coverage analysis results."""
        coverage_level = self.determine_coverage_level(result.overall_coverage)
        
        return {
            "file_path": result.file_path,
            "timestamp": result.timestamp,
            "overall_coverage": result.overall_coverage,
            "coverage_level": coverage_level.level,
            "coverage_color": coverage_level.color,
            "risk_level": result.risk_level,
            "total_recommendations": len(result.recommendations),
            "total_uncovered_areas": len(result.uncovered_areas),
            "summary": f"{coverage_level.color} {coverage_level.level} coverage ({result.overall_coverage:.1f}%)"
        }
    
    def export_results(self, result: CoverageResult, format: str = "json") -> str:
        """Export results in specified format."""
        if format.lower() == "json":
            return json.dumps(result.__dict__, indent=2)
        elif format.lower() == "text":
            return self._format_text_report(result)
        else:
            return json.dumps(result.__dict__, indent=2)
    
    def _format_text_report(self, result: CoverageResult) -> str:
        """Format results as human-readable text."""
        coverage_level = self.determine_coverage_level(result.overall_coverage)
        
        report = f"""
Coverage Analysis Report
========================
File: {result.file_path}
Timestamp: {result.timestamp}
Overall Coverage: {result.overall_coverage:.1f}%
Coverage Level: {coverage_level.level} {coverage_level.color}
Risk Level: {result.risk_level}

Coverage Breakdown:
- Line Coverage: {result.line_coverage:.1f}%
- Branch Coverage: {result.branch_coverage:.1f}%
- Function Coverage: {result.function_coverage:.1f}%
- Class Coverage: {result.class_coverage:.1f}%

Uncovered Areas ({len(result.uncovered_areas)}):
"""
        
        for area in result.uncovered_areas[:5]:  # Show first 5
            report += f"- {area}\n"
        
        if len(result.uncovered_areas) > 5:
            report += f"... and {len(result.uncovered_areas) - 5} more\n"
        
        report += f"\nTop Recommendations ({len(result.recommendations)}):\n"
        for i, rec in enumerate(result.recommendations[:5], 1):  # Show first 5
            report += f"{i}. {rec}\n"
        
        if len(result.recommendations) > 5:
            report += f"... and {len(result.recommendations) - 5} more\n"
        
        return report.strip()
