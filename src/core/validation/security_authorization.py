from datetime import datetime
from typing import Dict, List, Any, Optional
import re

    import argparse
from .base_validator import (

#!/usr/bin/env python3
"""
Security Authorization - Authorization validation for security system

Single Responsibility: Validate authorization policies and permissions.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""


    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class SecurityAuthorization(BaseValidator):
    """Validates authorization policies and permissions."""
    
    def __init__(self):
        """Initialize authorization validator."""
        super().__init__("SecurityAuthorization")
        self.valid_permission_levels = ["read", "write", "execute", "admin", "owner"]
        self.valid_resource_types = ["file", "database", "api", "service", "user", "role"]
        self.valid_policy_actions = ["allow", "deny", "require", "optional"]
    
    def validate_authorization(self, auth_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate authorization configuration."""
        results = []
        
        try:
            # Validate roles configuration
            if "roles" in auth_data:
                role_results = self._validate_roles(auth_data["roles"])
                results.extend(role_results)
            
            # Validate permissions configuration
            if "permissions" in auth_data:
                permission_results = self._validate_permissions(auth_data["permissions"])
                results.extend(permission_results)
            
            # Validate policies configuration
            if "policies" in auth_data:
                policy_results = self._validate_policies(auth_data["policies"])
                results.extend(policy_results)
            
            # Validate access control lists
            if "access_control" in auth_data:
                acl_results = self._validate_access_control(auth_data["access_control"])
                results.extend(acl_results)
            
        except Exception as e:
            error_result = self._create_result(
                rule_id="authorization_validation_error",
                rule_name="Authorization Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Authorization validation failed: {str(e)}"
            )
            results.append(error_result)
        
        return results
    
    def _validate_roles(self, roles: Any) -> List[ValidationResult]:
        """Validate roles configuration."""
        results = []
        
        if not isinstance(roles, dict):
            results.append(self._create_result(
                rule_id="roles_type",
                rule_name="Roles Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Roles must be a dictionary"
            ))
            return results
        
        for role_name, role_config in roles.items():
            if not isinstance(role_name, str):
                results.append(self._create_result(
                    rule_id="role_name_type",
                    rule_name="Role Name Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Role name must be a string: {role_name}"
                ))
                continue
            
            if not isinstance(role_config, dict):
                results.append(self._create_result(
                    rule_id="role_config_type",
                    rule_name="Role Config Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Role config must be a dictionary for role: {role_name}"
                ))
                continue
            
            # Validate role permissions
            if "permissions" in role_config:
                role_perms = role_config["permissions"]
                if not isinstance(role_perms, list):
                    results.append(self._create_result(
                        rule_id="role_permissions_type",
                        rule_name="Role Permissions Type",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Role permissions must be a list for role: {role_name}"
                    ))
        
        return results
    
    def _validate_permissions(self, permissions: Any) -> List[ValidationResult]:
        """Validate permissions configuration."""
        results = []
        
        if not isinstance(permissions, dict):
            results.append(self._create_result(
                rule_id="permissions_type",
                rule_name="Permissions Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Permissions must be a dictionary"
            ))
            return results
        
        for perm_name, perm_config in permissions.items():
            if not isinstance(perm_name, str):
                results.append(self._create_result(
                    rule_id="permission_name_type",
                    rule_name="Permission Name Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Permission name must be a string: {perm_name}"
                ))
                continue
            
            if not isinstance(perm_config, dict):
                results.append(self._create_result(
                    rule_id="permission_config_type",
                    rule_name="Permission Config Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Permission config must be a dictionary for permission: {perm_name}"
                ))
                continue
            
            # Validate permission level
            if "level" in perm_config:
                level = perm_config["level"]
                if level not in self.valid_permission_levels:
                    results.append(self._create_result(
                        rule_id="permission_level",
                        rule_name="Permission Level",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid permission level: {level}. Valid levels: {', '.join(self.valid_permission_levels)}"
                    ))
        
        return results
    
    def _validate_policies(self, policies: Any) -> List[ValidationResult]:
        """Validate policies configuration."""
        results = []
        
        if not isinstance(policies, list):
            results.append(self._create_result(
                rule_id="policies_type",
                rule_name="Policies Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Policies must be a list"
            ))
            return results
        
        for i, policy in enumerate(policies):
            if not isinstance(policy, dict):
                results.append(self._create_result(
                    rule_id="policy_item_type",
                    rule_name="Policy Item Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Policy item {i} must be a dictionary"
                ))
                continue
            
            # Validate policy action
            if "action" in policy:
                action = policy["action"]
                if action not in self.valid_policy_actions:
                    results.append(self._create_result(
                        rule_id="policy_action",
                        rule_name="Policy Action",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid policy action: {action}. Valid actions: {', '.join(self.valid_policy_actions)}"
                    ))
        
        return results
    
    def _validate_access_control(self, acl: Any) -> List[ValidationResult]:
        """Validate access control list configuration."""
        results = []
        
        if not isinstance(acl, list):
            results.append(self._create_result(
                rule_id="acl_type",
                rule_name="Access Control Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Access control must be a list"
            ))
            return results
        
        for i, entry in enumerate(acl):
            if not isinstance(entry, dict):
                results.append(self._create_result(
                    rule_id="acl_entry_type",
                    rule_name="ACL Entry Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"ACL entry {i} must be a dictionary"
                ))
                continue
            
            # Validate required fields
            required_fields = ["subject", "resource", "action"]
            for field in required_fields:
                if field not in entry:
                    results.append(self._create_result(
                        rule_id=f"acl_missing_{field}",
                        rule_name=f"ACL Missing {field.title()}",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"ACL entry {i} missing required field: {field}"
                    ))
        
        return results
    
    def get_authorization_summary(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get authorization validation summary."""
        try:
            results = self.validate_authorization(auth_data)
            
            return {
                "total_validations": len(results),
                "passed": len([r for r in results if r.status.value == "passed"]),
                "failed": len([r for r in results if r.status.value == "failed"]),
                "warnings": len([r for r in results if r.severity.value == "warning"]),
                "errors": len([r for r in results if r.severity.value == "error"]),
                "timestamp": self._get_current_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get authorization summary: {e}")
            return {"error": str(e)}
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()


def main():
    """CLI interface for Security Authorization testing."""
    
    parser = argparse.ArgumentParser(description="Security Authorization - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for Security Authorization."""
    print("🧪 Running Security Authorization smoke tests...")
    
    # Test creation
    auth_validator = SecurityAuthorization()
    assert auth_validator is not None
    print("✅ SecurityAuthorization creation test passed")
    
    # Test validation
    test_data = {
        "roles": {
            "admin": {
                "permissions": ["read", "write", "execute", "admin"]
            }
        },
        "permissions": {
            "read": {
                "level": "read"
            }
        },
        "policies": [
            {
                "action": "allow"
            }
        ],
        "access_control": [
            {
                "subject": "user1",
                "resource": "file1",
                "action": "allow"
            }
        ]
    }
    results = auth_validator.validate_authorization(test_data)
    assert len(results) > 0
    print("✅ Authorization validation test passed")
    
    # Test summary
    summary = auth_validator.get_authorization_summary(test_data)
    assert isinstance(summary, dict)
    print("✅ Summary test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
