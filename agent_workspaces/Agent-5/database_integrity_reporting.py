#!/usr/bin/env python3
"""
Database Integrity Reporting - EMERGENCY-RESTORE-004 Mission
===========================================================

Reporting system and CLI interface for database integrity checking.
Part of the emergency system restoration mission for Agent-5.
"""

import argparse
import sys
from typing import List
from .database_integrity_models import IntegrityReport, IntegrityCheck


class IntegrityReporter:
    """Reporting system for integrity checks"""
    
    def __init__(self):
        self.output_format = "text"  # text, json, csv
    
    def set_output_format(self, format_type: str):
        """Set the output format for reports"""
        valid_formats = ["text", "json", "csv"]
        if format_type.lower() in valid_formats:
            self.output_format = format_type.lower()
        else:
            raise ValueError(f"Invalid format: {format_type}. Valid formats: {valid_formats}")
    
    def format_report_text(self, report: IntegrityReport) -> str:
        """Format report as text output"""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append("DATABASE INTEGRITY REPORT")
        output.append("=" * 80)
        output.append(f"Report ID: {report.report_id}")
        output.append(f"Timestamp: {report.timestamp}")
        output.append(f"Overall Status: {report.overall_status}")
        output.append(f"Total Checks: {report.total_checks}")
        output.append(f"Passed: {report.passed_checks}")
        output.append(f"Failed: {report.failed_checks}")
        output.append(f"Warnings: {report.warning_checks}")
        
        # Check results
        if report.checks:
            output.append("")
            output.append("=" * 80)
            output.append("INTEGRITY CHECK RESULTS")
            output.append("=" * 80)
            
            for check in report.checks:
                status_icon = "✅" if check.status == "PASSED" else "❌" if check.status == "FAILED" else "⚠️"
                output.append(f"\n{status_icon} {check.check_name} - {check.status}")
                output.append(f"   Severity: {check.severity}")
                output.append(f"   Message: {check.message}")
                
                if check.details:
                    output.append(f"   Details: {check.details}")
        
        # Recommendations
        if report.recommendations:
            output.append("")
            output.append("=" * 80)
            output.append("RECOMMENDATIONS")
            output.append("=" * 80)
            
            for i, recommendation in enumerate(report.recommendations, 1):
                output.append(f"{i}. {recommendation}")
        
        return "\n".join(output)
    
    def format_report_json(self, report: IntegrityReport) -> str:
        """Format report as JSON output"""
        import json
        
        report_dict = {
            "report_id": report.report_id,
            "timestamp": report.timestamp,
            "overall_status": report.overall_status,
            "total_checks": report.total_checks,
            "passed_checks": report.passed_checks,
            "failed_checks": report.failed_checks,
            "warning_checks": report.warning_checks,
            "checks": [
                {
                    "check_id": check.check_id,
                    "check_name": check.check_name,
                    "status": check.status,
                    "severity": check.severity,
                    "message": check.message,
                    "details": check.details,
                    "timestamp": check.timestamp
                }
                for check in report.checks
            ],
            "recommendations": report.recommendations
        }
        
        return json.dumps(report_dict, indent=2)
    
    def format_report_csv(self, report: IntegrityReport) -> str:
        """Format report as CSV output"""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "Report ID", "Timestamp", "Overall Status", "Total Checks",
            "Passed Checks", "Failed Checks", "Warning Checks"
        ])
        
        # Write summary row
        writer.writerow([
            report.report_id, report.timestamp, report.overall_status,
            report.total_checks, report.passed_checks, report.failed_checks,
            report.warning_checks
        ])
        
        # Write check details
        writer.writerow([])  # Empty row
        writer.writerow([
            "Check ID", "Check Name", "Status", "Severity", "Message", "Details"
        ])
        
        for check in report.checks:
            writer.writerow([
                check.check_id, check.check_name, check.status,
                check.severity, check.message, str(check.details)
            ])
        
        return output.getvalue()
    
    def generate_report(self, report: IntegrityReport) -> str:
        """Generate report in the specified format"""
        if self.output_format == "text":
            return self.format_report_text(report)
        elif self.output_format == "json":
            return self.format_report_json(report)
        elif self.output_format == "csv":
            return self.format_report_csv(report)
        else:
            raise ValueError(f"Unknown output format: {self.output_format}")
    
    def print_report(self, report: IntegrityReport):
        """Print report to stdout"""
        formatted_report = self.generate_report(report)
        print(formatted_report)
    
    def save_report(self, report: IntegrityReport, output_file: str):
        """Save report to file"""
        formatted_report = self.generate_report(report)
        
        try:
            with open(output_file, 'w') as f:
                f.write(formatted_report)
            print(f"Report saved to: {output_file}")
        except Exception as e:
            print(f"Error saving report: {e}", file=sys.stderr)


