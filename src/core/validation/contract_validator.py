"""
Contract Validator - Unified Validation Framework

This module provides contract validation functionality, inheriting from BaseValidator
and following the unified validation framework patterns.
"""

from typing import Dict, List, Any
from .base_validator import BaseValidator, ValidationRule, ValidationSeverity, ValidationStatus, ValidationResult


class ContractValidator(BaseValidator):
    """Validates contract data and structure using unified validation framework"""
    
    def __init__(self):
        """Initialize contract validator"""
        super().__init__("ContractValidator")
    
    def _setup_default_rules(self) -> None:
        """Setup default contract validation rules"""
        default_rules = [
            ValidationRule(
                rule_id="required_fields",
                rule_name="Required Fields Check",
                rule_type="contract",
                description="Ensure all required contract fields are present",
                severity=ValidationSeverity.ERROR
            ),
            ValidationRule(
                rule_id="priority_validation",
                rule_name="Priority Validation",
                rule_type="contract",
                description="Validate contract priority values",
                severity=ValidationSeverity.ERROR
            ),
            ValidationRule(
                rule_id="capabilities_validation",
                rule_name="Capabilities Validation",
                rule_type="contract",
                description="Validate required capabilities format",
                severity=ValidationSeverity.ERROR
            ),
            ValidationRule(
                rule_id="deadline_validation",
                rule_name="Deadline Validation",
                rule_type="contract",
                description="Validate contract deadline format and logic",
                severity=ValidationSeverity.WARNING
            )
        ]
        
        for rule in default_rules:
            self.add_validation_rule(rule)
    
    def validate(self, contract_data: Dict[str, Any], **kwargs) -> List[ValidationResult]:
        """Validate contract data and return validation results"""
        results = []
        
        try:
            # Validate required fields
            required_fields = ["title", "description", "priority", "required_capabilities"]
            field_results = self._validate_required_fields(contract_data, required_fields)
            results.extend(field_results)
            
            # Validate priority field
            if "priority" in contract_data:
                priority_result = self._validate_priority(contract_data["priority"])
                if priority_result:
                    results.append(priority_result)
            
            # Validate capabilities field
            if "required_capabilities" in contract_data:
                capabilities_result = self._validate_capabilities(contract_data["required_capabilities"])
                if capabilities_result:
                    results.append(capabilities_result)
            
            # Validate deadline if present
            if "deadline" in contract_data:
                deadline_result = self._validate_deadline(contract_data["deadline"])
                if deadline_result:
                    results.append(deadline_result)
            
            # Add overall success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success_result = self._create_result(
                    rule_id="overall_validation",
                    rule_name="Overall Contract Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Contract validation passed successfully",
                    details={"total_checks": len(results)}
                )
                results.append(success_result)
            
        except Exception as e:
            error_result = self._create_result(
                rule_id="validation_error",
                rule_name="Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Validation error: {str(e)}",
                details={"error_type": type(e).__name__}
            )
            results.append(error_result)
        
        return results
    
    def _validate_priority(self, priority: Any) -> ValidationResult:
        """Validate contract priority value"""
        valid_priorities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        
        if not isinstance(priority, str):
            return self._create_result(
                rule_id="priority_type",
                rule_name="Priority Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Priority must be a string",
                field_path="priority",
                actual_value=type(priority).__name__,
                expected_value="str"
            )
        
        if priority not in valid_priorities:
            return self._create_result(
                rule_id="priority_value",
                rule_name="Priority Value Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid priority value: {priority}",
                field_path="priority",
                actual_value=priority,
                expected_value=f"one of {valid_priorities}"
            )
        
        return None
    
    def _validate_capabilities(self, capabilities: Any) -> ValidationResult:
        """Validate required capabilities format"""
        if not isinstance(capabilities, list):
            return self._create_result(
                rule_id="capabilities_type",
                rule_name="Capabilities Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Required capabilities must be a list",
                field_path="required_capabilities",
                actual_value=type(capabilities).__name__,
                expected_value="list"
            )
        
        if len(capabilities) == 0:
            return self._create_result(
                rule_id="capabilities_empty",
                rule_name="Capabilities Empty Check",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Required capabilities must be a non-empty list",
                field_path="required_capabilities",
                actual_value=capabilities,
                expected_value="non-empty list"
            )
        
        # Validate each capability is a string
        for i, capability in enumerate(capabilities):
            if not isinstance(capability, str):
                return self._create_result(
                    rule_id=f"capability_{i}_type",
                    rule_name=f"Capability {i} Type Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Capability {i} must be a string",
                    field_path=f"required_capabilities[{i}]",
                    actual_value=type(capability).__name__,
                    expected_value="str"
                )
        
        return None
    
    def _validate_deadline(self, deadline: Any) -> ValidationResult:
        """Validate contract deadline format and logic"""
        from datetime import datetime
        
        if not isinstance(deadline, str):
            return self._create_result(
                rule_id="deadline_type",
                rule_name="Deadline Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Deadline must be a string",
                field_path="deadline",
                actual_value=type(deadline).__name__,
                expected_value="str"
            )
        
        try:
            deadline_date = datetime.fromisoformat(deadline)
            if deadline_date < datetime.now():
                return self._create_result(
                    rule_id="deadline_past",
                    rule_name="Deadline Past Check",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message="Deadline is in the past",
                    field_path="deadline",
                    actual_value=deadline,
                    expected_value="future date"
                )
        except ValueError:
            return self._create_result(
                rule_id="deadline_format",
                rule_name="Deadline Format Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Invalid deadline format. Use ISO format (YYYY-MM-DD)",
                field_path="deadline",
                actual_value=deadline,
                expected_value="ISO format date string"
            )
        
        return None
    
    # Contract validation functionality integration (from duplicate validation.py)
    def validate_contract_legacy(self, contract_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Legacy contract validation method (from duplicate validation.py)"""
        results: List[Dict[str, Any]] = []
        
        try:
            required = ["title", "description", "priority", "required_capabilities"]
            for field in required:
                if field not in contract_data or not contract_data[field]:
                    results.append({
                        "field": field,
                        "issue": f"Required field '{field}' is missing or empty",
                        "severity": "critical",
                        "passed": False,
                    })

            if "priority" in contract_data:
                try:
                    # Try to validate priority against known values
                    priority = contract_data["priority"]
                    valid_priorities = ["low", "medium", "high", "critical"]
                    if priority not in valid_priorities:
                        results.append({
                            "field": "priority",
                            "issue": f"Invalid priority value: {priority}",
                            "severity": "critical",
                            "passed": False,
                        })
                except Exception:
                    results.append({
                        "field": "priority",
                        "issue": f"Invalid priority value: {contract_data['priority']}",
                        "severity": "critical",
                        "passed": False,
                    })

            if "required_capabilities" in contract_data:
                capabilities = contract_data["required_capabilities"]
                if not isinstance(capabilities, list) or len(capabilities) == 0:
                    results.append({
                        "field": "required_capabilities",
                        "issue": "Required capabilities must be a non-empty list",
                        "severity": "critical",
                        "passed": False,
                    })

            if not any(r["severity"] == "critical" and not r["passed"] for r in results):
                results.append({
                    "field": "overall",
                    "issue": "Contract validation passed",
                    "severity": "info",
                    "passed": True,
                })
                
        except Exception as e:
            results.append({
                "field": "validation_error",
                "issue": f"Validation error: {str(e)}",
                "severity": "critical",
                "passed": False,
            })
            
        return results
    
    def get_validation_summary(self, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get validation summary for contract data"""
        try:
            # Use both validation methods
            unified_results = self.validate(contract_data)
            legacy_results = self.validate_contract_legacy(contract_data)
            
            # Count results
            total_unified = len(unified_results)
            passed_unified = len([r for r in unified_results if r.status.value == "passed"])
            
            total_legacy = len(legacy_results)
            passed_legacy = len([r for r in legacy_results if r["passed"]])
            
            return {
                "unified_validation": {
                    "total": total_unified,
                    "passed": passed_unified,
                    "failed": total_unified - passed_unified,
                    "pass_rate": (passed_unified / total_unified * 100) if total_unified > 0 else 0
                },
                "legacy_validation": {
                    "total": total_legacy,
                    "passed": passed_legacy,
                    "failed": total_legacy - passed_legacy,
                    "pass_rate": (passed_legacy / total_legacy * 100) if total_legacy > 0 else 0
                },
                "timestamp": self._get_current_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get validation summary: {e}")
            return {"error": str(e)}
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
