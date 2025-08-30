#!/usr/bin/env python3
"""
Database Integrity Core - EMERGENCY-RESTORE-004 Mission
======================================================

Core integrity checking logic for database validation.
Part of the emergency system restoration mission for Agent-5.
"""

import datetime
from typing import Dict, List, Any
from .database_integrity_models import IntegrityCheck, IntegrityValidator


class IntegrityChecker:
    """Core integrity checking logic"""
    
    def __init__(self, contracts_data: Dict[str, Any]):
        self.contracts = contracts_data
    
    def check_contract_counts(self) -> IntegrityCheck:
        """Check contract count consistency"""
        total_claimed = self.contracts.get("claimed_contracts", 0)
        total_completed = self.contracts.get("completed_contracts", 0)
        total_available = self.contracts.get("available_contracts", 0)
        total_contracts = self.contracts.get("total_contracts", 0)
        
        # Count actual contracts in the data
        actual_total = 0
        if "contracts" in self.contracts:
            for category_name, category_data in self.contracts["contracts"].items():
                if "contracts" in category_data:
                    actual_total += len(category_data["contracts"])
        
        calculated_total = total_claimed + total_completed + total_available
        
        # Check both consistency checks
        header_consistent = calculated_total == total_contracts
        data_consistent = actual_total == total_contracts
        
        if header_consistent and data_consistent:
            return IntegrityValidator.create_check(
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
            return IntegrityValidator.create_check(
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
    
    def check_required_fields(self) -> List[IntegrityCheck]:
        """Check for missing required fields in contracts"""
        checks = []
        
        if "contracts" not in self.contracts:
            checks.append(IntegrityValidator.create_check(
                check_id="REQUIRED_FIELDS",
                check_name="Required Fields Check",
                status="FAILED",
                severity="CRITICAL",
                message="No contracts section found",
                details={}
            ))
            return checks
        
        required_fields = [
            "title", "description", "difficulty", "extra_credit_points",
            "requirements", "deliverables", "status"
        ]
        
        missing_field_contracts = []
        
        for category_name, category_data in self.contracts["contracts"].items():
            if "contracts" not in category_data:
                continue
            
            for contract in category_data["contracts"]:
                contract_id = contract.get("contract_id", "UNKNOWN")
                missing_fields = []
                
                for field in required_fields:
                    if field not in contract:
                        missing_fields.append(field)
                
                if missing_fields:
                    missing_field_contracts.append({
                        "contract_id": contract_id,
                        "missing_fields": missing_fields
                    })
        
        if missing_field_contracts:
            checks.append(IntegrityValidator.create_check(
                check_id="REQUIRED_FIELDS",
                check_name="Required Fields Check",
                status="FAILED",
                severity="HIGH",
                message=f"Found {len(missing_field_contracts)} contracts with missing required fields",
                details={"missing_field_contracts": missing_field_contracts}
            ))
        else:
            checks.append(IntegrityValidator.create_check(
                check_id="REQUIRED_FIELDS",
                check_name="Required Fields Check",
                status="PASSED",
                severity="HIGH",
                message="All contracts have required fields",
                details={}
            ))
        
        return checks
    
    def check_status_consistency(self) -> List[IntegrityCheck]:
        """Check contract status consistency"""
        checks = []
        
        if "contracts" not in self.contracts:
            checks.append(IntegrityValidator.create_check(
                check_id="STATUS_CONSISTENCY",
                check_name="Status Consistency Check",
                status="FAILED",
                severity="CRITICAL",
                message="No contracts section found",
                details={}
            ))
            return checks
        
        invalid_status_contracts = []
        valid_statuses = ["AVAILABLE", "CLAIMED", "COMPLETED"]
        
        for category_name, category_data in self.contracts["contracts"].items():
            if "contracts" not in category_data:
                continue
            
            for contract in category_data["contracts"]:
                contract_id = contract.get("contract_id", "UNKNOWN")
                status = contract.get("status", "").upper()
                
                if status not in valid_statuses:
                    invalid_status_contracts.append({
                        "contract_id": contract_id,
                        "invalid_status": status,
                        "valid_statuses": valid_statuses
                    })
        
        if invalid_status_contracts:
            checks.append(IntegrityValidator.create_check(
                check_id="STATUS_CONSISTENCY",
                check_name="Status Consistency Check",
                status="FAILED",
                severity="HIGH",
                message=f"Found {len(invalid_status_contracts)} contracts with invalid status",
                details={"invalid_status_contracts": invalid_status_contracts}
            ))
        else:
            checks.append(IntegrityValidator.create_check(
                check_id="STATUS_CONSISTENCY",
                check_name="Status Consistency Check",
                status="PASSED",
                severity="HIGH",
                message="All contracts have valid status",
                details={}
            ))
        
        return checks
    
    def check_duplicate_contracts(self) -> IntegrityCheck:
        """Check for duplicate contract IDs"""
        contract_ids = []
        duplicates = []
        
        if "contracts" in self.contracts:
            for category_name, category_data in self.contracts["contracts"].items():
                if "contracts" in category_data:
                    for contract in category_data["contracts"]:
                        contract_id = contract.get("contract_id", "UNKNOWN")
                        if contract_id in contract_ids:
                            duplicates.append(contract_id)
                        else:
                            contract_ids.append(contract_id)
        
        if duplicates:
            return IntegrityValidator.create_check(
                check_id="DUPLICATE_CONTRACTS",
                check_name="Duplicate Contract Check",
                status="FAILED",
                severity="HIGH",
                message=f"Found {len(duplicates)} duplicate contract IDs",
                details={"duplicate_contract_ids": list(set(duplicates))}
            )
        else:
            return IntegrityValidator.create_check(
                check_id="DUPLICATE_CONTRACTS",
                check_name="Duplicate Contract Check",
                status="PASSED",
                severity="MEDIUM",
                message="No duplicate contract IDs found",
                details={"total_unique_contracts": len(contract_ids)}
            )
    
    def run_all_checks(self) -> List[IntegrityCheck]:
        """Run all integrity checks"""
        checks = []
        
        # Add core checks
        checks.append(self.check_contract_counts())
        checks.extend(self.check_required_fields())
        checks.extend(self.check_status_consistency())
        checks.append(self.check_duplicate_contracts())
        
        return checks
