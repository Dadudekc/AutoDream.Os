#!/usr/bin/env python3
"""
Compliance Analyzer Module
==========================

Handles compliance analysis and reporting operations.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from .standards_core import StandardsCore, FileComplianceReport, StandardsViolation


@dataclass
class ComplianceSummary:
    """Summary of compliance analysis"""
    timestamp: str
    overall_compliance: float
    total_files: int
    compliant_files: int
    violation_counts: Dict[str, int]
    average_scores: Dict[str, float]
    recommendations: List[str]


class ComplianceAnalyzer:
    """Analyzes codebase compliance with coding standards"""
    
    def __init__(self, standards_core: StandardsCore):
        self.standards_core = standards_core
        self.analysis_results: List[FileComplianceReport] = []
        
    def analyze_codebase_compliance(self, src_directories: Optional[List[str]] = None) -> ComplianceSummary:
        """Analyze the entire codebase for coding standards compliance"""
        try:
            if src_directories is None:
                src_directories = ["src", "agent_workspaces", "scripts"]
            
            self.analysis_results.clear()
            
            # Analyze each source directory
            for src_dir in src_directories:
                src_path = self.standards_core.workspace_root / src_dir
                if src_path.exists():
                    self._analyze_directory(src_path)
            
            # Generate compliance summary
            summary = self._generate_compliance_summary()
            
            return summary
            
        except Exception as e:
            # Return error summary
            return ComplianceSummary(
                timestamp=datetime.now().isoformat(),
                overall_compliance=0.0,
                total_files=0,
                compliant_files=0,
                violation_counts={},
                average_scores={},
                recommendations=[f"Analysis error: {str(e)}"]
            )
    
    def _analyze_directory(self, directory_path: Path) -> None:
        """Analyze all Python files in a directory recursively"""
        try:
            # Find all Python files
            python_files = list(directory_path.rglob("*.py"))
            
            for file_path in python_files:
                # Skip certain directories
                if self._should_skip_file(file_path):
                    continue
                
                # Analyze file compliance
                compliance_report = self.standards_core.analyze_file_standards_compliance(file_path)
                self.analysis_results.append(compliance_report)
                
        except Exception as e:
            print(f"Error analyzing directory {directory_path}: {e}")
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if a file should be skipped from analysis"""
        try:
            # Skip common directories that don't need standards compliance
            skip_patterns = [
                "__pycache__",
                ".git",
                "node_modules",
                "venv",
                "env",
                ".venv",
                ".env"
            ]
            
            for pattern in skip_patterns:
                if pattern in str(file_path):
                    return True
            
            # Skip certain file types
            skip_files = [
                "setup.py",
                "requirements.txt",
                "README.md"
            ]
            
            if file_path.name in skip_files:
                return True
            
            return False
            
        except Exception:
            return False
    
    def _generate_compliance_summary(self) -> ComplianceSummary:
        """Generate comprehensive compliance summary from analysis results"""
        try:
            if not self.analysis_results:
                return ComplianceSummary(
                    timestamp=datetime.now().isoformat(),
                    overall_compliance=0.0,
                    total_files=0,
                    compliant_files=0,
                    violation_counts={},
                    average_scores={},
                    recommendations=[]
                )
            
            total_files = len(self.analysis_results)
            compliant_files = sum(1 for r in self.analysis_results if r.compliant)
            overall_compliance = (compliant_files / total_files) * 100 if total_files > 0 else 0.0
            
            # Count violations by type
            violation_counts = {}
            for report in self.analysis_results:
                for violation in report.violations:
                    violation_type = violation.violation_type
                    violation_counts[violation_type] = violation_counts.get(violation_type, 0) + 1
            
            # Calculate average scores
            average_scores = self._calculate_average_scores()
            
            # Generate recommendations
            recommendations = self._generate_recommendations(violation_counts, average_scores)
            
            return ComplianceSummary(
                timestamp=datetime.now().isoformat(),
                overall_compliance=overall_compliance,
                total_files=total_files,
                compliant_files=compliant_files,
                violation_counts=violation_counts,
                average_scores=average_scores,
                recommendations=recommendations
            )
            
        except Exception as e:
            return ComplianceSummary(
                timestamp=datetime.now().isoformat(),
                overall_compliance=0.0,
                total_files=0,
                compliant_files=0,
                violation_counts={},
                average_scores={},
                recommendations=[f"Error generating summary: {str(e)}"]
            )
    
    def _calculate_average_scores(self) -> Dict[str, float]:
        """Calculate average scores across all analyzed files"""
        try:
            scores = {
                "oop_score": [],
                "srp_score": [],
                "cli_score": [],
                "test_score": []
            }
            
            for report in self.analysis_results:
                scores["oop_score"].append(report.oop_score)
                scores["srp_score"].append(report.srp_score)
                scores["cli_score"].append(report.cli_score)
                scores["test_score"].append(report.test_score)
            
            average_scores = {}
            for score_type, score_list in scores.items():
                if score_list:
                    average_scores[score_type] = sum(score_list) / len(score_list)
                else:
                    average_scores[score_type] = 0.0
            
            return average_scores
            
        except Exception:
            return {
                "oop_score": 0.0,
                "srp_score": 0.0,
                "cli_score": 0.0,
                "test_score": 0.0
            }
    
    def _generate_recommendations(self, violation_counts: Dict[str, int], 
                                 average_scores: Dict[str, float]) -> List[str]:
        """Generate recommendations based on analysis results"""
        try:
            recommendations = []
            
            # Line count violations
            if "line_count" in violation_counts:
                count = violation_counts["line_count"]
                recommendations.append(f"Refactor {count} files to meet line count limits (≤400 LOC)")
            
            # OOP design violations
            if "oop_design" in violation_counts:
                count = violation_counts["oop_design"]
                recommendations.append(f"Improve OOP design in {count} files")
            
            # Single responsibility violations
            if "single_responsibility" in violation_counts:
                count = violation_counts["single_responsibility"]
                recommendations.append(f"Apply single responsibility principle to {count} files")
            
            # CLI interface violations
            if "cli_interface" in violation_counts:
                count = violation_counts["cli_interface"]
                recommendations.append(f"Add CLI interfaces to {count} files")
            
            # Smoke tests violations
            if "smoke_tests" in violation_counts:
                count = violation_counts["smoke_tests"]
                recommendations.append(f"Add smoke tests to {count} files")
            
            # Score-based recommendations
            oop_score = average_scores.get("oop_score", 0.0)
            if oop_score < 0.6:
                recommendations.append("Focus on improving overall OOP design across the codebase")
            
            srp_score = average_scores.get("srp_score", 0.0)
            if srp_score < 0.6:
                recommendations.append("Emphasize single responsibility principle in code reviews")
            
            cli_score = average_scores.get("cli_score", 0.0)
            if cli_score < 0.5:
                recommendations.append("Prioritize adding CLI interfaces to improve usability")
            
            test_score = average_scores.get("test_score", 0.0)
            if test_score < 0.5:
                recommendations.append("Increase test coverage with smoke tests")
            
            if not recommendations:
                recommendations.append("Codebase is well-compliant with V2 standards")
            
            return recommendations
            
        except Exception:
            return ["Error generating recommendations"]
    
    def get_violation_details(self, violation_type: Optional[str] = None) -> List[StandardsViolation]:
        """Get detailed violation information"""
        try:
            all_violations = []
            
            for report in self.analysis_results:
                if violation_type is None:
                    all_violations.extend(report.violations)
                else:
                    for violation in report.violations:
                        if violation.violation_type == violation_type:
                            all_violations.append(violation)
            
            return all_violations
            
        except Exception:
            return []
    
    def get_files_by_compliance_status(self, compliant: bool = True) -> List[str]:
        """Get list of files by compliance status"""
        try:
            if compliant:
                return [r.file_path for r in self.analysis_results if r.compliant]
            else:
                return [r.file_path for r in self.analysis_results if not r.compliant]
                
        except Exception:
            return []
    
    def export_compliance_report(self, output_file: str) -> bool:
        """Export comprehensive compliance report to JSON file"""
        try:
            summary = self._generate_compliance_summary()
            
            report_data = {
                "summary": asdict(summary),
                "file_reports": [asdict(r) for r in self.analysis_results],
                "export_timestamp": datetime.now().isoformat()
            }
            
            with open(output_file, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            return True
            
        except Exception:
            return False
    
    def get_compliance_trends(self) -> Dict[str, Any]:
        """Get compliance trends and statistics"""
        try:
            if not self.analysis_results:
                return {"error": "No analysis results available"}
            
            # Group by directory
            directory_stats = {}
            for report in self.analysis_results:
                file_path = Path(report.file_path)
                directory = file_path.parent.name
                
                if directory not in directory_stats:
                    directory_stats[directory] = {
                        "total_files": 0,
                        "compliant_files": 0,
                        "total_violations": 0
                    }
                
                directory_stats[directory]["total_files"] += 1
                if report.compliant:
                    directory_stats[directory]["compliant_files"] += 1
                directory_stats[directory]["total_violations"] += len(report.violations)
            
            # Calculate compliance rates by directory
            for directory, stats in directory_stats.items():
                stats["compliance_rate"] = (
                    stats["compliant_files"] / stats["total_files"] * 100
                    if stats["total_files"] > 0 else 0.0
                )
            
            return {
                "directory_compliance": directory_stats,
                "total_analysis": len(self.analysis_results),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}
