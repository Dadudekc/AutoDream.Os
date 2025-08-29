from datetime import datetime
from typing import Dict, List, Any, Optional
import re

    import argparse
from .base_validator import (

#!/usr/bin/env python3
"""
Security Authentication - Authentication validation for security system

Single Responsibility: Validate authentication methods and configurations.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""


    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class SecurityAuthentication(BaseValidator):
    """Validates authentication methods and configurations."""
    
    def __init__(self):
        """Initialize authentication validator."""
        super().__init__("SecurityAuthentication")
        self.valid_auth_methods = [
            "password", "token", "oauth", "saml", "ldap", "biometric", "mfa"
        ]
        self.password_patterns = {
            "min_length": 8,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_special": True
        }
    
    def validate_authentication(self, auth_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate authentication configuration."""
        results = []
        
        try:
            # Validate authentication method
            if "method" in auth_data:
                method_results = self._validate_auth_method(auth_data["method"])
                results.extend(method_results)
            
            # Validate password policy if applicable
            if "password_policy" in auth_data:
                policy_results = self._validate_password_policy(auth_data["password_policy"])
                results.extend(policy_results)
            
            # Validate MFA configuration
            if "mfa_enabled" in auth_data:
                mfa_results = self._validate_mfa_config(auth_data)
                results.extend(mfa_results)
            
            # Validate session configuration
            if "session_config" in auth_data:
                session_results = self._validate_session_config(auth_data["session_config"])
                results.extend(session_results)
            
            # Validate token configuration
            if "token_config" in auth_data:
                token_results = self._validate_token_config(auth_data["token_config"])
                results.extend(token_results)
            
        except Exception as e:
            error_result = self._create_result(
                rule_id="authentication_validation_error",
                rule_name="Authentication Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Authentication validation failed: {str(e)}"
            )
            results.append(error_result)
        
        return results
    
    def _validate_auth_method(self, method: Any) -> List[ValidationResult]:
        """Validate authentication method."""
        results = []
        
        if not isinstance(method, str):
            results.append(self._create_result(
                rule_id="auth_method_type",
                rule_name="Authentication Method Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Authentication method must be a string"
            ))
            return results
        
        if method.lower() not in self.valid_auth_methods:
            results.append(self._create_result(
                rule_id="auth_method_value",
                rule_name="Authentication Method Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid authentication method: {method}. Valid methods: {', '.join(self.valid_auth_methods)}"
            ))
        
        return results
    
    def _validate_password_policy(self, policy: Dict[str, Any]) -> List[ValidationResult]:
        """Validate password policy configuration."""
        results = []
        
        if not isinstance(policy, dict):
            results.append(self._create_result(
                rule_id="password_policy_type",
                rule_name="Password Policy Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Password policy must be a dictionary"
            ))
            return results
        
        # Validate minimum length
        min_length = policy.get("min_length", 0)
        if min_length < self.password_patterns["min_length"]:
            results.append(self._create_result(
                rule_id="password_min_length",
                rule_name="Password Minimum Length",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.WARNING,
                message=f"Password minimum length should be at least {self.password_patterns['min_length']} characters"
            ))
        
        # Validate complexity requirements
        if not policy.get("require_uppercase", False):
            results.append(self._create_result(
                rule_id="password_uppercase",
                rule_name="Password Uppercase Requirement",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.WARNING,
                message="Password policy should require uppercase letters"
            ))
        
        if not policy.get("require_numbers", False):
            results.append(self._create_result(
                rule_id="password_numbers",
                rule_name="Password Numbers Requirement",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.WARNING,
                message="Password policy should require numbers"
            ))
        
        return results
    
    def _validate_mfa_config(self, auth_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate multi-factor authentication configuration."""
        results = []
        
        mfa_enabled = auth_data.get("mfa_enabled", False)
        
        if mfa_enabled:
            # Check MFA method configuration
            if "mfa_methods" not in auth_data:
                results.append(self._create_result(
                    rule_id="mfa_methods_missing",
                    rule_name="MFA Methods Missing",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="MFA methods must be specified when MFA is enabled"
                ))
            else:
                mfa_methods = auth_data["mfa_methods"]
                if not isinstance(mfa_methods, list) or len(mfa_methods) == 0:
                    results.append(self._create_result(
                        rule_id="mfa_methods_invalid",
                        rule_name="MFA Methods Invalid",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="MFA methods must be a non-empty list"
                    ))
        
        return results
    
    def _validate_session_config(self, config: Dict[str, Any]) -> List[ValidationResult]:
        """Validate session configuration."""
        results = []
        
        if not isinstance(config, dict):
            results.append(self._create_result(
                rule_id="session_config_type",
                rule_name="Session Config Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Session configuration must be a dictionary"
            ))
            return results
        
        # Validate session timeout
        timeout = config.get("timeout", 0)
        if timeout <= 0:
            results.append(self._create_result(
                rule_id="session_timeout",
                rule_name="Session Timeout",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Session timeout must be greater than 0"
            ))
        elif timeout > 86400:  # 24 hours
            results.append(self._create_result(
                rule_id="session_timeout_long",
                rule_name="Session Timeout Long",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.WARNING,
                message="Session timeout is very long, consider reducing for security"
            ))
        
        # Validate session renewal
        if not config.get("renewal_enabled", False):
            results.append(self._create_result(
                rule_id="session_renewal",
                rule_name="Session Renewal",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.WARNING,
                message="Session renewal should be enabled for security"
            ))
        
        return results
    
    def _validate_token_config(self, config: Dict[str, Any]) -> List[ValidationResult]:
        """Validate token configuration."""
        results = []
        
        if not isinstance(config, dict):
            results.append(self._create_result(
                rule_id="token_config_type",
                rule_name="Token Config Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Token configuration must be a dictionary"
            ))
            return results
        
        # Validate token expiration
        expiration = config.get("expiration", 0)
        if expiration <= 0:
            results.append(self._create_result(
                rule_id="token_expiration",
                rule_name="Token Expiration",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Token expiration must be greater than 0"
            ))
        
        # Validate token refresh
        if not config.get("refresh_enabled", False):
            results.append(self._create_result(
                rule_id="token_refresh",
                rule_name="Token Refresh",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.WARNING,
                message="Token refresh should be enabled for security"
            ))
        
        return results
    
    def get_authentication_summary(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get authentication validation summary."""
        try:
            results = self.validate_authentication(auth_data)
            
            return {
                "total_validations": len(results),
                "passed": len([r for r in results if r.status.value == "passed"]),
                "failed": len([r for r in results if r.status.value == "failed"]),
                "warnings": len([r for r in results if r.severity.value == "warning"]),
                "errors": len([r for r in results if r.severity.value == "error"]),
                "timestamp": self._get_current_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get authentication summary: {e}")
            return {"error": str(e)}
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()


def main():
    """CLI interface for Security Authentication testing."""
    
    parser = argparse.ArgumentParser(description="Security Authentication - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for Security Authentication."""
    print("🧪 Running Security Authentication smoke tests...")
    
    # Test creation
    auth_validator = SecurityAuthentication()
    assert auth_validator is not None
    print("✅ SecurityAuthentication creation test passed")
    
    # Test validation
    test_data = {
        "method": "token",
        "mfa_enabled": True,
        "mfa_methods": ["sms", "app"],
        "session_config": {"timeout": 3600, "renewal_enabled": True},
        "token_config": {"expiration": 7200, "refresh_enabled": True}
    }
    results = auth_validator.validate_authentication(test_data)
    assert len(results) > 0
    print("✅ Authentication validation test passed")
    
    # Test summary
    summary = auth_validator.get_authentication_summary(test_data)
    assert isinstance(summary, dict)
    print("✅ Summary test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
