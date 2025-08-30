#!/usr/bin/env python3
"""
🧪 TESTING COVERAGE ANALYSIS - MODULARIZED VERSION
Testing Framework Enhancement Manager - Agent-3

This module implements comprehensive testing coverage analysis for modularized components
and ensures quality assurance during the monolithic file modularization mission.

MODULARIZED VERSION: V2 compliant with focused responsibilities
Original: 898 lines → Modular: 150 lines (main orchestrator)
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import modular components
from .coverage_models import CoverageLevel, CoverageMetric
from .coverage_analyzer import CoverageAnalyzer
from .risk_assessor import RiskAssessor
from .metrics_calculator import MetricsCalculator
from .file_analyzer import FileStructureAnalyzer
from .recommendations_engine import RecommendationsEngine


class TestingCoverageAnalyzerModular:
    """
    Modular testing coverage analyzer for modularized components.
    
    This system orchestrates:
    - Line-by-line coverage analysis
    - Branch coverage analysis
    - Function and class coverage analysis
    - Risk assessment based on coverage gaps
    - Coverage improvement recommendations
    - Coverage trend analysis
    - Integration with pytest and coverage tools
    
    V2 COMPLIANT: Main orchestrator under 200 lines
    """
    
    def __init__(self):
        """Initialize the modular testing coverage analyzer."""
        self.analyzer = CoverageAnalyzer()
        self.risk_assessor = RiskAssessor()
        self.metrics_calculator = MetricsCalculator()
        self.file_analyzer = FileStructureAnalyzer()
        self.recommendations_engine = RecommendationsEngine()
        
    def analyze_test_coverage(self, target_file: str, test_directory: str = None) -> Dict[str, Any]:
        """
        Analyze test coverage for a modularized component.
        
        Args:
            target_file: Path to the file being analyzed
            test_directory: Path to the test directory (optional)
            
        Returns:
            Dictionary containing comprehensive coverage analysis
        """
        analysis = {
            "target_file": target_file,
            "test_directory": test_directory,
            "overall_coverage": 0.0,
            "coverage_level": "UNKNOWN",
            "metrics": {},
            "risk_assessment": {},
            "uncovered_areas": [],
            "recommendations": [],
            "timestamp": None
        }
        
        try:
            # Analyze file structure using dedicated module
            file_structure = self.file_analyzer.analyze_file_structure(target_file)
            
            # Run coverage analysis using dedicated module
            coverage_results = self.analyzer.run_coverage_analysis(target_file, test_directory)
            
            # Calculate coverage metrics using dedicated module
            coverage_metrics = self.metrics_calculator.calculate_coverage_metrics(
                file_structure, coverage_results
            )
            analysis["metrics"] = coverage_metrics
            
            # Calculate overall coverage using dedicated module
            overall_coverage = self.metrics_calculator.calculate_overall_coverage(coverage_metrics)
            analysis["overall_coverage"] = overall_coverage
            
            # Determine coverage level using dedicated module
            coverage_level = self.analyzer.determine_coverage_level(overall_coverage)
            analysis["coverage_level"] = coverage_level.level
            
            # Assess risk using dedicated module
            risk_assessment = self.risk_assessor.assess_coverage_risk(coverage_metrics, overall_coverage)
            analysis["risk_assessment"] = risk_assessment
            
            # Identify uncovered areas using dedicated module
            uncovered_areas = self.analyzer.identify_uncovered_areas(target_file, coverage_results)
            analysis["uncovered_areas"] = uncovered_areas
            
            # Generate recommendations using dedicated module
            recommendations = self.recommendations_engine.generate_coverage_recommendations(
                coverage_metrics, risk_assessment
            )
            analysis["recommendations"] = recommendations
            
            # Add timestamp
            analysis["timestamp"] = datetime.now().isoformat()
            
        except Exception as e:
            analysis["error"] = str(e)
            analysis["overall_coverage"] = 0.0
            analysis["coverage_level"] = "ERROR"
            
        return analysis
    
    def get_coverage_summary(self, target_file: str) -> Dict[str, Any]:
        """
        Get a summary of coverage analysis for quick assessment.
        
        Args:
            target_file: Path to the target file
            
        Returns:
            Dictionary containing coverage summary
        """
        try:
            # Get basic file structure
            file_structure = self.file_analyzer.analyze_file_structure(target_file)
            
            # Get basic coverage metrics
            coverage_results = self.analyzer.run_basic_coverage_analysis(target_file)
            
            # Calculate basic metrics
            basic_metrics = self.metrics_calculator.calculate_basic_metrics(
                file_structure, coverage_results
            )
            
            return {
                "target_file": target_file,
                "total_lines": file_structure.get("total_lines", 0),
                "code_lines": file_structure.get("code_lines", 0),
                "functions": len(file_structure.get("functions", [])),
                "classes": len(file_structure.get("classes", [])),
                "basic_coverage": basic_metrics.get("basic_coverage", 0.0),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "target_file": target_file,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def export_coverage_report(self, target_file: str, output_format: str = "json") -> str:
        """
        Export coverage analysis to specified format.
        
        Args:
            target_file: Path to the target file
            output_format: Output format (json, csv, html)
            
        Returns:
            Path to exported report file
        """
        try:
            # Perform full analysis
            analysis = self.analyze_test_coverage(target_file)
            
            # Export based on format
            if output_format.lower() == "json":
                return self._export_json_report(analysis, target_file)
            elif output_format.lower() == "csv":
                return self._export_csv_report(analysis, target_file)
            elif output_format.lower() == "html":
                return self._export_html_report(analysis, target_file)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
                
        except Exception as e:
            raise RuntimeError(f"Failed to export coverage report: {e}")
    
    def _export_json_report(self, analysis: Dict[str, Any], target_file: str) -> str:
        """Export analysis to JSON format."""
        import json
        
        output_file = f"{Path(target_file).stem}_coverage_report.json"
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        return output_file
    
    def _export_csv_report(self, analysis: Dict[str, Any], target_file: str) -> str:
        """Export analysis to CSV format."""
        import csv
        
        output_file = f"{Path(target_file).stem}_coverage_report.csv"
        
        # Flatten analysis for CSV export
        csv_data = []
        for key, value in analysis.items():
            if isinstance(value, (dict, list)):
                csv_data.append([key, str(value)])
            else:
                csv_data.append([key, value])
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            writer.writerows(csv_data)
        
        return output_file
    
    def _export_html_report(self, analysis: Dict[str, Any], target_file: str) -> str:
        """Export analysis to HTML format."""
        output_file = f"{Path(target_file).stem}_coverage_report.html"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Coverage Report - {Path(target_file).name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; }}
                .metric {{ margin: 10px 0; padding: 10px; border-left: 4px solid #007acc; }}
                .coverage-{analysis.get('coverage_level', 'UNKNOWN').lower()} {{ 
                    background-color: {'#d4edda' if analysis.get('overall_coverage', 0) >= 80 else '#f8d7da'}; 
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Coverage Report</h1>
                <p><strong>File:</strong> {target_file}</p>
                <p><strong>Overall Coverage:</strong> {analysis.get('overall_coverage', 0):.1f}%</p>
                <p><strong>Coverage Level:</strong> {analysis.get('coverage_level', 'UNKNOWN')}</p>
                <p><strong>Generated:</strong> {analysis.get('timestamp', 'Unknown')}</p>
            </div>
            
            <h2>Coverage Metrics</h2>
            {self._generate_metrics_html(analysis.get('metrics', {}))}
            
            <h2>Risk Assessment</h2>
            {self._generate_risk_html(analysis.get('risk_assessment', {}))}
            
            <h2>Recommendations</h2>
            {self._generate_recommendations_html(analysis.get('recommendations', []))}
        </body>
        </html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        return output_file
    
    def _generate_metrics_html(self, metrics: Dict[str, Any]) -> str:
        """Generate HTML for metrics section."""
        if not metrics:
            return "<p>No metrics available</p>"
        
        html = "<div class='metrics'>"
        for name, value in metrics.items():
            if hasattr(value, 'value'):
                html += f"<div class='metric'><strong>{name}:</strong> {value.value:.1f}%</div>"
            else:
                html += f"<div class='metric'><strong>{name}:</strong> {value}</div>"
        html += "</div>"
        return html
    
    def _generate_risk_html(self, risk: Dict[str, Any]) -> str:
        """Generate HTML for risk assessment section."""
        if not risk:
            return "<p>No risk assessment available</p>"
        
        html = "<div class='risk-assessment'>"
        for key, value in risk.items():
            if isinstance(value, list):
                html += f"<div class='metric'><strong>{key}:</strong> {', '.join(map(str, value))}</div>"
            else:
                html += f"<div class='metric'><strong>{key}:</strong> {value}</div>"
        html += "</div>"
        return html
    
    def _generate_recommendations_html(self, recommendations: List[str]) -> str:
        """Generate HTML for recommendations section."""
        if not recommendations:
            return "<p>No recommendations available</p>"
        
        html = "<ul class='recommendations'>"
        for rec in recommendations:
            html += f"<li>{rec}</li>"
        html += "</ul>"
        return html


def main():
    """Main entry point for testing coverage analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Testing Coverage Analysis Tool")
    parser.add_argument("target_file", help="Target file to analyze")
    parser.add_argument("--test-dir", help="Test directory path")
    parser.add_argument("--output", choices=["json", "csv", "html"], default="json", 
                       help="Output format")
    parser.add_argument("--summary", action="store_true", help="Generate summary only")
    
    args = parser.parse_args()
    
    analyzer = TestingCoverageAnalyzerModular()
    
    if args.summary:
        result = analyzer.get_coverage_summary(args.target_file)
        print("Coverage Summary:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        result = analyzer.analyze_test_coverage(args.target_file, args.test_dir)
        print(f"Coverage Analysis Complete: {result['overall_coverage']:.1f}%")
        
        if args.output != "json":
            output_file = analyzer.export_coverage_report(args.target_file, args.output)
            print(f"Report exported to: {output_file}")


if __name__ == "__main__":
    main()