class CLIInterface:
    """Command-line interface for integrity checking"""
    
    def __init__(self):
        self.parser = self._setup_parser()
    
    def _setup_parser(self) -> argparse.ArgumentParser:
        """Setup command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="Database Integrity Checker - EMERGENCY-RESTORE-004 Mission",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python database_integrity_checker.py
  python database_integrity_checker.py --format json
  python database_integrity_checker.py --output report.json
  python database_integrity_checker.py --task-list custom_task_list.json
            """
        )
        
        parser.add_argument(
            "--task-list", "-t",
            default="agent_workspaces/meeting/task_list.json",
            help="Path to the task list file (default: agent_workspaces/meeting/task_list.json)"
        )
        
        parser.add_argument(
            "--format", "-f",
            choices=["text", "json", "csv"],
            default="text",
            help="Output format (default: text)"
        )
        
        parser.add_argument(
            "--output", "-o",
            help="Output file path (default: print to stdout)"
        )
        
        parser.add_argument(
            "--backup", "-b",
            action="store_true",
            help="Create backup before running checks"
        )
        
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Enable verbose logging"
        )
        
        return parser
    
    def parse_args(self):
        """Parse command-line arguments"""
        return self.parser.parse_args()
    
    def run(self):
        """Run the CLI interface"""
        args = self.parse_args()
        
        # Import here to avoid circular imports
        from .database_integrity_operations import DatabaseOperations
        from .database_integrity_core import IntegrityChecker
        from .database_integrity_models import IntegrityValidator
        
        # Setup operations
        db_ops = DatabaseOperations(args.task_list)
        
        # Load contracts
        if not db_ops.load_contracts():
            print("Error: Failed to load contracts", file=sys.stderr)
            sys.exit(1)
        
        # Create backup if requested
        if args.backup:
            if not db_ops.backup_contracts():
                print("Warning: Failed to create backup", file=sys.stderr)
        
        # Run integrity checks
        contracts_data = db_ops.get_contracts_data()
        checker = IntegrityChecker(contracts_data)
        checks = checker.run_all_checks()
        
        # Generate recommendations
        recommendations = []
        failed_checks = [check for check in checks if check.status == "FAILED"]
        
        if failed_checks:
            recommendations.append("Review and fix failed integrity checks")
            recommendations.append("Update contract data to resolve inconsistencies")
        
        warning_checks = [check for check in checks if check.status == "WARNING"]
        if warning_checks:
            recommendations.append("Address warning-level issues to improve data quality")
        
        # Create report
        report = IntegrityValidator.create_report(checks, recommendations)
        
        # Setup reporter
        reporter = IntegrityReporter()
        reporter.set_output_format(args.format)
        
        # Output report
        if args.output:
            reporter.save_report(report, args.output)
        else:
            reporter.print_report(report)
        
        # Exit with appropriate code
        if report.overall_status == "FAILED":
            sys.exit(1)
        elif report.overall_status == "WARNING":
            sys.exit(2)
        else:
            sys.exit(0)
