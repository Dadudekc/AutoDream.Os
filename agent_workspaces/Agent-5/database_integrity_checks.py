#!/usr/bin/env python3
"""
Database Integrity Checks - Core Checking Logic
==============================================

This module contains the core integrity checking logic for the database
integrity checker system. It provides all the validation and checking
methods used to assess database integrity.

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** V2-COMPLIANCE-005 - Database Audit System Modularization
**Status:** MODULARIZATION IN PROGRESS
**Target:** ≤250 lines per module, single responsibility principle
**V2 Compliance:** ✅ Under 250 lines, focused responsibility
"""

import datetime
import logging
from typing import Dict, List, Any
from pathlib import Path

from database_integrity_models import IntegrityCheck, ContractData, create_integrity_check


class DatabaseIntegrityChecks:
    """Core integrity checking logic for database validation"""
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.required_fields = [
            "title", "description", "difficulty", "extra_credit_points",
            "requirements", "deliverables", "status"
        ]
    
    def check_contract_counts(self, contracts_data: Dict[str, Any]) -> IntegrityCheck:
        """Check contract count consistency"""
        total_claimed = contracts_data.get("claimed_contracts", 0)
        total_completed = contracts_data.get("completed_contracts", 0)
        total_available = contracts_data.get("available_contracts", 0)
        total_contracts = contracts_data.get("total_contracts", 0)
        
        # Count actual contracts in the data
        actual_total = self._count_actual_contracts(contracts_data)
        calculated_total = total_claimed + total_completed + total_available
        
        # Check both consistency checks
        header_consistent = calculated_total == total_contracts
        data_consistent = actual_total == total_contracts
        
        if header_consistent and data_consistent:
            return create_integrity_check(
                check_id="COUNT_CONSISTENCY",
                check_name="Contract Count Consistency",
                status="PASSED",
                severity="CRITICAL",
                message="Contract counts are consistent",
                details={
                    "total_contracts": total_contracts,
                    "claimed": total_claimed,
                    "completed": total_completed,
                    "available": total_available,
                    "actual_count": actual_total
                }
            )
        else:
            return create_integrity_check(
                check_id="COUNT_CONSISTENCY",
                check_name="Contract Count Consistency",
                status="FAILED",
                severity="CRITICAL",
                message=f"Contract count mismatch: header={calculated_total}, data={actual_total}, declared={total_contracts}",
                details={
                    "total_contracts": total_contracts,
                    "claimed": total_claimed,
                    "completed": total_completed,
                    "available": total_available,
                    "calculated_total": calculated_total,
                    "actual_count": actual_total
                }
            )
    
    def check_required_fields(self, contracts_data: Dict[str, Any]) -> List[IntegrityCheck]:
        """Check for missing required fields in contracts"""
        checks = []
        
        if "contracts" not in contracts_data:
            checks.append(create_integrity_check(
                check_id="REQUIRED_FIELDS",
                check_name="Required Fields Check",
                status="FAILED",
                severity="CRITICAL",
                message="No contracts section found",
                details={}
            ))
            return checks
        
        missing_field_contracts = []
        
        for contract_id, contract in self._iter_contracts(contracts_data):
            missing_fields = [field for field in self.required_fields if field not in contract]
            
            if missing_fields:
                missing_field_contracts.append({
                    "contract_id": contract_id,
                    "missing_fields": missing_fields,
                })
        
        if missing_field_contracts:
            checks.append(create_integrity_check(
                check_id="REQUIRED_FIELDS",
                check_name="Required Fields Check",
                status="FAILED",
                severity="HIGH",
                message=f"Found {len(missing_field_contracts)} contracts with missing required fields",
                details={"missing_field_contracts": missing_field_contracts}
            ))
        else:
            checks.append(create_integrity_check(
                check_id="REQUIRED_FIELDS",
                check_name="Required Fields Check",
                status="PASSED",
                severity="HIGH",
                message="All contracts have required fields",
                details={}
            ))
        
        return checks
    
    def check_status_consistency(self, contracts_data: Dict[str, Any]) -> List[IntegrityCheck]:
        """Check contract status consistency"""
        checks = []
        
        if "contracts" not in contracts_data:
            return checks
        
        status_issues = []
        
        for contract_id, contract in self._iter_contracts(contracts_data):
            status = contract.get("status")
            claimed_by = contract.get("claimed_by")
            claimed_at = contract.get("claimed_at")
            completed_at = contract.get("completed_at")
            
            # Check CLAIMED status consistency
            if status == "CLAIMED":
                if not claimed_by:
                    status_issues.append({
                        "contract_id": contract_id,
                        "issue": "CLAIMED status without agent assignment"
                    })
                if not claimed_at:
                    status_issues.append({
                        "contract_id": contract_id,
                        "issue": "CLAIMED status without claim timestamp"
                    })
            
            # Check COMPLETED status consistency
            elif status == "COMPLETED":
                if not completed_at:
                    status_issues.append({
                        "contract_id": contract_id,
                        "issue": "COMPLETED status without completion timestamp"
                    })
        
        if status_issues:
            checks.append(create_integrity_check(
                check_id="STATUS_CONSISTENCY",
                check_name="Contract Status Consistency",
                status="FAILED",
                severity="HIGH",
                message=f"Found {len(status_issues)} status consistency issues",
                details={"status_issues": status_issues}
            ))
        else:
            checks.append(create_integrity_check(
                check_id="STATUS_CONSISTENCY",
                check_name="Contract Status Consistency",
                status="PASSED",
                severity="HIGH",
                message="All contract statuses are consistent",
                details={}
            ))
        
        return checks
    
    def check_timestamp_validity(self, contracts_data: Dict[str, Any]) -> List[IntegrityCheck]:
        """Check timestamp validity and format"""
        checks = []
        
        if "contracts" not in contracts_data:
            return checks
        
        timestamp_issues = []
        
        for contract_id, contract in self._iter_contracts(contracts_data):
            # Check claimed_at timestamp
            if "claimed_at" in contract and contract["claimed_at"]:
                issue = self._validate_timestamp(contract["claimed_at"], "claim")
                if issue:
                    timestamp_issues.append({
                        "contract_id": contract_id,
                        "issue": issue,
                        "timestamp": contract["claimed_at"]
                    })
            
            # Check completed_at timestamp
            if "completed_at" in contract and contract["completed_at"]:
                issue = self._validate_timestamp(contract["completed_at"], "completion")
                if issue:
                    timestamp_issues.append({
                        "contract_id": contract_id,
                        "issue": issue,
                        "timestamp": contract["completed_at"]
                    })
        
        if timestamp_issues:
            checks.append(create_integrity_check(
                check_id="TIMESTAMP_VALIDITY",
                check_name="Timestamp Validity",
                status="FAILED",
                severity="MEDIUM",
                message=f"Found {len(timestamp_issues)} timestamp issues",
                details={"timestamp_issues": timestamp_issues}
            ))
        else:
            checks.append(create_integrity_check(
                check_id="TIMESTAMP_VALIDITY",
                check_name="Timestamp Validity",
                status="PASSED",
                severity="MEDIUM",
                message="All timestamps are valid",
                details={}
            ))
        
        return checks
    
    def _count_actual_contracts(self, contracts_data: Dict[str, Any]) -> int:
        """Count the actual number of contracts in the data"""
        if "contracts" not in contracts_data:
            return 0
        return len(contracts_data["contracts"])
    
    def _iter_contracts(self, contracts_data: Dict[str, Any]):
        """Iterate over contracts in the data"""
        if "contracts" not in contracts_data:
            return
        
        for contract_id, contract in contracts_data["contracts"].items():
            yield contract_id, contract
    
    def _validate_timestamp(self, timestamp_str: str, timestamp_type: str) -> str:
        """Validate a timestamp string and return issue description if invalid"""
        try:
            # Handle ISO format with or without timezone
            if timestamp_str.endswith('Z'):
                timestamp_str = timestamp_str.replace('Z', '+00:00')
            
            timestamp = datetime.datetime.fromisoformat(timestamp_str)
            current_dt = datetime.datetime.now(timestamp.tzinfo)
            
            if timestamp > current_dt:
                return f"Future {timestamp_type} timestamp"
            
            return None  # No issue
            
        except ValueError:
            return f"Invalid {timestamp_type} timestamp format"
