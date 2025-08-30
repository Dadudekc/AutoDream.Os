"""
Emergency Database Recovery Models

This module contains all data structures and models for the emergency database recovery system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path


@dataclass
class FileInfo:
    """Information about a file in the database."""
    exists: bool
    readable: bool
    valid_json: bool
    size: int
    last_modified: Optional[datetime]
    error_message: Optional[str] = None


@dataclass
class StructureValidation:
    """Results of database structure validation."""
    total_contracts: int
    valid_contracts: int
    invalid_contracts: int
    missing_fields: List[str]
    data_type_errors: List[str]
    validation_errors: List[str]


@dataclass
class MetadataConsistency:
    """Results of metadata consistency checks."""
    contract_count_matches: bool
    id_consistency: bool
    status_consistency: bool
    timestamp_consistency: bool
    inconsistencies: List[str]


@dataclass
class IntegrityIssue:
    """Represents an integrity issue found in the database."""
    issue_id: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    affected_contracts: List[str]
    suggested_fix: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class RecoveryAction:
    """Represents a recovery action to be taken."""
    action_id: str
    priority: int
    description: str
    affected_components: List[str]
    estimated_time: int  # minutes
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AuditResult:
    """Complete audit result for the database."""
    timestamp: datetime
    file_analysis: Dict[str, FileInfo]
    structure_validation: StructureValidation
    metadata_consistency: MetadataConsistency
    critical_issues: List[str]
    integrity_issues: List[IntegrityIssue]
    recovery_actions: List[RecoveryAction]
    overall_status: str  # HEALTHY, WARNING, CRITICAL, FAILED


@dataclass
class ContractValidation:
    """Results of contract validation."""
    total_contracts: int
    valid_contracts: int
    corrupted_contracts: int
    missing_contracts: int
    validation_errors: List[str]
    corruption_details: List[Dict[str, Any]]


@dataclass
class IntegrityCheckResult:
    """Results of integrity checks."""
    checks_performed: int
    checks_passed: int
    checks_failed: int
    critical_failures: int
    warnings: int
    recommendations: List[str]
    next_actions: List[str]


@dataclass
class RecoveryReport:
    """Complete recovery report."""
    timestamp: datetime
    audit_results: AuditResult
    integrity_check_results: IntegrityCheckResult
    recovery_actions_taken: List[RecoveryAction]
    system_status: str
    recommendations: List[str]
    next_steps: List[str]
