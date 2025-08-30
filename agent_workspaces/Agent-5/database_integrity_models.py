#!/usr/bin/env python3
"""
Database Integrity Models - EMERGENCY-RESTORE-004 Mission
========================================================

Data models and validation utilities for database integrity checking.
Part of the emergency system restoration mission for Agent-5.
"""

import datetime
from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class IntegrityCheck:
    """Represents a single integrity check"""
    check_id: str
    check_name: str
    status: str  # PASSED, FAILED, WARNING
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    message: str
    details: Dict[str, Any]
    timestamp: str


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


class IntegrityValidator:
    """Validation utilities for integrity checks"""
    
    @staticmethod
    def validate_check_status(status: str) -> bool:
        """Validate that a check status is valid"""
        valid_statuses = ["PASSED", "FAILED", "WARNING"]
        return status.upper() in valid_statuses
    
    @staticmethod
    def validate_severity(severity: str) -> bool:
        """Validate that a severity level is valid"""
        valid_severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        return severity.upper() in valid_severities
    
    @staticmethod
    def create_check(check_id: str, check_name: str, status: str, 
                    severity: str, message: str, details: Dict[str, Any]) -> IntegrityCheck:
        """Create a validated integrity check"""
        if not IntegrityValidator.validate_check_status(status):
            raise ValueError(f"Invalid status: {status}")
        
        if not IntegrityValidator.validate_severity(severity):
            raise ValueError(f"Invalid severity: {severity}")
        
        return IntegrityCheck(
            check_id=check_id,
            check_name=check_name,
            status=status.upper(),
            severity=severity.upper(),
            message=message,
            details=details,
            timestamp=datetime.datetime.now().isoformat()
        )
    
    @staticmethod
    def create_report(checks: List[IntegrityCheck], 
                     recommendations: List[str] = None) -> IntegrityReport:
        """Create a complete integrity report from checks"""
        if recommendations is None:
            recommendations = []
        
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
            report_id=f"INTEGRITY_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.datetime.now().isoformat(),
            total_checks=len(checks),
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            warning_checks=warning_checks,
            overall_status=overall_status,
            checks=checks,
            recommendations=recommendations
        )
