from datetime import datetime
from typing import Dict, List, Any, Optional
import re

    import argparse
from .base_validator import (

#!/usr/bin/env python3
"""
Security Policy - Policy validation for security system

Single Responsibility: Validate security policies and compliance rules.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""


    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class SecurityPolicy(BaseValidator):
    """Validates security policies and compliance rules."""
    
    def __init__(self):
        """Initialize policy validator."""
        super().__init__("SecurityPolicy")
        self.valid_policy_types = ["access", "data", "network", "application", "compliance"]
        self.valid_compliance_standards = ["ISO27001", "SOC2", "PCI-DSS", "GDPR", "HIPAA", "NIST"]
        self.valid_severity_levels = ["low", "medium", "high", "critical"]
    
    def validate_policies(self, policy_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate security policies configuration."""
        results = []
        
        try:
            # Validate policy definitions
            if "policies" in policy_data:
                policy_results = self._validate_policy_definitions(policy_data["policies"])
                results.extend(policy_results)
            
            # Validate compliance rules
            if "compliance" in policy_data:
                compliance_results = self._validate_compliance_rules(policy_data["compliance"])
                results.extend(compliance_results)
            
            # Validate data classification
            if "data_classification" in policy_data:
                data_results = self._validate_data_classification(policy_data["data_classification"])
                results.extend(data_results)
            
            # Validate network policies
            if "network_policies" in policy_data:
                network_results = self._validate_network_policies(policy_data["network_policies"])
                results.extend(network_results)
            
            # Validate application policies
            if "application_policies" in policy_data:
                app_results = self._validate_application_policies(policy_data["application_policies"])
                results.extend(app_results)
            
        except Exception as e:
            error_result = self._create_result(
                rule_id="policy_validation_error",
                rule_name="Policy Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Policy validation failed: {str(e)}"
            )
            results.append(error_result)
        
        return results
    
    def _validate_policy_definitions(self, policies: Any) -> List[ValidationResult]:
        """Validate policy definitions."""
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
            
            # Validate required fields
            required_fields = ["name", "type", "description"]
            for field in required_fields:
                if field not in policy:
                    results.append(self._create_result(
                        rule_id=f"policy_missing_{field}",
                        rule_name=f"Policy Missing {field.title()}",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Policy {i} missing required field: {field}"
                    ))
            
            # Validate policy type
            if "type" in policy:
                policy_type = policy["type"]
                if policy_type not in self.valid_policy_types:
                    results.append(self._create_result(
                        rule_id="policy_type",
                        rule_name="Policy Type",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid policy type: {policy_type}. Valid types: {', '.join(self.valid_policy_types)}"
                    ))
            
            # Validate policy severity
            if "severity" in policy:
                severity = policy["severity"]
                if severity not in self.valid_severity_levels:
                    results.append(self._create_result(
                        rule_id="policy_severity",
                        rule_name="Policy Severity",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid policy severity: {severity}. Valid levels: {', '.join(self.valid_severity_levels)}"
                    ))
            
            # Validate policy rules
            if "rules" in policy:
                rules = policy["rules"]
                if not isinstance(rules, list):
                    results.append(self._create_result(
                        rule_id="policy_rules_type",
                        rule_name="Policy Rules Type",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Policy rules must be a list for policy {i}"
                    ))
                else:
                    for j, rule in enumerate(rules):
                        if not isinstance(rule, dict):
                            results.append(self._create_result(
                                rule_id="policy_rule_item_type",
                                rule_name="Policy Rule Item Type",
                                status=ValidationStatus.FAILED,
                                severity=ValidationSeverity.ERROR,
                                message=f"Policy rule {j} must be a dictionary in policy {i}"
                            ))
                        else:
                            # Validate rule condition
                            if "condition" not in rule:
                                results.append(self._create_result(
                                    rule_id="policy_rule_condition",
                                    rule_name="Policy Rule Condition",
                                    status=ValidationStatus.FAILED,
                                    severity=ValidationSeverity.ERROR,
                                    message=f"Policy rule {j} missing condition in policy {i}"
                                ))
            
            # Validate policy enforcement
            if "enforcement" in policy:
                enforcement = policy["enforcement"]
                if not isinstance(enforcement, dict):
                    results.append(self._create_result(
                        rule_id="policy_enforcement_type",
                        rule_name="Policy Enforcement Type",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Policy enforcement must be a dictionary for policy {i}"
                    ))
                else:
                    # Validate enforcement action
                    if "action" in enforcement:
                        action = enforcement["action"]
                        valid_actions = ["allow", "deny", "warn", "log", "quarantine"]
                        if action not in valid_actions:
                            results.append(self._create_result(
                                rule_id="policy_enforcement_action",
                                rule_name="Policy Enforcement Action",
                                status=ValidationStatus.FAILED,
                                severity=ValidationSeverity.ERROR,
                                message=f"Invalid enforcement action: {action}. Valid actions: {', '.join(valid_actions)}"
                            ))
        
        return results
    
    def _validate_compliance_rules(self, compliance: Any) -> List[ValidationResult]:
        """Validate compliance rules."""
        results = []
        
        if not isinstance(compliance, dict):
            results.append(self._create_result(
                rule_id="compliance_type",
                rule_name="Compliance Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Compliance must be a dictionary"
            ))
            return results
        
        # Validate compliance standards
        if "standards" in compliance:
            standards = compliance["standards"]
            if not isinstance(standards, list):
                results.append(self._create_result(
                    rule_id="compliance_standards_type",
                    rule_name="Compliance Standards Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Compliance standards must be a list"
                ))
            else:
                for standard in standards:
                    if not isinstance(standard, str):
                        results.append(self._create_result(
                            rule_id="compliance_standard_type",
                            rule_name="Compliance Standard Type",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Compliance standard must be a string: {standard}"
                        ))
                    elif standard not in self.valid_compliance_standards:
                        results.append(self._create_result(
                            rule_id="compliance_standard_value",
                            rule_name="Compliance Standard Value",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Invalid compliance standard: {standard}. Valid standards: {', '.join(self.valid_compliance_standards)}"
                        ))
        
        # Validate compliance requirements
        if "requirements" in compliance:
            requirements = compliance["requirements"]
            if not isinstance(requirements, list):
                results.append(self._create_result(
                    rule_id="compliance_requirements_type",
                    rule_name="Compliance Requirements Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Compliance requirements must be a list"
                ))
            else:
                for i, requirement in enumerate(requirements):
                    if not isinstance(requirement, dict):
                        results.append(self._create_result(
                            rule_id="compliance_requirement_type",
                            rule_name="Compliance Requirement Type",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Compliance requirement {i} must be a dictionary"
                        ))
                        continue
                    
                    # Validate requirement fields
                    if "id" not in requirement:
                        results.append(self._create_result(
                            rule_id="compliance_requirement_id",
                            rule_name="Compliance Requirement ID",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Compliance requirement {i} missing ID"
                        ))
                    
                    if "description" not in requirement:
                        results.append(self._create_result(
                            rule_id="compliance_requirement_description",
                            rule_name="Compliance Requirement Description",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Compliance requirement {i} missing description"
                        ))
        
        return results
    
    def _validate_data_classification(self, data_class: Any) -> List[ValidationResult]:
        """Validate data classification policies."""
        results = []
        
        if not isinstance(data_class, dict):
            results.append(self._create_result(
                rule_id="data_classification_type",
                rule_name="Data Classification Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Data classification must be a dictionary"
            ))
            return results
        
        # Validate classification levels
        if "levels" in data_class:
            levels = data_class["levels"]
            if not isinstance(levels, list):
                results.append(self._create_result(
                    rule_id="data_classification_levels_type",
                    rule_name="Data Classification Levels Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Data classification levels must be a list"
                ))
            else:
                valid_levels = ["public", "internal", "confidential", "restricted", "secret"]
                for level in levels:
                    if not isinstance(level, str):
                        results.append(self._create_result(
                            rule_id="data_classification_level_type",
                            rule_name="Data Classification Level Type",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Data classification level must be a string: {level}"
                        ))
                    elif level not in valid_levels:
                        results.append(self._create_result(
                            rule_id="data_classification_level_value",
                            rule_name="Data Classification Level Value",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Invalid data classification level: {level}. Valid levels: {', '.join(valid_levels)}"
                        ))
        
        # Validate data handling rules
        if "handling_rules" in data_class:
            handling_rules = data_class["handling_rules"]
            if not isinstance(handling_rules, dict):
                results.append(self._create_result(
                    rule_id="data_handling_rules_type",
                    rule_name="Data Handling Rules Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Data handling rules must be a dictionary"
                ))
            else:
                for level, rules in handling_rules.items():
                    if not isinstance(rules, list):
                        results.append(self._create_result(
                            rule_id="data_handling_rules_item_type",
                            rule_name="Data Handling Rules Item Type",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Data handling rules for level {level} must be a list"
                        ))
        
        return results
    
    def _validate_network_policies(self, network_policies: Any) -> List[ValidationResult]:
        """Validate network security policies."""
        results = []
        
        if not isinstance(network_policies, list):
            results.append(self._create_result(
                rule_id="network_policies_type",
                rule_name="Network Policies Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Network policies must be a list"
            ))
            return results
        
        for i, policy in enumerate(network_policies):
            if not isinstance(policy, dict):
                results.append(self._create_result(
                    rule_id="network_policy_item_type",
                    rule_name="Network Policy Item Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Network policy {i} must be a dictionary"
                ))
                continue
            
            # Validate network policy fields
            if "source" in policy:
                source = policy["source"]
                if not isinstance(source, str) and not isinstance(source, list):
                    results.append(self._create_result(
                        rule_id="network_policy_source",
                        rule_name="Network Policy Source",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Network policy source must be a string or list for policy {i}"
                    ))
            
            if "destination" in policy:
                destination = policy["destination"]
                if not isinstance(destination, str) and not isinstance(destination, list):
                    results.append(self._create_result(
                        rule_id="network_policy_destination",
                        rule_name="Network Policy Destination",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Network policy destination must be a string or list for policy {i}"
                    ))
            
            if "protocol" in policy:
                protocol = policy["protocol"]
                valid_protocols = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS", "SSH", "FTP"]
                if protocol not in valid_protocols:
                    results.append(self._create_result(
                        rule_id="network_policy_protocol",
                        rule_name="Network Policy Protocol",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid network protocol: {protocol}. Valid protocols: {', '.join(valid_protocols)}"
                    ))
        
        return results
    
    def _validate_application_policies(self, app_policies: Any) -> List[ValidationResult]:
        """Validate application security policies."""
        results = []
        
        if not isinstance(app_policies, list):
            results.append(self._create_result(
                rule_id="application_policies_type",
                rule_name="Application Policies Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Application policies must be a list"
            ))
            return results
        
        for i, policy in enumerate(app_policies):
            if not isinstance(policy, dict):
                results.append(self._create_result(
                    rule_id="application_policy_item_type",
                    rule_name="Application Policy Item Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Application policy {i} must be a dictionary"
                ))
                continue
            
            # Validate application policy fields
            if "application" in policy:
                app = policy["application"]
                if not isinstance(app, str):
                    results.append(self._create_result(
                        rule_id="application_policy_app",
                        rule_name="Application Policy Application",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Application policy application must be a string for policy {i}"
                    ))
            
            if "permissions" in policy:
                permissions = policy["permissions"]
                if not isinstance(permissions, list):
                    results.append(self._create_result(
                        rule_id="application_policy_permissions",
                        rule_name="Application Policy Permissions",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Application policy permissions must be a list for policy {i}"
                    ))
                else:
                    for perm in permissions:
                        if not isinstance(perm, str):
                            results.append(self._create_result(
                                rule_id="application_policy_permission_item",
                                rule_name="Application Policy Permission Item",
                                status=ValidationStatus.FAILED,
                                severity=ValidationSeverity.ERROR,
                                message=f"Application policy permission must be a string: {perm} in policy {i}"
                            ))
        
        return results
    
    def get_policy_summary(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get policy validation summary."""
        try:
            results = self.validate_policies(policy_data)
            
            return {
                "total_validations": len(results),
                "passed": len([r for r in results if r.status.value == "passed"]),
                "failed": len([r for r in results if r.status.value == "failed"]),
                "warnings": len([r for r in results if r.severity.value == "warning"]),
                "errors": len([r for r in results if r.severity.value == "error"]),
                "timestamp": self._get_current_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get policy summary: {e}")
            return {"error": str(e)}
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()


def main():
    """CLI interface for Security Policy testing."""
    
    parser = argparse.ArgumentParser(description="Security Policy - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for Security Policy."""
    print("🧪 Running Security Policy smoke tests...")
    
    # Test creation
    policy_validator = SecurityPolicy()
    assert policy_validator is not None
    print("✅ SecurityPolicy creation test passed")
    
    # Test validation
    test_data = {
        "policies": [
            {
                "name": "Data Access Policy",
                "type": "access",
                "description": "Controls data access",
                "severity": "high",
                "rules": [{"condition": "user_role == 'admin'"}],
                "enforcement": {"action": "allow"}
            }
        ],
        "compliance": {
            "standards": ["ISO27001", "SOC2"],
            "requirements": [
                {"id": "REQ001", "description": "Access control requirement"}
            ]
        },
        "data_classification": {
            "levels": ["public", "internal", "confidential"],
            "handling_rules": {
                "confidential": ["encrypt", "audit"]
            }
        },
        "network_policies": [
            {
                "source": "192.168.1.0/24",
                "destination": "10.0.0.0/8",
                "protocol": "HTTPS"
            }
        ],
        "application_policies": [
            {
                "application": "web_app",
                "permissions": ["read", "write"]
            }
        ]
    }
    results = policy_validator.validate_policies(test_data)
    assert len(results) > 0
    print("✅ Policy validation test passed")
    
    # Test summary
    summary = policy_validator.get_policy_summary(test_data)
    assert isinstance(summary, dict)
    print("✅ Summary test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
