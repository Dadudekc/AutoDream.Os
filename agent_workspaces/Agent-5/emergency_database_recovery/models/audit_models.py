#!/usr/bin/env python3
"""
Audit Models for Emergency Database Recovery
Contract: EMERGENCY-RESTORE-004
Agent: Agent-5
Description: Data structures for database audit operations
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime

@dataclass
class FileAnalysis:
    """Analysis results for a single file"""
    filename: str
    exists: bool
    readable: bool
    writable: bool
    valid_json: bool
    size_bytes: int
    last_modified: Optional[datetime] = None
    error_message: Optional[str] = None
    checksum: Optional[str] = None

@dataclass
class StructureValidation:
    """Validation results for database structure"""
    total_contracts: int
    valid_contracts: int
    invalid_contracts: int
    missing_required_fields: List[str] = field(default_factory=list)
    duplicate_contract_ids: List[str] = field(default_factory=list)
    invalid_status_values: List[str] = field(default_factory=list)
    structure_errors: List[str] = field(default_factory=list)

@dataclass
class MetadataConsistency:
    """Metadata consistency validation results"""
    total_files: int
    consistent_files: int
    inconsistent_files: int
    timestamp_discrepancies: List[str] = field(default_factory=list)
    version_mismatches: List[str] = field(default_factory=list)
    metadata_errors: List[str] = field(default_factory=list)

@dataclass
class AuditResult:
    """Complete audit results"""
    timestamp: datetime
    file_analysis: Dict[str, FileAnalysis]
    structure_validation: StructureValidation
    metadata_consistency: MetadataConsistency
    critical_issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    def has_critical_issues(self) -> bool:
        """Check if there are any critical issues"""
        return len(self.critical_issues) > 0
    
    def get_issue_summary(self) -> Dict[str, int]:
        """Get summary of issues by severity"""
        return {
            'critical': len(self.critical_issues),
            'warnings': len(self.warnings),
            'total_files': self.metadata_consistency.total_files,
            'valid_files': self.metadata_consistency.consistent_files
        }
