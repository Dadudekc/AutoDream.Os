#!/usr/bin/env python3
"""
Recovery Models for Emergency Database Recovery
Contract: EMERGENCY-RESTORE-004
Agent: Agent-5
Description: Data structures for recovery reporting and status tracking
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

class RecoveryStatus(Enum):
    """Recovery operation status"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PARTIALLY_COMPLETED = "PARTIALLY_COMPLETED"
    CANCELLED = "CANCELLED"

class RecoveryPhase(Enum):
    """Phases of the recovery process"""
    AUDIT = "AUDIT"
    VALIDATION = "VALIDATION"
    CORRUPTION_SCAN = "CORRUPTION_SCAN"
    INTEGRITY_CHECKS = "INTEGRITY_CHECKS"
    RECOVERY_EXECUTION = "RECOVERY_EXECUTION"
    VERIFICATION = "VERIFICATION"
    REPORTING = "REPORTING"

@dataclass
class RecoveryReport:
    """Complete recovery operation report"""
    report_id: str
    timestamp: datetime
    overall_status: RecoveryStatus
    phases_completed: List[RecoveryPhase] = field(default_factory=list)
    phases_failed: List[RecoveryPhase] = field(default_factory=list)
    total_issues_found: int = 0
    issues_resolved: int = 0
    issues_failed: int = 0
    critical_issues: int = 0
    warnings: int = 0
    execution_time: Optional[str] = None
    summary: str = ""
    recommendations: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    
    def get_success_rate(self) -> float:
        """Calculate recovery success rate"""
        if self.total_issues_found == 0:
            return 100.0
        return (self.issues_resolved / self.total_issues_found) * 100.0
    
    def is_successful(self) -> bool:
        """Check if recovery was successful"""
        return self.overall_status in [RecoveryStatus.COMPLETED, RecoveryStatus.PARTIALLY_COMPLETED]
    
    def get_phase_summary(self) -> Dict[str, int]:
        """Get summary of phases by status"""
        return {
            'completed': len(self.phases_completed),
            'failed': len(self.phases_failed),
            'total_phases': len(RecoveryPhase)
        }

@dataclass
class PhaseResult:
    """Result of a single recovery phase"""
    phase: RecoveryPhase
    status: RecoveryStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    issues_found: int = 0
    issues_resolved: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    execution_time: Optional[str] = None
    
    def is_complete(self) -> bool:
        """Check if phase is complete"""
        return self.status in [RecoveryStatus.COMPLETED, RecoveryStatus.FAILED]
    
    def get_duration(self) -> Optional[str]:
        """Get phase duration if complete"""
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            return str(duration)
        return None
