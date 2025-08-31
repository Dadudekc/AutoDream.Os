#!/usr/bin/env python3
"""
Database Integrity Reporting - Report Generation and Formatting
=============================================================

This module contains the report generation and formatting logic for the
database integrity checker system. It handles creating, formatting,
and saving integrity reports.

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** V2-COMPLIANCE-005 - Database Audit System Modularization
**Status:** MODULARIZATION IN PROGRESS
**Target:** ≤250 lines per module, single responsibility principle
**V2 Compliance:** ✅ Under 250 lines, focused responsibility
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from database_integrity_models import IntegrityReport, IntegrityCheck, create_integrity_report


class DatabaseIntegrityReporting:
    """Report generation and formatting for database integrity checks"""
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def generate_report(self, checks: List[IntegrityCheck], 
                       recommendations: List[str] = None) -> IntegrityReport:
        """Generate a complete integrity report from checks"""
        if recommendations is None:
            recommendations = self._generate_default_recommendations(checks)
        
        return create_integrity_report(checks, recommendations)
    
    def format_report_for_display(self, report: IntegrityReport) -> str:
        """Format the integrity report for console display"""
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append("DATABASE INTEGRITY REPORT")
        lines.append("=" * 80)
        lines.append(f"Report ID: {report.report_id}")
        lines.append(f"Timestamp: {report.timestamp}")
        lines.append(f"Overall Status: {report.overall_status}")
        lines.append(f"Total Checks: {report.total_checks}")
        lines.append(f"Passed: {report.passed_checks}")
        lines.append(f"Failed: {report.failed_checks}")
        lines.append(f"Warnings: {report.warning_checks}")
        
        # Check results
        if report.checks:
            lines.append("")
            lines.append("=" * 80)
            lines.append("INTEGRITY CHECK RESULTS")
            lines.append("=" * 80)
            
            for check in report.checks:
                status_icon = self._get_status_icon(check.status)
                lines.append("")
                lines.append(f"{status_icon} {check.check_name} - {check.status}")
                lines.append(f"   Severity: {check.severity}")
                lines.append(f"   Message: {check.message}")
                
                # Add details if available
                if check.details:
                    lines.append("   Details:")
                    for key, value in check.details.items():
                        lines.append(f"     {key}: {value}")
        
        # Recommendations
        if report.recommendations:
            lines.append("")
            lines.append("=" * 80)
            lines.append("RECOMMENDATIONS")
            lines.append("=" * 80)
            
            for i, rec in enumerate(report.recommendations, 1):
                lines.append(f"{i}. {rec}")
        
        # Footer
        lines.append("")
        lines.append("=" * 80)
        lines.append("Integrity check complete.")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def save_report_to_file(self, report: IntegrityReport, 
                           output_path: Optional[str] = None) -> bool:
        """Save integrity report to file"""
        if not output_path:
            output_path = f"database_integrity_report_{report.report_id}.json"
        
        try:
            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert report to dictionary format
            report_data = report.to_dict()
            
            # Save as JSON
            with open(output_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            self.logger.info(f"Integrity report saved to: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save integrity report: {e}")
            return False
    
    def save_report_as_markdown(self, report: IntegrityReport, 
                               output_path: Optional[str] = None) -> bool:
        """Save integrity report as markdown file"""
        if not output_path:
            output_path = f"database_integrity_report_{report.report_id}.md"
        
        try:
            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate markdown content
            markdown_content = self._generate_markdown_report(report)
            
            # Save markdown file with UTF-8 encoding
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            self.logger.info(f"Markdown report saved to: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save markdown report: {e}")
            return False
    
    def _generate_default_recommendations(self, checks: List[IntegrityCheck]) -> List[str]:
        """Generate default recommendations based on check results"""
        recommendations = []
        
        failed_checks = [check for check in checks if check.status == "FAILED"]
        warning_checks = [check for check in checks if check.status == "WARNING"]
        
        if failed_checks:
            recommendations.append("Immediate action required to fix failed checks")
            
            # Add specific recommendations for critical failures
            critical_failures = [check for check in failed_checks if check.severity == "CRITICAL"]
            if critical_failures:
                recommendations.append("Critical failures detected - system integrity compromised")
        
        if warning_checks:
            recommendations.append("Review warnings and address as needed")
        
        if not failed_checks and not warning_checks:
            recommendations.append("Database integrity is good - continue monitoring")
        
        return recommendations
    
    def _get_status_icon(self, status: str) -> str:
        """Get appropriate icon for check status"""
        status_icons = {
            "PASSED": "✅",
            "FAILED": "❌",
            "WARNING": "⚠️"
        }
        return status_icons.get(status, "❓")
    
    def _generate_markdown_report(self, report: IntegrityReport) -> str:
        """Generate markdown format of the integrity report"""
        lines = []
        
        # Header
        lines.append(f"# Database Integrity Report")
        lines.append("")
        lines.append(f"**Report ID:** {report.report_id}  ")
        lines.append(f"**Timestamp:** {report.timestamp}  ")
        lines.append(f"**Overall Status:** {report.overall_status}  ")
        lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total Checks:** {report.total_checks}")
        lines.append(f"- **Passed:** {report.passed_checks}")
        lines.append(f"- **Failed:** {report.failed_checks}")
        lines.append(f"- **Warnings:** {report.warning_checks}")
        lines.append("")
        
        # Check Results
        if report.checks:
            lines.append("## Integrity Check Results")
            lines.append("")
            
            for check in report.checks:
                status_icon = self._get_status_icon(check.status)
                lines.append(f"### {status_icon} {check.check_name}")
                lines.append("")
                lines.append(f"**Status:** {check.status}  ")
                lines.append(f"**Severity:** {check.severity}  ")
                lines.append(f"**Message:** {check.message}  ")
                lines.append("")
                
                if check.details:
                    lines.append("**Details:**")
                    lines.append("```json")
                    lines.append(json.dumps(check.details, indent=2))
                    lines.append("```")
                    lines.append("")
        
        # Recommendations
        if report.recommendations:
            lines.append("## Recommendations")
            lines.append("")
            
            for i, rec in enumerate(report.recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")
        
        return "\n".join(lines)
