from datetime import datetime
from typing import Dict, List, Any, Optional
import re

    from .base_validator import BaseValidator
    import argparse
from .base_validator import (

#!/usr/bin/env python3
"""
Security Core - Core security validation functionality

Single Responsibility: Core security validation logic and orchestration.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""


    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class SecurityCore(BaseValidator):
    """Core security validation functionality."""
    
    def __init__(self):
        """Initialize security core validator."""
        super().__init__("SecurityCore")
        self.security_patterns = self._config.get("patterns", {})
        self.sensitive_fields = [
            "password", "secret", "key", "token", "credential",
            "auth", "private", "sensitive", "confidential", "secure"
        ]
    
    def validate(self, security_data: Dict[str, Any], **kwargs) -> List[ValidationResult]:
        """Validate security data and return validation results."""
        results = []
        
        try:
            # Validate security data structure
            structure_results = self._validate_security_structure(security_data)
            results.extend(structure_results)
            
            # Validate required fields
            required_fields = ["security_level", "authentication_method", "timestamp"]
            field_results = self._validate_required_fields(security_data, required_fields)
            results.extend(field_results)
            
            # Validate security level if present
            if "security_level" in security_data:
                level_result = self._validate_security_level(security_data["security_level"])
                if level_result:
                    results.append(level_result)
            
            # Add overall success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success_result = self._create_result(
                    rule_id="overall_security_validation",
                    rule_name="Overall Security Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Security validation completed successfully"
                )
                results.append(success_result)
            
        except Exception as e:
            error_result = self._create_result(
                rule_id="security_validation_error",
                rule_name="Security Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Security validation failed: {str(e)}"
            )
            results.append(error_result)
        
        return results
    
    def _validate_security_structure(self, security_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate security data structure."""
        results = []
        
        if not isinstance(security_data, dict):
            results.append(self._create_result(
                rule_id="security_structure_type",
                rule_name="Security Data Structure Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Security data must be a dictionary"
            ))
            return results
        
        if not security_data:
            results.append(self._create_result(
                rule_id="security_structure_empty",
                rule_name="Security Data Structure Empty",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Security data cannot be empty"
            ))
        
        return results
    
    def _validate_security_level(self, security_level: Any) -> Optional[ValidationResult]:
        """Validate security level value."""
        valid_levels = ["low", "medium", "high", "critical"]
        
        if not isinstance(security_level, str):
            return self._create_result(
                rule_id="security_level_type",
                rule_name="Security Level Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Security level must be a string"
            )
        
        if security_level.lower() not in valid_levels:
            return self._create_result(
                rule_id="security_level_value",
                rule_name="Security Level Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Security level must be one of: {', '.join(valid_levels)}"
            )
        
        return None
    
    def _check_sensitive_data_exposure(self, security_data: Dict[str, Any]) -> List[ValidationResult]:
        """Check for sensitive data exposure."""
        results = []
        
        for field_name, field_value in security_data.items():
            if any(sensitive in field_name.lower() for sensitive in self.sensitive_fields):
                if field_value and not self._is_properly_secured(field_value):
                    results.append(self._create_result(
                        rule_id="sensitive_data_exposure",
                        rule_name="Sensitive Data Exposure",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Sensitive field '{field_name}' may be exposed"
                    ))
        
        return results
    
    def _is_properly_secured(self, value: Any) -> bool:
        """Check if a value is properly secured."""
        if isinstance(value, str):
            # Check if value is masked or encrypted
            return value.startswith("***") or value.startswith("encrypted:")
        return True
    
    def get_security_summary(self, security_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get security validation summary."""
        try:
            results = self.validate(security_data)
            
            return {
                "total_validations": len(results),
                "passed": len([r for r in results if r.status.value == "passed"]),
                "failed": len([r for r in results if r.status.value == "failed"]),
                "warnings": len([r for r in results if r.severity.value == "warning"]),
                "errors": len([r for r in results if r.severity.value == "error"]),
                "timestamp": self._get_current_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get security summary: {e}")
            return {"error": str(e)}
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()


def main():
    """CLI interface for Security Core testing."""
    
    parser = argparse.ArgumentParser(description="Security Core - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for Security Core."""
    print("🧪 Running Security Core smoke tests...")
    
    # Test core creation
    security_core = SecurityCore()
    assert security_core is not None
    print("✅ SecurityCore creation test passed")
    
    # Test validation
    test_data = {
        "security_level": "high",
        "authentication_method": "token",
        "timestamp": "2024-01-01T00:00:00"
    }
    results = security_core.validate(test_data)
    assert len(results) > 0
    print("✅ Validation test passed")
    
    # Test summary
    summary = security_core.get_security_summary(test_data)
    assert isinstance(summary, dict)
    print("✅ Summary test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
