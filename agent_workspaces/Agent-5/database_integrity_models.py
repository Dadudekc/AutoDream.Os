#!/usr/bin/env python3
"""
Database Integrity Models - Core Data Structures
===============================================

This module contains the core data models and structures for the database
integrity checking system. It provides the foundational classes used
throughout the integrity checking process.

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** V2-COMPLIANCE-005 - Database Audit System Modularization
**Status:** MODULARIZATION IN PROGRESS
**Target:** ≤250 lines per module, single responsibility principle
**V2 Compliance:** ✅ Under 250 lines, focused responsibility
"""

import datetime
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class IntegrityCheck:
    """Represents a single integrity check result"""
    check_id: str
    check_name: str
    status: str  # PASSED, FAILED, WARNING
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    message: str
    details: Dict[str, Any]
    timestamp: str

    def __post_init__(self):
        """Validate the integrity check data after initialization"""
        if self.status not in ["PASSED", "FAILED", "WARNING"]:
            raise ValueError(f"Invalid status: {self.status}")
        
        if self.severity not in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            raise ValueError(f"Invalid severity: {self.severity}")
        
        if not self.check_id or not self.check_name:
            raise ValueError("check_id and check_name are required")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the integrity check to a dictionary"""
        return {
            "check_id": self.check_id,
            "check_name": self.check_name,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IntegrityCheck':
        """Create an IntegrityCheck instance from a dictionary"""
        return cls(
            check_id=data["check_id"],
            check_name=data["check_name"],
            status=data["status"],
            severity=data["severity"],
            message=data["message"],
            details=data.get("details", {}),
            timestamp=data["timestamp"]
        )


@dataclass
class IntegrityReport:
    """Complete integrity check report"""
    report_id: str
    timestamp: str
    total_checks: int
    passed_checks: int
    failed_checks: int
    warning_checks: int
    overall_status: str
    checks: List[IntegrityCheck]
    recommendations: List[str]

    def __post_init__(self):
        """Validate the integrity report data after initialization"""
        if self.overall_status not in ["PASSED", "FAILED", "WARNING"]:
            raise ValueError(f"Invalid overall_status: {self.overall_status}")
        
        if self.total_checks != (self.passed_checks + self.failed_checks + self.warning_checks):
            raise ValueError("Total checks must equal sum of individual check counts")
        
        if not self.report_id:
            raise ValueError("report_id is required")

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the integrity report"""
        return {
            "report_id": self.report_id,
            "timestamp": self.timestamp,
            "summary": {
                "total_checks": self.total_checks,
                "passed_checks": self.passed_checks,
                "failed_checks": self.failed_checks,
                "warning_checks": self.warning_checks,
                "overall_status": self.overall_status
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert the integrity report to a dictionary"""
        return {
            "report_id": self.report_id,
            "timestamp": self.timestamp,
            "summary": self.get_summary()["summary"],
            "checks": [check.to_dict() for check in self.checks],
            "recommendations": self.recommendations
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IntegrityReport':
        """Create an IntegrityReport instance from a dictionary"""
        checks = [IntegrityCheck.from_dict(check_data) for check_data in data["checks"]]
        
        return cls(
            report_id=data["report_id"],
            timestamp=data["timestamp"],
            total_checks=data["summary"]["total_checks"],
            passed_checks=data["summary"]["passed_checks"],
            failed_checks=data["summary"]["failed_checks"],
            warning_checks=data["summary"]["warning_checks"],
            overall_status=data["summary"]["overall_status"],
            checks=checks,
            recommendations=data.get("recommendations", [])
        )


@dataclass
class ContractData:
    """Represents contract data for integrity checking"""
    contract_id: str
    title: str
    status: str
    claimed_by: str = None
    claimed_at: str = None
    completed_at: str = None
    extra_data: Dict[str, Any] = None

    def __post_init__(self):
        """Validate contract data after initialization"""
        if not self.contract_id or not self.title:
            raise ValueError("contract_id and title are required")
        
        if self.extra_data is None:
            self.extra_data = {}

    def has_required_fields(self, required_fields: List[str]) -> bool:
        """Check if the contract has all required fields"""
        return all(hasattr(self, field) and getattr(self, field) is not None 
                   for field in required_fields)

    def get_field_value(self, field_name: str, default: Any = None) -> Any:
        """Get a field value, checking both direct attributes and extra_data"""
        if hasattr(self, field_name):
            value = getattr(self, field_name)
            if value is not None:
                return value
        
        return self.extra_data.get(field_name, default)


# Utility functions for working with integrity models
def create_integrity_check(check_id: str, check_name: str, status: str, 
                          severity: str, message: str, details: Dict[str, Any] = None) -> IntegrityCheck:
    """Create an integrity check with current timestamp"""
    if details is None:
        details = {}
    
    return IntegrityCheck(
        check_id=check_id,
        check_name=check_name,
        status=status,
        severity=severity,
        message=message,
        details=details,
        timestamp=datetime.datetime.now().isoformat()
    )


def create_integrity_report(checks: List[IntegrityCheck], 
                           recommendations: List[str] = None) -> IntegrityReport:
    """Create an integrity report from a list of checks"""
    if recommendations is None:
        recommendations = []
    
    total_checks = len(checks)
    passed_checks = sum(1 for check in checks if check.status == "PASSED")
    failed_checks = sum(1 for check in checks if check.status == "FAILED")
    warning_checks = sum(1 for check in checks if check.status == "WARNING")
    
    # Determine overall status
    if failed_checks > 0:
        overall_status = "FAILED"
    elif warning_checks > 0:
        overall_status = "WARNING"
    else:
        overall_status = "PASSED"
    
    return IntegrityReport(
        report_id=f"integrity_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
        timestamp=datetime.datetime.now().isoformat(),
        total_checks=total_checks,
        passed_checks=passed_checks,
        failed_checks=failed_checks,
        warning_checks=warning_checks,
        overall_status=overall_status,
        checks=checks,
        recommendations=recommendations
    )
