#!/usr/bin/env python3
"""
Audit Results Data Models

This module contains data structures for storing and managing audit results:
- File analysis information
- Structure validation results
- Metadata consistency checks
- Critical issue tracking
"""

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class FileAnalysis:
    """Individual file analysis results"""

    filename: str
    filepath: str
    exists: bool
    readable: bool
    valid_json: bool
    size_bytes: int
    last_modified: Optional[str]
    json_error: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return asdict(self)

    @property
    def status_summary(self) -> str:
        """Get human-readable status summary"""
        if not self.exists:
            return "NOT_FOUND"
        elif not self.readable:
            return "NOT_READABLE"
        elif not self.valid_json:
            return "INVALID_JSON"
        else:
            return "HEALTHY"

    @property
    def size_kb(self) -> float:
        """Get file size in kilobytes"""
        return round(self.size_bytes / 1024, 2)


@dataclass
class AuditResults:
    """Complete audit results for database structure"""

    timestamp: str
    file_analysis: Dict[str, FileAnalysis]
    structure_validation: Dict[str, Any]
    metadata_consistency: Dict[str, Any]
    critical_issues: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "timestamp": self.timestamp,
            "file_analysis": {k: v.to_dict() for k, v in self.file_analysis.items()},
            "structure_validation": self.structure_validation,
            "metadata_consistency": self.metadata_consistency,
            "critical_issues": self.critical_issues,
        }

    @property
    def total_files_analyzed(self) -> int:
        """Get total number of files analyzed"""
        return len(self.file_analysis)

    @property
    def healthy_files_count(self) -> int:
        """Get count of healthy files"""
        return sum(
            1 for f in self.file_analysis.values() if f.status_summary == "HEALTHY"
        )

    @property
    def critical_issues_count(self) -> int:
        """Get count of critical issues"""
        return len(self.critical_issues)

    @property
    def overall_health_score(self) -> float:
        """Calculate overall health score (0.0 to 1.0)"""
        if self.total_files_analyzed == 0:
            return 0.0

        healthy_ratio = self.healthy_files_count / self.total_files_analyzed
        issue_penalty = min(self.critical_issues_count * 0.1, 0.5)  # Max 50% penalty

        return max(0.0, healthy_ratio - issue_penalty)

    @property
    def health_status(self) -> str:
        """Get human-readable health status"""
        score = self.overall_health_score

        if score >= 0.9:
            return "EXCELLENT"
        elif score >= 0.7:
            return "GOOD"
        elif score >= 0.5:
            return "FAIR"
        elif score >= 0.3:
            return "POOR"
        else:
            return "CRITICAL"

    def add_critical_issue(self, issue: str):
        """Add a critical issue to the audit results"""
        if issue not in self.critical_issues:
            self.critical_issues.append(issue)

    def get_file_summary(self, filename: str) -> Optional[FileAnalysis]:
        """Get file analysis for specific filename"""
        return self.file_analysis.get(filename)

    def get_problematic_files(self) -> List[FileAnalysis]:
        """Get list of files with issues"""
        return [f for f in self.file_analysis.values() if f.status_summary != "HEALTHY"]

    def get_healthy_files(self) -> List[FileAnalysis]:
        """Get list of healthy files"""
        return [f for f in self.file_analysis.values() if f.status_summary == "HEALTHY"]
