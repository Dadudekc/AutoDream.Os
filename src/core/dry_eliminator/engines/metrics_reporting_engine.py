#!/usr/bin/env python3
"""
DRY Elimination Metrics & Reporting Engine
==========================================

Metrics and reporting engine for DRY elimination system.
Handles progress tracking, summary generation, and reporting.
V2 COMPLIANT: Focused metrics and reporting under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR METRICS & REPORTING
@license MIT
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from ..dry_eliminator_models import (
    DRYViolation, EliminationResult, EliminationMetrics, create_elimination_metrics
)


class MetricsReportingEngine:
    """Metrics and reporting engine for DRY elimination system"""
    
    def __init__(self):
        """Initialize metrics and reporting engine"""
        self.logger = logging.getLogger(__name__)
        self.metrics = create_elimination_metrics()
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def start_analysis(self):
        """Start analysis timing"""
        self.start_time = datetime.now()
        self.metrics.analysis_start_time = self.start_time.isoformat()
    
    def end_analysis(self):
        """End analysis timing"""
        self.end_time = datetime.now()
        self.metrics.analysis_end_time = self.end_time.isoformat()
        
        if self.start_time:
            duration = self.end_time - self.start_time
            self.metrics.analysis_duration_seconds = duration.total_seconds()
    
    def update_file_metrics(self, total_files: int, analyzed_files: int):
        """Update file analysis metrics"""
        self.metrics.total_files_analyzed = total_files
        self.metrics.files_processed = analyzed_files
    
    def update_violation_metrics(self, violations: List[DRYViolation]):
        """Update violation detection metrics"""
        self.metrics.violations_detected = len(violations)
        
        # Count by type
        type_counts = defaultdict(int)
        for violation in violations:
            type_counts[violation.violation_type.value] += 1
        
        self.metrics.imports_consolidated = type_counts.get('duplicate_imports', 0)
        self.metrics.methods_consolidated = type_counts.get('duplicate_methods', 0)
        self.metrics.constants_consolidated = type_counts.get('duplicate_constants', 0)
        self.metrics.unused_imports_removed = type_counts.get('unused_imports', 0)
    
    def update_elimination_metrics(self, results: List[EliminationResult]):
        """Update elimination execution metrics"""
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]
        
        self.metrics.eliminations_attempted = len(results)
        self.metrics.eliminations_successful = len(successful_results)
        self.metrics.eliminations_failed = len(failed_results)
        
        # Calculate total lines removed
        total_lines_removed = sum(r.lines_removed for r in successful_results)
        self.metrics.total_lines_removed = total_lines_removed
        
        # Calculate files modified
        modified_files = set()
        for result in successful_results:
            modified_files.update(result.files_modified)
        self.metrics.files_modified = len(modified_files)
    
    def generate_summary_report(self, violations: List[DRYViolation], 
                               results: List[EliminationResult]) -> Dict[str, Any]:
        """Generate comprehensive summary report"""
        return {
            'analysis_info': {
                'start_time': self.metrics.analysis_start_time,
                'end_time': self.metrics.analysis_end_time,
                'duration_seconds': self.metrics.analysis_duration_seconds,
                'total_files_analyzed': self.metrics.total_files_analyzed,
                'files_processed': self.metrics.files_processed
            },
            'violation_summary': {
                'total_violations_detected': self.metrics.violations_detected,
                'violations_by_type': self._get_violations_by_type(violations),
                'violations_by_severity': self._get_violations_by_severity(violations),
                'total_potential_savings': sum(v.potential_savings for v in violations)
            },
            'elimination_summary': {
                'eliminations_attempted': self.metrics.eliminations_attempted,
                'eliminations_successful': self.metrics.eliminations_successful,
                'eliminations_failed': self.metrics.eliminations_failed,
                'success_rate': self.metrics.eliminations_successful / self.metrics.eliminations_attempted if self.metrics.eliminations_attempted > 0 else 0,
                'total_lines_removed': self.metrics.total_lines_removed,
                'files_modified': self.metrics.files_modified
            },
            'performance_metrics': {
                'violations_per_file': self.metrics.violations_detected / self.metrics.total_files_analyzed if self.metrics.total_files_analyzed > 0 else 0,
                'lines_removed_per_violation': self.metrics.total_lines_removed / self.metrics.violations_detected if self.metrics.violations_detected > 0 else 0,
                'elimination_efficiency': self.metrics.eliminations_successful / self.metrics.violations_detected if self.metrics.violations_detected > 0 else 0
            }
        }
    
    def _get_violations_by_type(self, violations: List[DRYViolation]) -> Dict[str, int]:
        """Get violation count by type"""
        type_counts = defaultdict(int)
        for violation in violations:
            type_counts[violation.violation_type.value] += 1
        return dict(type_counts)
    
    def _get_violations_by_severity(self, violations: List[DRYViolation]) -> Dict[str, int]:
        """Get violation count by severity"""
        severity_counts = defaultdict(int)
        for violation in violations:
            severity_counts[violation.severity.value] += 1
        return dict(severity_counts)
    
    def generate_detailed_report(self, violations: List[DRYViolation], 
                                results: List[EliminationResult]) -> str:
        """Generate detailed text report"""
        report = []
        report.append("DRY Elimination Analysis Report")
        report.append("=" * 40)
        report.append("")
        
        # Analysis info
        report.append("Analysis Information:")
        report.append(f"  Start Time: {self.metrics.analysis_start_time}")
        report.append(f"  End Time: {self.metrics.analysis_end_time}")
        report.append(f"  Duration: {self.metrics.analysis_duration_seconds:.2f} seconds")
        report.append(f"  Files Analyzed: {self.metrics.total_files_analyzed}")
        report.append("")
        
        # Violation summary
        report.append("Violation Summary:")
        report.append(f"  Total Violations: {self.metrics.violations_detected}")
        
        type_counts = self._get_violations_by_type(violations)
        for violation_type, count in type_counts.items():
            report.append(f"    {violation_type}: {count}")
        
        severity_counts = self._get_violations_by_severity(violations)
        report.append("  By Severity:")
        for severity, count in severity_counts.items():
            report.append(f"    {severity}: {count}")
        
        report.append(f"  Total Potential Savings: {sum(v.potential_savings for v in violations)} lines")
        report.append("")
        
        # Elimination summary
        report.append("Elimination Summary:")
        report.append(f"  Attempted: {self.metrics.eliminations_attempted}")
        report.append(f"  Successful: {self.metrics.eliminations_successful}")
        report.append(f"  Failed: {self.metrics.eliminations_failed}")
        
        if self.metrics.eliminations_attempted > 0:
            success_rate = self.metrics.eliminations_successful / self.metrics.eliminations_attempted
            report.append(f"  Success Rate: {success_rate:.2%}")
        
        report.append(f"  Lines Removed: {self.metrics.total_lines_removed}")
        report.append(f"  Files Modified: {self.metrics.files_modified}")
        report.append("")
        
        # Performance metrics
        report.append("Performance Metrics:")
        if self.metrics.total_files_analyzed > 0:
            violations_per_file = self.metrics.violations_detected / self.metrics.total_files_analyzed
            report.append(f"  Violations per File: {violations_per_file:.2f}")
        
        if self.metrics.violations_detected > 0:
            lines_per_violation = self.metrics.total_lines_removed / self.metrics.violations_detected
            report.append(f"  Lines Removed per Violation: {lines_per_violation:.2f}")
        
        if self.metrics.violations_detected > 0:
            efficiency = self.metrics.eliminations_successful / self.metrics.violations_detected
            report.append(f"  Elimination Efficiency: {efficiency:.2%}")
        
        return "\n".join(report)
    
    def export_metrics_to_file(self, file_path: Path) -> bool:
        """Export metrics to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("DRY Elimination Metrics\n")
                f.write("=" * 25 + "\n\n")
                
                # Write metrics in a structured format
                f.write(f"Analysis Start Time: {self.metrics.analysis_start_time}\n")
                f.write(f"Analysis End Time: {self.metrics.analysis_end_time}\n")
                f.write(f"Analysis Duration: {self.metrics.analysis_duration_seconds} seconds\n")
                f.write(f"Total Files Analyzed: {self.metrics.total_files_analyzed}\n")
                f.write(f"Files Processed: {self.metrics.files_processed}\n")
                f.write(f"Violations Detected: {self.metrics.violations_detected}\n")
                f.write(f"Eliminations Attempted: {self.metrics.eliminations_attempted}\n")
                f.write(f"Eliminations Successful: {self.metrics.eliminations_successful}\n")
                f.write(f"Eliminations Failed: {self.metrics.eliminations_failed}\n")
                f.write(f"Total Lines Removed: {self.metrics.total_lines_removed}\n")
                f.write(f"Files Modified: {self.metrics.files_modified}\n")
            
            return True
        except Exception as e:
            self.logger.error(f"Error exporting metrics: {e}")
            return False
    
    def get_metrics_dict(self) -> Dict[str, Any]:
        """Get metrics as dictionary"""
        return self.metrics.to_dict()
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics = create_elimination_metrics()
        self.start_time = None
        self.end_time = None


# Factory function for dependency injection
def create_metrics_reporting_engine() -> MetricsReportingEngine:
    """Factory function to create metrics and reporting engine"""
    return MetricsReportingEngine()


# Export for DI
__all__ = ['MetricsReportingEngine', 'create_metrics_reporting_engine']
