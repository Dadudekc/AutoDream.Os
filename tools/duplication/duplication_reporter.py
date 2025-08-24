#!/usr/bin/env python3
"""
Duplication Reporter - Agent Cellphone V2
=========================================

Reporting and output generation for duplication detection.
Follows V2 standards: ≤200 LOC, OOP design, SRP compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from .duplication_types import DuplicationIssue, DuplicationReport, DuplicationSeverity


class DuplicationReporter:
    """Generates reports for duplication detection results"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_report(self, issues: List[DuplicationIssue], 
                       total_files: int = 0) -> DuplicationReport:
        """Generate comprehensive duplication report"""
        timestamp = datetime.now().isoformat()
        
        # Group issues by severity
        issues_by_severity = self._group_issues_by_severity(issues)
        
        # Generate summary
        summary = self._generate_summary(issues, total_files)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(issues)
        
        report = DuplicationReport(
            timestamp=timestamp,
            total_files_analyzed=total_files,
            total_issues_found=len(issues),
            issues_by_severity=issues_by_severity,
            summary=summary,
            recommendations=recommendations
        )
        
        return report
    
    def print_report(self, report: DuplicationReport):
        """Print formatted report to console"""
        print("\n" + "="*60)
        print("🔍 DUPLICATION DETECTION REPORT")
        print("="*60)
        print(f"📅 Timestamp: {report.timestamp}")
        print(f"📁 Files Analyzed: {report.total_files_analyzed}")
        print(f"⚠️  Issues Found: {report.total_issues_found}")
        print()
        
        # Print issues by severity
        for severity in DuplicationSeverity:
            count = report.issues_by_severity.get(severity.value, 0)
            if count > 0:
                icon = self._get_severity_icon(severity)
                print(f"{icon} {severity.value.upper()}: {count} issues")
        
        print()
        print("📋 SUMMARY:")
        print(report.summary)
        
        if report.recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(report.recommendations, 1):
                print(f"  {i}. {rec}")
        
        print("="*60)
    
    def save_json_report(self, report: DuplicationReport, output_path: str):
        """Save report as JSON file"""
        try:
            # Convert report to dict for JSON serialization
            report_dict = {
                'timestamp': report.timestamp,
                'total_files_analyzed': report.total_files_analyzed,
                'total_issues_found': report.total_issues_found,
                'issues_by_severity': report.issues_by_severity,
                'summary': report.summary,
                'recommendations': report.recommendations
            }
            
            with open(output_path, 'w') as f:
                json.dump(report_dict, f, indent=2)
            
            self.logger.info(f"Report saved to: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")
    
    def generate_detailed_report(self, issues: List[DuplicationIssue]) -> str:
        """Generate detailed text report"""
        lines = []
        lines.append("DETAILED DUPLICATION REPORT")
        lines.append("=" * 50)
        lines.append("")
        
        # Group by issue type
        issues_by_type = {}
        for issue in issues:
            if issue.issue_type not in issues_by_type:
                issues_by_type[issue.issue_type] = []
            issues_by_type[issue.issue_type].append(issue)
        
        for issue_type, type_issues in issues_by_type.items():
            lines.append(f"📋 {issue_type.upper()} ISSUES ({len(type_issues)})")
            lines.append("-" * 30)
            
            for issue in type_issues:
                lines.append(f"Severity: {issue.severity.value}")
                lines.append(f"Description: {issue.description}")
                lines.append(f"Files: {', '.join(issue.files_involved)}")
                lines.append(f"Similarity: {issue.similarity_score:.2f}")
                lines.append(f"Action: {issue.suggested_action}")
                lines.append("")
        
        return "\n".join(lines)
    
    def _group_issues_by_severity(self, issues: List[DuplicationIssue]) -> Dict[str, int]:
        """Group issues by severity level"""
        groups = {}
        for issue in issues:
            severity = issue.severity.value
            groups[severity] = groups.get(severity, 0) + 1
        return groups
    
    def _generate_summary(self, issues: List[DuplicationIssue], total_files: int) -> str:
        """Generate summary of duplication analysis"""
        if not issues:
            return "No duplication issues found. Codebase is clean!"
        
        critical_count = len([i for i in issues if i.severity == DuplicationSeverity.CRITICAL])
        high_count = len([i for i in issues if i.severity == DuplicationSeverity.HIGH])
        medium_count = len([i for i in issues if i.severity == DuplicationSeverity.MEDIUM])
        low_count = len([i for i in issues if i.severity == DuplicationSeverity.LOW])
        
        summary = f"Found {len(issues)} duplication issues across {total_files} files. "
        summary += f"Critical: {critical_count}, High: {high_count}, "
        summary += f"Medium: {medium_count}, Low: {low_count}."
        
        if critical_count > 0 or high_count > 0:
            summary += " Immediate attention required for high-severity issues."
        
        return summary
    
    def _generate_recommendations(self, issues: List[DuplicationIssue]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Analyze issue patterns
        issue_types = [i.issue_type for i in issues]
        severity_counts = {}
        
        for issue in issues:
            severity = issue.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Generate specific recommendations
        if severity_counts.get('CRITICAL', 0) > 0:
            recommendations.append("Address critical duplication issues immediately")
        
        if severity_counts.get('HIGH', 0) > 0:
            recommendations.append("Refactor high-severity duplications within 1-2 days")
        
        if 'exact_duplicate' in issue_types:
            recommendations.append("Extract exact duplicates to shared utility functions")
        
        if 'similar_structure' in issue_types:
            recommendations.append("Create base classes for similar code structures")
        
        if 'duplicate_import' in issue_types:
            recommendations.append("Consolidate duplicate imports in shared modules")
        
        if 'backup_file' in issue_types:
            recommendations.append("Remove backup files and use version control")
        
        if len(issues) > 10:
            recommendations.append("Schedule regular duplication reviews")
        
        if not recommendations:
            recommendations.append("Monitor for new duplication issues")
        
        return recommendations
    
    def _get_severity_icon(self, severity: DuplicationSeverity) -> str:
        """Get icon for severity level"""
        icons = {
            DuplicationSeverity.CRITICAL: "🚨",
            DuplicationSeverity.HIGH: "⚠️",
            DuplicationSeverity.MEDIUM: "🔶",
            DuplicationSeverity.LOW: "ℹ️"
        }
        return icons.get(severity, "❓")
