#!/usr/bin/env python3
"""
Integrity Models for Emergency Database Recovery
Contract: EMERGENCY-RESTORE-004
Agent: Agent-5
Description: Data structures for integrity checking and recovery actions
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

class IssueSeverity(Enum):
    """Severity levels for integrity issues"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IssueType(Enum):
    """Types of integrity issues"""
    CORRUPTION = "CORRUPTION"
    MISSING_DATA = "MISSING_DATA"
    INVALID_FORMAT = "INVALID_FORMAT"
    DUPLICATE_ENTRY = "DUPLICATE_ENTRY"
    REFERENCE_INTEGRITY = "REFERENCE_INTEGRITY"
    TIMESTAMP_INCONSISTENCY = "TIMESTAMP_INCONSISTENCY"

@dataclass
class IntegrityIssue:
    """Base class for integrity issues"""
    issue_id: str
    issue_type: IssueType
    severity: IssueSeverity
    description: str
    affected_file: str
    affected_contract: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CorruptionIssue(IntegrityIssue):
    """Specific corruption issue details"""
    corruption_type: str
    data_location: str
    expected_value: Optional[str] = None
    actual_value: Optional[str] = None
    recovery_difficulty: str = "UNKNOWN"
    estimated_repair_time: Optional[str] = None

@dataclass
class RecoveryAction:
    """Recovery action to resolve an integrity issue"""
    action_id: str
    issue_id: str
    action_type: str
    description: str
    required_tools: List[str] = field(default_factory=list)
    estimated_duration: Optional[str] = None
    success_probability: float = 0.0
    prerequisites: List[str] = field(default_factory=list)
    rollback_plan: Optional[str] = None
    status: str = "PENDING"
    executed_at: Optional[datetime] = None
    result: Optional[str] = None
    
    def can_execute(self) -> bool:
        """Check if action can be executed"""
        return self.status == "PENDING" and self.success_probability > 0.0
    
    def mark_executed(self, result: str):
        """Mark action as executed"""
        self.status = "EXECUTED"
        self.executed_at = datetime.now()
        self.result = result
